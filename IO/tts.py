from pathlib import Path
import subprocess, sys, winsound, logging, time
from config import TTS_BACKEND

ROOT = Path(__file__).resolve().parent.parent
PIPER_DIR = ROOT / "piper"

PIPER_EXE = PIPER_DIR / "piper.exe"
MODEL = PIPER_DIR / "en_US-hfc_female-medium.onnx"
OUTPUT = ROOT / "output.wav"

_coqui_ready = False

def initialize_tts():
    """Initialize selected TTS backend."""
    global _coqui_ready
    if TTS_BACKEND == "coqui":
        try:
            from IO import coqui_backend as cb
            _coqui_ready = cb.initialize_coqui()
            if _coqui_ready:
                logging.info("[TTS] Using Coqui TTS backend")
            else:
                logging.error("[TTS] Coqui TTS initialization failed; falling back to Piper")
        except Exception as e:
            logging.error(f"[TTS] Failed to init Coqui TTS backend: {e}")
            _coqui_ready = False
    
    # Fallback / Piper init (always validate Piper so we can fallback mid-run)
    if not PIPER_EXE.exists():
        raise FileNotFoundError(f"Piper executable not found at: {PIPER_EXE}")
    if not MODEL.exists():
        raise FileNotFoundError(f"Model not found at: {MODEL}")
    logging.info("[TTS] Piper backend validated")

def _sanitize(text: str) -> str:
    import re
    # Remove fenced code blocks ```...``` and triple single-quoted blocks '''...'''
    sanitized = re.sub(r"```[\s\S]*?```", "", text)
    sanitized = re.sub(r"'''[\s\S]*?'''", "", sanitized)
    sanitized = "\n".join(line.rstrip() for line in sanitized.splitlines())
    return sanitized.strip()

def _speak_piper(sanitized: str):
    cmd = [str(PIPER_EXE), "-m", str(MODEL), "-f", str(OUTPUT)]
    cp = subprocess.run(cmd, input=sanitized.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        logging.error(f"[TTS] Piper exited with code {cp.returncode}: {cp.stderr.decode(errors='ignore')[:200]}")
        return
    if OUTPUT.exists():
        try:
            winsound.PlaySound(str(OUTPUT), winsound.SND_FILENAME)
        finally:
            try:
                OUTPUT.unlink()
            except Exception:
                pass
    else:
        logging.warning("[TTS] Piper produced no output file")

def _speak_coqui(sanitized: str):
    from IO import coqui_backend as cb
    wav_path = cb.synthesize(sanitized)
    if wav_path and wav_path.exists():
        try:
            # Get audio duration for proper timing
            try:
                import wave
                with wave.open(str(wav_path), 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    sample_rate = wav_file.getframerate()
                    duration = frames / float(sample_rate)
                    # Add 1 second buffer for safety
                    wait_time = max(duration + 1.0, 3.0)  # Minimum 3 seconds
            except Exception as e:
                logging.warning(f"[TTS] Could not determine audio duration: {e}, using default wait time")
                # Estimate based on text length (roughly 150 words per minute)
                word_count = len(sanitized.split())
                estimated_duration = (word_count / 150) * 60  # Convert to seconds
                wait_time = max(estimated_duration + 2.0, 4.0)  # Minimum 4 seconds
            
            logging.info(f"[TTS] Playing Coqui TTS audio: {wav_path} (duration: {wait_time:.1f}s)")
            # Use ASYNC flag to avoid blocking, but still play audio
            winsound.PlaySound(str(wav_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            logging.info("[TTS] Coqui TTS playback initiated")
            
            # Wait for calculated duration to allow playback to complete
            time.sleep(wait_time)
            logging.debug(f"[TTS] Playback wait completed ({wait_time:.1f}s)")
            
        except Exception as e:
            logging.error(f"[TTS] Coqui TTS playback failed: {e}")
        finally:
            # Clean up after playback delay
            try:
                if wav_path.exists():
                    wav_path.unlink()
                    logging.debug(f"[TTS] Cleaned up temporary file: {wav_path}")
            except Exception:
                pass
    else:
        logging.error(f"[TTS] Coqui TTS synthesis failed (path={wav_path}); falling back to Piper")
        _speak_piper(sanitized)

def speak(text: str):
    """Unified speak API for either Piper or Coqui TTS."""
    sanitized = _sanitize(text)
    if not sanitized:
        return
    if TTS_BACKEND == "coqui":
        if _coqui_ready:
            _speak_coqui(sanitized)
        else:
            logging.info("[TTS] Coqui TTS requested but not ready; using Piper fallback")
            _speak_piper(sanitized)
    else:
        _speak_piper(sanitized)