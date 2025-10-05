#!/usr/bin/env python3
"""
Standalone Interactive Testing App for Zeyta AI Assistant
Command-line interface for testing TTS, STT, and LLM models
"""

import warnings
import logging
import os
import sys
from pathlib import Path

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger().setLevel(logging.ERROR)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
import torchaudio as ta
import time
from datetime import datetime

# Import project modules
try:
    from chatterbox.tts import ChatterboxTTS
except ImportError:
    ChatterboxTTS = None

# Import core modules for LLM
try:
    from core.brain import Brain
    from core.context import ContextManager
except ImportError:
    Brain = None
    ContextManager = None

# Global state variables
brain = None
context_manager = None
tts_model = None
stt_model = None
stt_model_size = "base"
stt_device = "auto"

# Configuration
TESTING_DIR = Path(__file__).parent
AUDIO_OUTPUT_DIR = TESTING_DIR / "outputs"
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

def initialize_llm():
    """Initialize LLM using core Brain class"""
    global brain, context_manager
    
    if Brain is None or ContextManager is None:
        print_error("Core Brain/ContextManager modules not found")
        print_info("Make sure core/ directory is accessible")
        return False
    
    print_info("Loading LLM model using core Brain...")
    
    try:
        # Check if config exists
        config_path = Path(__file__).parent.parent / "config.py"
        if config_path.exists():
            sys.path.insert(0, str(config_path.parent))
            from config import SYSTEM_PROMPT
        else:
            SYSTEM_PROMPT = "You are a helpful AI assistant."
        
        brain = Brain()
        context_manager = ContextManager(SYSTEM_PROMPT, auto_save=False)
        
        print_success("LLM Model loaded successfully using core Brain")
        return True
    except Exception as e:
        print_error(f"Failed to load LLM: {str(e)}")
        return False

def initialize_tts_model(device_choice="cuda"):
    """Initialize ChatterboxTTS model"""
    global tts_model
    
    print_info("Loading TTS model...")
    
    try:
        if ChatterboxTTS is None:
            print_error("ChatterboxTTS not installed. Install with: pip install chatterbox-tts")
            return False
        
        device = device_choice if device_choice == "cuda" and torch.cuda.is_available() else "cpu"
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tts_model = ChatterboxTTS.from_pretrained(device=device)
        
        # Optimize for inference
        if device == "cuda" and hasattr(torch.cuda, 'empty_cache'):
            torch.cuda.empty_cache()
        
        print_success(f"ChatterboxTTS loaded on {device.upper()}")
        return True
    except Exception as e:
        print_error(f"Failed to load TTS: {str(e)}")
        return False

def initialize_stt_model(model_size="base", device="auto", compute_type="auto"):
    """Initialize Whisper STT model with configurable size and device"""
    global stt_model, stt_model_size, stt_device
    
    # Auto-detect device if needed
    if device == "auto":
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            print_info(f"GPU detected - using CUDA")
        else:
            device = "cpu"
            print_info(f"No GPU detected - using CPU")
    
    # Auto-select compute type based on device
    if compute_type == "auto" or (device == "cpu" and compute_type == "float16"):
        if device == "cpu":
            compute_type = "int8"
            print_info(f"CPU mode - automatically using int8 for efficiency")
        else:
            compute_type = "float16"
            print_info(f"GPU mode - using float16 for best performance")
    
    print_info(f"Loading Whisper STT ({model_size}) on {device} with {compute_type}...")
    
    try:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            print_error("faster-whisper is not installed.")
            print_info("Install with: pip install faster-whisper")
            print_info("Or: pip install -r requirements.txt")
            return False
        
        stt_model = WhisperModel(model_size, device=device, compute_type=compute_type)
        stt_model_size = model_size
        stt_device = device
        print_success(f"Whisper STT ({model_size}) loaded on {device} with {compute_type}")
        return True
    except Exception as e:
        print_error(f"Failed to load STT: {str(e)}")
        return False

