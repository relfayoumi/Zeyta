# 🤖 Zeyta Integrated Testing App

A comprehensive, user-friendly web application for testing all components of the Zeyta AI Assistant.

## Features

### 🗣️ Text-to-Speech (TTS) Testing
- Test ChatterboxTTS models located in the `testing/` folder
- Support for voice cloning with reference audio
- Advanced controls for expressiveness, temperature, and emotion
- Real-time audio generation and playback
- Save generated audio files

### 🎤 Speech-to-Text (STT) Testing
- Test Whisper models with different sizes (tiny, base, small, medium, large-v3)
- Upload audio files or record directly from microphone
- Real-time transcription with language detection
- Performance metrics (transcription time, confidence scores)

### 💬 Text-to-Text (LLM) Testing
- Interactive chat with the configured LLM
- Adjustable temperature and max tokens
- Full conversation history
- Clean, modern chat interface

### 🔄 Full Pipeline Testing
- Test complete voice assistant pipeline in one go
- Steps: STT → LLM → TTS
- Optional TTS output (can test just STT + LLM)
- See intermediate results at each step

## Quick Start

### 1. Installation

Make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration (Optional)

If you have a `config.py` file, the app will use your configured models. Otherwise, it uses sensible defaults:
- LLM: Llama-3.2-3B-Instruct-uncensored
- STT: Whisper base model
- TTS: ChatterboxTTS

### 3. Run the App

```bash
python testing/integrated_app.py
```

Or from the testing directory:

```bash
cd testing
python integrated_app.py
```

The app will start a web server and automatically open in your default browser at `http://localhost:7860`

## Usage Guide

### First Time Setup

1. **Navigate to each tab** you want to use
2. **Click "Initialize Model"** to load the respective model
3. **Wait for confirmation** that the model is loaded

### TTS Testing

1. Go to **🗣️ Text-to-Speech** tab
2. Click **Initialize TTS Model** (choose GPU if available)
3. Enter text in the text box
4. (Optional) Upload reference audio for voice cloning
5. Adjust advanced settings if desired
6. Click **Generate Speech**
7. Listen to the output and check the generation info

**Tips:**
- Reference audio should be 5-10 seconds for best results
- Temperature controls expressiveness (0.8 is a good starting point)
- Higher exaggeration = more dramatic/emotional speech

### STT Testing

1. Go to **🎤 Speech-to-Text** tab
2. Click **Initialize STT Model** (choose model size)
3. Either:
   - Upload an audio file, OR
   - Click the microphone icon to record
4. Click **Transcribe**
5. View transcription results with language detection

**Model Sizes:**
- `tiny`: Fastest, least accurate (~1GB)
- `base`: Good balance (~1GB)
- `small`: Better accuracy (~2GB)
- `medium`: High accuracy (~5GB)
- `large-v3`: Best accuracy (~10GB) - requires good GPU

### LLM Chat Testing

1. Go to **💬 Text-to-Text (LLM)** tab
2. Click **Initialize LLM Model** (this may take a minute)
3. Type your message in the text box
4. Click **Send** or press Enter
5. Adjust temperature/max tokens in settings as needed

**Settings:**
- Temperature: Lower = more focused, Higher = more creative
- Max Tokens: How long the response can be

### Full Pipeline Testing

1. Go to **🔄 Full Pipeline** tab
2. Make sure STT and LLM are initialized (TTS optional)
3. Record or upload audio of you speaking
4. Check "Generate Speech Output" if you want TTS
5. Click **Run Full Pipeline**
6. Watch the step-by-step process and results

**This tests:**
1. Your voice → Text (STT)
2. Text → AI Response (LLM)
3. AI Response → Speech (TTS, optional)

## Output Files

All generated audio files are saved to:
```
testing/outputs/
```

Files are named with timestamps:
- `tts_output_<timestamp>.wav` - TTS test outputs
- `pipeline_output_<timestamp>.wav` - Full pipeline outputs

## System Requirements

### Minimum
- Python 3.8+
- 8GB RAM
- CPU inference (slow)

### Recommended
- Python 3.10+
- 16GB RAM
- NVIDIA GPU with 6GB+ VRAM
- CUDA 11.8+

## Troubleshooting

### Models Won't Load

**Problem:** Error messages when initializing models

**Solutions:**
1. Check that all dependencies are installed: `pip install -r requirements.txt`
2. For GPU issues, ensure CUDA is properly installed
3. Try CPU mode if GPU fails
4. Check available disk space for model downloads

### Out of Memory Errors

**Problem:** CUDA out of memory or system RAM exhausted

**Solutions:**
1. Use smaller models (e.g., `base` instead of `large-v3` for STT)
2. Close other applications
3. Use CPU mode for some models
4. Reduce max tokens in LLM settings

### Audio Not Playing

**Problem:** Generated audio doesn't play

**Solutions:**
1. Check browser audio permissions
2. Try downloading the audio file manually
3. Check the `testing/outputs/` folder for saved files
4. Verify your system audio is working

### Slow Performance

**Problem:** Models are very slow

**Solutions:**
1. Use GPU if available (much faster)
2. Use smaller model sizes
3. Reduce max tokens for LLM
4. Close other GPU-intensive applications

## Advanced Features

### Voice Cloning

Upload a reference audio file (5-10 seconds) in the TTS tab for voice cloning:
- Clear, high-quality audio works best
- Single speaker
- Natural speaking style
- No background noise

### Custom Models

To use custom models, edit `config.py`:

```python
LLM_MODEL_ID = "your-model-name"
STT_MODEL_SIZE = "large-v3"
```

Then restart the app.

## Development

### Adding New Features

The app is structured to be easily extensible:

1. **New model types**: Add initialization functions
2. **New tabs**: Add to the `create_interface()` function
3. **New parameters**: Add sliders/inputs in the relevant tab

### Code Structure

```python
# Model initialization functions
initialize_llm()
initialize_tts_model(device)
initialize_stt_model(size)

# Core functionality
generate_tts(...)
transcribe_audio(...)
chat_with_llm(...)
full_pipeline_test(...)

# UI
create_interface()  # Main Gradio interface
```

## Future Improvements

Planned features:
- [ ] Model comparison tools (A/B testing)
- [ ] Batch processing for multiple inputs
- [ ] Performance metrics and benchmarking
- [ ] Custom model upload/loading
- [ ] Voice profile management and switching
- [ ] Audio quality analysis
- [ ] Export conversation history
- [ ] API endpoint for programmatic access
- [ ] Real-time STT streaming
- [ ] Multi-language support UI

## Support

For issues, questions, or feature requests:
1. Check this documentation
2. Look at the main README.md
3. Open an issue on GitHub

## License

Same as the main Zeyta project.
