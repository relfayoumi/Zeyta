# Zeyta Interface Comparison Guide

This document helps you choose the right interface for your needs.

## Overview

Zeyta provides three different interfaces:

1. **`app.py`** - AI Assistant Application (NEW ⭐)
2. **`testing/integrated_app.py`** - Testing Suite
3. **`main.py`** - Command-Line Voice Assistant

## When to Use Each Interface

### Use `app.py` when you want to:
- ✅ Chat with AI using text
- ✅ Upload and discuss documents (PDF, DOCX, TXT)
- ✅ Choose your input/output method (text or voice)
- ✅ Have a flexible, user-friendly interface
- ✅ Switch between different pipeline modes easily
- ✅ Use the AI for daily tasks

**Best for**: General users, document analysis, flexible AI interaction

### Use `testing/integrated_app.py` when you want to:
- ✅ Test and compare different models
- ✅ Fine-tune model parameters
- ✅ Benchmark performance
- ✅ Develop new features
- ✅ Debug model behavior
- ✅ Test voice cloning

**Best for**: Developers, model testing, performance tuning

### Use `main.py` when you want to:
- ✅ Pure voice-based interaction
- ✅ Command-line interface
- ✅ Simple voice assistant
- ✅ No GUI needed
- ✅ Embedded/headless systems

**Best for**: Voice-only use cases, scripting, headless systems

## Detailed Comparison

### Interface Type

| Feature | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| **Interface** | Web UI (Gradio) | Web UI (Gradio) | Command Line |
| **Accessibility** | Browser-based | Browser-based | Terminal |
| **Visual** | ✅ Modern UI | ✅ Technical UI | ❌ Text only |

### Input Methods

| Feature | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| **Text Input** | ✅ Yes | ✅ Yes (LLM tab) | ❌ No |
| **Voice Input** | ✅ Optional | ✅ Test only | ✅ Primary |
| **File Upload** | ✅ Documents | ✅ Audio only | ❌ No |
| **Microphone** | ✅ Yes | ✅ Yes | ✅ Yes |

### Output Methods

| Feature | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| **Text Output** | ✅ Yes | ✅ Yes | ❌ No |
| **Voice Output** | ✅ Optional | ✅ Test only | ✅ Primary |
| **Audio Files** | ✅ Saved | ✅ Saved | ✅ Played |

### Pipeline Configuration

| Feature | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| **Switchable Modes** | ✅ 4 modes | ❌ Fixed tabs | ❌ Fixed |
| **Text Only** | ✅ Yes | ✅ Yes | ❌ No |
| **Voice Only** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Mixed Mode** | ✅ Yes | ❌ No | ❌ No |

### Features

| Feature | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| **Chat History** | ✅ In-session | ✅ In-session | ✅ Persistent |
| **Document Upload** | ✅ Yes | ❌ No | ❌ No |
| **Model Selection** | ✅ Via config | ✅ Via UI | ✅ Via config |
| **Parameter Tuning** | ✅ Basic | ✅ Advanced | ❌ Config only |
| **Voice Cloning** | ⚠️ Via TTS | ✅ Yes | ✅ Yes |

### Use Cases

| Use Case | Recommended Interface |
|----------|----------------------|
| Daily AI chat | **app.py** |
| Document analysis | **app.py** |
| Code review | **app.py** |
| Voice conversation | **app.py** or **main.py** |
| Model testing | **integrated_app.py** |
| Performance tuning | **integrated_app.py** |
| Voice cloning setup | **integrated_app.py** |
| Embedded system | **main.py** |
| Hands-free only | **main.py** |

## Feature Matrix

### Document Processing

| Format | app.py | integrated_app.py | main.py |
|--------|--------|-------------------|---------|
| TXT | ✅ | ❌ | ❌ |
| PDF | ✅ | ❌ | ❌ |
| DOCX | ✅ | ❌ | ❌ |
| MD | ✅ | ❌ | ❌ |

### Model Components

| Component | app.py | integrated_app.py | main.py |
|-----------|--------|-------------------|---------|
| LLM | ✅ | ✅ | ✅ |
| STT | ✅ Optional | ✅ Separate tab | ✅ Required |
| TTS | ✅ Optional | ✅ Separate tab | ✅ Required |

