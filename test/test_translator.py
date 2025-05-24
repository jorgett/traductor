import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from translator import Translator

class TestTranslator:
    """Test the Translator class functionality"""
    
    def test_translator_init(self):
        """Test translator initialization"""
        translator = Translator("test_dir")
        assert translator.models_dir == "test_dir"
        assert len(translator.models) == 0
        
    def test_get_supported_langs_empty(self):
        """Test getting supported languages in empty directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            result = translator.get_supported_langs()
            assert result == []
        
    def test_get_supported_langs_with_models(self):
        """Test getting supported languages with valid model directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a model directory
            model_dir = os.path.join(temp_dir, "opus-mt-en-es")
            os.makedirs(model_dir)
            
            translator = Translator(temp_dir)
            result = translator.get_supported_langs()
            assert isinstance(result, list)
            assert ['en', 'es'] in result
            
    @patch('translator.MarianMTModel.from_pretrained')
    @patch('translator.MarianTokenizer.from_pretrained')
    def test_load_model_success(self, mock_tokenizer, mock_model):
        """Test successful model loading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup mocks
            mock_model.return_value = MagicMock()
            mock_tokenizer.return_value = MagicMock()
            
            # Create model directory
            model_path = os.path.join(temp_dir, "opus-mt-en-es")
            os.makedirs(model_path)
            
            translator = Translator(temp_dir)
            success_code, message = translator.load_model("en-es")
            
            assert success_code == 1
            assert "Successfully loaded" in message
            assert "en-es" in translator.models
        
    def test_load_model_nonexistent(self):
        """Test loading a non-existent model"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            success_code, message = translator.load_model("fr-de")
            
            assert success_code == 0
            assert "not found" in message
            assert "fr-de" not in translator.models
            
    def test_translate_model_not_loaded(self):
        """Test translation with model not loaded"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            result = translator.translate("fr", "de", "Hello")
            # Should return error message
            assert "not found" in result.lower() or "error" in result.lower()
            
    def test_get_loaded_models(self):
        """Test getting loaded models"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            
            # Add some mock models
            translator.models["en-es"] = (MagicMock(), MagicMock())
            translator.models["fr-en"] = (MagicMock(), MagicMock())
            
            loaded = translator.get_loaded_models()
            assert isinstance(loaded, list)
            assert "en-es" in loaded
            assert "fr-en" in loaded
            
    def test_unload_model(self):
        """Test model unloading"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            
            # Add a mock model
            translator.models["en-es"] = (MagicMock(), MagicMock())
            
            result = translator.unload_model("en-es")
            assert result is True
            assert "en-es" not in translator.models
            
    def test_unload_nonexistent_model(self):
        """Test unloading a model that doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            result = translator.unload_model("fr-de")
            assert result is False
            
    def test_clear_all_models(self):
        """Test clearing all loaded models"""
        with tempfile.TemporaryDirectory() as temp_dir:
            translator = Translator(temp_dir)
            
            # Add some mock models
            translator.models["en-es"] = (MagicMock(), MagicMock())
            translator.models["fr-en"] = (MagicMock(), MagicMock())
            
            translator.clear_all_models()
            assert len(translator.models) == 0
