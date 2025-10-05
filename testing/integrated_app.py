#!/usr/bin/env python3
"""
Integrated Testing App for Zeyta AI Assistant
Allows testing of TTS, STT, and LLM models in a user-friendly interface
"""

import warnings
import logging
import os
import sys
from pathlib import Path

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger().setLevel(logging.ERROR)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gradio as gr
import torch
import torchaudio as ta
import time
import json
from datetime import datetime

# Import project modules
try:
    from chatterbox.tts import ChatterboxTTS
except ImportError:
    ChatterboxTTS = None

# Global state variables
llm_model = None
tts_model = None
stt_model = None
chat_history = []

# Configuration
TESTING_DIR = Path(__file__).parent
AUDIO_OUTPUT_DIR = TESTING_DIR / "outputs"
AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)

def initialize_llm():
    """Initialize LLM model for text-to-text testing"""
    global llm_model
    try:
        from transformers import pipeline
        import torch
        
        # Check if config exists
        config_path = Path(__file__).parent.parent / "config.py"
        if config_path.exists():
            sys.path.insert(0, str(config_path.parent))
            from config import LLM_MODEL_ID, GENERATION_ARGS
        else:
            # Default configuration
            LLM_MODEL_ID = "chuanli11/Llama-3.2-3B-Instruct-uncensored"
            GENERATION_ARGS = {
                "max_new_tokens": 512,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.95,
                "repetition_penalty": 1.3,
            }
        
        llm_model = pipeline(
            "text-generation",
            model=LLM_MODEL_ID,
            device_map="auto",
            return_full_text=False,
            torch_dtype=torch.float16
        )
        
        # Add pad_token_id
        if hasattr(llm_model, 'tokenizer') and hasattr(llm_model.tokenizer, 'eos_token_id'):
            GENERATION_ARGS['pad_token_id'] = llm_model.tokenizer.eos_token_id
        
        return "✅ LLM Model loaded successfully!", llm_model, GENERATION_ARGS
    except Exception as e:
        return f"❌ Failed to load LLM: {str(e)}", None, None

def initialize_tts_model(device_choice="cuda"):
    """Initialize ChatterboxTTS model"""
    global tts_model
    try:
        if ChatterboxTTS is None:
            return "❌ ChatterboxTTS not installed. Install with: pip install chatterbox-tts"
        
        device = device_choice if device_choice == "cuda" and torch.cuda.is_available() else "cpu"
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tts_model = ChatterboxTTS(device=device)
        
        # Optimize for inference
        if device == "cuda":
            tts_model.model.eval()
            if hasattr(torch.cuda, 'empty_cache'):
                torch.cuda.empty_cache()
        
        return f"✅ ChatterboxTTS loaded on {device.upper()}"
    except Exception as e:
        return f"❌ Failed to load TTS: {str(e)}"

def initialize_stt_model(model_size="base"):
    """Initialize Whisper STT model"""
    global stt_model
    try:
        from faster_whisper import WhisperModel
        
        stt_model = WhisperModel(model_size, device="auto", compute_type="float16")
        return f"✅ Whisper STT ({model_size}) loaded successfully"
    except Exception as e:
        return f"❌ Failed to load STT: {str(e)}"

