# Zeyta AI Assistant - User Guide

## Overview

The Zeyta AI Assistant (`app.py`) is a user-friendly Python application that allows you to:

- 💬 Chat with AI in a clean interface
- 📎 Upload and discuss documents (TXT, PDF, DOCX, MD)
- 🔧 Configure your processing pipeline
- 🎤 Use voice input and output

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: For document support
pip install PyPDF2 python-docx

# Optional: For standalone window mode (recommended)
pip install pywebview

# Platform-specific enhancements (optional):
# Windows: pip install pywebview[cef]
# Linux: pip install pywebview[qt]
# macOS: pip install pywebview[qt]
```

### Running the Application

```bash
python app.py
```

The application will launch in a **standalone window** (if pywebview is installed) or in your default browser.

**Standalone Window Mode (Recommended):**
- Runs as a native desktop application
- No browser required
- Better compatibility and user experience
- Install pywebview to enable: `pip install pywebview`

**Browser Mode (Fallback):**
- Opens in your default web browser
- Used if pywebview is not installed
- Access at `http://localhost:7860`

## Pipeline Modes

The application supports four different pipeline configurations:

### 1. Text Chat Only
- **Components**: LLM only
- **Use case**: Standard text-based chat
- **Requirements**: Initialize LLM model

### 2. Voice to Text
- **Components**: STT → LLM
- **Use case**: Speak to the AI, get text responses
- **Requirements**: Initialize STT and LLM models

### 3. Voice to Voice
- **Components**: STT → LLM → TTS
- **Use case**: Full voice conversation
- **Requirements**: Initialize all three models (STT, LLM, TTS)

### 4. Text to Voice
- **Components**: LLM → TTS
- **Use case**: Type messages, hear responses
- **Requirements**: Initialize LLM and TTS models

## Features

### File Upload

Upload documents to discuss their content with the AI:

1. Click the **"📎 Upload File"** button
2. Select a file (supported formats: TXT, PDF, DOCX, MD)
3. Optionally add a message asking about the file
4. Click **Send**

The AI will read and understand the file content and respond to your questions.

### Voice Input

For voice-enabled pipeline modes:

1. Select **"Voice to Text"** or **"Voice to Voice"** mode
2. Click the microphone icon or upload an audio file
3. Speak your message
4. Click **Send**

### Configuration

#### Model Initialization

Before using the application, initialize the required models:

1. Expand **"Model Setup"** accordion
2. Click initialization buttons for needed models:
   - **🧠 Initialize LLM**: Required for all modes
   - **🎤 Initialize STT**: Required for voice input
   - **🔊 Initialize TTS**: Required for voice output

#### Settings

Adjust generation parameters:

- **Temperature** (0.1-2.0): Controls randomness and creativity
  - Lower (0.3-0.7): More focused, deterministic responses
  - Higher (0.8-1.5): More creative, varied responses
  
- **Max Tokens** (64-2048): Maximum length of AI responses
  - Lower values: Shorter, concise responses
  - Higher values: Longer, detailed responses

## Usage Examples

### Example 1: Text Chat

```
Pipeline Mode: Text Chat Only
Message: "Explain quantum computing in simple terms"
```

### Example 2: Discussing a Document

```
Pipeline Mode: Text Chat Only
Upload: research_paper.pdf
Message: "Summarize the key findings of this paper"
```

### Example 3: Voice Conversation

```
Pipeline Mode: Voice to Voice
Voice Input: [Speak your question]
Result: Hear AI's response
```

### Example 4: Upload and Voice Response

```
Pipeline Mode: Text to Voice
Upload: meeting_notes.txt
Message: "What are the action items?"
Result: Hear the action items read aloud
```

## Tips

1. **Initialize models first**: Models must be initialized before use
2. **Choose the right pipeline**: Select based on your input/output preferences
3. **GPU acceleration**: If available, use CUDA for faster processing
4. **File size**: Keep uploaded files under 10MB for best performance
5. **Clear chat**: Use the Clear button to start fresh conversations

## Troubleshooting

### Application opens in browser instead of window
- Install pywebview for standalone window mode:
  ```bash
  pip install pywebview
  ```
- Platform-specific enhancements:
  - Windows: `pip install pywebview[cef]`
  - Linux: `pip install pywebview[qt]`
  - macOS: `pip install pywebview[qt]`

### "Model not initialized" error
- Click the appropriate initialization button in Model Setup

### STT/TTS features unavailable
- Install required packages:
  ```bash
  pip install faster-whisper chatterbox-tts
  ```

### Document upload not working
- Install document processing libraries:
  ```bash
  pip install PyPDF2 python-docx
  ```

### Slow performance
- Use smaller models (e.g., STT: "tiny" or "base")
- Reduce max tokens
- Use CPU if GPU memory is insufficient

## Advanced Configuration

### Custom LLM Model

Edit `config.py` to use a different language model:

```python
LLM_MODEL_ID = "your-preferred-model-id"
```

### Custom System Prompt

Modify the system prompt in `app.py`:

```python
messages = [{"role": "system", "content": "Your custom system prompt"}]
```

## Comparison with Testing Suite

| Feature | app.py | testing/integrated_app.py |
|---------|--------|---------------------------|
| Purpose | User application | Testing/development |
| File upload | ✅ Documents | ❌ Audio only |
| Pipeline config | ✅ Flexible | ❌ Fixed tabs |
| Interface | User-friendly | Technical |
| Use case | Daily use | Model testing |

## System Requirements

- **Python**: 3.11+
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: CUDA-capable GPU recommended for optimal performance
- **Disk**: 10GB free space for models

## Support

For issues or questions:
1. Check this guide
2. Review the main README.md
3. Open an issue on GitHub

## License

This application is part of the Zeyta project. See LICENSE for details.
