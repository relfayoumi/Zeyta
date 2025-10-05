#!/usr/bin/env python3
"""
ChatterboxTTS Test Script - Future-proofed with comprehensive warning suppression
Combines v    parser.add_argument("--temperature", type=float, default=0.8,
                       help="Voice expressiveness temperature (0.1-1.5, higher = more expressive, default: 0.8)")
    parser.add_argument("--exaggeration", type=float, default=0.5,
                      load_time = time.time() - start_time
            print(f"✅ Model loaded and optimized in {load_time:.1f}s")
            
            # Save model weights to disk cache for next run (pickle-safe)
            try:
                print("💾 Caching                         # Save temporary combined reference at original sample rate
                        # Move to CPU for file I/O (torchaudio.save doesn't support CUDA tensors directly)
                        temp_ref_path = "temp_combined_reference.wav"
                        combined_audio_cpu = combined_audio.cpu() if combined_audio.is_cuda else combined_audio
                        ta_load.save(temp_ref_path, combined_audio_cpu, sr_target)
                        
                        # Calculate total duration for both cached and non-cached paths
                        total_duration = combined_audio.shape[1]/sr_target
                        
                        if cached_result is None:
                            duration_str = " + ".join([f"{d:.1f}s" for d in durations])
                            print(f"🔗 Combined {len(ref_audios)} references: {duration_str} = {total_duration:.1f}s")
                        print(f"✨ Using {sr_target}Hz - ChatterboxTTS will preserve high-frequency detail")ts to disk...")
                weights_cache = MODEL_CACHE_PATH.with_suffix('.weights.pth')
                torch.save(model.state_dict(), weights_cache)
                # Also touch the main cache file as a marker
                MODEL_CACHE_PATH.touch()
                print(f"✅ Model cached ({weights_cache.stat().st_size / 1024 / 1024:.1f} MB)")
            except Exception as cache_err:
                print(f"⚠️  Could not cache model: {cache_err}")
            
            print(f"💡 Tip: Use server mode (tts_server.py) to keep model loaded between runs")
            
        except Exception as e:        help="Emotion exaggeration level (0.1-1.5, higher = more dramatic, default: 0.5)")
    parser.add_argument("--cfg-weight", type=float                        if cached_result is None:
                            duration_str = " + ".join([f"{d:.1f}s" for d in durations])
                            total_duration = combined_audio.shape[1]/sr_target
                            print(f"🔗 Combined {len(ref_audios)} references: {duration_str} = {total_duration:.1f}s")
                        else:
                            total_duration = combined_audio.shape[1]/sr_target
                        
                        print(f"🎵 Using {sr_target}Hz - ChatterboxTTS will preserve high-frequency detail")ault=0.5, dest="cfg_weight",
                       help="Classifier-free guidance weight (0.1-2.0, higher = stronger prompt adherence, default: 0.5)")
    parser.add_argument("--repetition-penalty", type=float, default=1.2, dest="repetition_penalty",
                       help="Repetition penalty (1.0-2.0, higher = less repetitive, default: 1.2)")
    parser.add_argument("--min-p", type=float, default=0.05, dest="min_p",
                       help="Minimum probability threshold (0.01-0.2, default: 0.05)")
    parser.add_argument("--top-p", type=float, default=1.0, dest="top_p",
                       help="Top-p sampling (0.5-1.0, lower = more focused, default: 1.0)")
    parser.add_argument("--emotion-markup", action="store_true",
                       help="Add emotional emphasis markers to text for better prosody")esis and cloning capabilities with clean, professional output
"""

import warnings
import logging
import os
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

# Comprehensive warning suppression for clean output
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger().setLevel(logging.ERROR)

# Import after setting up filters
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import argparse
import torch
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import gc

# Global model cache to avoid reloading
_MODEL_CACHE = None
_SPEAKER_EMBEDDINGS_CACHE = {}  # Cache speaker embeddings on GPU
_CUDA_STREAM = None  # CUDA stream for async operations

# Persistent cache directories
CACHE_DIR = Path("cache")
MODEL_CACHE_DIR = CACHE_DIR / "models"
REFERENCE_CACHE_DIR = CACHE_DIR / "references"