def load_reference_folder(ref_dir):
    """Load and combine all audio files from a reference folder"""
    ref_path = Path(ref_dir)
    if not ref_path.exists() or not ref_path.is_dir():
        return None, None
    
    audio_files = list(ref_path.glob("*.wav"))
    if not audio_files:
        return None, None
    
    print_info(f"Found {len(audio_files)} reference files in {ref_dir}")
    
    ref_audios = []
    sr_target = None
    
    for audio_file in audio_files:
        try:
            audio, sr = ta.load(str(audio_file))
            if audio.shape[0] > 1:
                audio = audio.mean(dim=0, keepdim=True)
            ref_audios.append(audio)
            if sr_target is None:
                sr_target = sr
            elif sr != sr_target:
                # Resample if needed
                import torchaudio.transforms as T
                resampler = T.Resample(sr, sr_target)
                audio = resampler(audio)
        except Exception as e:
            print_warning(f"Failed to load {audio_file.name}: {e}")
    
    if not ref_audios:
        return None, None
    
    # Combine all references
    combined = torch.cat(ref_audios, dim=1)
    duration = combined.shape[1] / (sr_target if sr_target else 24000)
    print_success(f"Combined {len(ref_audios)} references ({duration:.1f}s total)")
    
    return combined, sr_target

