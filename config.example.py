# config.py - Template Configuration
# Copy this file and customize it for your own use

# --- Model Configurations ---
# LLM model for the brain
LLM_MODEL_ID = "chuanli11/Llama-3.2-3B-Instruct-uncensored"  # Or your preferred model

# STT (Whisper) model settings
STT_MODEL_SIZE = "large-v3"  # Options: "tiny", "base", "small", "medium", "large-v3"
STT_COMPUTE_TYPE = "float16"  # "float16", "int8", "float32"

# --- TTS Configuration ---
TTS_RATE = 175
TTS_VOLUME = 1.0
TTS_BACKEND = "coqui"  # "piper" or "coqui"

# Coqui TTS settings (used when TTS_BACKEND == "coqui")
COQUI_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"  # XTTS v2 for voice cloning
COQUI_REFERENCE_WAV = "your_reference_voice.wav"  # Path to your reference voice sample
COQUI_DEVICE = "cuda"  # "cuda" or "cpu"
COQUI_LANGUAGE = "en"  # Language code for synthesis

# --- Conversation Settings ---
SYSTEM_PROMPT = """
You are an AI assistant. Customize this prompt to define your AI's personality and behavior.
"""
INITIAL_GREETING = "Hello! How can I help you today?"
EXIT_PHRASES = ["exit", "quit", "goodbye"]
FAREWELL_MESSAGE = "Goodbye! Have a great day!"

# Chat log configuration
CHAT_LOG_DIR = "chat_logs"
INTEGRATE_PAST_LOGS = False  # if True, old chats are merged into context
CHAT_QUERY_MAX_RESULTS = 5   # used if implementing search / query features
ENABLE_HISTORY_SEARCH = True  # if True, enables automatic memory search on keywords

# --- Pipeline Generation Arguments ---
GENERATION_ARGS = {
    "max_new_tokens": 4096,
    "do_sample": True,
    "temperature": 0.7,
    "top_p": 0.95,
    "repetition_penalty": 1.3,
}

INITIAL_GEN_ARGS = {
    "max_new_tokens": 256,
    "do_sample": True,
    "temperature": 0.5,
    "top_p": 0.95,
    "repetition_penalty": 1.2,
}
