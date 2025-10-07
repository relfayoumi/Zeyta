#!/usr/bin/env python3
"""
Zeyta - Interactive AI Assistant Application

A user-friendly interface for chatting with AI, uploading files,
and configuring the processing pipeline.
"""

import warnings
import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger().setLevel(logging.ERROR)

import gradio as gr
import torch

# Global state variables
llm_model = None
stt_model = None
tts_model = None
chat_history = []

# Configuration
APP_DIR = Path(__file__).parent
OUTPUT_DIR = APP_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_file_content(file_path: str) -> str:
    """Extract text content from uploaded files"""
    try:
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_ext == '.pdf':
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                return "ΓÜá∩╕Å PyPDF2 not installed. Install with: pip install PyPDF2"
        
        elif file_ext in ['.doc', '.docx']:
            try:
                import docx
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                return "ΓÜá∩╕Å python-docx not installed. Install with: pip install python-docx"
        
        elif file_ext == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            return f"ΓÜá∩╕Å Unsupported file type: {file_ext}"
            
    except Exception as e:
        return f"Γ¥î Error reading file: {str(e)}"


def initialize_llm(model_id: str = None):
    """Initialize LLM model"""
    global llm_model
    try:
        from transformers import pipeline
        
        # Check if config exists
        config_path = APP_DIR / "config.py"
        if config_path.exists() and model_id is None:
            sys.path.insert(0, str(config_path.parent))
            from config import LLM_MODEL_ID
            model_id = LLM_MODEL_ID
        elif model_id is None:
            model_id = "chuanli11/Llama-3.2-3B-Instruct-uncensored"
        
        llm_model = pipeline(
            "text-generation",
            model=model_id,
            device_map="auto",
            return_full_text=False,
            torch_dtype=torch.float16
        )
        
        return f"Γ£à LLM Model loaded: {model_id}"
    except Exception as e:
        return f"Γ¥î Failed to load LLM: {str(e)}"


def initialize_stt(model_size: str = "base"):
    """Initialize Speech-to-Text model"""
    global stt_model
    try:
        from faster_whisper import WhisperModel
        stt_model = WhisperModel(model_size, device="auto", compute_type="float16")
        return f"Γ£à STT Model loaded: Whisper {model_size}"
    except Exception as e:
        return f"Γ¥î Failed to load STT: {str(e)}"


def initialize_tts(device: str = "cuda"):
    """Initialize Text-to-Speech model"""
    global tts_model
    try:
        from chatterbox.tts import ChatterboxTTS
        
        device = device if device == "cuda" and torch.cuda.is_available() else "cpu"
        tts_model = ChatterboxTTS(device=device)
        
        if device == "cuda":
            tts_model.model.eval()
            torch.cuda.empty_cache()
        
        return f"Γ£à TTS Model loaded on {device.upper()}"
    except Exception as e:
        return f"Γ¥î Failed to load TTS: {str(e)}"


