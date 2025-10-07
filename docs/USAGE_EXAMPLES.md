# Example Usage of Zeyta AI Assistant

This file demonstrates various usage patterns of the Zeyta AI Assistant application.

## Pipeline Configurations

### 1. Text Chat Only (Minimal Setup)

**Use Case**: Simple text-based conversations with AI

**Requirements**:
- Initialize: LLM model only
- No audio models needed

**Example**:
```
User: "What is machine learning?"
AI: "Machine learning is a subset of artificial intelligence..."
```

### 2. Voice to Text (Voice Input)

**Use Case**: Speak to the AI, read text responses

**Requirements**:
- Initialize: STT + LLM models
- Microphone or audio file

**Example**:
```
[User speaks]: "Tell me about quantum computing"
[STT transcribes]: "Tell me about quantum computing"
AI: [Text response about quantum computing]
```

### 3. Voice to Voice (Full Voice Assistant)

**Use Case**: Complete voice conversation

**Requirements**:
- Initialize: STT + LLM + TTS models
- Microphone or audio file
- Audio output

**Example**:
```
[User speaks]: "What's the weather like?"
[STT → LLM → TTS]
[AI speaks]: "I don't have access to weather data..."
```

### 4. Text to Voice (Read Aloud)

**Use Case**: Type messages, hear AI responses

**Requirements**:
- Initialize: LLM + TTS models
- Audio output

**Example**:
```
User: "Read me a story about space"
[AI generates text and converts to speech]
```

## File Upload Examples

### Uploading a Document

1. Select pipeline mode (usually "Text Chat Only")
2. Click "Upload File" and select a PDF, DOCX, TXT, or MD file
3. Type a question or leave empty
4. The AI will process the document

**Example Workflow**:
```
Upload: research_paper.pdf
Message: "What is the main conclusion of this paper?"
AI: "Based on the document, the main conclusion is..."
```

### Analyzing Code

```
Upload: script.py
Message: "Explain what this code does and suggest improvements"
AI: "This code implements... Improvements could include..."
```

### Summarizing Meeting Notes

```
Upload: meeting_notes.txt
Message: "Create a bullet-point summary of action items"
AI: "Here are the action items:
- Item 1...
- Item 2..."
```

## Advanced Scenarios

### Multi-turn Conversation with Document

```
Upload: documentation.pdf

Turn 1:
User: "What are the main features?"
AI: [Explains features from document]

Turn 2:
User: "How do I install it?"
AI: [Provides installation steps from document]

Turn 3:
User: "Are there any prerequisites?"
AI: [Lists prerequisites]
```

### Voice Dictation with File

```
Pipeline: Voice to Text
Upload: template.txt
[Speak]: "Add a new section about security best practices"
AI: [Suggests content based on template and request]
```

### Reading Documents Aloud

```
Pipeline: Text to Voice
Upload: article.txt
Message: "Read this article to me"
[AI converts document to speech]
```

## Settings Recommendations

### For Creative Writing
- Temperature: 0.9-1.2
- Max Tokens: 1024-2048

### For Factual Q&A
- Temperature: 0.3-0.6
- Max Tokens: 256-512

### For Code Generation
- Temperature: 0.5-0.7
- Max Tokens: 512-1024

### For Summarization
- Temperature: 0.4-0.6
- Max Tokens: 256-512

## Tips for Best Results

1. **Initialize models once**: Models stay loaded for the session
2. **Clear chat when changing topics**: Prevents context confusion
3. **Adjust temperature**: Lower for factual, higher for creative
4. **Use file upload wisely**: Smaller files (< 5MB) process faster
5. **Pipeline selection**: Match mode to your needs (don't load TTS if you don't need voice)
6. **GPU usage**: Enable CUDA for TTS/LLM if available
7. **STT model size**: "base" is good balance, "tiny" for speed, "large-v3" for accuracy

## Troubleshooting

### Issue: Model initialization fails
**Solution**: Check RAM/GPU memory, try smaller models

### Issue: File upload shows error
**Solution**: Install PyPDF2/python-docx, check file format

### Issue: Voice input not working
**Solution**: Check microphone permissions, initialize STT model

### Issue: No audio output
**Solution**: Initialize TTS model, check system audio settings

### Issue: Slow responses
**Solution**: Use smaller models, reduce max tokens, use GPU if available
