# Zeyta AI Assistant - Quick Reference

## One-Minute Start Guide

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
python app.py

# 3. Open browser at http://localhost:7860

# 4. Initialize LLM model (click "Initialize LLM" button)

# 5. Start chatting!
```

## Pipeline Modes Quick Reference

| Mode | Input | Output | Models Required |
|------|-------|--------|-----------------|
| Text Chat Only | 💬 Text | 💬 Text | LLM |
| Voice to Text | 🎤 Voice | 💬 Text | STT + LLM |
| Voice to Voice | 🎤 Voice | 🔊 Voice | STT + LLM + TTS |
| Text to Voice | 💬 Text | 🔊 Voice | LLM + TTS |

## Common Commands

### Initialize Models
```
Click "🧠 Initialize LLM" → Required
Click "🎤 Initialize STT" → For voice input
Click "🔊 Initialize TTS" → For voice output
```

### Upload a Document
```
1. Click "📎 Upload File"
2. Select TXT, PDF, DOCX, or MD file
3. (Optional) Type a question
4. Click "Send 📤"
```

### Use Voice Input
```
1. Select "Voice to Text" or "Voice to Voice" mode
2. Click microphone icon or upload audio
3. Speak or play your audio
4. Click "Send 📤"
```

### Clear Conversation
```
Click "Clear 🗑️" button
```

## Keyboard Shortcuts

- **Enter**: Send message (when in text box)
- **Shift+Enter**: New line in text box

## Settings Quick Guide

### Temperature
- **0.3**: Factual, focused
- **0.7**: Balanced (default)
- **1.2**: Creative, varied

### Max Tokens
- **256**: Short answers
- **512**: Medium (default)
- **1024**: Detailed responses

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model not initialized" | Click initialization button |
| File upload fails | Install `pip install PyPDF2 python-docx` |
| Voice not working | Initialize STT/TTS models |
| Slow responses | Use smaller models, reduce tokens |
| Out of memory | Use CPU mode, smaller models |

## File Format Support

✅ Supported:
- `.txt` - Text files
- `.md` - Markdown
- `.pdf` - PDF (needs PyPDF2)
- `.docx` - Word (needs python-docx)

❌ Not Supported:
- `.xlsx`, `.pptx`, `.jpg`, `.png`, etc.

## Model Sizes (STT)

| Size | Speed | Accuracy | RAM |
|------|-------|----------|-----|
| tiny | ⚡⚡⚡ | ⭐⭐ | ~1GB |
| base | ⚡⚡ | ⭐⭐⭐ | ~2GB |
| small | ⚡ | ⭐⭐⭐⭐ | ~3GB |
| medium | ⚡ | ⭐⭐⭐⭐⭐ | ~5GB |
| large-v3 | ⚡ | ⭐⭐⭐⭐⭐ | ~10GB |

## Tips

💡 **Best Practices**:
1. Initialize models before chatting
2. Use GPU (CUDA) for faster processing
3. Keep files under 5MB for best performance
4. Clear chat when changing topics
5. Adjust temperature based on task

💡 **For Best Results**:
- Factual Q&A: Temperature 0.3-0.6
- Creative writing: Temperature 0.9-1.2
- Code generation: Temperature 0.5-0.7
- Summarization: Temperature 0.4-0.6

## Quick Examples

### Ask a Question
```
Pipeline: Text Chat Only
Message: "Explain photosynthesis"
```

### Analyze a Document
```
Pipeline: Text Chat Only
Upload: report.pdf
Message: "Summarize key points"
```

### Voice Conversation
```
Pipeline: Voice to Voice
[Speak]: "Tell me a joke"
[Hear]: AI's voice response
```

### Get Code Help
```
Pipeline: Text Chat Only
Upload: script.py
Message: "Review and improve this code"
```

## Status Indicators

- ✅ Model loaded successfully
- ⚠️ Warning (model not loaded, etc.)
- ❌ Error (operation failed)
- 🎤 Voice input active
- 🔊 Voice output generated
- 📎 File uploaded

## Default Configuration

- **LLM Model**: Llama-3.2-3B-Instruct-uncensored
- **STT Model**: Whisper base
- **TTS Device**: CUDA (if available) or CPU
- **Temperature**: 0.7
- **Max Tokens**: 512
- **Port**: 7860

## Custom Configuration

Edit `config.py`:
```python
LLM_MODEL_ID = "your-model-id"
SYSTEM_PROMPT = "Your custom prompt"
```

## Links

- **Full Guide**: APP_GUIDE.md
- **Examples**: USAGE_EXAMPLES.md
- **Features**: FEATURE_SHOWCASE.md
- **Architecture**: ARCHITECTURE.md
- **Main README**: README.md

## Support

Having issues? Check:
1. This quick reference
2. APP_GUIDE.md for details
3. GitHub issues

## Version Info

Application: Zeyta AI Assistant (app.py)
Python: 3.11+
UI: Gradio
License: See LICENSE
