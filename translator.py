from transformers.models.marian import MarianTokenizer, MarianMTModel
import os
from typing import List, Tuple, Union

class Translator():
    def __init__(self, models_dir: str = "data"):
        """
        Initialize the Translator with a directory containing downloaded models.
        
        Args:
            models_dir (str): Directory where the opus-mt models are stored
        """
        self.models = {}
        self.models_dir = models_dir 

    def get_supported_langs(self) -> List[List[str]]:
        """
        Get list of supported language pairs based on downloaded models.
        
        Returns:
            List of [source, target] language pairs
        """
        if not os.path.exists(self.models_dir):
            return []
            
        routes = []
        for folder in os.listdir(self.models_dir):
            if folder.startswith('opus-mt-') and len(folder.split('-')) >= 4:
                # Extract source and target languages from folder name
                # Format: opus-mt-{source}-{target}
                parts = folder.split('-')
                if len(parts) >= 4:
                    source = parts[2]
                    target = parts[3]
                    routes.append([source, target])
        return routes 

    def load_model(self, route: str) -> Tuple[int, str]:
        """
        Load a translation model into memory.
        
        Args:
            route (str): Language route in format 'source-target' (e.g., 'en-es')
            
        Returns:
            Tuple of (success_code, message)
            success_code: 1 for success, 0 for failure
            message: Description of the result
        """
        model_name = f'opus-mt-{route}'
        path = os.path.join(self.models_dir, model_name)
        
        if not os.path.exists(path):
            return 0, f"Model directory not found: {path}. Make sure you have downloaded model for {route} translation"
            
        try:
            print(f"Loading model from {path}...")
            model = MarianMTModel.from_pretrained(path)
            tokenizer = MarianTokenizer.from_pretrained(path)
            
            self.models[route] = (model, tokenizer)
            return 1, f"Successfully loaded model for {route} translation"
            
        except Exception as e:
            return 0, f"Error loading model for {route}: {str(e)}"

    def translate(self, source: str, target: str, text: str) -> str:
        """
        Translate text from source language to target language.
        
        Args:
            source (str): Source language code (e.g., 'en')
            target (str): Target language code (e.g., 'es') 
            text (str): Text to translate
            
        Returns:
            Translated text or error message
        """
        route = f'{source}-{target}'
        
        # Load model if not already in memory
        if route not in self.models:
            success_code, message = self.load_model(route)
            if not success_code:
                return message 

        try:
            model, tokenizer = self.models[route]
            
            # Use modern transformers API
            batch = tokenizer(text, return_tensors="pt")
            generated = model.generate(**batch)
            translated: List[str] = tokenizer.batch_decode(generated, skip_special_tokens=True)
            
            return translated[0] if translated else "Translation failed"
            
        except Exception as e:
            return f"Error during translation: {str(e)}"

    def translate_batch(self, source: str, target: str, texts: List[str]) -> List[str]:
        """
        Translate multiple texts at once for better efficiency.
        
        Args:
            source (str): Source language code
            target (str): Target language code
            texts (List[str]): List of texts to translate
            
        Returns:
            List of translated texts
        """
        route = f'{source}-{target}'
        
        # Load model if not already in memory
        if route not in self.models:
            success_code, message = self.load_model(route)
            if not success_code:
                return [message] * len(texts)

        try:
            model, tokenizer = self.models[route]
            
            # Tokenize all texts
            batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
            generated = model.generate(**batch)
            translated: List[str] = tokenizer.batch_decode(generated, skip_special_tokens=True)
            
            return translated
            
        except Exception as e:
            error_msg = f"Error during batch translation: {str(e)}"
            return [error_msg] * len(texts)

    def get_loaded_models(self) -> List[str]:
        """
        Get list of currently loaded models in memory.
        
        Returns:
            List of loaded model routes
        """
        return list(self.models.keys())

    def unload_model(self, route: str) -> bool:
        """
        Remove a model from memory to free up resources.
        
        Args:
            route (str): Language route to unload
            
        Returns:
            True if successfully unloaded, False if model wasn't loaded
        """
        if route in self.models:
            del self.models[route]
            return True
        return False

    def clear_all_models(self):
        """Clear all loaded models from memory."""
        self.models.clear()
