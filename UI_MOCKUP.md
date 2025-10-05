# Zeyta AI Assistant - UI Mockup

This document shows a visual representation of the application interface.

## Main Application Window

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                        🤖 Zeyta AI Assistant                                   ║
║                                                                                 ║
║        Chat with AI, upload files, and configure your processing pipeline.     ║
╚════════════════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────┬──────────────────────────────────────┐
│                                        │                                      │
│  🔧 Pipeline Configuration             │  ⚙️ Settings                        │
│                                        │                                      │
│  Select Pipeline Mode:                 │  Temperature: [●────────] 0.7       │
│  ⦿ Text Chat Only                      │               ↑                     │
│  ○ Voice to Text                       │           Creativity                │
│  ○ Voice to Voice                      │                                      │
│  ○ Text to Voice                       │  Max Tokens:  [──●──────] 512       │
│                                        │               ↑                     │
│  ▼ Model Setup (Click to expand)       │           Response Length            │
│                                        │                                      │
│  [🧠 Initialize LLM]                   │                                      │
│  LLM Status: ✅ Model loaded           │                                      │
│                                        │                                      │
│  STT Size: [base ▼]                    │                                      │
│  [🎤 Initialize STT]                   │                                      │
│  STT Status: Not initialized           │                                      │
│                                        │                                      │
│  TTS Device: ⦿ CUDA  ○ CPU             │                                      │
│  [🔊 Initialize TTS]                   │                                      │
│  TTS Status: Not initialized           │                                      │
│                                        │                                      │
└────────────────────────────────────────┴──────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  Conversation                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────│
│                                                                                 │
│  👤 User: Hello! Can you help me understand quantum computing?                │
│                                                                                 │
│  🤖 AI: Hello! I'd be happy to help you understand quantum computing.          │
│      Quantum computing is a revolutionary approach to computation that         │
│      leverages the principles of quantum mechanics. Unlike classical           │
│      computers that use bits (0 or 1), quantum computers use quantum           │
│      bits or "qubits" which can exist in multiple states simultaneously...    │
│                                                                                 │
│  👤 User: [Document uploaded: quantum_paper.pdf]                              │
│      What are the main findings in this paper?                                │
│                                                                                 │
│  🤖 AI: Based on the paper you uploaded, here are the main findings:          │
│      1. The researchers demonstrated quantum supremacy using...                │
│      2. They achieved error rates below 1% for the first time...              │
│      3. The quantum algorithm showed exponential speedup...                    │
│                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────│
│                                                                                 │
│  Your Message:                                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐          │
│  │ Type your message here...                                        │          │
│  │                                                                  │          │
│  │                                                                  │          │
│  └─────────────────────────────────────────────────────────────────┘          │
│                                                                                 │
│  [   Send 📤   ]  [  Clear 🗑️  ]                                              │
│                                                                                 │
│  ┌─────────────────────────────────────┬─────────────────────────────────────┐│
│  │ 🎤 Voice Input                      │ 📎 Upload File                      ││
│  │ (for Voice to Text/Voice modes)     │ (TXT, PDF, DOCX, MD)                ││
│  │                                     │                                     ││
│  │ [🎙️ Click to record]                │ [📁 Browse files...]                ││
│  │  or                                 │                                     ││
│  │ [📁 Upload audio file]              │ Selected: quantum_paper.pdf         ││
│  └─────────────────────────────────────┴─────────────────────────────────────┘│
│                                                                                 │
│  🔊 AI Voice Response (for Voice modes)                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │ ▶️ [Audio Player]  0:00 / 0:15                                           │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                          │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────┐
│  💡 Quick Guide                                                                │
│                                                                                 │
│  Pipeline Modes:                                                               │
│  • Text Chat Only: Type messages to chat with AI                              │
│  • Voice to Text: Speak and get text responses                                │
│  • Voice to Voice: Speak and get voice responses                              │
│  • Text to Voice: Type and get voice responses                                │
│                                                                                 │
│  File Upload:                                                                  │
│  Upload documents to discuss their content with the AI.                        │
│                                                                                 │
│  Tips:                                                                          │
│  1. Initialize required models first                                           │
│  2. Select your preferred pipeline mode                                        │
│  3. Upload files or speak/type your message                                    │
│  4. Adjust temperature for creativity                                          │
│                                                                                 │
│  ▼ System Info (Click to expand)                                              │
│  🖥️ GPU: ✅ Available - NVIDIA RTX 4090                                       │
└────────────────────────────────────────────────────────────────────────────────┘
```

## Status Indicators

The application uses clear status indicators throughout:

```
✅ Success        - Operation completed successfully
⚠️ Warning        - Model not initialized or minor issue
❌ Error          - Operation failed
🎤 Voice Active   - Recording or processing voice
🔊 Audio Ready    - Voice output generated
📎 File Attached  - Document uploaded
```

## Pipeline Mode Visual Indicators

When you select different pipeline modes, the interface adapts:

### Text Chat Only Mode
```
┌─────────────────────────────────┐
│ Active Components:               │
│ ✅ Text Input                    │
│ ✅ LLM Processing                │
│ ✅ Text Output                   │
│ ❌ Voice Input (disabled)        │
│ ❌ Voice Output (disabled)       │
└─────────────────────────────────┘
```

### Voice to Text Mode
```
┌─────────────────────────────────┐
│ Active Components:               │
│ ✅ Voice Input                   │
│ ✅ STT (Whisper)                 │
│ ✅ LLM Processing                │
│ ✅ Text Output                   │
│ ❌ Voice Output (disabled)       │
└─────────────────────────────────┘
```

### Voice to Voice Mode (Full Pipeline)
```
┌─────────────────────────────────┐
│ Active Components:               │
│ ✅ Voice Input                   │
│ ✅ STT (Whisper)                 │
│ ✅ LLM Processing                │
│ ✅ TTS (ChatterboxTTS)           │
│ ✅ Voice Output                  │
└─────────────────────────────────┘
```

### Text to Voice Mode
```
┌─────────────────────────────────┐
│ Active Components:               │
│ ✅ Text Input                    │
│ ✅ LLM Processing                │
│ ✅ TTS (ChatterboxTTS)           │
│ ✅ Voice Output                  │
│ ❌ Voice Input (disabled)        │
└─────────────────────────────────┘
```

## Model Initialization Flow

Visual representation of model initialization:

```
Step 1: Click "Initialize LLM"
┌─────────────────────────────────┐
│ [🧠 Initialize LLM]             │
│ Status: Loading model...        │
└─────────────────────────────────┘
         ↓