def transcribe_audio(audio_file: str) -> str:
    """Transcribe audio using STT"""
    global stt_model
    
    if stt_model is None:
        return "ΓÜá∩╕Å STT model not initialized"
    
    if audio_file is None:
        return "ΓÜá∩╕Å No audio file provided"
    
    try:
        segments, info = stt_model.transcribe(audio_file, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text
    except Exception as e:
        return f"Γ¥î Transcription failed: {str(e)}"


def generate_speech(text: str) -> Optional[str]:
    """Generate speech from text using TTS"""
    global tts_model
    
    if tts_model is None or not text:
        return None
    
    try:
        import torchaudio as ta
        import time
        
        with torch.no_grad():
            audio_data = tts_model.generate(text=text, temperature=0.8)
        
        output_path = OUTPUT_DIR / f"speech_{int(time.time())}.wav"
        sample_rate = getattr(tts_model, 'sample_rate', 24000)
        
        if torch.is_tensor(audio_data):
            audio_data = audio_data.cpu()
        
        ta.save(str(output_path), audio_data, sample_rate)
        return str(output_path)
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def chat_with_pipeline(
    message: str,
    history: List[Tuple[str, str]],
    uploaded_file,
    audio_input,
    pipeline_config: str,
    temperature: float = 0.7,
    max_tokens: int = 512
) -> Tuple[List[Tuple[str, str]], Optional[str]]:
    """
    Main chat function with pipeline configuration
    
    Pipeline options:
    - Text Chat Only: Just LLM
    - Voice to Text: STT + LLM
    - Voice to Voice: STT + LLM + TTS
    - Text to Voice: LLM + TTS
    """
    global llm_model, stt_model, tts_model
    
    # Build the user input
    user_input = message
    audio_output = None
    
    # Handle file upload
    if uploaded_file is not None:
        file_content = extract_file_content(uploaded_file)
        if file_content:
            user_input = f"[File content]\n{file_content}\n\n[User message]\n{message}" if message else file_content
    
    # Handle audio input (STT)
    if audio_input is not None and pipeline_config in ["Voice to Text", "Voice to Voice"]:
        if stt_model is None:
            return history + [[message or "[Audio input]", "ΓÜá∩╕Å STT model not initialized"]], None
        
        transcribed_text = transcribe_audio(audio_input)
        if transcribed_text.startswith("Γ¥î") or transcribed_text.startswith("ΓÜá∩╕Å"):
            return history + [[message or "[Audio input]", transcribed_text]], None
        
        # Combine transcribed text with typed message
        user_input = f"{transcribed_text}\n{message}" if message else transcribed_text
    
    # Check if LLM is initialized
    if llm_model is None:
        return history + [[user_input or message, "ΓÜá∩╕Å LLM model not initialized"]], None
    
    # Generate LLM response
    try:
        # Build conversation history
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": user_input})
        
        # Generate response
        gen_args = {
            "max_new_tokens": max_tokens,
            "do_sample": True,
            "temperature": temperature,
            "top_p": 0.95,
            "repetition_penalty": 1.3,
        }
        
        if hasattr(llm_model, 'tokenizer') and hasattr(llm_model.tokenizer, 'eos_token_id'):
            gen_args['pad_token_id'] = llm_model.tokenizer.eos_token_id
        
        output = llm_model(messages, **gen_args)
        response = output[0]['generated_text']
        
        # Generate speech if needed (TTS)
        if pipeline_config in ["Voice to Voice", "Text to Voice"]:
            if tts_model is not None:
                audio_output = generate_speech(response)
        
        return history + [[user_input, response]], audio_output
        
    except Exception as e:
        return history + [[user_input or message, f"Γ¥î Error: {str(e)}"]], None


def create_app():
    """Create the Gradio application interface"""
    
    with gr.Blocks(title="Zeyta AI Assistant", theme=gr.themes.Soft()) as app:
        gr.Markdown(
            """
            # ≡ƒñû Zeyta AI Assistant
            
            Chat with AI, upload files, and configure your processing pipeline.
            """
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # Pipeline Configuration
                gr.Markdown("### ≡ƒöº Pipeline Configuration")
                
                with gr.Row():
                    pipeline_selector = gr.Radio(
                        choices=[
                            "Text Chat Only",
                            "Voice to Text", 
                            "Voice to Voice",
                            "Text to Voice"
                        ],
                        value="Text Chat Only",
                        label="Select Pipeline Mode",
                        info="Choose which components to use"
                    )
                
                # Model Initialization
                with gr.Accordion("Model Setup", open=False):
                    gr.Markdown("**Initialize models before use:**")
                    
                    with gr.Row():
                        llm_init_btn = gr.Button("≡ƒºá Initialize LLM", size="sm")
                        llm_status = gr.Textbox(label="LLM Status", interactive=False, scale=2)
                    
                    with gr.Row():
                        stt_size = gr.Dropdown(
                            ["tiny", "base", "small", "medium", "large-v3"],
                            value="base",
                            label="STT Model Size",
                            scale=1
                        )
                        stt_init_btn = gr.Button("≡ƒÄñ Initialize STT", size="sm")
                        stt_status = gr.Textbox(label="STT Status", interactive=False, scale=2)
                    
                    with gr.Row():
                        tts_device = gr.Radio(
                            ["cuda", "cpu"],
                            value="cuda" if torch.cuda.is_available() else "cpu",
                            label="TTS Device",
                            scale=1
                        )
                        tts_init_btn = gr.Button("≡ƒöè Initialize TTS", size="sm")
                        tts_status = gr.Textbox(label="TTS Status", interactive=False, scale=2)
            
            with gr.Column(scale=1):
                # Settings
                gr.Markdown("### ΓÜÖ∩╕Å Settings")
                
                temperature = gr.Slider(
                    minimum=0.1,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature"
                )
                
                max_tokens = gr.Slider(
                    minimum=64,
                    maximum=2048,
                    value=512,
                    step=64,
                    label="Max Tokens"
                )
        
        gr.Markdown("---")
        
        # Main Chat Interface
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=500,
                    show_copy_button=True
                )
                
                with gr.Row():
                    with gr.Column(scale=4):
                        msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            lines=3,
                            show_label=False
                        )
                    
                    with gr.Column(scale=1):
                        send_btn = gr.Button("Send ≡ƒôñ", variant="primary", size="lg")
                        clear_btn = gr.Button("Clear ≡ƒùæ∩╕Å", size="lg")
                
                # Audio and File Upload
                with gr.Row():
                    audio_input = gr.Audio(
                        label="≡ƒÄñ Voice Input (for Voice modes)",
                        type="filepath",
                        sources=["upload", "microphone"]
                    )
                    
                    file_upload = gr.File(
                        label="≡ƒôÄ Upload File (TXT, PDF, DOCX, MD)",
                        file_types=[".txt", ".pdf", ".docx", ".doc", ".md"]
                    )
                
                # Audio Output
                audio_output = gr.Audio(
                    label="≡ƒöè AI Voice Response (for Voice modes)",
                    autoplay=True
                )
            
            with gr.Column(scale=1):
                gr.Markdown(
                    """
                    ### ≡ƒÆí Quick Guide
                    
                    **Pipeline Modes:**
                    
                    - **Text Chat Only**: Type messages to chat with AI
                    - **Voice to Text**: Speak and get text responses
                    - **Voice to Voice**: Speak and get voice responses
                    - **Text to Voice**: Type and get voice responses
                    
                    **File Upload:**
                    
                    Upload documents to discuss their content with the AI.
                    
                    **Tips:**
                    
                    1. Initialize required models first
                    2. Select your preferred pipeline mode
                    3. Upload files or speak/type your message
                    4. Adjust temperature for creativity
                    """
                )
                
                # System info
                with gr.Accordion("System Info", open=False):
                    device_info = "≡ƒûÑ∩╕Å **GPU:** " + ("Γ£à Available" if torch.cuda.is_available() else "Γ¥î Not Available")
                    if torch.cuda.is_available():
                        device_info += f"\n- {torch.cuda.get_device_name(0)}"
                    gr.Markdown(device_info)
        
        # Event handlers
        def clear_chat():
            return None, None, None
        
        # Initialize models
        llm_init_btn.click(
            fn=initialize_llm,
            outputs=[llm_status]
        )
        
        stt_init_btn.click(
            fn=initialize_stt,
            inputs=[stt_size],
            outputs=[stt_status]
        )
        
        tts_init_btn.click(
            fn=initialize_tts,
            inputs=[tts_device],
            outputs=[tts_status]
        )
        
        # Chat interaction
        send_btn.click(
            fn=chat_with_pipeline,
            inputs=[msg, chatbot, file_upload, audio_input, pipeline_selector, temperature, max_tokens],
            outputs=[chatbot, audio_output]
        ).then(
            fn=lambda: (None, None, None),
            outputs=[msg, file_upload, audio_input]
        )
        
        msg.submit(
            fn=chat_with_pipeline,
            inputs=[msg, chatbot, file_upload, audio_input, pipeline_selector, temperature, max_tokens],
            outputs=[chatbot, audio_output]
        ).then(
            fn=lambda: (None, None, None),
            outputs=[msg, file_upload, audio_input]
        )
        
        clear_btn.click(
            fn=lambda: None,
            outputs=[chatbot]
        ).then(
            fn=clear_chat,
            outputs=[msg, file_upload, audio_input]
        )
    
    return app


