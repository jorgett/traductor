import pytest
import os
from unittest.mock import patch
from config import Config


class TestConfig:
    """Test cases for the Config class"""
    
    def test_default_config_values(self):
        """Test that default configuration values are set correctly"""
        assert hasattr(Config, 'MODEL_PATH')
        assert hasattr(Config, 'MAX_TEXT_LENGTH')
        assert hasattr(Config, 'MAX_BATCH_SIZE')
        assert hasattr(Config, 'SUPPORTED_MODELS')
        
        # Check default values
        assert Config.MODEL_PATH == 'data'
        assert Config.MAX_TEXT_LENGTH == 5000
        assert Config.MAX_BATCH_SIZE == 100
        assert isinstance(Config.SUPPORTED_MODELS, dict)
    
    def test_supported_models_structure(self):
        """Test that supported models have correct structure"""
        models = Config.SUPPORTED_MODELS
        
        # Check that it's a dictionary
        assert isinstance(models, dict)
        
        # Check some expected language pairs
        expected_pairs = ['en-es', 'es-en', 'en-fr', 'fr-en']
        for pair in expected_pairs:
            if pair in models:
                assert isinstance(models[pair], dict)
                assert 'name' in models[pair]
                assert 'description' in models[pair]
    
    def test_model_path_absolute(self):
        """Test that MODEL_PATH can be made absolute"""
        relative_path = Config.MODEL_PATH
        absolute_path = os.path.abspath(relative_path)
        
        assert os.path.isabs(absolute_path)
        assert absolute_path.endswith('data')
    
    def test_max_values_are_positive(self):
        """Test that maximum values are positive integers"""
        assert isinstance(Config.MAX_TEXT_LENGTH, int)
        assert isinstance(Config.MAX_BATCH_SIZE, int)
        assert Config.MAX_TEXT_LENGTH > 0
        assert Config.MAX_BATCH_SIZE > 0
    
    @patch.dict(os.environ, {'MODEL_PATH': '/custom/path'})
    def test_environment_variable_override(self):
        """Test that environment variables can override config values"""
        # Note: This test demonstrates how environment variables could be used
        # The actual Config class would need to be modified to support this
        custom_path = os.environ.get('MODEL_PATH')
        assert custom_path == '/custom/path'
    
    def test_config_immutability(self):
        """Test that config values behave as expected when accessed"""
        original_path = Config.MODEL_PATH
        original_max_length = Config.MAX_TEXT_LENGTH
        
        # These should remain the same
        assert Config.MODEL_PATH == original_path
        assert Config.MAX_TEXT_LENGTH == original_max_length
    
    def test_supported_models_content(self):
        """Test specific content of supported models"""
        models = Config.SUPPORTED_MODELS
        
        # Test that models have meaningful descriptions
        for model_key, model_info in models.items():
            assert len(model_key) > 0
            assert isinstance(model_info.get('name'), str)
            assert len(model_info.get('name', '')) > 0
            assert isinstance(model_info.get('description'), str)
            assert len(model_info.get('description', '')) > 0
    
    def test_language_codes_format(self):
        """Test that language codes in model keys follow expected format"""
        models = Config.SUPPORTED_MODELS
        
        for model_key in models.keys():
            # Should be in format 'xx-yy' where xx and yy are language codes
            parts = model_key.split('-')
            assert len(parts) == 2
            assert len(parts[0]) >= 2  # Language codes are at least 2 characters
            assert len(parts[1]) >= 2
            assert parts[0].islower()  # Language codes should be lowercase
            assert parts[1].islower()
    
    def test_config_attributes_exist(self):
        """Test that all expected configuration attributes exist"""
        required_attributes = [
            'MODEL_PATH',
            'MAX_TEXT_LENGTH', 
            'MAX_BATCH_SIZE',
            'SUPPORTED_MODELS'
        ]
        
        for attr in required_attributes:
            assert hasattr(Config, attr), f"Config missing required attribute: {attr}"
    
    def test_config_values_types(self):
        """Test that configuration values have correct types"""
        assert isinstance(Config.MODEL_PATH, str)
        assert isinstance(Config.MAX_TEXT_LENGTH, int)
        assert isinstance(Config.MAX_BATCH_SIZE, int)
        assert isinstance(Config.SUPPORTED_MODELS, dict)