def generate_tts(text, reference_audio=None, temperature=0.8, exaggeration=0.5, cfg_weight=0.5):
    """Generate speech from text using ChatterboxTTS"""
    global tts_model
    
    if not text:
        return None, "⚠️ Please enter text to synthesize"
    
    if tts_model is None:
        return None, "⚠️ TTS model not loaded. Please initialize it first."
    
    try:
        start_time = time.time()
        
        # Handle reference audio if provided
        ref_audio = None
        sr_target = None
        if reference_audio is not None:
            try:
                ref_audio, sr_target = ta.load(reference_audio)
                # Ensure mono
                if ref_audio.shape[0] > 1:
                    ref_audio = ref_audio.mean(dim=0, keepdim=True)
            except Exception as e:
                return None, f"❌ Failed to load reference audio: {str(e)}"
        
        # Generate speech
        with torch.no_grad():
            if ref_audio is not None:
                audio_data = tts_model.generate(
                    text=text,
                    reference_audio=ref_audio,
                    temperature=temperature,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            else:
                audio_data = tts_model.generate(
                    text=text,
                    temperature=temperature,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
        
        # Save output
        output_path = AUDIO_OUTPUT_DIR / f"tts_output_{int(time.time())}.wav"
        
        # Get sample rate from model or use default
        sample_rate = sr_target if sr_target is not None else 24000
        if hasattr(tts_model, 'sample_rate'):
            sample_rate = tts_model.sample_rate
        
        # Ensure audio is on CPU for saving
        if torch.is_tensor(audio_data):
            audio_data = audio_data.cpu()
        
        ta.save(str(output_path), audio_data, sample_rate)
        
        elapsed = time.time() - start_time
        
        return str(output_path), f"✅ Generated in {elapsed:.2f}s\n📁 Saved to: {output_path.name}"
        
    except Exception as e:
        return None, f"❌ Generation failed: {str(e)}"

def transcribe_audio(audio_file):
    """Transcribe audio using Whisper STT"""
    global stt_model
    
    if stt_model is None:
        return "⚠️ STT model not loaded. Please initialize it first."
    
    if audio_file is None:
        return "⚠️ Please upload or record audio"
    
    try:
        start_time = time.time()
        
        # Transcribe
        segments, info = stt_model.transcribe(audio_file, beam_size=5)
        
        # Collect all segments
        text = " ".join([segment.text for segment in segments])
        
        elapsed = time.time() - start_time
        
        result = f"📝 Transcription ({elapsed:.2f}s):\n\n{text}\n\n"
        result += f"Language: {info.language} (confidence: {info.language_probability:.2%})"
        
        return result
        
    except Exception as e:
        return f"❌ Transcription failed: {str(e)}"

def chat_with_llm(message, history, temperature=0.7, max_tokens=512):
    """Chat with LLM model"""
    global llm_model, chat_history
    
    if llm_model is None:
        return "⚠️ LLM model not loaded. Please initialize it first."
    
    try:
        # Build conversation history
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        
        # Add previous messages
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
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
        
        return response
        
    except Exception as e:
        return f"❌ Generation failed: {str(e)}"

def full_pipeline_test(audio_input, tts_enabled=True, temperature=0.7, max_tokens=256):
    """Test full pipeline: STT -> LLM -> TTS"""
    global stt_model, llm_model, tts_model
    
    results = []
    
    # Step 1: Transcribe audio
    if audio_input is None:
        return "⚠️ Please provide audio input", None
    
    results.append("🎤 Step 1: Transcribing audio...")
    
    if stt_model is None:
        return "⚠️ STT model not loaded", None
    
    try:
        segments, info = stt_model.transcribe(audio_input, beam_size=5)
        user_text = " ".join([segment.text for segment in segments])
        results.append(f"📝 Transcribed: {user_text}\n")
    except Exception as e:
        return f"❌ Transcription failed: {str(e)}", None
    
    # Step 2: Generate LLM response
    results.append("🤖 Step 2: Generating AI response...")
    
    if llm_model is None:
        return "\n".join(results) + "\n⚠️ LLM model not loaded", None
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_text}
        ]
        
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
        ai_response = output[0]['generated_text']
        results.append(f"💬 AI Response: {ai_response}\n")
    except Exception as e:
        return "\n".join(results) + f"\n❌ LLM generation failed: {str(e)}", None
    
    # Step 3: Generate speech (if enabled)
    audio_output = None
    if tts_enabled and tts_model is not None:
        results.append("🔊 Step 3: Generating speech...")
        try:
            with torch.no_grad():
                audio_data = tts_model.generate(text=ai_response, temperature=0.8)
            
            output_path = AUDIO_OUTPUT_DIR / f"pipeline_output_{int(time.time())}.wav"
            sample_rate = 24000
            if hasattr(tts_model, 'sample_rate'):
                sample_rate = tts_model.sample_rate
            
            if torch.is_tensor(audio_data):
                audio_data = audio_data.cpu()
            
            ta.save(str(output_path), audio_data, sample_rate)
            audio_output = str(output_path)
            results.append(f"✅ Speech saved to: {output_path.name}")
        except Exception as e:
            results.append(f"⚠️ TTS generation failed: {str(e)}")
    elif tts_enabled:
        results.append("⚠️ TTS model not loaded - skipping speech generation")
    
    return "\n".join(results), audio_output

