#!/usr/bin/env python3
"""
ChatterboxTTS HTTP Server - Keep model loaded for instant generation
Implements server mode for zero-reload overhead across multiple requests
"""

import warnings
import logging
import os
import sys
import time
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO, BytesIO

# Comprehensive warning suppression
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger().setLevel(logging.ERROR)

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Flask app
app = Flask(__name__)

# Global model instance (loaded once, reused forever)
MODEL = None
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Cache directories
CACHE_DIR = Path("cache")
MODEL_CACHE_DIR = CACHE_DIR / "models"
REFERENCE_CACHE_DIR = CACHE_DIR / "references"
OUTPUT_DIR = Path("outputs")

# Create directories
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
REFERENCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_CACHE_PATH = MODEL_CACHE_DIR / "chatterbox_cached.pth"


def load_model():
    """Load model once at server startup"""
    global MODEL
    
    print("=" * 60)
    print("🚀 ChatterboxTTS Server - Starting Up")
    print("=" * 60)
    
    # Enable torch optimizations
    torch.backends.cudnn.benchmark = True
    torch.set_float32_matmul_precision('high')
    
    captured = StringIO()
    
    # Try to load from disk cache
    if MODEL_CACHE_PATH.exists():
        print(f"📦 Loading model from disk cache...")
        start_time = time.time()
        
        try:
            with redirect_stderr(captured), redirect_stdout(captured):
                MODEL = torch.load(MODEL_CACHE_PATH, map_location=DEVICE)
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded from cache in {load_time:.1f}s")
            
        except Exception as e:
            print(f"⚠️  Cache corrupted ({e}), rebuilding...")
            MODEL_CACHE_PATH.unlink(missing_ok=True)
            MODEL = None
    
    # Load from scratch if needed
    if MODEL is None:
        print(f"📥 Loading model from scratch...")
        start_time = time.time()
        
        try:
            with redirect_stderr(captured), redirect_stdout(captured):
                MODEL = ChatterboxTTS.from_pretrained(device=DEVICE)
            
            # Save to disk
            print(f"💾 Saving model to disk cache...")
            torch.save(MODEL, MODEL_CACHE_PATH)
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded in {load_time:.1f}s")
            print(f"💾 Cached ({MODEL_CACHE_PATH.stat().st_size / 1024 / 1024:.1f} MB)")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            sys.exit(1)
    
    # Apply torch.compile if available
    try:
        if hasattr(torch, 'compile') and callable(torch.compile):
            print(f"⚡ Applying torch.compile() optimization...")
            compile_start = time.time()
            original_generate = MODEL.generate
            MODEL.generate = torch.compile(original_generate, mode='reduce-overhead')
            compile_time = time.time() - compile_start
            print(f"✅ torch.compile() applied in {compile_time:.1f}s")
    except Exception as e:
        print(f"⚠️  torch.compile() failed ({e}), continuing without it")
    
    print(f"\n✅ Server ready on http://localhost:5000")
    print(f"🔧 Device: {DEVICE.upper()}")
    print(f"⚡ Model loaded and cached - zero reload overhead!")
    print("=" * 60)


