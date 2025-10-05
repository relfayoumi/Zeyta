# 🚀 Quick Start Guide - Integrated Testing App

Get started with the Zeyta Integrated Testing App in 3 easy steps!

## Step 1: Install Dependencies

```bash
pip install gradio torch transformers faster-whisper chatterbox-tts
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Step 2: Launch the App

### Option A: Run directly
```bash
python testing/integrated_app.py
```

### Option B: Use launcher script

**Linux/Mac:**
```bash
./testing/launch_app.sh
```

**Windows:**
```
testing\launch_app.bat
```

## Step 3: Access the Interface

The app will automatically open in your browser at:
```
http://localhost:7860
```

If it doesn't open automatically, copy that URL into your browser.

## First Steps in the App

### 1️⃣ Initialize Models

Before using any feature, you need to initialize the corresponding model:

- Go to the **🗣️ Text-to-Speech** tab → Click "Initialize TTS Model"
- Go to the **🎤 Speech-to-Text** tab → Click "Initialize STT Model"  
- Go to the **💬 Text-to-Text** tab → Click "Initialize LLM Model"

*Note: Model initialization may take 30-60 seconds depending on your hardware*

### 2️⃣ Test Each Feature

**TTS (Text-to-Speech):**
1. Enter some text
2. Click "Generate Speech"
3. Listen to the result!

**STT (Speech-to-Text):**
1. Click the microphone icon to record
2. Speak clearly
3. Click "Transcribe"
4. See your words in text!

**LLM Chat:**
1. Type a message
2. Press Enter or click "Send"
3. Get an AI response!

**Full Pipeline:**
1. Make sure STT and LLM are initialized
2. Record yourself asking a question
3. Click "Run Full Pipeline"
4. Get a complete voice response!

## Tips for Best Results

### 🎤 For Speech Recognition
- Speak clearly and at normal pace
- Use a quiet environment
- Position microphone 6-12 inches from mouth
- Start with the "base" model, upgrade to "small" or "medium" if needed

### 🗣️ For Speech Generation  
- Use clear, grammatically correct text
- Reference audio should be 5-10 seconds
- Keep reference audio clean (no background noise)
- Experiment with temperature/exaggeration settings

### 💬 For LLM Chat
- Be specific in your questions
- Use temperature 0.7 for balanced responses
- Lower temperature (0.3-0.5) for factual answers
- Higher temperature (0.8-1.2) for creative responses

## Hardware Recommendations

### Minimum (CPU Only)
- 8GB RAM
- Modern CPU (Intel i5 or equivalent)
- Expect slower performance

### Recommended (GPU)
- 16GB RAM
- NVIDIA GPU with 6GB+ VRAM
- CUDA 11.8 or newer
- Fast performance!

### Optimal (High-end GPU)
- 32GB RAM
- NVIDIA RTX 3080 or better (12GB+ VRAM)
- Can use large models comfortably

## Troubleshooting

**"Model not loaded" error:**
- Click the "Initialize Model" button in the respective tab
- Wait for the success message before proceeding

**Slow performance:**
- Use smaller models (e.g., STT "base" instead of "large-v3")
- Close other applications
- Check GPU usage with `nvidia-smi` (if available)

**Out of memory:**
- Restart the app
- Use CPU mode instead of GPU
- Use smaller models

**Can't hear audio:**
- Check browser permissions for audio
- Check system volume
- Try downloading the file from `testing/outputs/`

## Need Help?

1. Check [`testing/INTEGRATED_APP.md`](INTEGRATED_APP.md) for detailed docs
2. Check the main [`README.md`](../README.md)
3. File an issue on GitHub

---

**Enjoy testing your AI models!** 🎉