if __name__ == "__main__":
    print("=" * 60)
    print("≡ƒÜÇ Starting Zeyta AI Assistant")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("≡ƒôª Checking dependencies...")
    
    try:
        import faster_whisper
        print("Γ£à Faster-Whisper available")
    except ImportError:
        print("ΓÜá∩╕Å  Faster-Whisper not found (needed for voice features)")
    
    try:
        from transformers import pipeline
        print("Γ£à Transformers available")
    except ImportError:
        print("Γ¥î Transformers not found - LLM features will not work")
    
    try:
        from chatterbox.tts import ChatterboxTTS
        print("Γ£à ChatterboxTTS available")
    except ImportError:
        print("ΓÜá∩╕Å  ChatterboxTTS not found (needed for voice output)")
    
    if torch.cuda.is_available():
        print(f"Γ£à CUDA available - {torch.cuda.get_device_name(0)}")
    else:
        print("ΓÜá∩╕Å  CUDA not available - models will run on CPU")
    
    print()
    print("=" * 60)
    print("≡ƒûÑ∩╕Å  Launching application in standalone window...")
    print("=" * 60)
    
    app = create_app()
    
    # Try to launch in a standalone window using webview
    try:
        import webview
        import threading
        
        # Start Gradio server in a thread
        def start_server():
            app.launch(
                server_name="127.0.0.1",
                server_port=7860,
                share=False,
                show_error=True,
                inbrowser=False,  # Don't open browser
                quiet=True
            )
        
        # Start server in background thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for server to start
        import time
        time.sleep(2)
        
        # Create and show the window
        print("Γ£à Opening application window...")
        webview.create_window(
            "Zeyta AI Assistant",
            "http://127.0.0.1:7860",
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            min_size=(800, 600)
        )
        webview.start()
        
    except ImportError:
        print("ΓÜá∩╕Å  pywebview not installed - falling back to browser mode")
        print("   Install with: pip install pywebview")
        print("   For best experience on different platforms:")
        print("   - Windows: pip install pywebview[cef]")
        print("   - Linux: pip install pywebview[qt]")
        print("   - macOS: pip install pywebview[qt]")
        print()
        print("≡ƒîÉ Opening in browser instead...")
        
        # Fallback to browser mode
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
