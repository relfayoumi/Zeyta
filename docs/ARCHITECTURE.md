# Zeyta AI Assistant - Application Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Zeyta AI Assistant (app.py)                      │
│                         User Interface (Gradio)                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│   Text Input │           │  Voice Input │           │ File Upload  │
│              │           │   (Audio)    │           │  (Documents) │
└──────┬───────┘           └──────┬───────┘           └──────┬───────┘
       │                          │                          │
       │                          │                          │
       │                          ▼                          │
       │                  ┌──────────────┐                  │
       │                  │  STT Module  │                  │
       │                  │  (Whisper)   │                  │
       │                  └──────┬───────┘                  │
       │                         │                          │
       │                         │                          │
       └─────────────────────────┼──────────────────────────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │  File Extractor    │
                      │  - TXT, MD         │
                      │  - PDF (PyPDF2)    │
                      │  - DOCX (docx)     │
                      └─────────┬──────────┘
                                │
                                ▼
                      ┌────────────────────┐
                      │   Text Processor   │
                      │  (Combines inputs) │
                      └─────────┬──────────┘
                                │
                                ▼
                      ┌────────────────────┐
                      │    LLM Module      │
                      │  (Transformers)    │
                      │   - Load Model     │
                      │   - Generate Text  │
                      └─────────┬──────────┘
                                │
                                ▼
                      ┌────────────────────┐
                      │  Response Router   │
                      │ (Pipeline Config)  │
                      └─────────┬──────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
            ┌──────────────┐        ┌──────────────┐
            │ Text Output  │        │  TTS Module  │
            │  (Display)   │        │(ChatterboxTTS)│
            └──────────────┘        └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │Voice Output  │
                                    │  (Audio)     │
                                    └──────────────┘
```

## Pipeline Configurations

### 1. Text Chat Only
```
User Input (Text) → LLM → Text Output
```

### 2. Voice to Text
```
Voice Input → STT → LLM → Text Output
```

### 3. Voice to Voice (Full Pipeline)
```
Voice Input → STT → LLM → TTS → Voice Output
```

### 4. Text to Voice
```
Text Input → LLM → TTS → Voice Output
```

### 5. Document + Text Chat
```
File Upload → File Extractor → 
Text Input → Text Processor → LLM → Text Output
```

## Component Breakdown

### User Interface Layer (Gradio)
- **Chat Interface**: Displays conversation history
- **Input Controls**: Text box, file upload, audio recorder
- **Pipeline Selector**: Radio buttons for mode selection
- **Model Controls**: Initialization buttons and status displays
- **Settings**: Temperature and token sliders

### Input Processing Layer
- **Text Input**: Direct text from user
- **Audio Input**: Microphone or file upload
- **File Input**: Document upload with format detection

### Model Layer
- **STT (Speech-to-Text)**: Whisper models (tiny to large-v3)
- **LLM (Language Model)**: Transformers-based models
- **TTS (Text-to-Speech)**: ChatterboxTTS

### Processing Layer
- **File Extractor**: Converts documents to text
- **Text Processor**: Combines and formats inputs
- **Response Router**: Determines output format based on pipeline config

### Output Layer
- **Text Display**: Chatbot interface
- **Audio Player**: For voice responses

## Data Flow Example: Voice to Voice Pipeline

```
1. User clicks microphone and speaks
   ↓
2. Audio recorded and sent to STT module
   ↓
3. STT (Whisper) transcribes audio to text
   "What is machine learning?"
   ↓
4. Transcribed text sent to LLM with conversation history
   ↓
5. LLM generates response
   "Machine learning is a subset of AI that..."
   ↓
6. Response text sent to TTS module
   ↓
7. TTS (ChatterboxTTS) converts text to audio
   ↓
8. Audio playback and text displayed in chat
```

## File Upload Example: Document Analysis

```
1. User uploads research_paper.pdf
   ↓
2. File Extractor detects PDF format
   ↓
3. PyPDF2 extracts text from all pages
   ↓
4. User types: "Summarize the key findings"
   ↓
5. Text Processor combines:
   - File content (document text)
   - User message
   ↓
6. Combined input sent to LLM
   ↓
7. LLM generates summary based on document
   ↓
8. Summary displayed in chat
```

## State Management

```
Global State Variables:
├── llm_model: Loaded language model instance
├── stt_model: Loaded STT model instance
├── tts_model: Loaded TTS model instance
└── chat_history: List of conversation turns

Session State:
├── Current conversation context
├── Uploaded file content
├── Selected pipeline mode
└── User settings (temperature, max_tokens)
```

## Model Initialization Flow

```
User clicks "Initialize LLM"
    ↓
