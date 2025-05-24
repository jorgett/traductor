import pytest
import os
import tempfile
from unittest.mock import patch, mock_open


class TestUtilities:
    """Test cases for utility functions and edge cases"""
    
    def test_file_operations(self):
        """Test file operations used in the application"""
        # Test with temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            temp_path = f.name
        
        try:
            # Test file exists
            assert os.path.exists(temp_path)
            
            # Test file reading
            with open(temp_path, 'r') as f:
                content = f.read()
                assert content == 'test content'
                
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_directory_operations(self):
        """Test directory operations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test directory exists
            assert os.path.exists(temp_dir)
            assert os.path.isdir(temp_dir)
            
            # Test creating subdirectory
            sub_dir = os.path.join(temp_dir, 'models')
            os.makedirs(sub_dir)
            assert os.path.exists(sub_dir)
            
            # Test listing directory
            contents = os.listdir(temp_dir)
            assert 'models' in contents
    
    def test_path_operations(self):
        """Test path manipulation operations"""
        # Test path joining
        path = os.path.join('data', 'opus-mt-en-es')
        assert 'data' in path
        assert 'opus-mt-en-es' in path
        
        # Test path normalization
        normalized = os.path.normpath(path)
        assert normalized == path.replace('/', os.sep)
        
        # Test absolute path
        abs_path = os.path.abspath(path)
        assert os.path.isabs(abs_path)
    
    def test_error_handling_patterns(self):
        """Test common error handling patterns"""
        
        # Test handling non-existent file
        with pytest.raises(FileNotFoundError):
            with open('non_existent_file.txt', 'r') as f:
                f.read()
        
        # Test handling permission errors (simulation)
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = PermissionError("Access denied")
            
            with pytest.raises(PermissionError):
                with open('some_file.txt', 'r') as f:
                    f.read()
    
    def test_json_operations(self):
        """Test JSON serialization/deserialization"""
        import json
        
        # Test valid JSON
        data = {
            'source': 'en',
            'target': 'es', 
            'text': 'Hello world'
        }
        
        json_str = json.dumps(data)
        parsed_data = json.loads(json_str)
        
        assert parsed_data == data
        
        # Test invalid JSON
        with pytest.raises(json.JSONDecodeError):
            json.loads('invalid json')
    
    def test_language_code_validation(self):
        """Test language code validation patterns"""
        
        def is_valid_language_code(code):
            """Simple language code validation"""
            return isinstance(code, str) and len(code) >= 2 and code.islower()
        
        # Test valid codes
        valid_codes = ['en', 'es', 'fr', 'de', 'zh']
        for code in valid_codes:
            assert is_valid_language_code(code)
        
        # Test invalid codes
        invalid_codes = ['EN', '1', '', 'x', None, 123]
        for code in invalid_codes:
            assert not is_valid_language_code(code)
    
    def test_text_validation(self):
        """Test text input validation patterns"""
        
        def validate_text(text, max_length=5000):
            """Validate text input"""
            if not isinstance(text, str):
                return False, "Text must be a string"
            if len(text) == 0:
                return False, "Text cannot be empty"
            if len(text) > max_length:
                return False, f"Text too long (max {max_length} characters)"
            return True, "Valid"
        
        # Test valid text
        valid, message = validate_text("Hello world")
        assert valid is True
        
        # Test empty text
        valid, message = validate_text("")
        assert valid is False
        assert "empty" in message
        
        # Test too long text
        long_text = "x" * 6000
        valid, message = validate_text(long_text, max_length=5000)
        assert valid is False
        assert "too long" in message
        
        # Test non-string
        valid, message = validate_text(123)
        assert valid is False
        assert "string" in message
    
    def test_model_name_generation(self):
        """Test model name generation patterns"""
        
        def generate_model_name(source, target):
            """Generate model name from language codes"""
            return f"opus-mt-{source}-{target}"
        
        # Test normal case
        model_name = generate_model_name("en", "es")
        assert model_name == "opus-mt-en-es"
        
        # Test different languages
        model_name = generate_model_name("fr", "de")
        assert model_name == "opus-mt-fr-de"
    
    def test_batch_processing_helpers(self):
        """Test batch processing utility functions"""
        
        def chunk_list(lst, chunk_size):
            """Split list into chunks"""
            for i in range(0, len(lst), chunk_size):
                yield lst[i:i + chunk_size]
        
        # Test normal chunking
        data = list(range(10))
        chunks = list(chunk_list(data, 3))
        
        assert len(chunks) == 4
        assert chunks[0] == [0, 1, 2]
        assert chunks[1] == [3, 4, 5]
        assert chunks[2] == [6, 7, 8]
        assert chunks[3] == [9]
        
        # Test empty list
        chunks = list(chunk_list([], 3))
        assert len(chunks) == 0
        
        # Test chunk size larger than list
        chunks = list(chunk_list([1, 2], 5))
        assert len(chunks) == 1
        assert chunks[0] == [1, 2]
    
    def test_response_formatting(self):
        """Test API response formatting utilities"""
        
        def format_success_response(data):
            """Format successful API response"""
            response = {'success': True}
            response.update(data)
            return response
        
        def format_error_response(error_message, error_code=None):
            """Format error API response"""
            response = {
                'success': False,
                'error': error_message
            }
            if error_code:
                response['error_code'] = error_code
            return response
        
        # Test success response
        success_resp = format_success_response({
            'translated_text': 'Hola mundo',
            'source_language': 'en'
        })
        
        assert success_resp['success'] is True
        assert success_resp['translated_text'] == 'Hola mundo'
        
        # Test error response
        error_resp = format_error_response("Model not found", "MODEL_NOT_FOUND")
        
        assert error_resp['success'] is False
        assert error_resp['error'] == "Model not found"
        assert error_resp['error_code'] == "MODEL_NOT_FOUND"
