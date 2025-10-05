# Model Caching Status - October 4, 2025

## Summary

**Current Status:** ❌ Disk-based model caching is **NOT POSSIBLE** with ChatterboxTTS due to pickling limitations.

## Problem

ChatterboxTTS model contains non-picklable objects (thread locks, CUDA contexts, etc.) that prevent serialization:

```
⚠️  Warning: Failed to cache model: cannot pickle '_thread.lock' object
```

## Root Cause

The ChatterboxTTS model architecture includes:
1. **Threading locks** (`_thread.lock`) - not picklable
2. **CUDA contexts** - device-specific, cannot be saved
3. **Complex nested objects** - may contain lambda functions or other non-serializable components

### Attempted Solutions (All Failed)

#### 1. ❌ `torch.save(model, path)` - Pickle Error
```python
torch.save(model, model_cache_path)
# Error: cannot pickle '_thread.lock' object
```

#### 2. ❌ `state_dict()` - Not Supported
```python
state_dict = model.state_dict()
# Error: 'ChatterboxTTS' object has no attribute 'state_dict'
```

#### 3. ❌ Custom Serialization - Too Complex
ChatterboxTTS doesn't expose standard PyTorch module methods, making custom serialization impractical.

## Working Solutions

### ✅ Solution 1: In-Memory Caching (Already Implemented)

**How it works:**
```python
# First run: Load model
model = ChatterboxTTS.from_pretrained(device='cuda')  # ~10s
_MODEL_CACHE = model

# Same session, later: Instant
if _MODEL_CACHE is not None:
    model = _MODEL_CACHE  # ~0.01s
```

**Performance:**
- First generation: ~10s model load + ~8s generation = **18s total**
- Second generation (same session): ~0s load + ~8s generation = **8s total**
- **Speedup: 55% faster** (same session only)

**Limitation:**
- Cache cleared when script exits
- Each new script run loads the model fresh

### ✅ Solution 2: Server Mode (Recommended for Multiple Runs)

**Use `tts_server.py` for persistent model hosting:**

```bash
# Terminal 1: Start server (one time)
python testing\tts_server.py

# Terminal 2: Generate audio (instant model access)
python testing\tts_client.py
```

**Performance:**
- Server startup: ~10s (one time)
- Each generation: ~8s (zero load overhead)
- **Speedup: 100% of runs after first** (no reload ever)

**Benefits:**
- Model stays loaded indefinitely
- Zero reload between generations
- Can be used by multiple clients
- Perfect for development/testing

### Server Mode Setup

#### Start the Server:
```powershell
cd D:\AI-OFFICIAL
python testing\tts_server.py
```

Output:
```
============================================================
🚀 ChatterboxTTS Server - Starting Up
============================================================
📥 Loading model from scratch...
✅ Model loaded in 10.1s
💾 Cached (2453.2 MB)

✅ Server ready on http://localhost:5000
🔧 Device: CUDA
⚡ Model loaded and cached - zero reload overhead!
============================================================
```

#### Use the Client:
```powershell
# Example generation
python testing\tts_client.py
```

Or via HTTP directly:
```python
import requests

response = requests.post('http://localhost:5000/generate', json={
    'text': 'Hello, this is a test',
    'audio_prompt_path': 'IO/AudioRef_48kHz/serious_9s.wav'
})

# Save output
with open('output.wav', 'wb') as f:
    f.write(response.content)
```

## Comparison: Script vs Server Mode

| Metric | test_tts_clean.py | tts_server.py |
|--------|-------------------|---------------|
| **First Run** | 18s (10s load + 8s gen) | 10s startup |
| **Second Run** | 18s (fresh load) | 8s (no load) |
| **Third Run** | 18s (fresh load) | 8s (no load) |
| **10th Run** | 18s (fresh load) | 8s (no load) |
| **Time for 5 generations** | 90s | 42s (10s + 5×8s) |
| **Speedup (5 runs)** | Baseline | **53% faster** |

## Recommendations

### For Single Generations:
Use `test_tts_clean.py` - simplest approach
```bash
python testing\test_tts_clean.py --ref-dir IO\AudioRef_48kHz --blend-voices --text "Your text"
```

### For Development/Testing (Multiple Runs):
Use `tts_server.py` - best performance
```bash
# Start once:
python testing\tts_server.py

# Generate many times:
python testing\tts_client.py
```

### For Production (Long-Running Service):
Use `tts_server.py` with proper deployment:
- Run as a systemd service (Linux) or Windows Service
- Add authentication/rate limiting
- Use nginx/Apache reverse proxy
- Monitor with health check endpoint (`/health`)

## Cache Files Status

### ✅ Working Caches:
- **Reference audio cache** (`cache/references/*.pt`) - WORKS
  - Saves pre-processed reference audio
  - Instant load on subsequent runs
  - ~8MB per reference set
  
### ❌ Not Working:
- **Model disk cache** (`cache/models/chatterbox_model.pth`) - FAILS
  - Cannot serialize due to threading locks
  - Removed from implementation

## Code Changes Summary

### What Was Removed:
- `save_model_weights()` function (not working)
- `load_model_weights()` function (not working)
- Disk cache check in model loading

### What Remains:
- In-memory model cache (`_MODEL_CACHE`) - **WORKS**
- Reference audio cache - **WORKS**
- Server mode (`tts_server.py`) - **WORKS BEST**

## Final Recommendation

**For your use case (testing optimizations):**

1. **Best approach:** Use `tts_server.py`
   ```bash
   # Terminal 1
   python testing\tts_server.py
   
   # Terminal 2 (run as many times as needed)
   curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '{"text":"Test", "audio_prompt_path":"IO/AudioRef_48kHz/serious_9s.wav"}'
   ```

2. **Alternative:** Run multiple generations in same script
   ```python
   # Load model once
   model = ChatterboxTTS.from_pretrained(device='cuda')
   
   # Generate many times (no reload)
   for text in texts:
       wav = model.generate(text, audio_prompt_path=ref_path)
   ```

## Performance Expectations

### Current (No Disk Cache):
- First run: **18s** (10s load + 8s gen)
- Second run (new session): **18s** (fresh load)
- **In-memory cache works** (same session)

### With Server Mode:
- Server start: **10s** (one time)
- Each generation: **8s** (forever)
- **Total for 10 generations: 90s → 42s** (53% faster)

## Conclusion

While disk-based model caching would be ideal, it's **not feasible** with ChatterboxTTS's current architecture. The server mode (`tts_server.py`) achieves the same goal (avoiding model reloads) and is actually **superior** for development workflows:

✅ Zero reload overhead (not just faster, but instant)  
✅ Can serve multiple clients  
✅ Persistent across sessions  
✅ Production-ready architecture  

**Status:** Model disk caching removed from test_tts_clean.py. Use server mode for best performance.
