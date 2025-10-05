# coqui_backend.py - Simple Coqui TTS backend similar to Piper setup

import logging
import time
from pathlib import Path

_tts_model = None
_ready = False

def initialize_coqui():
    """Initialize Coqui TTS model."""
    global _tts_model, _ready
    
    try:
        # Lazy import to avoid startup overhead
        from TTS.api import TTS
        import torch
        from config import COQUI_DEVICE
        
        # Determine device
        device = "cuda" if COQUI_DEVICE.lower() == "cuda" and torch.cuda.is_available() else "cpu"
        logging.info(f"[Coqui] Using device: {device}")
        
        # Initialize TTS model
        logging.info("[Coqui] Loading Tacotron2 model...")
        _tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)
        
        _ready = True
        logging.info("[Coqui] TTS initialized successfully")
        return True
        
    except Exception as e:
        logging.error(f"[Coqui] Failed to initialize: {e}")
        _ready = False
        return False

def synthesize(text: str) -> Path | None:
    """Synthesize text to audio file."""
    global _tts_model, _ready
    
    if not _ready or _tts_model is None:
        logging.error("[Coqui] TTS not initialized")
        return None
        
    try:
        # Generate unique output filename
        output_file = Path.cwd() / f"coqui_out_{int(time.time() * 1000)}.wav"
        
        # Synthesize audio
        logging.debug(f"[Coqui] Synthesizing: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        _tts_model.tts_to_file(text=text, file_path=str(output_file))
        
        if output_file.exists():
            logging.debug(f"[Coqui] Audio generated: {output_file.name}")
            return output_file
        else:
            logging.error("[Coqui] Audio file was not generated")
            return None
            
    except Exception as e:
        logging.error(f"[Coqui] Synthesis failed: {e}")
        return None

def is_ready() -> bool:
    """Check if Coqui TTS is ready."""
    return _ready