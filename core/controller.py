# core/controller.py
import logging
import json
import os
from datetime import datetime
from core.brain import Brain
from core.context import ContextManager
from IO import stt, tts
from config import SYSTEM_PROMPT, INITIAL_GREETING, EXIT_PHRASES, FAREWELL_MESSAGE, CHAT_LOG_DIR, INTEGRATE_PAST_LOGS


# Ensure the chat log directory exists
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

class ChatLogManager:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def load_logs(self):
        """Loads all past conversation logs."""
        logs = []
        for filename in sorted(os.listdir(self.log_dir)):
            if filename.endswith(".json"):
                file_path = os.path.join(self.log_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        logs.append(json.load(f))
                except Exception as e:
                    logging.error(f"Failed to load chat log {filename}: {e}")
        return logs

    def save_log(self, conversation_history):
        """Saves the current conversation to a new JSON file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"chat_{timestamp}.json"
        file_path = os.path.join(self.log_dir, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_history, f, indent=4)
            logging.info(f"Conversation saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save chat log: {e}")

def conversation_loop():
    """
    The main control loop for the assistant.
    Orchestrates listening, thinking, and speaking.
    """
    chat_log_manager = ChatLogManager(CHAT_LOG_DIR)  # Create early
    context = None

    try:
        # --- Initialization ---
        brain = Brain()
        context = ContextManager(SYSTEM_PROMPT)
        stt.initialize_stt()
        tts.initialize_tts()

        # --- Load and inform AI of past conversations ---
        past_logs = chat_log_manager.load_logs() if INTEGRATE_PAST_LOGS else []
        if INTEGRATE_PAST_LOGS and past_logs:
            logging.info("[controller] Integrating past logs (legacy mode)")
            for conversation in past_logs:
                # Each past conversation is expected to be a list of {'role': ..., 'content': ...}
                for msg in conversation:
                    role = msg.get("role")
                    content = msg.get("content")
                    if role and content:
                        context.add_message(role, content)
        else:
            logging.info("[controller] Starting fresh conversation (no past integration)")

        # --- Initial AI Response ---
        logging.info("Generating initial AI response...")
        context.add_message("user", INITIAL_GREETING)
        initial_response = brain.generate_response(context.get_history(), initial=True)
        context.add_message("assistant", initial_response)
        logging.info(f"AI: {initial_response}")
        tts.speak(initial_response)

        # --- Main Conversation Loop ---
        while True:
            logging.info("Listening for user input...")
            user_text, audio = stt.listen_and_transcribe()
            if not user_text:
                continue

            logging.info(f"You: {user_text}")

            if user_text.lower() in EXIT_PHRASES:
                logging.info(f"AI: {FAREWELL_MESSAGE}")
                tts.speak(FAREWELL_MESSAGE)
                break

            context.add_message("user", user_text)
            ai_response = brain.generate_response(context.get_history())
            context.add_message("assistant", ai_response)
            logging.info(f"AI: {ai_response}")
            tts.speak(ai_response)

    except Exception as e:
        logging.critical(f"A critical error occurred in the main loop: {e}", exc_info=True)
    finally:
        if context:
            chat_log_manager.save_log(context.get_history())
            context.save_snapshot()
        logging.info("Shutting down Neuro Assistant.")