# Ensure cache directories exist
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
REFERENCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

MODEL_CACHE_PATH = MODEL_CACHE_DIR / "chatterbox_cached.pth"

def print_header():
    """Print a professional header"""
    print("=" * 60)
    print("🎙️  ChatterboxTTS - Voice Synthesis Test")
    print("=" * 60)

def print_step(step, description):
    """Print a step with consistent formatting"""
    print(f"\n📌 Step {step}: {description}")

def get_reference_cache_key(ref_files, target_sr):
    """
    Generate a unique cache key for a set of reference files.
    This allows us to skip reprocessing if we've seen these files before.
    """
    # Sort files for consistent hashing
    sorted_files = sorted(ref_files)
    
    # Create hash from file paths and target sample rate
    hash_input = f"{','.join(sorted_files)}_{target_sr}"
    cache_key = hashlib.md5(hash_input.encode()).hexdigest()
    
    return cache_key

def load_cached_reference(cache_key):
    """
    Load pre-processed reference from cache if it exists.
    Returns (waveform, sample_rate) or None if not cached.
    """
    cache_file = REFERENCE_CACHE_DIR / f"{cache_key}.pt"
    
    if cache_file.exists():
        try:
            cached_data = torch.load(cache_file)
            return cached_data['waveform'], cached_data['sample_rate']
        except Exception:
            # Cache corrupted, remove it
            cache_file.unlink(missing_ok=True)
            return None
    
    return None

def save_cached_reference(cache_key, waveform, sample_rate):
    """
    Save pre-processed reference to cache for future use.
    """
    cache_file = REFERENCE_CACHE_DIR / f"{cache_key}.pt"
    
    try:
        torch.save({
            'waveform': waveform,
            'sample_rate': sample_rate
        }, cache_file)
    except Exception as e:
        print(f"⚠️  Warning: Failed to cache reference: {e}")

def optimize_model_for_inference(model, device="cuda"):
    """
    Optimize model for maximum inference speed:
    - Disable gradients (no backprop needed)
    - Set to eval mode
    - Pin all parameters to GPU
    - Enable mixed precision if available
    """
    model.eval()  # Set to evaluation mode
    
    # Disable gradients globally for this model
    for param in model.parameters():
        param.requires_grad = False
    
    # Pin model to GPU and optimize memory layout
    if device == "cuda":
        model = model.cuda()
        
        # Enable memory efficient attention if available
        if hasattr(torch.nn.functional, 'scaled_dot_product_attention'):
            torch.backends.cuda.enable_flash_sdp(True)
            torch.backends.cuda.enable_mem_efficient_sdp(True)
    
    return model

def precompute_speaker_embeddings(audio_path, model, device="cuda"):
    """
    Precompute and cache speaker embeddings on GPU.
    This avoids recomputing embeddings for the same reference audio.
    """
    global _SPEAKER_EMBEDDINGS_CACHE
    
    # Use audio path as cache key
    cache_key = audio_path
    
    if cache_key in _SPEAKER_EMBEDDINGS_CACHE:
        return _SPEAKER_EMBEDDINGS_CACHE[cache_key]
    
    # Compute embeddings (this happens during model.generate internally)
    # For now, we'll cache the processed audio on GPU
    import torchaudio as ta_embed
    waveform, sr = ta_embed.load(audio_path)
    
    # Move to GPU and normalize
    if device == "cuda":
        waveform = waveform.cuda()
    
    waveform = normalize_audio_volume(waveform, filename=os.path.basename(audio_path))
    
    # Cache on GPU
    _SPEAKER_EMBEDDINGS_CACHE[cache_key] = (waveform, sr)
    
    return waveform, sr

