# 📸 Integrated App Screenshots & Features

## Interface Overview

The Zeyta Integrated Testing App provides a modern, tabbed interface with the following sections:

### Main Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 Zeyta AI Testing Suite                                      │
│                                                                  │
│  Comprehensive testing interface for TTS, STT, and LLM models.  │
│                                                                  │
│  Features:                                                       │
│  - 🗣️ Text-to-Speech (ChatterboxTTS)                           │
│  - 🎤 Speech-to-Text (Whisper)                                  │
│  - 💬 Text-to-Text (LLM Chat)                                   │
│  - 🔄 Full Pipeline Testing                                     │
├─────────────────────────────────────────────────────────────────┤
│ [🗣️ TTS] [🎤 STT] [💬 LLM] [🔄 Pipeline] [ℹ️ About]          │
└─────────────────────────────────────────────────────────────────┘
```

## Tab 1: 🗣️ Text-to-Speech

**Features:**
- Model initialization with GPU/CPU selection
- Text input field for synthesis
- Reference audio upload for voice cloning
- Advanced parameter controls:
  - Temperature slider (0.1-1.5)
  - Exaggeration slider (0.1-1.5)
  - CFG Weight slider (0.1-2.0)
- Real-time audio playback
- Download generated audio

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ Test ChatterboxTTS models                                    │
├─────────────────────────────────────────────────────────────┤
│ Device: [○ CUDA] [○ CPU]                                     │
│ [Initialize TTS Model]                                       │
│ Status: [Ready/Not Loaded]                                   │
├─────────────────────────────────────────────────────────────┤
│ Left Column:                  │ Right Column:                │
│ ┌───────────────────────────┐ │ ┌──────────────────────────┐│
│ │ Text to Synthesize:       │ │ │ Generated Audio:         ││
│ │ [___________________]     │ │ │ [▶ Audio Player]         ││
│ │ [___________________]     │ │ │                          ││
│ │ [___________________]     │ │ │ Generation Info:         ││
│ └───────────────────────────┘ │ │ [Time: 2.3s]            ││
│                               │ │ [File: output_123.wav]   ││
│ Reference Audio (Optional):   │ │                          ││
│ [🎤 Upload or Record]         │ └──────────────────────────┘│
│                               │                              │
│ ▼ Advanced Settings           │                              │
│   Temperature: [====|----] 0.8│                              │
│   Exaggeration: [===|-----] 0.5                              │
│   CFG Weight: [===|-----] 0.5 │                              │
│                               │                              │
│ [Generate Speech]             │                              │
└───────────────────────────────┴──────────────────────────────┘
```

## Tab 2: 🎤 Speech-to-Text

**Features:**
- Model size selection (tiny, base, small, medium, large-v3)
- Audio upload or microphone recording
- Real-time transcription
- Language detection
- Confidence scores

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ Test Whisper STT models                                      │
├─────────────────────────────────────────────────────────────┤
│ Model Size: [▼ base]                                         │
│ [Initialize STT Model]                                       │
│ Status: [Ready/Not Loaded]                                   │
├─────────────────────────────────────────────────────────────┤
│ Left Column:                  │ Right Column:                │
│ ┌───────────────────────────┐ │ ┌──────────────────────────┐│
│ │ Audio Input:              │ │ │ Transcription:           ││
│ │ [🎤 Record] [📁 Upload]   │ │ │                          ││
│ │                           │ │ │ [Your transcribed text   ││
│ │ [▶ Audio Player]          │ │ │  will appear here...]    ││
│ └───────────────────────────┘ │ │                          ││
│                               │ │ Language: en (99%)       ││
│ [Transcribe]                  │ │ Time: 1.2s               ││
│                               │ └──────────────────────────┘│
└───────────────────────────────┴──────────────────────────────┘
```

## Tab 3: 💬 Text-to-Text (LLM)

**Features:**
- Interactive chat interface
- Conversation history
- Adjustable temperature
- Max tokens control
- Clear chat functionality

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ Chat with the LLM                                            │
├─────────────────────────────────────────────────────────────┤
│ [Initialize LLM Model]  Status: [Ready/Not Loaded]          │
├─────────────────────────────────────────────────────────────┤
│ Conversation (75%):           │ Settings (25%):             │
│ ┌───────────────────────────┐ │ ┌─────────────────────────┐│
│ │ 👤 User: Hello!           │ │ │ ▼ Settings              ││
│ │ 🤖 AI: Hi! How can I help?│ │ │                         ││
│ │                           │ │ │ Temperature:            ││
│ │ 👤 User: What's the       │ │ │ [====|----] 0.7         ││
│ │        weather like?      │ │ │                         ││
│ │ 🤖 AI: I don't have access│ │ │ Max Tokens:             ││
│ │        to real-time data. │ │ │ [=======|--] 512        ││
│ │                           │ │ │                         ││
│ │ [Scroll for more...]      │ │ └─────────────────────────┘│
│ └───────────────────────────┘ │                             │
│ Your Message:                 │                             │
│ [Type here...]                │                             │
│ [Send] [Clear Chat]           │                             │
└───────────────────────────────┴─────────────────────────────┘
```