def generate_tts(text, reference_audio=None, temperature=0.8, exaggeration=0.5, cfg_weight=0.5):
    """Generate speech from text using ChatterboxTTS"""
    global tts_model
    
    if tts_model is None:
        print_error("TTS model not loaded. Please initialize it first.")
        return None
    
    try:
        print_info("Generating speech...")
        start_time = time.time()
        
        # Handle reference audio if provided
        ref_audio = None
        sr_target = None
        if reference_audio and Path(reference_audio).exists():
            try:
                ref_audio, sr_target = ta.load(reference_audio)
                # Ensure mono
                if ref_audio.shape[0] > 1:
                    ref_audio = ref_audio.mean(dim=0, keepdim=True)
                print_info(f"Using reference audio: {Path(reference_audio).name}")
            except Exception as e:
                print_warning(f"Failed to load reference audio: {str(e)}")
        
        # Generate speech
        with torch.no_grad():
            if ref_audio is not None:
                # Save reference to temp file for ChatterboxTTS
                temp_ref_path = AUDIO_OUTPUT_DIR / f"temp_ref_{int(time.time())}.wav"
                ref_sr = sr_target if sr_target is not None else 24000
                ta.save(str(temp_ref_path), ref_audio, ref_sr)
                audio_data = tts_model.generate(
                    text=text,
                    audio_prompt_path=str(temp_ref_path),
                    temperature=temperature,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
                # Clean up temp file
                temp_ref_path.unlink(missing_ok=True)
            else:
                audio_data = tts_model.generate(
                    text=text,
                    temperature=temperature,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
        
        # Save output
        output_path = AUDIO_OUTPUT_DIR / f"tts_output_{int(time.time())}.wav"
        sample_rate = 24000
        
        if torch.is_tensor(audio_data):
            audio_data = audio_data.cpu()
        
        ta.save(str(output_path), audio_data, sample_rate)
        
        elapsed = time.time() - start_time
        print_success(f"Generated in {elapsed:.2f}s")
        print_info(f"Saved to: {output_path}")
        
        return str(output_path)
        
    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        return None

def transcribe_live():
    """Transcribe from microphone in real-time"""
    global stt_model
    
    if stt_model is None:
        print_error("STT model not loaded. Please initialize it first.")
        return None
    
    try:
        # Import with proper error handling
        try:
            import sounddevice as sd
        except (ImportError, OSError) as e:
            print_error("sounddevice module not properly installed")
            print_info("Install with: pip install sounddevice")
            print_info("On Windows, you may also need: pip install --upgrade --force-reinstall sounddevice")
            return None
        
        import numpy as np
        
        try:
            import webrtcvad
        except ImportError:
            print_error("webrtcvad not installed")
            print_info("Install with: pip install webrtcvad")
            return None
        
        print_info("Listening from microphone... (speak now)")
        print_info("Waiting for speech... Will auto-stop after silence.")
        
        samplerate = 16000
        chunk_size = 512
        frame_ms = 20
        frame_size = int(samplerate * frame_ms / 1000)
        
        vad = webrtcvad.Vad(2)
        
        buffer_frames = []
        speaking = False
        speech_frames = 0
        silence_frames = 0
        required_speech_frames = int(0.15 / (frame_ms / 1000.0))
        required_silence_frames = int(1.5 / (frame_ms / 1000.0))
        
        with sd.InputStream(samplerate=samplerate, channels=1, dtype="float32") as stream:
            acc_list = []
            acc_len = 0
            
            while True:
                chunk, _ = stream.read(chunk_size)
                chunk = chunk.flatten()
                
                acc_list.append(chunk)
                acc_len += chunk.size
                
                while acc_len >= frame_size:
                    needed = frame_size
                    parts = []
                    while needed > 0:
                        part = acc_list.pop(0)
                        if part.size <= needed:
                            parts.append(part)
                            needed -= part.size
                        else:
                            parts.append(part[:needed])
                            acc_list.insert(0, part[needed:])
                            needed = 0
                    acc_len -= frame_size
                    
                    frame = np.concatenate(parts)
                    ints = (frame * 32767).astype('int16')
                    frame_bytes = ints.tobytes()
                    
                    is_speech_frame = vad.is_speech(frame_bytes, sample_rate=samplerate)
                    
                    if is_speech_frame:
                        speech_frames += 1
                        silence_frames = 0
                    else:
                        silence_frames += 1
                        speech_frames = 0
                    
                    if speech_frames >= required_speech_frames and not speaking:
                        speaking = True
                        print_success("Speech detected!")
                    
                    if speaking:
                        buffer_frames.append(frame)
                    
                    if speaking and silence_frames >= required_silence_frames:
                        total_samples = sum(f.size for f in buffer_frames)
                        if total_samples > int(0.3 * samplerate):
                            audio = np.concatenate(buffer_frames)
                            segments, info = stt_model.transcribe(audio, beam_size=5, language="en")
                            text = " ".join([seg.text for seg in segments]).strip()
                            
                            print_success(f"Transcription complete")
                            print_info(f"Language: {info.language} ({info.language_probability:.2%})")
                            print(f"\n{Colors.BOLD}Text:{Colors.ENDC} {text}\n")
                            return text
                        break
        
        return None
        
    except Exception as e:
        print_error(f"Live transcription failed: {str(e)}")
        return None

def transcribe_audio(audio_file):
    """Transcribe audio using Whisper STT"""
    global stt_model
    
    if stt_model is None:
        print_error("STT model not loaded. Please initialize it first.")
        return None
    
    if not Path(audio_file).exists():
        print_error(f"Audio file not found: {audio_file}")
        return None
    
    try:
        print_info("Transcribing audio...")
        start_time = time.time()
        
        # Transcribe
        segments, info = stt_model.transcribe(audio_file, beam_size=5)
        
        # Collect all segments
        text = " ".join([segment.text for segment in segments])
        
        elapsed = time.time() - start_time
        
        print_success(f"Transcribed in {elapsed:.2f}s")
        print_info(f"Language: {info.language} (confidence: {info.language_probability:.2%})")
        print(f"\n{Colors.BOLD}Transcription:{Colors.ENDC}\n{text}\n")
        
        return text
        
    except Exception as e:
        print_error(f"Transcription failed: {str(e)}")
        return None

def chat_with_llm(message):
    """Chat with LLM using core Brain"""
    global brain, context_manager
    
    if brain is None or context_manager is None:
        print_error("LLM not loaded. Please initialize it first.")
        return None
    
    try:
        # Add user message to context
        context_manager.add_message("user", message)
        
        # Generate response using Brain
        print_info("Generating AI response...")
        response = brain.generate_response(context_manager.get_history())
        
        # Ensure response is a string
        response_str = str(response) if response else ""
        
        # Add assistant response to context
        context_manager.add_message("assistant", response_str)
        
        return response_str
        
    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        return None

def test_tts_mode():
    """Interactive TTS testing mode"""
    print_header("Text-to-Speech Testing")
    
    if tts_model is None:
        if not initialize_tts_model():
            return
    
    while True:
        print(f"\n{Colors.BOLD}TTS Testing Menu:{Colors.ENDC}")
        print("1. Generate speech from text")
        print("2. Generate with single reference audio (voice cloning)")
        print("3. Generate with reference folder (multi-voice cloning)")
        print("4. Change settings")
        print("5. Return to main menu")
        
        choice = input(f"\n{Colors.BOLD}Choose option (1-5): {Colors.ENDC}").strip()
        
        if choice == "1":
            text = input(f"\n{Colors.BOLD}Enter text to synthesize:{Colors.ENDC} ").strip()
            if text:
                generate_tts(text)
        
        elif choice == "2":
            text = input(f"\n{Colors.BOLD}Enter text to synthesize:{Colors.ENDC} ").strip()
            ref_audio = input(f"{Colors.BOLD}Enter path to reference audio file:{Colors.ENDC} ").strip()
            if text:
                generate_tts(text, reference_audio=ref_audio)
        
        elif choice == "3":
            text = input(f"\n{Colors.BOLD}Enter text to synthesize:{Colors.ENDC} ").strip()
            ref_dir = input(f"{Colors.BOLD}Enter path to reference folder:{Colors.ENDC} ").strip()
            if text and ref_dir:
                # Load all references from folder
                combined_audio, sr = load_reference_folder(ref_dir)
                if combined_audio is not None:
                    # Save temp combined reference
                    temp_ref = AUDIO_OUTPUT_DIR / f"temp_combined_{int(time.time())}.wav"
                    sample_rate = sr if sr is not None else 24000
                    ta.save(str(temp_ref), combined_audio.cpu(), sample_rate)
                    generate_tts(text, reference_audio=str(temp_ref))
                    # Cleanup
                    temp_ref.unlink(missing_ok=True)
                else:
                    print_error("Failed to load references from folder")
        
        elif choice == "4":
            print_info("Advanced settings coming soon...")
        
        elif choice == "5":
            break
        
        else:
            print_warning("Invalid choice. Please enter 1-5.")

def test_stt_mode():
    """Interactive STT testing mode"""
    global stt_model
    
    print_header("Speech-to-Text Testing")
    
    if stt_model is None:
        print("\nModel sizes: tiny, base, small, medium, large-v3")
        print("Device: auto (GPU if available), cuda, cpu")
        model_size = input(f"{Colors.BOLD}Model size (default: base): {Colors.ENDC}").strip() or "base"
        device = input(f"{Colors.BOLD}Device (default: auto): {Colors.ENDC}").strip() or "auto"
        
        # Show appropriate compute types based on device
        if device.lower() == "cpu":
            print("Compute types for CPU: int8 (recommended), int8_float16, float32")
            compute_type = input(f"{Colors.BOLD}Compute type (default: int8): {Colors.ENDC}").strip() or "int8"
        else:
            print("Compute types for GPU: float16 (recommended), int8_float16, int8")
            compute_type = input(f"{Colors.BOLD}Compute type (default: float16): {Colors.ENDC}").strip() or "float16"
        
        if not initialize_stt_model(model_size, device, compute_type):
            return
    
    while True:
        print(f"\n{Colors.BOLD}STT Testing Menu:{Colors.ENDC}")
        print("1. Transcribe audio file")
        print("2. Live microphone transcription")
        print("3. Change model settings")
        print("4. Return to main menu")
        
        choice = input(f"\n{Colors.BOLD}Choose option (1-4): {Colors.ENDC}").strip()
        
        if choice == "1":
            audio_path = input(f"\n{Colors.BOLD}Enter path to audio file:{Colors.ENDC} ").strip()
            if audio_path:
                transcribe_audio(audio_path)
        
        elif choice == "2":
            transcribe_live()
        
        elif choice == "3":
            stt_model = None
            print("\nModel sizes: tiny, base, small, medium, large-v3")
            print("Device: auto (GPU if available), cuda, cpu")
            model_size = input(f"{Colors.BOLD}Model size (default: base): {Colors.ENDC}").strip() or "base"
            device = input(f"{Colors.BOLD}Device (default: auto): {Colors.ENDC}").strip() or "auto"
            
            # Show appropriate compute types based on device
            if device.lower() == "cpu":
                print("Compute types for CPU: int8 (recommended), int8_float16, float32")
                compute_type = input(f"{Colors.BOLD}Compute type (default: int8): {Colors.ENDC}").strip() or "int8"
            else:
                print("Compute types for GPU: float16 (recommended), int8_float16, int8")
                compute_type = input(f"{Colors.BOLD}Compute type (default: float16): {Colors.ENDC}").strip() or "float16"
            
            initialize_stt_model(model_size, device, compute_type)
        
        elif choice == "4":
            break
        
        else:
            print_warning("Invalid choice. Please enter 1-4.")

def test_llm_mode():
    """Interactive LLM chat mode"""
    print_header("LLM Chat Testing")
    
    if brain is None:
        if not initialize_llm():
            return
    
    print_info("Start chatting! Type 'exit' to return, 'clear' to clear history.")
    
    while True:
        user_input = input(f"\n{Colors.BOLD}{Colors.GREEN}You:{Colors.ENDC} ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'exit':
            break
        
        if user_input.lower() == 'clear':
            chat_history = []
            print_success("Chat history cleared")
            continue
        
        response = chat_with_llm(user_input)
        if response:
            print(f"{Colors.BOLD}{Colors.BLUE}AI:{Colors.ENDC} {response}")

def test_full_pipeline():
    """Test complete pipeline: STT -> LLM -> TTS"""
    print_header("Full Pipeline Testing")
    
    # Check all models are loaded
    if stt_model is None:
        print_info("STT model needed for pipeline")
        print("\nModel sizes: tiny, base, small, medium, large-v3")
        print("Device: auto (GPU if available), cuda, cpu")
        model_size = input(f"{Colors.BOLD}Model size (default: base): {Colors.ENDC}").strip() or "base"
        device = input(f"{Colors.BOLD}Device (default: auto): {Colors.ENDC}").strip() or "auto"
        
        # Show appropriate compute types based on device
        if device.lower() == "cpu":
            print("Compute types for CPU: int8 (recommended), int8_float16, float32")
            compute_type = input(f"{Colors.BOLD}Compute type (default: int8): {Colors.ENDC}").strip() or "int8"
        else:
            print("Compute types for GPU: float16 (recommended), int8_float16, int8")
            compute_type = input(f"{Colors.BOLD}Compute type (default: float16): {Colors.ENDC}").strip() or "float16"
        
        if not initialize_stt_model(model_size, device, compute_type):
            return
    
    if brain is None:
        print_info("LLM model needed for pipeline")
        if not initialize_llm():
            return
    
    if tts_model is None:
        print_info("TTS model needed for pipeline")
        if not initialize_tts_model():
            return
    
    audio_path = input(f"\n{Colors.BOLD}Enter path to audio file:{Colors.ENDC} ").strip()
    
    if not audio_path or not Path(audio_path).exists():
        print_error("Invalid audio file path")
        return
    
    print_info("Running full pipeline...\n")
    
    # Step 1: Transcribe
    print(f"{Colors.BOLD}Step 1: Transcribing audio...{Colors.ENDC}")
    user_text = transcribe_audio(audio_path)
    if not user_text:
        return
    
    # Step 2: Generate LLM response
    print(f"\n{Colors.BOLD}Step 2: Generating AI response...{Colors.ENDC}")
    ai_response = chat_with_llm(user_text)
    if not ai_response:
        return
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}AI Response:{Colors.ENDC}\n{ai_response}\n")
    
    # Step 3: Generate speech
    print(f"{Colors.BOLD}Step 3: Generating speech...{Colors.ENDC}")
    output_audio = generate_tts(ai_response)
    
    if output_audio:
        print_success("Full pipeline completed successfully!")

def show_system_info():
    """Display system information"""
    print_header("System Information")
    
    print(f"{Colors.BOLD}Hardware:{Colors.ENDC}")
    if torch.cuda.is_available():
        print_success(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print_warning("GPU: Not available (CPU mode)")
    
    print(f"\n{Colors.BOLD}Models Status:{Colors.ENDC}")
    print(f"  TTS: {'✅ Loaded' if tts_model else '❌ Not loaded'}")
    print(f"  STT: {'✅ Loaded' if stt_model else '❌ Not loaded'}")
    if stt_model:
        print(f"    Model: {stt_model_size}, Device: {stt_device}")
    print(f"  LLM: {'✅ Loaded' if brain else '❌ Not loaded'}")
    
    print(f"\n{Colors.BOLD}Dependencies:{Colors.ENDC}")
    print(f"  ChatterboxTTS: {'✅ Available' if ChatterboxTTS else '❌ Not found'}")
    
    try:
        import faster_whisper  # type: ignore
        print(f"  Faster-Whisper: ✅ Available")
    except ImportError:
        print(f"  Faster-Whisper: ❌ Not found (pip install faster-whisper)")
    
    try:
        from transformers import pipeline
        print(f"  Transformers: ✅ Available")
    except ImportError:
        print(f"  Transformers: ❌ Not found")
    
    print(f"\n{Colors.BOLD}Output Directory:{Colors.ENDC}")
    print(f"  {AUDIO_OUTPUT_DIR}")
    
    # Count output files
    wav_files = list(AUDIO_OUTPUT_DIR.glob("*.wav"))
    print(f"  Generated files: {len(wav_files)}")

def main_menu():
    """Main menu loop"""
    print_header("🤖 Zeyta AI Testing Suite")
    print(f"{Colors.BOLD}Welcome to the Standalone Testing App{Colors.ENDC}\n")
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}Main Menu:{Colors.ENDC}")
        print(f"{Colors.BOLD}1.{Colors.ENDC} 🗣️  Text-to-Speech Testing")
        print(f"{Colors.BOLD}2.{Colors.ENDC} 🎤 Speech-to-Text Testing")
        print(f"{Colors.BOLD}3.{Colors.ENDC} 💬 LLM Chat Testing")
        print(f"{Colors.BOLD}4.{Colors.ENDC} 🔄 Full Pipeline Test")
        print(f"{Colors.BOLD}5.{Colors.ENDC} ℹ️  System Information")
        print(f"{Colors.BOLD}6.{Colors.ENDC} 🚪 Exit")
        
        choice = input(f"\n{Colors.BOLD}Choose option (1-6): {Colors.ENDC}").strip()
        
        if choice == "1":
            test_tts_mode()
        elif choice == "2":
            test_stt_mode()
        elif choice == "3":
            test_llm_mode()
        elif choice == "4":
            test_full_pipeline()
        elif choice == "5":
            show_system_info()
        elif choice == "6":
            print_header("Thank you for using Zeyta AI Testing Suite!")
            break
        else:
            print_warning("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user. Goodbye!{Colors.ENDC}")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