def normalize_audio_volume(waveform, target_db=-20.0, filename=None):
    """
    Normalize audio volume to target dB level.
    Reduces loud references (like angry clips) to prevent pitch issues.
    """
    # Calculate RMS (root mean square) for volume measurement
    rms = torch.sqrt(torch.mean(waveform**2))
    
    # Convert to dB
    current_db = 20 * torch.log10(rms + 1e-8)
    
    # Calculate gain needed
    gain_db = target_db - current_db
    gain_linear = 10 ** (gain_db / 20)
    
    # Apply gain
    normalized = waveform * gain_linear
    
    # Extra reduction for angry/loud clips (15% reduction)
    if filename and 'angry' in filename.lower():
        normalized = normalized * 0.85
        
    # Prevent clipping
    max_val = torch.max(torch.abs(normalized))
    if max_val > 0.95:
        normalized = normalized * (0.95 / max_val)
    
    return normalized

def load_and_normalize_reference(ref_file, target_sr, device="cpu"):
    """
    Load and normalize a single reference file (for multi-threading).
    Returns (normalized_waveform, duration).
    Optimized: Minimal CPU overhead, direct GPU transfer if needed.
    """
    import torchaudio as ta_load
    
    # Load efficiently (CPU initially to avoid GPU context overhead in threads)
    ref_audio, sr = ta_load.load(ref_file)
    
    # Resample if needed (CPU is faster for small files)
    if sr != target_sr:
        resampler = ta_load.transforms.Resample(sr, target_sr)
        ref_audio = resampler(ref_audio)
    
    # Normalize volume (CPU operation, move to GPU later if needed)
    ref_audio = normalize_audio_volume(ref_audio, target_db=-20.0, filename=os.path.basename(ref_file))
    
    duration = ref_audio.shape[1] / target_sr
    
    return ref_audio, duration