## Tab 4: 🔄 Full Pipeline

**Features:**
- End-to-end testing (STT → LLM → TTS)
- Audio input (upload/record)
- Toggle TTS output
- Adjustable LLM parameters
- Step-by-step results display

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ Test Complete Pipeline                                       │
│                                                              │
│ Test the full voice assistant pipeline:                     │
│ 1. 🎤 Speech-to-Text (transcribe your voice)                │
│ 2. 🤖 LLM Processing (generate AI response)                 │
│ 3. 🔊 Text-to-Speech (convert response to audio)            │
├─────────────────────────────────────────────────────────────┤
│ Left Column:                  │ Right Column:                │
│ ┌───────────────────────────┐ │ ┌──────────────────────────┐│
│ │ Speak or Upload Audio:    │ │ │ Pipeline Results:        ││
│ │ [🎤 Record] [📁 Upload]   │ │ │                          ││
│ │                           │ │ │ 🎤 Step 1: Transcribing  ││
│ │ [▶ Your Audio]            │ │ │ 📝 Transcribed: "Hello"  ││
│ └───────────────────────────┘ │ │                          ││
│                               │ │ 🤖 Step 2: Generating... ││
│ ☑ Generate Speech Output      │ │ 💬 AI: "Hi! How are you?"││
│ LLM Temperature: [===|---] 0.7│ │                          ││
│ Max Tokens: [====|----] 256   │ │ 🔊 Step 3: Generating... ││
│                               │ │ ✅ Complete!             ││
│ [Run Full Pipeline]           │ └──────────────────────────┘│
│                               │                              │
│                               │ AI Response Audio:           │
│                               │ [▶ Audio Player]             │
└───────────────────────────────┴──────────────────────────────┘
```

## Tab 5: ℹ️ About

**Features:**
- System information
- GPU availability
- Model descriptions
- Quick tips
- Future improvements roadmap

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│ Zeyta AI Testing Suite                                       │
├─────────────────────────────────────────────────────────────┤
│ System Information                                           │
│                                                              │
│ 🖥️ GPU Available: ✅ Yes                                    │
│    - Device: NVIDIA GeForce RTX 3080                         │
│    - Memory: 10.00 GB                                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Models                                                       │
│                                                              │
│ TTS (Text-to-Speech):                                        │
│ - ChatterboxTTS with voice cloning support                  │
│ - Located in testing/ folder                                │
│                                                              │
│ STT (Speech-to-Text):                                        │
│ - Faster-Whisper models (tiny - large-v3)                   │
│ - Optimized for real-time transcription                     │
│                                                              │
│ LLM (Large Language Model):                                  │
│ - Configured in config.py                                   │
│ - Default: Llama-3.2-3B-Instruct                            │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Tips & Future Improvements                                   │
│ [See documentation for details...]                           │
└─────────────────────────────────────────────────────────────┘
```

## Color Scheme

The app uses Gradio's "Soft" theme with:
- Clean, modern aesthetics
- High contrast for readability
- Intuitive button colors:
  - Primary actions: Blue
  - Success messages: Green
  - Warnings: Yellow
  - Errors: Red

## Responsive Design

- Works on desktop browsers (1024px+ recommended)
- Adjusts layout for different screen sizes
- Mobile-friendly (portrait/landscape)

## Accessibility Features

- Clear labels for all controls
- Emoji icons for visual cues
- Status messages for screen readers
- Keyboard navigation support
- High contrast UI elements

## User Experience Highlights

1. **Progressive Disclosure**: Advanced settings hidden by default
2. **Clear Feedback**: Status messages for every action
3. **Error Handling**: Helpful error messages with solutions
4. **Real-time Updates**: Live status during processing
5. **Persistent State**: Models stay loaded across tabs
6. **File Management**: Automatic output directory creation
7. **Performance Info**: Shows processing times and stats

## Example Workflows

### Workflow 1: Test TTS Voice Cloning
1. Initialize TTS model (GPU)
2. Upload 5-second reference audio
3. Type text: "Hello, this is a test of voice cloning"
4. Adjust temperature to 0.9 for expressiveness
5. Generate and listen

### Workflow 2: Test STT Accuracy
1. Initialize STT model (base)
2. Record yourself speaking clearly
3. Transcribe
4. Compare with what you said
5. Try different model sizes

### Workflow 3: Chat with AI
1. Initialize LLM
2. Ask: "Explain quantum computing in simple terms"
3. Review response
4. Follow up: "Can you give an analogy?"
5. See conversation context maintained

### Workflow 4: Full Pipeline
1. Initialize all models
2. Record: "What's the capital of France?"
3. Run pipeline
4. Hear AI respond: "The capital of France is Paris."
5. Verify each step in results

---

💡 The interface is designed to be intuitive - first-time users can get started in minutes!