Check if config.py exists
    ├── Yes: Load model ID from config
    └── No: Use default model ID
    ↓
Load model using transformers.pipeline()
    ↓
Configure device (auto/cuda/cpu)
    ↓
Set model to eval mode
    ↓
Update status display
    ↓
Store model in global state
```

## Error Handling Strategy

```
Input Validation
    ↓
Model Availability Check
    ├── Not loaded → Return warning message
    └── Loaded → Continue
    ↓
Try-Except Blocks
    ├── Success → Return result
    └── Error → Return formatted error message
    ↓
User Feedback
    └── Display status/error in UI
```

## File Type Detection Flow

```
File Upload
    ↓
Get file extension
    ├── .txt → Direct read
    ├── .md → Direct read
    ├── .pdf → Check PyPDF2 → Extract with PyPDF2
    ├── .docx → Check python-docx → Extract with docx
    └── Other → Return unsupported error
    ↓
Return extracted text or error message
```

## Performance Considerations

### Model Loading
- Models loaded once and cached in memory
- GPU acceleration (CUDA) when available
- Automatic device selection (auto/cuda/cpu)

### Audio Processing
- No-gradient mode for inference
- Efficient tensor operations
- Proper memory cleanup

### File Processing
- Streaming for large files (if needed)
- Format-specific optimizations
- Error recovery for corrupt files

## Security Considerations

### Input Sanitization
- File type validation
- Size limits (handled by Gradio)
- Path traversal prevention

### Model Security
- Local model execution (no external API calls)
- Controlled generation parameters
- Memory management to prevent OOM

## Extensibility Points

### Adding New File Formats
```python
def extract_file_content(file_path: str) -> str:
    # ... existing code ...
    
    elif file_ext == '.new_format':
        # Add new extraction logic
        return extracted_text
```

### Adding New Pipeline Modes
```python
pipeline_selector = gr.Radio(
    choices=[
        # ... existing modes ...
        "New Custom Mode"
    ]
)
```

### Custom Model Integration
```python
def initialize_custom_model():
    # Load custom model
    return custom_model
```

## Directory Structure

```
Zeyta/
├── app.py                 # Main application
├── APP_GUIDE.md          # User documentation
├── FEATURE_SHOWCASE.md   # Feature overview
├── USAGE_EXAMPLES.md     # Usage scenarios
├── outputs/              # Generated files
│   ├── speech_*.wav      # TTS outputs
│   └── ...
├── core/                 # Core modules
│   ├── brain.py          # LLM handling
│   └── ...
├── IO/                   # Input/Output
│   ├── stt.py           # Speech-to-Text
│   ├── tts.py           # Text-to-Speech
│   └── ...
└── tests/               # Test files
    └── test_app.py      # App tests
```

## Technology Stack

- **UI Framework**: Gradio 
- **LLM**: Hugging Face Transformers
- **STT**: Faster-Whisper
- **TTS**: ChatterboxTTS
- **Document Processing**: PyPDF2, python-docx
- **Audio Processing**: PyTorch, torchaudio
- **Python**: 3.11+

## Deployment Options

### Local Development
```bash
python app.py
# Access at http://localhost:7860
```

### Network Access
```bash
# Edit app.py: server_name="0.0.0.0"
python app.py
# Access at http://<your-ip>:7860
```

### Gradio Share (Temporary Public Link)
```bash
# Edit app.py: share=True
python app.py
# Get temporary public URL
```

## Resource Requirements

### Minimum (CPU Mode)
- RAM: 8GB
- Storage: 10GB (for models)
- CPU: Multi-core recommended

### Recommended (GPU Mode)
- RAM: 16GB
- VRAM: 8GB (CUDA GPU)
- Storage: 20GB
- GPU: NVIDIA RTX 3060 or better

### Model Size Comparison
| Model | STT Size | LLM Size | TTS Size | Total |
|-------|----------|----------|----------|-------|
| Small | ~150MB   | ~3GB     | ~500MB   | ~4GB  |
| Medium| ~500MB   | ~7GB     | ~500MB   | ~8GB  |
| Large | ~3GB     | ~13GB    | ~500MB   | ~16GB |

## Performance Metrics

### Typical Response Times
- **Text Chat**: 2-5 seconds
- **Voice to Text**: 5-10 seconds
- **Voice to Voice**: 10-20 seconds
- **Document Upload**: 1-3 seconds (parsing) + chat time

### Model Loading Times
- **LLM**: 10-30 seconds (first load)
- **STT**: 5-10 seconds
- **TTS**: 5-15 seconds

### Concurrent Usage
- Single user per instance
- Models shared across tabs
- Session-based state management
