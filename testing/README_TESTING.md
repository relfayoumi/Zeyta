# 🧪 Testing Directory

This directory contains comprehensive testing tools for the Zeyta AI Assistant.

## 📁 Contents

### Main Applications

#### 🌟 Integrated Testing App (NEW!)
- **File**: `integrated_app.py`
- **Description**: Complete web-based testing interface for all AI components
- **Features**: TTS, STT, LLM chat, and full pipeline testing
- **Documentation**: 
  - [QUICK_START.md](QUICK_START.md) - Get started in 3 steps
  - [INTEGRATED_APP.md](INTEGRATED_APP.md) - Complete documentation
  - [INTERFACE_GUIDE.md](INTERFACE_GUIDE.md) - Visual guide
  - [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

#### 🎙️ TTS Testing Tools
- **File**: `test_tts_clean.py`
- **Description**: Standalone ChatterboxTTS testing with optimizations
- **Features**: Voice cloning, multi-reference blending, benchmark mode

#### 🌐 TTS Server
- **File**: `tts_server.py`
- **Description**: Persistent TTS server for development
- **Features**: Keep model loaded, HTTP API, instant generation

#### 📡 TTS Client
- **File**: `tts_client.py`
- **Description**: Client for TTS server API
- **Features**: Simple interface to tts_server.py

### Launcher Scripts

- **launch_app.sh** - Linux/Mac launcher for integrated app
- **launch_app.bat** - Windows launcher for integrated app

### Documentation

- **INTEGRATED_APP.md** - Complete app documentation (268 lines)
- **QUICK_START.md** - Quick start guide (136 lines)
- **INTERFACE_GUIDE.md** - Visual interface guide (314 lines)
- **IMPLEMENTATION_SUMMARY.md** - Technical summary (241 lines)
- **FIXES_APPLIED.md** - TTS optimization documentation
- **CACHING_INVESTIGATION.md** - Caching analysis
- **MODEL_CACHING_*.md** - Model caching documentation

## 🚀 Quick Start

### Option 1: Integrated App (Recommended)

```bash
# Install dependencies
pip install gradio

# Launch the app
python integrated_app.py

# Or use launcher
./launch_app.sh          # Linux/Mac
launch_app.bat           # Windows
```

Then open http://localhost:7860 in your browser.

### Option 2: Standalone TTS Testing

```bash
# Basic usage
python test_tts_clean.py --text "Hello world"

# With voice cloning
python test_tts_clean.py --text "Hello" --ref-dir ../IO/AudioRef_48kHz --blend-voices

# GPU mode with expressiveness
python test_tts_clean.py --text "Hello" --device cuda --expressive --temperature 0.9
```

### Option 3: TTS Server Mode

```bash
# Terminal 1: Start server
python tts_server.py

# Terminal 2: Use client
python tts_client.py --text "Hello from the server"
```

## 📊 Comparison

| Tool | Best For | Interface | Models |
|------|----------|-----------|--------|
| **integrated_app.py** | All-in-one testing | Web UI | TTS + STT + LLM |
| **test_tts_clean.py** | TTS optimization | CLI | TTS only |
| **tts_server.py** | Development | HTTP API | TTS only |

## 🎯 Use Cases

### Testing Voice Cloning
1. Use **integrated_app.py** for interactive testing
2. Upload reference audio
3. Try different parameters
4. Compare results

### Optimizing TTS Performance
1. Use **test_tts_clean.py** with `--benchmark`
2. Test different device modes
3. Measure generation times
4. Analyze caching benefits

### Development Workflow
1. Start **tts_server.py** to keep model loaded
2. Use **tts_client.py** for quick tests
3. Iterate on prompts without reload overhead

### Full Pipeline Testing
1. Use **integrated_app.py** Pipeline tab
2. Test STT → LLM → TTS flow
3. Verify end-to-end functionality

## 📝 Output Files

All test outputs are saved to:
```
testing/outputs/
├── tts_output_<timestamp>.wav      # Integrated app TTS
├── pipeline_output_<timestamp>.wav # Pipeline results
└── test-*.wav                       # test_tts_clean.py outputs
```

## 🔧 Configuration

The integrated app uses:
- `config.py` if available (main project config)
- Sensible defaults if config.py doesn't exist
- Per-model configuration in the UI

## 📚 More Information

- Main project: [../README.md](../README.md)
- Voice cloning tips: [../QUALITY_GUIDE.md](../QUALITY_GUIDE.md)
- Security info: [../SECURITY_CHANGES.md](../SECURITY_CHANGES.md)

## 🐛 Troubleshooting

**Integrated app won't start:**
```bash
pip install gradio torch transformers
```

**TTS test fails:**
```bash
pip install chatterbox-tts
```

**STT not working:**
```bash
pip install faster-whisper
```

**LLM errors:**
```bash
pip install transformers accelerate
```

## 🎓 Learning Resources

1. Start with **QUICK_START.md** for integrated app
2. Read **INTEGRATED_APP.md** for detailed features
3. Check **INTERFACE_GUIDE.md** for UI overview
4. Review **test_tts_clean.py** for advanced TTS usage

## 🤝 Contributing

When adding new testing tools:
1. Add documentation in this README
2. Include usage examples
3. Update relevant markdown files
4. Test cross-platform compatibility

---

💡 **Tip**: Start with the integrated app for the best experience!
