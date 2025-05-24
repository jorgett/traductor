import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    try:
        from app import app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            with app.app_context():
                yield client
    except ImportError:
        # If app can't be imported, create a mock client
        yield Mock()


@pytest.fixture
def temp_model_dir():
    """Create a temporary directory for test models"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_translator():
    """Create a mock translator for testing"""
    try:
        from translator import Translator
        translator = Mock(spec=Translator)
    except ImportError:
        translator = Mock()
    
    translator.models = {}
    translator.supported_languages = [['en', 'es'], ['es', 'en']]
    translator.translate.return_value = "Mocked translation"
    translator.translate_batch.return_value = ["Mocked translation 1", "Mocked translation 2"]
    return translator


@pytest.fixture
def sample_model_dir(temp_model_dir):
    """Create a sample model directory structure"""
    model_name = "opus-mt-en-es"
    model_path = os.path.join(temp_model_dir, model_name)
    os.makedirs(model_path)
    
    # Create dummy model files
    files = ['config.json', 'pytorch_model.bin', 'source.spm', 'target.spm', 
             'tokenizer_config.json', 'vocab.json']
    
    for file in files:
        with open(os.path.join(model_path, file), 'w') as f:
            f.write('{"dummy": "content"}')
    
    return temp_model_dir


@pytest.fixture
def mock_config(temp_model_dir):
    """Create a mock config with temporary model directory"""
    try:
        with patch('config.Config.MODEL_PATH', temp_model_dir):
            yield temp_model_dir
    except ImportError:
        yield temp_model_dir