def normalize_audio_volume(waveform, target_db=-20.0, filename=None):
    """Normalize audio volume to prevent pitch issues"""
    # Calculate RMS
    rms = torch.sqrt(torch.mean(waveform**2))
    current_db = 20 * torch.log10(rms + 1e-8)
    
    # Apply gain
    gain_db = target_db - current_db
    gain_linear = 10 ** (gain_db / 20)
    normalized = waveform * gain_linear
    
    # Extra reduction for angry clips
    if filename and 'angry' in filename.lower():
        normalized = normalized * 0.85
    
    # Prevent clipping
    max_val = torch.max(torch.abs(normalized))
    if max_val > 0.95:
        normalized = normalized * (0.95 / max_val)
    
    return normalized


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "device": DEVICE
    })


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate speech from text
    
    POST /generate
    {
        "text": "Hello world",
        "reference_files": ["path/to/ref1.wav", "path/to/ref2.wav"],  // optional
        "temperature": 0.8,  // optional
        "exaggeration": 0.5,  // optional
        "cfg_weight": 0.5,  // optional
        "repetition_penalty": 1.2,  // optional
        "min_p": 0.05,  // optional
        "top_p": 1.0,  // optional
        "output_format": "wav"  // optional: wav, mp3
    }
    
    Returns: Audio file or JSON with error
    """
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        text = data['text']
        reference_files = data.get('reference_files', [])
        
        # Generation parameters
        temperature = data.get('temperature', 0.8)
        exaggeration = data.get('exaggeration', 0.5)
        cfg_weight = data.get('cfg_weight', 0.5)
        repetition_penalty = data.get('repetition_penalty', 1.2)
        min_p = data.get('min_p', 0.05)
        top_p = data.get('top_p', 1.0)
        
        print(f"\n📝 Request: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        start_time = time.time()
        
        # Handle reference files
        if reference_files:
            print(f"🎤 Loading {len(reference_files)} reference file(s)...")
            
            # Load and concatenate references
            ref_audios = []
            ref1, sr_target = ta.load(reference_files[0])
            ref1 = normalize_audio_volume(ref1, filename=os.path.basename(reference_files[0]))
            ref_audios.append(ref1)
            
            for ref_file in reference_files[1:]:
                ref_audio, sr = ta.load(ref_file)
                
                # Resample if needed
                if sr != sr_target:
                    resampler = ta.transforms.Resample(sr, sr_target)
                    ref_audio = resampler(ref_audio)
                
                ref_audio = normalize_audio_volume(ref_audio, filename=os.path.basename(ref_file))
                ref_audios.append(ref_audio)
            
            # Combine
            combined_audio = torch.cat(ref_audios, dim=1)
            
            # Save temp file
            temp_ref_path = OUTPUT_DIR / "temp_reference.wav"
            ta.save(str(temp_ref_path), combined_audio, sr_target)
            
            generation_kwargs = {
                'audio_prompt_path': str(temp_ref_path),
                'temperature': temperature,
                'exaggeration': exaggeration,
                'cfg_weight': cfg_weight,
                'repetition_penalty': repetition_penalty,
                'min_p': min_p,
                'top_p': top_p
            }
        else:
            # Default voice
            generation_kwargs = {
                'temperature': temperature,
                'exaggeration': exaggeration,
                'cfg_weight': cfg_weight,
                'repetition_penalty': repetition_penalty,
                'min_p': min_p,
                'top_p': top_p
            }
        
        # Generate speech
        captured = StringIO()
        with redirect_stderr(captured):
            wav = MODEL.generate(text, **generation_kwargs)
        
        # Clean up temp file
        if reference_files and temp_ref_path.exists():
            temp_ref_path.unlink()
        
        generation_time = time.time() - start_time
        
        # Save output
        output_path = OUTPUT_DIR / f"output_{int(time.time())}.wav"
        ta.save(str(output_path), wav, MODEL.sr)
        
        file_size_kb = output_path.stat().st_size / 1024
        
        print(f"✅ Generated in {generation_time:.1f}s ({file_size_kb:.1f} KB)")
        
        # Return audio file
        return send_file(
            str(output_path),
            mimetype='audio/wav',
            as_attachment=True,
            download_name='output.wav'
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/stats', methods=['GET'])
def stats():
    """Get server statistics"""
    cache_files = list(REFERENCE_CACHE_DIR.glob("*.pt"))
    cache_size = sum(f.stat().st_size for f in cache_files) / 1024 / 1024  # MB
    
    model_size = MODEL_CACHE_PATH.stat().st_size / 1024 / 1024 if MODEL_CACHE_PATH.exists() else 0
    
    return jsonify({
        "model_cached": MODEL_CACHE_PATH.exists(),
        "model_cache_size_mb": round(model_size, 2),
        "reference_cache_count": len(cache_files),
        "reference_cache_size_mb": round(cache_size, 2),
        "device": DEVICE,
        "torch_compile_available": hasattr(torch, 'compile')
    })


if __name__ == "__main__":
    # Load model at startup
    load_model()
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