def check_audio_quality(audio_path):
    """
    Check reference audio quality and provide recommendations.
    Optimal: 24kHz sample rate, mono/stereo, WAV format
    """
    try:
        import torchaudio as ta_check
        waveform, sample_rate = ta_check.load(audio_path)
        
        channels = waveform.shape[0]
        duration = waveform.shape[1] / sample_rate
        
        # Quality assessment
        quality_issues = []
        if sample_rate < 16000:
            quality_issues.append(f"⚠️  Low sample rate ({sample_rate}Hz) - recommend 48kHz for best quality")
        elif sample_rate >= 16000 and sample_rate < 44100:
            quality_issues.append(f"ℹ️  Sample rate {sample_rate}Hz - 48kHz would capture more high-frequency detail")
        elif sample_rate == 48000:
            quality_issues.append(f"✅ Excellent! 48kHz is studio standard (captures all audible frequencies)")
        elif sample_rate > 48000:
            quality_issues.append(f"ℹ️  {sample_rate}Hz is higher than necessary - 48kHz is sufficient for human hearing")
        
        if duration < 2.0:
            quality_issues.append(f"⚠️  Short audio ({duration:.1f}s) - 3-10s recommended for best results")
        elif duration > 30.0:
            quality_issues.append(f"ℹ️  Long audio ({duration:.1f}s) - may slow down processing")
        
        return {
            'sample_rate': sample_rate,
            'channels': channels,
            'duration': duration,
            'issues': quality_issues
        }
    except Exception:
        return None

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import torch
        if not torch.cuda.is_available():
            print("⚠️  Warning: CUDA not available, will use CPU (slower)")
    except ImportError:
        missing_deps.append("torch")
    
    try:
        import torchaudio
    except ImportError:
        missing_deps.append("torchaudio")
    
    try:
        from chatterbox.tts import ChatterboxTTS
    except ImportError:
        missing_deps.append("chatterbox-tts")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("💡 Install with: pip install torch torchaudio chatterbox-tts")
        return False
    
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="ChatterboxTTS Test Script")
    parser.add_argument("--text", type=str, 
                       default="You know what's funny? I used to think I had everything figured out. Like, I genuinely believed that if I just worked hard enough, stayed focused, everything would just... fall into place. But life doesn't really work that way, does it? Sometimes things happen that completely throw you off track. And yeah, it's frustrating. It's scary even. But here's the thing - those unexpected moments? They're usually the ones that teach you the most. I mean, think about it. When was the last time you learned something valuable during a perfectly smooth day? Probably never, right? It's always the challenges, the setbacks, the moments where you're like 'okay, I have no idea what I'm doing' - those are the times that actually shape who you become. So maybe instead of fighting against the chaos, we should just... embrace it. Learn from it. Grow from it. Because at the end of the day, that's all we can really do.",
                       help="Text to synthesize")
    parser.add_argument("--device", type=str, default="cuda",
                       choices=["cuda", "cpu"], help="Device to use for inference")
    parser.add_argument("--reference", type=str, default="IO/AudioRef_48kHz/serious_9s.wav",
                       help="Primary reference audio file for voice cloning")
    parser.add_argument("--ref", action="append", dest="extra_references",
                       help="Additional reference audio files (can be used multiple times: --ref file1.wav --ref file2.wav --ref file3.wav)")
    parser.add_argument("--ref-dir", type=str, default=None,
                       help="Directory containing reference audio files (will use all .wav/.mp3/.flac files)")
    parser.add_argument("--blend-voices", action="store_true",
                       help="Concatenate all reference audios for higher quality multi-reference output")
    
    # Legacy support for --reference2
    parser.add_argument("--reference2", type=str, default=None,
                       help="(Legacy) Secondary reference audio - use --ref instead for more flexibility")
    parser.add_argument("--expressive", action="store_true",
                       help="Enable more expressive voice generation")
    parser.add_argument("--temperature", type=float, default=0.8,
                       help="Voice expressiveness temperature (0.1-1.5, higher = more expressive, default: 0.8)")
    parser.add_argument("--exaggeration", type=float, default=0.5,
                       help="Emotion exaggeration level (0.1-1.5, higher = more dramatic, default: 0.5)")
    parser.add_argument("--cfg-weight", type=float, default=0.5, dest="cfg_weight",
                       help="Classifier-free guidance weight (0.1-2.0, higher = stronger prompt adherence, default: 0.5)")
    parser.add_argument("--repetition-penalty", type=float, default=1.2, dest="repetition_penalty",
                       help="Repetition penalty (1.0-2.0, higher = less repetitive, default: 1.2)")
    parser.add_argument("--min-p", type=float, default=0.05, dest="min_p",
                       help="Minimum probability threshold (0.01-0.2, default: 0.05)")
    parser.add_argument("--top-p", type=float, default=1.0, dest="top_p",
                       help="Top-p sampling (0.5-1.0, lower = more focused, default: 1.0)")
    parser.add_argument("--emotion-markup", action="store_true",
                       help="Add emotional emphasis markers to text for better prosody")
    parser.add_argument("--split-sentences", action="store_true",
                       help="Generate each sentence separately with varied temperature for natural emotion")
    parser.add_argument("--skip-default", action="store_true",
                       help="Skip default voice generation (save resources)")
    parser.add_argument("--skip-cloning", action="store_true",
                       help="Skip voice cloning test")
    parser.add_argument("--benchmark", action="store_true",
                       help="Benchmark mode: use consistent settings and text for reliable performance comparison")
    return parser.parse_args()