# Create Gradio interface
def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="Zeyta AI Testing Suite", theme=gr.themes.Soft()) as app:
        gr.Markdown(
            """
            # 🤖 Zeyta AI Testing Suite
            
            Comprehensive testing interface for TTS, STT, and LLM models.
            
            **Features:**
            - 🗣️ Text-to-Speech (ChatterboxTTS)
            - 🎤 Speech-to-Text (Whisper)
            - 💬 Text-to-Text (LLM Chat)
            - 🔄 Full Pipeline Testing
            """
        )
        
        with gr.Tabs():
            # ===== TTS Testing Tab =====
            with gr.Tab("🗣️ Text-to-Speech"):
                gr.Markdown("### Test ChatterboxTTS models")
                
                with gr.Row():
                    with gr.Column():
                        tts_device = gr.Radio(
                            ["cuda", "cpu"], 
                            label="Device", 
                            value="cuda" if torch.cuda.is_available() else "cpu"
                        )
                        tts_init_btn = gr.Button("Initialize TTS Model", variant="primary")
                        tts_status = gr.Textbox(label="Status", interactive=False)
                
                gr.Markdown("---")
                
                with gr.Row():
                    with gr.Column():
                        tts_text = gr.Textbox(
                            label="Text to Synthesize",
                            placeholder="Enter text to convert to speech...",
                            lines=3
                        )
                        tts_ref_audio = gr.Audio(
                            label="Reference Audio (Optional - for voice cloning)",
                            type="filepath"
                        )
                        
                        with gr.Accordion("Advanced Settings", open=False):
                            tts_temperature = gr.Slider(
                                minimum=0.1, maximum=1.5, value=0.8, step=0.1,
                                label="Temperature (expressiveness)"
                            )
                            tts_exaggeration = gr.Slider(
                                minimum=0.1, maximum=1.5, value=0.5, step=0.1,
                                label="Exaggeration (emotion)"
                            )
                            tts_cfg_weight = gr.Slider(
                                minimum=0.1, maximum=2.0, value=0.5, step=0.1,
                                label="CFG Weight"
                            )
                        
                        tts_generate_btn = gr.Button("Generate Speech", variant="primary")
                    
                    with gr.Column():
                        tts_output_audio = gr.Audio(label="Generated Audio")
                        tts_output_status = gr.Textbox(label="Generation Info", interactive=False)
                
                tts_init_btn.click(
                    fn=initialize_tts_model,
                    inputs=[tts_device],
                    outputs=[tts_status]
                )
                
                tts_generate_btn.click(
                    fn=generate_tts,
                    inputs=[tts_text, tts_ref_audio, tts_temperature, tts_exaggeration, tts_cfg_weight],
                    outputs=[tts_output_audio, tts_output_status]
                )
            
            # ===== STT Testing Tab =====
            with gr.Tab("🎤 Speech-to-Text"):
                gr.Markdown("### Test Whisper STT models")
                
                with gr.Row():
                    with gr.Column():
                        stt_model_size = gr.Dropdown(
                            ["tiny", "base", "small", "medium", "large-v3"],
                            label="Model Size",
                            value="base"
                        )
                        stt_init_btn = gr.Button("Initialize STT Model", variant="primary")
                        stt_status = gr.Textbox(label="Status", interactive=False)
                
                gr.Markdown("---")
                
                with gr.Row():
                    with gr.Column():
                        stt_audio_input = gr.Audio(
                            label="Audio Input",
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        stt_transcribe_btn = gr.Button("Transcribe", variant="primary")
                    
                    with gr.Column():
                        stt_output = gr.Textbox(
                            label="Transcription",
                            lines=10,
                            interactive=False
                        )
                
                stt_init_btn.click(
                    fn=initialize_stt_model,
                    inputs=[stt_model_size],
                    outputs=[stt_status]
                )
                
                stt_transcribe_btn.click(
                    fn=transcribe_audio,
                    inputs=[stt_audio_input],
                    outputs=[stt_output]
                )
            
            # ===== LLM Chat Tab =====
            with gr.Tab("💬 Text-to-Text (LLM)"):
                gr.Markdown("### Chat with the LLM")
                
                with gr.Row():
                    llm_init_btn = gr.Button("Initialize LLM Model", variant="primary")
                    llm_status = gr.Textbox(label="Status", interactive=False, scale=3)
                
                gr.Markdown("---")
                
                with gr.Row():
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(label="Conversation", height=400)
                        msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            lines=2
                        )
                        with gr.Row():
                            send_btn = gr.Button("Send", variant="primary")
                            clear_btn = gr.Button("Clear Chat")
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("Settings", open=True):
                            llm_temperature = gr.Slider(
                                minimum=0.1, maximum=2.0, value=0.7, step=0.1,
                                label="Temperature"
                            )
                            llm_max_tokens = gr.Slider(
                                minimum=64, maximum=2048, value=512, step=64,
                                label="Max Tokens"
                            )
                
                def user_message(message, history):
                    return "", history + [[message, None]]
                
                def bot_response(history, temperature, max_tokens):
                    message = history[-1][0]
                    response = chat_with_llm(message, history[:-1], temperature, max_tokens)
                    history[-1][1] = response
                    return history
                
                llm_init_btn.click(
                    fn=lambda: initialize_llm()[0],
                    outputs=[llm_status]
                )
                
                msg.submit(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
                    bot_response, [chatbot, llm_temperature, llm_max_tokens], chatbot
                )
                send_btn.click(user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
                    bot_response, [chatbot, llm_temperature, llm_max_tokens], chatbot
                )
                clear_btn.click(lambda: None, None, chatbot, queue=False)
            
            # ===== Full Pipeline Tab =====
            with gr.Tab("🔄 Full Pipeline"):
                gr.Markdown(
                    """
                    ### Test Complete Pipeline
                    
                    Test the full voice assistant pipeline:
                    1. 🎤 Speech-to-Text (transcribe your voice)
                    2. 🤖 LLM Processing (generate AI response)
                    3. 🔊 Text-to-Speech (convert response to audio)
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        pipeline_audio_input = gr.Audio(
                            label="Speak or Upload Audio",
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        
                        with gr.Row():
                            pipeline_tts_enabled = gr.Checkbox(
                                label="Generate Speech Output",
                                value=True
                            )
                            pipeline_temperature = gr.Slider(
                                minimum=0.1, maximum=2.0, value=0.7, step=0.1,
                                label="LLM Temperature"
                            )
                            pipeline_max_tokens = gr.Slider(
                                minimum=64, maximum=512, value=256, step=64,
                                label="Max Response Tokens"
                            )
                        
                        pipeline_run_btn = gr.Button("Run Full Pipeline", variant="primary", size="lg")
                    
                    with gr.Column():
                        pipeline_output = gr.Textbox(
                            label="Pipeline Results",
                            lines=15,
                            interactive=False
                        )
                        pipeline_audio_output = gr.Audio(label="AI Response Audio")
                
                pipeline_run_btn.click(
                    fn=full_pipeline_test,
                    inputs=[pipeline_audio_input, pipeline_tts_enabled, pipeline_temperature, pipeline_max_tokens],
                    outputs=[pipeline_output, pipeline_audio_output]
                )
            
            # ===== About Tab =====
            with gr.Tab("ℹ️ About"):
                gr.Markdown(
                    """
                    ## Zeyta AI Testing Suite
                    
                    ### System Information
                    """
                )
                
                device_info = "🖥️ **GPU Available:** " + ("✅ Yes" if torch.cuda.is_available() else "❌ No")
                if torch.cuda.is_available():
                    device_info += f"\n- Device: {torch.cuda.get_device_name(0)}"
                    device_info += f"\n- Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
                
                gr.Markdown(device_info)
                
                gr.Markdown(
                    """
                    ### Models
                    
                    **TTS (Text-to-Speech):**
                    - ChatterboxTTS with voice cloning support
                    - Located in `testing/` folder
                    
                    **STT (Speech-to-Text):**
                    - Faster-Whisper models (tiny, base, small, medium, large-v3)
                    - Optimized for real-time transcription
                    
                    **LLM (Large Language Model):**
                    - Configured in `config.py`
                    - Default: Llama-3.2-3B-Instruct
                    
                    ### Tips
                    
                    1. **Initialize models** before using them (click the Initialize button in each tab)
                    2. **GPU acceleration** is used automatically if available
                    3. **Reference audio** for TTS should be 5-10 seconds for best results
                    4. **Pipeline mode** tests all components together
                    5. **Generated files** are saved to `testing/outputs/`
                    
                    ### Future Improvements
                    
                    - Model comparison tools
                    - Batch processing
                    - Performance metrics
                    - Custom model loading
                    - Voice profile management
                    """
                )
        
        gr.Markdown(
            """
            ---
            
            💡 **Quick Start:** Initialize the models you want to test, then try each feature!
            """
        )
    
    return app

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Zeyta AI Testing Suite")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    
    deps_ok = True
    
    if ChatterboxTTS is None:
        print("⚠️  ChatterboxTTS not found - TTS features will be limited")
        deps_ok = False
    else:
        print("✅ ChatterboxTTS available")
    
    try:
        import faster_whisper
        print("✅ Faster-Whisper available")
    except ImportError:
        print("⚠️  Faster-Whisper not found - STT features will be limited")
        deps_ok = False
    
    try:
        from transformers import pipeline
        print("✅ Transformers available")
    except ImportError:
        print("⚠️  Transformers not found - LLM features will be limited")
        deps_ok = False
    
    if torch.cuda.is_available():
        print(f"✅ CUDA available - {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  CUDA not available - models will run on CPU (slower)")
    
    print()
    print("=" * 60)
    print("🌐 Launching web interface...")
    print("=" * 60)
    
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