### Configuration

| Setting | app.py | integrated_app.py | main.py |
|---------|--------|-------------------|---------|
| Temperature | ✅ UI slider | ✅ UI slider | ⚙️ config.py |
| Max Tokens | ✅ UI slider | ✅ UI slider | ⚙️ config.py |
| Model Selection | ⚙️ config.py | ✅ UI dropdown | ⚙️ config.py |
| System Prompt | ⚙️ config.py | ⚙️ Hard-coded | ⚙️ config.py |

## Installation Requirements

All interfaces require the same base dependencies:

```bash
pip install -r requirements.txt
```

### Optional Dependencies

**For app.py document support:**
```bash
pip install PyPDF2 python-docx
```

**For TTS (all interfaces):**
```bash
pip install chatterbox-tts
```

**For STT (all interfaces):**
```bash
pip install faster-whisper
```

## Running Each Interface

### app.py
```bash
python app.py
# Opens at http://localhost:7860
```

### integrated_app.py
```bash
python testing/integrated_app.py
# Opens at http://localhost:7860
```

### main.py
```bash
python main.py
# Runs in terminal
```

## Switching Between Interfaces

You can run all three interfaces (not simultaneously on same port), and they share:
- Model configurations (config.py)
- Core modules (core/, IO/)
- Dependencies

## Resource Usage

| Interface | RAM | GPU | Storage |
|-----------|-----|-----|---------|
| **app.py** | 8GB+ | Optional | 10GB+ |
| **integrated_app.py** | 8GB+ | Optional | 10GB+ |
| **main.py** | 6GB+ | Optional | 8GB+ |

**Notes:**
- All can run on CPU (slower)
- GPU recommended for better performance
- Model sizes vary (3GB-13GB for LLM)

## Performance Comparison

### Response Time (Approximate)

| Task | app.py | integrated_app.py | main.py |
|------|--------|-------------------|---------|
| Text Chat | 2-5s | 2-5s | N/A |
| Voice Input | 5-10s | 5-10s | 3-8s |
| Voice Output | +8-15s | +8-15s | 8-15s |
| Document Upload | 1-3s | N/A | N/A |

### Startup Time

| Interface | First Launch | Subsequent |
|-----------|--------------|------------|
| **app.py** | ~10s | ~5s |
| **integrated_app.py** | ~10s | ~5s |
| **main.py** | ~15s | ~15s |

**Note:** Model loading happens on demand in app.py and integrated_app.py

## Migration Guide

### From main.py to app.py

1. Keep your `config.py` settings
2. Run `python app.py`
3. Initialize LLM model
4. Use "Text Chat Only" or "Voice to Voice" mode

**Benefits:**
- ✅ Add file upload capability
- ✅ Get visual interface
- ✅ Keep voice features

### From integrated_app.py to app.py

1. Note your preferred settings
2. Run `python app.py`
3. Initialize required models
4. Adjust temperature/tokens in settings

**What you lose:**
- ❌ Advanced testing features
- ❌ Model comparison tools
- ❌ Separate component testing

**What you gain:**
- ✅ File upload
- ✅ Pipeline flexibility
- ✅ Cleaner interface

## Recommendations by User Type

### Casual User
**Recommended: `app.py`**
- Easy to use
- Flexible input/output
- Document support

### Power User
**Recommended: `app.py` + `integrated_app.py`**
- Use app.py for daily tasks
- Use integrated_app.py for model tuning

### Developer
**Recommended: All three**
- app.py: End-user testing
- integrated_app.py: Development and testing
- main.py: CLI integration testing

### Voice-Only User
**Recommended: `main.py` or `app.py` (Voice to Voice)**
- main.py: Simple, dedicated
- app.py: More features, visual feedback

## Summary

| Priority | Choose |
|----------|--------|
| **Ease of use** | app.py |
| **Flexibility** | app.py |
| **Documents** | app.py |
| **Testing** | integrated_app.py |
| **Development** | integrated_app.py |
| **Voice-only** | main.py |
| **CLI-only** | main.py |

## Getting Started

1. **First time?** → Start with `app.py`
2. **Need testing?** → Use `integrated_app.py`
3. **Voice-only?** → Try `main.py`

Each interface serves a specific purpose. Choose based on your needs!
