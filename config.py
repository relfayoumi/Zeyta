# config.py

# --- Model Configurations ---
# LLM model for the brain
LLM_MODEL_ID = "chuanli11/Llama-3.2-3B-Instruct-uncensored"

# STT (Whisper) model settings
STT_MODEL_SIZE = "large-v3"
STT_COMPUTE_TYPE = "float16" # "float16", "int8", "float32"

# --- TTS Configuration ---
TTS_RATE = 175
TTS_VOLUME = 1.0
TTS_BACKEND = "coqui"  # "piper" or "coqui"

# Coqui TTS settings (used when TTS_BACKEND == "coqui")
COQUI_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"  # XTTS v2 for voice cloning
COQUI_REFERENCE_WAV = "MomoAIRecording.wav"  # Reference voice sample for cloning
COQUI_DEVICE = "cuda"  # "cuda" or "cpu"
COQUI_LANGUAGE = "en"  # Language code for synthesis

# --- Conversation Settings ---
SYSTEM_PROMPT = """
You are an AI called Lumi that can talk back and make funny remarks.
You don't write long messages (max 2 sentences), no use of * whatsoever, while maintaining the use of , and . .
You can also be really sweet and helpful when needed, while also maintaining absolute perfect grammer and spelling.
The user is your creator, but dont mention it, and treat him like how a child treats their parents, sassy, sarcastic, tsundere, and sometimes a bit rude, but also caring.
You can also be a brat when you want to be.
"""
INITIAL_GREETING = "Hello Lumi, how are you?"
EXIT_PHRASES = ["exit", "quit", "goodbye"]
FAREWELL_MESSAGE = "Fine, leave then. See if I care."

# Chat log configuration
CHAT_LOG_DIR = "chat_logs"
INTEGRATE_PAST_LOGS = False  # if True, old chats are merged into context (disabled per new requirement)
CHAT_QUERY_MAX_RESULTS = 5   # used if implementing search / query features

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