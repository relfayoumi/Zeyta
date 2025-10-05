# core/brain.py
import torch
from transformers import pipeline
import logging
from config import LLM_MODEL_ID, GENERATION_ARGS, INITIAL_GEN_ARGS

class Brain:
    """
    Handles loading the Language Model and generating text responses.
    """
    def __init__(self):
        self.pipe = self._load_model()

    def _load_model(self):
        """Loads the text-generation pipeline."""
        logging.info(f"Loading language model: {LLM_MODEL_ID}")
        try:
            pipe = pipeline(
                "text-generation",
                model=LLM_MODEL_ID,
                device_map="auto",
                return_full_text=False,
                torch_dtype=torch.float16
            )
            if device_map := pipe.model.device.type == 'cuda':
                logging.info(f"Model loaded on GPU: {torch.cuda.get_device_name(0)}")
            else:
                logging.info("Model loaded on CPU.")
            logging.info("Language model loaded successfully.")
            return pipe
        except Exception as e:
            logging.error(f"Fatal error loading the language model: {e}")
            raise

    def generate_response(self, messages, initial=False):
        """Generates a response from the LLM based on the conversation history."""
        if not self.pipe:
            logging.error("Model pipeline is not available.")
            return "My brain isn't working right now."

        try:
            # Use different generation arguments for the initial greeting
            gen_args = INITIAL_GEN_ARGS if initial else GENERATION_ARGS
            
            # Add the pad_token_id to the arguments if tokenizer is available
            try:
                tokenizer = getattr(self.pipe, 'tokenizer', None)
                if tokenizer is not None and getattr(tokenizer, 'eos_token_id', None) is not None:
                    gen_args['pad_token_id'] = tokenizer.eos_token_id
                else:
                    # fallback: use pad_token_id=0 safely if tokenizer doesn't expose eos_token_id
                    gen_args.setdefault('pad_token_id', 0)
            except Exception:
                gen_args.setdefault('pad_token_id', 0)
            
            outputs = self.pipe(messages, **gen_args)
            return outputs[0]['generated_text']
        except Exception as e:
            logging.error(f"An error occurred during AI response generation: {e}")
            return "Ugh, my brain just short-circuited. Try that again, I guess."