Step 2: Model loads
┌─────────────────────────────────┐
│ [🧠 Initialize LLM]             │
│ Status: ✅ Model loaded:        │
│         Llama-3.2-3B-Instruct   │
└─────────────────────────────────┘
```

## File Upload Flow

Visual representation of document upload:

```
Step 1: Select file
┌─────────────────────────────────┐
│ 📎 Upload File                  │
│ [📁 Browse files...]            │
└─────────────────────────────────┘
         ↓
Step 2: File selected
┌─────────────────────────────────┐
│ 📎 Upload File                  │
│ Selected: research_paper.pdf    │
│ (2.3 MB)                        │
└─────────────────────────────────┘
         ↓
Step 3: Type question (optional)
┌─────────────────────────────────┐
│ Your Message:                   │
│ "Summarize the key findings"    │
└─────────────────────────────────┘
         ↓
Step 4: Click Send
┌─────────────────────────────────┐
│ [   Send 📤   ]                 │
└─────────────────────────────────┘
         ↓
Step 5: AI processes and responds
```

## Conversation Flow Example

```
┌─────────────────────────────────────────────────────────────┐
│ 👤 User: Can you help me with Python?                      │
├─────────────────────────────────────────────────────────────┤
│ 🤖 AI: Of course! I'd be happy to help you with Python.    │
│     What specific topic or problem would you like          │
│     assistance with?                                        │
├─────────────────────────────────────────────────────────────┤
│ 👤 User: [Uploads: script.py]                              │
│     Can you review this code and suggest improvements?     │
├─────────────────────────────────────────────────────────────┤
│ 🤖 AI: I've reviewed your code. Here are my suggestions:   │
│     1. Line 15: Consider using list comprehension...       │
│     2. Line 22: This could be optimized with...            │
│     3. Add error handling for...                            │
│                                                             │
│     Would you like me to provide the improved code?        │
├─────────────────────────────────────────────────────────────┤
│ 👤 User: Yes, please show the improved version.            │
├─────────────────────────────────────────────────────────────┤
│ 🤖 AI: Here's the improved version:                        │
│     ```python                                               │
│     # Improved code with suggestions applied               │
│     ...                                                     │
│     ```                                                     │
└─────────────────────────────────────────────────────────────┘
```

## Settings Panel Detail

```
┌──────────────────────────────────────┐
│ ⚙️ Settings                          │
├──────────────────────────────────────┤
│                                      │
│ Temperature: [●────────] 0.7         │
│ ├─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐               │
│ 0.1      1.0       2.0               │
│                                      │
│ Controls creativity:                 │
│ • Low (0.3): Factual, focused        │
│ • Medium (0.7): Balanced ⭐          │
│ • High (1.5): Creative, varied       │
│                                      │
│ Max Tokens: [──●──────] 512          │
│ ├─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐               │
│ 64      512      2048                │
│                                      │
│ Controls response length:            │
│ • Short (256): Concise answers       │
│ • Medium (512): Balanced ⭐          │
│ • Long (1024): Detailed explanations │
│                                      │
└──────────────────────────────────────┘
```

## Responsive Layout

The application adapts to different screen sizes:

### Desktop View (Wide)
- Two-column layout
- Settings on the right
- Full-width chat area

### Tablet View (Medium)
- Stacked sections
- Collapsible settings
- Optimized chat area

### Mobile View (Narrow)
- Single column
- Accordion-style sections
- Touch-optimized controls

## Color Scheme

The application uses the Gradio Soft theme with:
- Primary color: Blue (#007bff)
- Success: Green (#28a745)
- Warning: Yellow (#ffc107)
- Error: Red (#dc3545)
- Background: Light gray (#f8f9fa)
- Text: Dark gray (#212529)

## Interactive Elements

All buttons and controls provide visual feedback:
- Hover: Slight color change
- Click: Pressed effect
- Loading: Spinner animation
- Success: Checkmark animation
- Error: Shake animation

## Accessibility Features

- Clear, high-contrast text
- Keyboard navigation support
- Screen reader compatible
- Touch-friendly controls
- Status announcements
- Error messages with suggestions

---

**Note**: This is a text-based mockup. The actual Gradio interface is fully interactive with modern web UI components, animations, and responsive design.

To see the real interface, run:
```bash
python app.py
```

Then open http://localhost:7860 in your browser.
