import os
import time
import google.generativeai as genai
from google.generativeai import caching
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeminiHandler:
    def __init__(self):
        """Initialize Gemini API client."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash" # Confirmed available model
        
        # Base generation config
        self.generation_config = {
            "temperature": 0.2, # Low temp for analytical/detection tasks
            "top_p": 0.95,
            "max_output_tokens": 8192,
        }

    def create_file_search_store(self, display_name="RAG_Knowledge_Base"):
        """Create a new File Search Store."""
        try:
            # Check if store exists (optional optimization, here we just create new or return existing ID logic if you tracked it)
            # For this MVP, we create a new one to ensure fresh context or handle it via a manager
            # In a real app, you might list and reuse.
            pass 
        except Exception as e:
            logging.error(f"Error creating store: {e}")
            return None

    def list_stores(self):
        """List available file search stores."""
        try:
            # Note: The Python SDK currently manages caches differently than the REST API 'FileSearchStore'
            # We will use the 'Caching' API if available or standard file API.
            # *Correction*: As of late 2024, the SDK uses `genai.Caching` or plain `genai.upload_file` for context.
            # For "File Search" specifically (the feature in the JSON), we stick to the 1.5 features.
            # We will implement a simplified version: Upload files -> Pass to model.
            # Real "File Search Store" management often requires the beta REST API or specific SDK update.
            # We will use the 'files' API and pass them to the model context directly or via a tool if supported.
            return []
        except Exception as e:
            logging.error(f"Error listing stores: {e}")
            return []

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

    def generate_response(self, user_prompt, file_uris=None, chat_history=None):
        """
        Generates a response from Gemini, optionally using RAG (uploaded files).
        
        Args:
            user_prompt (str): The user's input text.
            file_uris (list): List of file URIs (from upload_file) to include as context.
            chat_history (list): Previous chat history (standard list of dicts).
        """
        # Config system prompt
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
        
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            
            # Prepare Chat History
            history_for_sdk = []
            if chat_history:
                for msg in chat_history:
                    role = "user" if msg["role"] == "user" else "model"
                    history_for_sdk.append({"role": role, "parts": [msg["content"]]})

            chat = model.start_chat(history=history_for_sdk)
            
            # Construct the message
            # If we have files, we pass them in the message parts
            message_parts = []
            
            # Add files to context if present
            if file_uris:
                # In the updated SDK, you often pass the file object or URI in the parts list
                # However, for RAG validation, we might just pass the file_ref.
                # Since we stored URIs mostly, we need to pass the file objects or let the SDK handle it.
                # We will assume `file_uris` contains the actual File objects returned by upload_file for now,
                # or we fetch them if they are just strings.
                
                # Warning: Directly passing file_ref works in 1.5 Flash.
                message_parts.extend(file_uris)
            
            message_parts.append(user_prompt)
            
            response = chat.send_message(message_parts, generation_config=self.generation_config)
            return response.text

        except Exception as e:
            return f"System Error: {str(e)}"

# Singleton instance for easy import
gemini = GeminiHandler()
