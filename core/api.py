import os
import time
import google.generativeai as genai
from google.generativeai import caching
import logging
from google.api_core import exceptions

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiHandler:
    def __init__(self):
        """Initialize Gemini API client."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)
        
        # Primary and Fallback Models
        # User environment seems to specificall support 'gemini-2.5-flash' (despite 429s).
        # Standard 1.5 models are returning 404s.
        self.primary_model = "gemini-2.5-flash" 
        self.fallback_model = "gemini-2.0-flash-exp" # Guessing another experimental one?

        
        # Base generation config
        self.generation_config = {
            "temperature": 0.2, 
            "top_p": 0.95,
            "max_output_tokens": 8192,
        }

    def upload_file(self, file_path, display_name=None):
        """Uploads a file to Google GenAI."""
        try:
            logging.info(f"Uploading file: {file_path}")
            if not display_name:
                display_name = os.path.basename(file_path)
                
            file_ref = genai.upload_file(path=file_path, display_name=display_name)
            
            # Wait for file to be processed
            while file_ref.state.name == "PROCESSING":
                time.sleep(1)
                file_ref = genai.get_file(file_ref.name)
                
            if file_ref.state.name == "FAILED":
                raise ValueError(f"File upload failed: {file_ref.state.name}")
            
            logging.info(f"File uploaded successfully: {file_ref.name}")
            return file_ref
        except Exception as e:
            logging.error(f"Upload failed: {e}")
            return None

    def _get_response_with_retry(self, model_name, system_instruction, history, message_parts):
        """Helper to call API with retries."""
        max_retries = 3
        delay = 2 # Initial delay seconds
        
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
                chat = model.start_chat(history=history)
                response = chat.send_message(message_parts, generation_config=self.generation_config)
                return response.text
                
            except exceptions.ResourceExhausted as e:
                # 429 Quota Exceeded
                logging.warning(f"Quota exceeded for {model_name}. Attempt {attempt+1}/{max_retries}. Retrying in {delay}s...")
                if attempt == max_retries - 1:
                    raise e # Re-raise if final attempt
                time.sleep(delay)
                delay *= 2 # Exponential backoff
                
            except exceptions.ServiceUnavailable as e:
                # 503 Service Unavailable
                logging.warning(f"Service unavailable for {model_name}. Retrying in {delay}s...")
                time.sleep(delay)
            except Exception as e:
                # Other errors, maybe fail fast?
                if "429" in str(e):
                     # Handle cases where Exception wraps the 429
                    logging.warning(f"Rate limit hit ({e}). Retrying...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise e
                    
        raise Exception("Max retries exceeded.")

    def generate_response(self, user_prompt, file_uris=None, chat_history=None):
        """
        Generates a response from Gemini, handling rate limits and fallbacks.
        """
        system_instruction = """
        You are an elite AI Content Detection Analyst. Your task is to analyze the input text and determine the likelihood of it being AI-generated.
        
        **OUTPUT FORMAT REQUIREMENTS:**
        1. **Confidence Score**: You MUST start your response with exactly this format: `<<SCORE:XX>>` where XX is the percentage (0-100) representing the probability of AI generation.
        2. **Language**: The rest of your analysis MUST be provided in BOTH **Traditional Chinese (繁體中文)** and **English**.
        
        **Analysis Structure:**
        - **Verdict / 判斷**: A clear statement (Human-written / AI-generated / Mixed).
        - **Key Observations / 關鍵觀察**: Bullet points highlighting specific linguistic features, perplexity cues, or structural patterns.
        - **Detailed Analysis / 詳細分析**: In-depth explanation of why you assigned the score.
        
        If reference files are provided (RAG context), compare the input style to those documents to inform your decision.
        """
        
        # Prepare Chat History
        history_for_sdk = []
        if chat_history:
            for msg in chat_history:
                role = "user" if msg["role"] == "user" else "model"
                history_for_sdk.append({"role": role, "parts": [msg["content"]]})
        
        message_parts = []
        if file_uris:
            message_parts.extend(file_uris)
        message_parts.append(user_prompt)

        # Strategy: Try Primary -> Try Fallback -> Try Final -> Return Friendly Error
        try:
            return self._get_response_with_retry(self.primary_model, system_instruction, history_for_sdk, message_parts)
        except Exception as e_primary:
            logging.error(f"Primary model {self.primary_model} failed: {e_primary}")
            
            # Try Fallback 1 (Flash 8b)
            try:
                logging.info(f"Switching to fallback model 1: {self.fallback_model}")
                return self._get_response_with_retry(self.fallback_model, system_instruction, history_for_sdk, message_parts)
            except Exception as e_fallback_1:
                logging.error(f"Fallback model 1 failed: {e_fallback_1}")
                
                # Try Fallback 2 (Pro - different quota bucket usually)
                try:
                     logging.info(f"Switching to fallback model 2: gemini-1.5-pro")
                     return self._get_response_with_retry("gemini-1.5-pro", system_instruction, history_for_sdk, message_parts)
                except Exception as e_fallback_2:
                    logging.error(f"Fallback 2 failed: {e_fallback_2}")
                    
                    # Try Ultimate Fallback (Legacy 1.0 Pro)
                    try:
                        logging.info(f"Switching to legacy fallback: gemini-pro")
                        return self._get_response_with_retry("gemini-pro", system_instruction, history_for_sdk, message_parts)
                    except Exception as e_final:
                        # Auto-discovery fallback
                        try:
                            logging.info("Attempting auto-discovery of available models...")
                            available_models = []
                            all_models_debug = []
                            for m in genai.list_models():
                                all_models_debug.append(f"{m.name} ({m.supported_generation_methods})")
                                if 'generateContent' in m.supported_generation_methods:
                                    # Prefer flash models if available
                                    if "flash" in m.name:
                                        available_models.insert(0, m.name)
                                    else:
                                        available_models.append(m.name)
                            
                            debug_model_list = "\n".join(all_models_debug) if all_models_debug else "No models returned by ListModels."

                            if available_models:
                                # Try the first 3 discovered models
                                for model_name in available_models[:3]:
                                    try:
                                        logging.info(f"Trying auto-discovered model: {model_name}")
                                        return self._get_response_with_retry(model_name, system_instruction, history_for_sdk, message_parts)
                                    except Exception as e:
                                        logging.warning(f"Auto-discovered model {model_name} failed: {e}")
                                
                                raise Exception("All auto-discovered models failed.")
                            else:
                                raise Exception(f"No models found with generateContent capability. Visible: {debug_model_list}")

                        except Exception as e_auto:
                            logging.error(f"Auto-discovery failed: {e_auto}")
                            # Clean up debug list for display
                            safe_debug_list = debug_model_list if 'debug_model_list' in locals() else "List failed"
                            
                            return f"""⚠️ **System Error / 系統錯誤**: 
All AI models are currently unavailable.

**Diagnosis**:
The Primary model ({self.primary_model}) hit a 429 Quota limit ({str(e_primary)[:100]}...).
We attempted to find other models, but failed.

**Available Models on your Account**:
```
{safe_debug_list}
```

**Action**:
1. If you see 'gemini-1.5-flash' in the list above, the API names might be mismatching.
2. If the list is empty or only contains experimental models, your API Key might be restricted.
3. Please check your [Google AI Studio](https://aistudio.google.com/) API key settings.
"""

# Singleton instance for easy import
gemini = GeminiHandler()