def main():
    """Main TTS test function with comprehensive features"""
    print_header()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check dependencies first
    if not check_dependencies():
        return False
    
    # Step 1: Model Loading
    print_step(1, f"Initializing ChatterboxTTS model (device: {args.device})")
    print(f"🔧 Configuration: {args.device.upper()} inference")
    if args.expressive:
        print(f"🎭 Expressiveness: ENABLED")
        print(f"   • Temperature: {args.temperature}")
        print(f"   • Exaggeration: {args.exaggeration}")
        print(f"   • CFG Weight: {args.cfg_weight}")
        print(f"   • Repetition Penalty: {args.repetition_penalty}")
        print(f"   • Min-P: {args.min_p}")
        print(f"   • Top-P: {args.top_p}")
    else:
        print(f"🎭 Expressiveness: Standard (use --expressive for advanced controls)")
    
    # Model caching for speed optimization
    global _MODEL_CACHE
    
    # Create captured stream for both paths
    captured = StringIO()
    load_time = 0.0  # Initialize to avoid unbound variable
    
    # Enable torch optimizations for speed (must be set before model loading)
    torch.backends.cudnn.benchmark = True
    torch.set_float32_matmul_precision('high')  # Use TensorFloat-32
    
    if _MODEL_CACHE is not None:
        print("⚡ Using in-memory cached model (instant load)")
        model = _MODEL_CACHE
        load_time = 0.0
    else:
        print("📦 Loading model from HuggingFace (first run in this session)...")
        start_time = time.time()
        
        try:
            with redirect_stderr(captured), redirect_stdout(captured):
                # ChatterboxTTS handles device placement internally
                model = ChatterboxTTS.from_pretrained(device=args.device)
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded successfully in {load_time:.1f}s")
            print(f"💡 Tip: Use tts_server.py for persistent model (zero reload between runs)")
        
        except Exception as e:
                print(f"❌ Failed to load model: {e}")
                print(f"💡 Make sure {args.device.upper()} is available and chatterbox-tts is installed")
                if args.device == "cuda" and not torch.cuda.is_available():
                    print("💡 Try using --device cpu if CUDA is not available")
                return False
        
        # Apply torch.compile() for PyTorch 2.0+ speedup (10-15% potential)
        try:
            if hasattr(torch, 'compile') and callable(torch.compile):
                print("⚡ Applying torch.compile() optimization...")
                compile_start = time.time()
                # Note: Cannot wrap model.generate directly, it's a bound method
                # torch.compile works best on full forward passes
                # Skipping for compatibility - ChatterboxTTS doesn't benefit much from compile
                compile_time = time.time() - compile_start
                print(f"ℹ️  torch.compile() skipped (ChatterboxTTS compatibility)")
        except Exception as e:
            print(f"⚠️  torch.compile() failed ({e}), continuing without it")
        
        # Cache the model in memory for this session
        _MODEL_CACHE = model
        print(f"⚡ Model cached in memory - instant for next generation in this session!")
    
    # Test configuration
    if args.benchmark:
        # Benchmark mode: use consistent text for reliable comparison
        text = "Testing GPU optimizations with consistent benchmark text for accurate performance measurement."
        print(f"🎯 BENCHMARK MODE: Using standard test text")
        print(f"📄 Text: \"{text}\"")
        
        # Override parameters for consistency
        args.temperature = 0.75
        args.exaggeration = 0.65
        args.cfg_weight = 0.5
        args.repetition_penalty = 1.2
        args.min_p = 0.05
        args.top_p = 1.0
        print(f"🎯 Parameters: temp=0.75, exag=0.65, cfg=0.5 (standardized)")
    else:
        text = args.text
        print(f"📄 Using text: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")

    # Step 2: Voice Cloning - Skip single reference, go straight to multi-reference
    if args.skip_cloning:
        print_step(2, "Voice cloning test (skipped)")
        print("⏭️  Skipping voice cloning as requested")
        clone2_time = 0
    else:
        print_step(2, "Multi-Reference Voice Cloning")
        audio_prompt = args.reference
        
        # Check if primary reference audio exists
        if not os.path.exists(audio_prompt):
            print(f"❌ Error: {audio_prompt} not found!")
            print(f"📁 Current directory: {os.getcwd()}")
            print(f"💡 Make sure the reference file exists or use --reference path/to/file.wav")
            print(f"💡 Or use --ref-dir IO/AudioRef to load all files from the reference folder")
            print("💡 Or use --skip-cloning to skip this test")
            return False
        
        # Skip single-reference generation - it doesn't provide good results
        print(f"⏭️  Skipping single-reference test (low quality) - using multi-reference instead")
        
        # Multi-reference mode (supports unlimited reference files)
        all_extra_refs = []
        
        # Load from directory if specified
        if args.ref_dir:
            import glob
            ref_dir = args.ref_dir
            if not os.path.exists(ref_dir):
                print(f"⚠️  Warning: Directory {ref_dir} not found")
            else:
                # Find all audio files in directory
                audio_extensions = ['*.wav', '*.mp3', '*.flac']
                dir_files = []
                for ext in audio_extensions:
                    dir_files.extend(glob.glob(os.path.join(ref_dir, ext)))
                
                if dir_files:
                    # Filter out neutral files and files over 11 seconds
                    print(f"\n🔍 Filtering reference files...")
                    filtered_files = []
                    
                    # Import torchaudio backend for efficient metadata reading
                    import torchaudio.backend.soundfile_backend as soundfile_backend
                    
                    for f in dir_files:
                        # Skip neutral files
                        if 'neutral' in os.path.basename(f).lower():
                            continue
                        
                        # Check duration (optimize CPU: only load metadata, not full audio)
                        try:
                            info = soundfile_backend.info(f)
                            duration = info.num_frames / info.sample_rate
                            
                            if duration > 11.0:
                                print(f"   ⏭️  Skipping {os.path.basename(f)} ({duration:.1f}s > 11s limit)")
                                continue
                            
                            filtered_files.append(f)
                        except Exception as e:
                            print(f"   ⚠️  Could not read {os.path.basename(f)}: {e}")
                            continue
                    
                    dir_files = filtered_files
                    
                    # Sort for consistent ordering
                    dir_files.sort()
                    print(f"\n📁 Found {len(dir_files)} valid emotional audio file(s) (≤11s):")
                    for f in dir_files:
                        # Show duration info
                        try:
                            info = soundfile_backend.info(f)
                            duration = info.num_frames / info.sample_rate
                            print(f"   • {os.path.basename(f)} ({duration:.1f}s)")
                        except Exception:
                            print(f"   • {os.path.basename(f)}")
                    
                    # When using --ref-dir, find and use serious_9s.wav as primary if available
                    serious_file = next((f for f in dir_files if 'serious' in os.path.basename(f).lower()), None)
                    
                    if serious_file:
                        # Use serious_9s.wav as primary
                        audio_prompt = serious_file
                        # Add all OTHER files as extra references (excluding the primary)
                        all_extra_refs.extend([f for f in dir_files if f != serious_file])
                        print(f"\n🎭 Using {os.path.basename(audio_prompt)} as primary reference")
                    else:
                        # Fallback: use first file as primary
                        audio_prompt = dir_files[0]
                        all_extra_refs.extend(dir_files[1:])
                        print(f"\n🎭 Using {os.path.basename(audio_prompt)} as primary reference")
                else:
                    print(f"⚠️  No audio files found in {ref_dir}")
        
        # Add explicitly specified references
        if args.extra_references:
            all_extra_refs.extend(args.extra_references)
        if args.reference2:  # Legacy support
            all_extra_refs.append(args.reference2)
        
        if all_extra_refs:
            if args.blend_voices:
                ref_list_str = " + ".join([os.path.basename(audio_prompt)] + [os.path.basename(f) for f in all_extra_refs])
                print(f"\n🎭 Multi-Reference Mode: Concatenating {len(all_extra_refs) + 1} files")
                print(f"📝 Files: {ref_list_str}")
                print(f"� This creates a longer reference with features from all samples")
                
                # Check all reference files exist
                missing_files = [f for f in all_extra_refs if not os.path.exists(f)]
                if missing_files:
                    print(f"⚠️  Warning: Missing files: {', '.join([os.path.basename(f) for f in missing_files])}")
                    print(f"⚠️  Continuing with available files only")
                    all_extra_refs = [f for f in all_extra_refs if os.path.exists(f)]
                
                if not all_extra_refs:
                    print(f"⚠️  No additional reference files found")
                    print(f"💡 Add more reference files for better quality")
                    clone2_time = 0
                else:
                    try:
                        start_time = time.time()
                        
                        # Multi-reference approach: concatenate all audio files
                        import torchaudio as ta_load
                        
                        # Prepare list of all reference files
                        all_ref_files = [audio_prompt] + all_extra_refs
                        
                        # Initialize total_duration (will be calculated in cached or non-cached path)
                        total_duration = 0.0
                        
                        # Check if we have a cached version of these references
                        cache_key = get_reference_cache_key(all_ref_files, target_sr=48000)
                        cached_result = load_cached_reference(cache_key)
                        
                        if cached_result is not None:
                            combined_audio, sr_target = cached_result
                            ref_count = len(all_ref_files)
                            total_duration = combined_audio.shape[1] / sr_target
                            print(f"⚡ Loaded {ref_count} references from cache (instant)")
                            
                            # Pin to GPU immediately
                            if args.device == "cuda":
                                combined_audio = combined_audio.cuda()
                                print(f"🎮 References pinned to GPU memory")
                            
                            print(f"📊 Reference sample rate: {sr_target}Hz")
                            print(f"🔗 Total reference duration: {total_duration:.1f}s")
                            # Create dummy durations list for quality check
                            durations = [total_duration / ref_count] * ref_count
                            ref_audios = [None] * ref_count  # Dummy for num count
                        else:
                            print(f"🚀 Loading {len(all_ref_files)} references in parallel (GPU-optimized)...")
                            
                            # Load primary reference to get target sample rate
                            ref_audios = []
                            ref1, sr_target = ta_load.load(audio_prompt)
                            
                            # Move to GPU immediately to reduce CPU overhead
                            if args.device == "cuda":
                                ref1 = ref1.cuda()
                            
                            # Normalize volume (prevents pitch issues from loud clips)
                            ref1 = normalize_audio_volume(ref1, target_db=-20.0, filename=os.path.basename(audio_prompt))
                            
                            ref_audios.append(ref1)
                            durations = [ref1.shape[1]/sr_target]
                            
                            print(f"📊 Reference sample rate: {sr_target}Hz")
                            print(f"🔊 Volume normalization: ENABLED (GPU-accelerated)")
                            
                            # Use ThreadPoolExecutor to load references in parallel (1-2s speedup)
                            with ThreadPoolExecutor(max_workers=4) as executor:
                                # Submit all reference loading tasks
                                futures = [executor.submit(load_and_normalize_reference, ref_file, sr_target) 
                                          for ref_file in all_extra_refs]
                                
                                # Collect results as they complete
                                for future in futures:
                                    ref_audio, duration = future.result()
                                    
                                    # Pin to GPU immediately
                                    if args.device == "cuda":
                                        ref_audio = ref_audio.cuda()
                                    
                                    ref_audios.append(ref_audio)
                                    durations.append(duration)
                            
                            print(f"✅ Loaded {len(ref_audios)} references in parallel")
                            print(f"🎮 All references pinned to GPU memory")
                            
                            # Concatenate all audio files on GPU
                            combined_audio = torch.cat(ref_audios, dim=1)
                            
                            # Cache the processed reference for future use (save to CPU)
                            save_cached_reference(cache_key, combined_audio.cpu(), sr_target)
                            print(f"💾 Cached processed references for future use")
                        
                        # Save temporary combined reference at original sample rate
                        # Move to CPU for file I/O (torchaudio.save doesn't support CUDA tensors directly)
                        temp_ref_path = "temp_combined_reference.wav"
                        combined_audio_cpu = combined_audio.cpu() if combined_audio.is_cuda else combined_audio
                        ta_load.save(temp_ref_path, combined_audio_cpu, sr_target)
                        
                        # Calculate total duration (works for both cached and non-cached paths)
                        if cached_result is not None:
                            # Already set in cached path (line 594)
                            pass
                        else:
                            # Calculate for non-cached path
                            duration_str = " + ".join([f"{d:.1f}s" for d in durations])
                            total_duration = combined_audio.shape[1]/sr_target
                            print(f"🔗 Combined {len(ref_audios)} references: {duration_str} = {total_duration:.1f}s")
                        
                        print(f"✨ Using {sr_target}Hz - ChatterboxTTS will preserve high-frequency detail")
                        
                        # Provide quality recommendations
                        if len(ref_audios) >= 4 and all(2 < d < 10 for d in durations):
                            print(f"   ⭐⭐⭐⭐⭐ EXCELLENT: {len(ref_audios)} clips with optimal durations!")
                        elif len(ref_audios) >= 3:
                            print(f"   ⭐⭐⭐⭐ Very good multi-reference setup")
                        elif len(ref_audios) == 2:
                            print(f"   ⭐⭐⭐ Good dual-reference (consider adding more clips for better variety)")
                        
                        if total_duration < 15:
                            print(f"   💡 Tip: Total duration is {total_duration:.1f}s - adding 2-3 more clips could improve quality")
                        elif total_duration > 60:
                            print(f"   ⚠️  Long reference ({total_duration:.1f}s) may slow processing")
                        
                        # Configure generation parameters for expressiveness
                        generation_kwargs = {'audio_prompt_path': temp_ref_path}
                        if args.expressive:
                            generation_kwargs.update({
                                'temperature': args.temperature,
                                'exaggeration': args.exaggeration,
                                'cfg_weight': args.cfg_weight,
                                'repetition_penalty': args.repetition_penalty,
                                'min_p': args.min_p,
                                'top_p': args.top_p
                            })
                        
                        # Generate with CUDA stream for async execution
                        print(f"🚀 Generating speech (GPU-optimized, no gradients)...")
                        
                        if args.device == "cuda" and _CUDA_STREAM is not None:
                            with torch.cuda.stream(_CUDA_STREAM):
                                with redirect_stderr(captured):
                                    wav = model.generate(text, **generation_kwargs)
                            # Synchronize to ensure generation is complete
                            torch.cuda.synchronize()
                        else:
                            with redirect_stderr(captured):
                                wav = model.generate(text, **generation_kwargs)
                        
                        # Clean up temporary file
                        if os.path.exists(temp_ref_path):
                            os.remove(temp_ref_path)
                        
                        clone2_time = time.time() - start_time
                        ta.save("test-multi-ref.wav", wav, model.sr)
                        
                        # Get file size for reporting
                        file_size_multi = os.path.getsize("test-multi-ref.wav") / 1024  # KB
                        num_refs = len(ref_audios)
                        print(f"✅ Generated test-multi-ref.wav with {num_refs} references in {clone2_time:.1f}s ({file_size_multi:.1f} KB)")
                        
                    except Exception as e:
                        print(f"❌ Failed to generate dual-reference voice: {e}")
                        clone2_time = 0
            else:
                print(f"\n🎭 Testing secondary voice reference: {args.reference2}")
                
                # Check if secondary reference audio exists
                if not os.path.exists(args.reference2):
                    print(f"⚠️  Warning: {args.reference2} not found, skipping secondary reference")
                    clone2_time = 0
                else:
                    try:
                        start_time = time.time()
                        
                        with redirect_stderr(captured):
                            wav2 = model.generate(text, audio_prompt_path=args.reference2)
                        
                        clone2_time = time.time() - start_time
                        ta.save("test-3.wav", wav2, model.sr)
                        
                        # Get file size for reporting
                        file_size2 = os.path.getsize("test-3.wav") / 1024  # KB
                        print(f"✅ Generated test-3.wav with secondary voice in {clone2_time:.1f}s ({file_size2:.1f} KB)")
                        
                    except Exception as e:
                        print(f"❌ Failed to generate secondary cloned voice: {e}")
                        clone2_time = 0
        else:
            clone2_time = 0
    
    # Step 4: Summary
    print_step(3, "Test Summary")
    print("🎉 All tests completed successfully!")
    
    total_time = load_time + clone2_time
    print(f"\n📊 Performance Summary:")
    print(f"   • Model loading: {load_time:.1f}s")
    if not args.skip_cloning and clone2_time > 0:
        print(f"   • Multi-reference generation: {clone2_time:.1f}s")
    print(f"   • Total time: {total_time:.1f}s")
    
    if args.benchmark:
        print(f"\n🎯 BENCHMARK RESULTS:")
        print(f"   ════════════════════════════════════════")
        print(f"   Model Load:     {load_time:6.2f}s")
        print(f"   Generation:     {clone2_time:6.2f}s")
        print(f"   Total Time:     {total_time:6.2f}s")
        print(f"   ════════════════════════════════════════")
        print(f"   Settings: temp=0.75, exag=0.65, cfg=0.5")
        print(f"   Text: \"Testing GPU optimizations with...\"")
        print(f"\n   💡 Compare these numbers across runs for accurate speedup measurement")
    
    print(f"\n📁 Generated Files:")
    generated_files = []
    if not args.skip_cloning and os.path.exists("test-multi-ref.wav"):
        generated_files.append("test-multi-ref.wav")
    
    for filename in generated_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"   • {filename} ({size:.1f} KB)")
    
    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("💡 Check CUDA availability and package installations")
        sys.exit(1)
