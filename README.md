# Zeyta - AI Assistant with Voice

A modular voice-based AI assistant powered by local language models, speech-to-text, and optimized text-to-speech with voice cloning capabilities.

## Features

- 🎙️ **Voice Interaction**: Speech-to-text using Whisper and text-to-speech with voice cloning
- 🧠 **Local LLM**: Runs on your hardware using transformers
- 🎭 **Voice Cloning**: Multi-reference voice cloning using ChatterboxTTS
- ⚡ **GPU Optimized**: CUDA acceleration, memory pinning, and streaming
- 📝 **Conversation History**: Maintains context across sessions
- 🎯 **Customizable Personality**: Configure your AI's behavior via prompts

## Architecture

The project is organized into a modular structure to separate concerns and improve maintainability.

- **`main.py`**: The main entry point of the application
- **`config.py`**: Contains all constants, model IDs, and configuration settings
- **`core/`**: The core logic of the assistant
  - `brain.py`: Handles interaction with the Large Language Model (LLM)
  - `context.py`: Manages the conversation history
  - `controller.py`: The main loop that orchestrates the flow between I/O and the brain
- **`io/`**: Handles all input and output operations
  - `stt.py`: Speech-to-Text using faster-whisper
  - `tts.py`: Text-to-Speech using Coqui/Piper
  - `coqui_backend.py`: Voice cloning backend
- **`integrations/`**: Modules for controlling third-party systems (placeholders)
- **`utils/`**: Helper scripts for logging, tools, and profiling
- **`testing/`**: TTS optimization scripts
  - `test_tts_clean.py`: Standalone TTS testing with optimizations
  - `tts_server.py`: Persistent TTS server mode
  - `integrated_app.py`: Web-based testing interface for all components
- **`tests/`**: Unit tests for the modules

## Setup

### 1. Prerequisites

- Python 3.11+
- CUDA-capable GPU (recommended for optimal performance)
- FFmpeg installed on your system

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/relfayoumi/Zeyta.git
cd Zeyta

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example config
cp config.example.py config.py

# Edit config.py with your preferences:
# - Set your AI's personality in SYSTEM_PROMPT
# - Configure TTS backend (coqui or piper)
# - Set reference voice file path (for voice cloning)
# - Adjust model sizes based on your hardware
```

### 4. Running

```bash
# Run the voice assistant
python main.py

# Or test TTS independently
python testing/test_tts_clean.py --ref-dir IO/AudioRef_48kHz --blend-voices --text "Hello world"

# Or run TTS server mode (for development)
python testing/tts_server.py

# Or launch the integrated testing app (recommended for testing)
python testing/integrated_app.py
```

## 🧪 Integrated Testing App

We provide a comprehensive web-based testing interface for all AI components:

```bash
python testing/integrated_app.py
```

The app provides:
- 🗣️ **TTS Testing**: Test ChatterboxTTS models with voice cloning
- 🎤 **STT Testing**: Test Whisper models with microphone support
- 💬 **LLM Chat**: Interactive text-to-text chat interface
- 🔄 **Full Pipeline**: Test complete STT → LLM → TTS workflow

See [`testing/INTEGRATED_APP.md`](testing/INTEGRATED_APP.md) for detailed documentation.

## TTS Optimization Features

The testing suite includes advanced optimizations:

- ✅ **Reference Filtering**: Automatically filters audio files >11 seconds
- ✅ **GPU Optimizations**: CUDA streams, pinned memory, disabled gradients
- ✅ **Multi-threading**: Parallel reference loading
- ✅ **Caching**: Reference audio caching for faster subsequent runs
- ✅ **Benchmark Mode**: Consistent performance testing
- ✅ **Server Mode**: Zero-reload persistent model hosting

See `testing/FIXES_APPLIED.md` for detailed optimization documentation.

## Voice Cloning Setup

1. Record reference audio samples (5-10 seconds each)
2. Place them in `IO/AudioRef_48kHz/` directory
3. Use `--blend-voices` flag for multi-reference cloning
4. See `QUALITY_GUIDE.md` for recording tips

## Performance

- **Model Loading**: ~10s (first run), ~0s (in-memory cache)
- **TTS Generation**: ~8-10s per sentence (GPU)
- **Server Mode**: Zero reload overhead between generations

## Documentation

- `QUALITY_GUIDE.md` - Voice recording quality guidelines
- `testing/CACHING_INVESTIGATION.md` - Caching implementation details
- `testing/MODEL_CACHING_STATUS.md` - Model serialization limitations
- `testing/FIXES_APPLIED.md` - Complete optimization summary

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source. Please check individual dependencies for their licenses.

## Credits

- Uses [ChatterboxTTS](https://github.com/resemble-ai/chatterbox) for voice cloning
- Powered by [Whisper](https://github.com/openai/whisper) for speech recognition
- LLM support via [Transformers](https://github.com/huggingface/transformers)
```
