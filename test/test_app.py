import pytest
import json
import os
from unittest.mock import patch, MagicMock
from app import app

class TestFlaskApp:
    """Test cases for Flask application endpoints"""
    
    def test_index_route_redirects(self, client):
        """Test the main index route redirects to chat"""
        response = client.get('/')
        assert response.status_code == 302  # Redirect status
        assert '/chat' in response.location
        
    def test_chat_route(self, client):
        """Test the chat interface route"""
        response = client.get('/chat')
        assert response.status_code == 200
        
    def test_api_info_route(self, client):
        """Test the API info route"""
        response = client.get('/api')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'message' in data
        assert 'loaded_models' in data
        assert 'supported_languages' in data
        
    def test_health_check_route(self, client):
        """Test the health check route"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        
    @patch('app.translator')
    def test_supported_languages_route(self, mock_translator, client):
        """Test the supported languages route"""
        mock_translator.get_supported_langs.return_value = [['en', 'es'], ['es', 'en'], ['fr', 'en']]
        
        response = client.get('/supported_languages')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'supported_pairs' in data
        assert 'grouped_by_source' in data
        assert 'total_pairs' in data
        assert data['total_pairs'] == 3
        
    @patch('app.translator')
    def test_translate_success(self, mock_translator, client):
        """Test successful translation"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate.return_value = "Hola mundo"
        
        data = {
            'source': 'en',
            'target': 'es',
            'text': 'Hello world'
        }
        response = client.post('/translate',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert result['translated_text'] == "Hola mundo"
        assert result['source_language'] == 'en'
        assert result['target_language'] == 'es'
        
    def test_translate_missing_fields(self, client):
        """Test translation with missing required fields"""
        data = {
            'source': 'en',
            # Missing 'target' and 'text'
        }
        response = client.post('/translate',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Missing required fields' in result['error']
        
    def test_translate_invalid_json(self, client):
        """Test translation with invalid JSON"""
        response = client.post('/translate',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        
    def test_translate_empty_text(self, client):
        """Test translation with empty text"""
        data = {
            'source': 'en',
            'target': 'es',
            'text': '   '  # Empty/whitespace text
        }
        response = client.post('/translate',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'empty' in result['error'].lower()
        
    @patch('app.translator')
    def test_translate_unsupported_language_pair(self, mock_translator, client):
        """Test translation with unsupported language pair"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        
        data = {
            'source': 'fr',
            'target': 'de',
            'text': 'Bonjour'
        }
        response = client.post('/translate',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'not supported' in result['error']
        
    @patch('app.translator')
    def test_translate_batch_success(self, mock_translator, client):
        """Test successful batch translation"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate_batch.return_value = ["Hola mundo", "Adiós mundo"]
        
        data = {
            'source': 'en',
            'target': 'es',
            'texts': ['Hello world', 'Goodbye world']
        }
        response = client.post('/translate/batch',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert result['count'] == 2
        assert len(result['results']) == 2
        
    def test_translate_batch_missing_fields(self, client):
        """Test batch translation with missing fields"""
        data = {
            'source': 'en',
            # Missing 'target' and 'texts'
        }
        response = client.post('/translate/batch',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Missing required fields' in result['error']
        
    def test_translate_batch_empty_texts(self, client):
        """Test batch translation with empty texts array"""
        data = {
            'source': 'en',
            'target': 'es',
            'texts': []
        }
        response = client.post('/translate/batch',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'empty' in result['error'].lower()
        
    def test_translate_batch_invalid_texts_type(self, client):
        """Test batch translation with invalid texts type"""
        data = {
            'source': 'en',
            'target': 'es',
            'texts': 'not a list'
        }
        response = client.post('/translate/batch',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'list' in result['error']
        
    @patch('app.translator')
    def test_models_info_route(self, mock_translator, client):
        """Test the models info route"""
        mock_translator.get_loaded_models.return_value = ['en-es', 'fr-en']
        mock_translator.get_supported_langs.return_value = [['en', 'es'], ['fr', 'en']]
        mock_translator.models_dir = '/test/models'
        
        response = client.get('/models')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'loaded_models' in data
        assert 'supported_languages' in data
        assert 'models_directory' in data
        assert len(data['loaded_models']) == 2
        
    @patch('subprocess.run')
    def test_download_model_success(self, mock_subprocess, client):
        """Test successful model download"""
        # Mock successful subprocess
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Model downloaded successfully"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        data = {
            'source': 'en',
            'target': 'fr'
        }
        response = client.post('/download_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert 'downloaded successfully' in result['message']
        
    def test_download_model_missing_fields(self, client):
        """Test model download with missing fields"""
        data = {
            'source': 'en'
            # Missing 'target'
        }
        response = client.post('/download_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Missing required fields' in result['error']
        
    def test_download_model_same_languages(self, client):
        """Test model download with same source and target"""
        data = {
            'source': 'en',
            'target': 'en'
        }
        response = client.post('/download_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'different' in result['error']
        
    @patch('subprocess.run')
    def test_download_model_subprocess_error(self, mock_subprocess, client):
        """Test model download with subprocess error"""
        # Mock failed subprocess
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Download failed"
        mock_subprocess.return_value = mock_result
        
        data = {
            'source': 'en',
            'target': 'de'
        }
        response = client.post('/download_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 500
        result = json.loads(response.data)
        assert result['success'] is False
        assert 'Failed to download' in result['message']
        
    @patch('os.path.exists')
    @patch('shutil.rmtree')
    def test_delete_model_success(self, mock_rmtree, mock_exists, client):
        """Test successful model deletion"""
        mock_exists.return_value = True
        
        data = {
            'source': 'en',
            'target': 'es'
        }
        response = client.post('/delete_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert 'deleted successfully' in result['message']
        
    def test_delete_model_missing_fields(self, client):
        """Test model deletion with missing fields"""
        data = {
            'source': 'en'
            # Missing 'target'
        }
        response = client.post('/delete_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Missing required fields' in result['error']
        
    @patch('os.path.exists')
    def test_delete_model_not_found(self, mock_exists, client):
        """Test deletion of non-existent model"""
        mock_exists.return_value = False
        
        data = {
            'source': 'fr',
            'target': 'de'
        }
        response = client.post('/delete_model',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result
        assert 'not found' in result['error']
        
    def test_delete_model_invalid_json(self, client):
        """Test model deletion with invalid JSON"""
        response = client.post('/delete_model',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        
    def test_lang_routes(self, client):
        """Test the lang_routes endpoint"""
        response = client.get('/lang_routes?lang=en')
        assert response.status_code == 200
        
    def test_lang_routes_missing_param(self, client):
        """Test lang_routes without required parameter"""
        response = client.get('/lang_routes')
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        
    def test_404_error_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result
        assert 'not found' in result['error'].lower()
        
    def test_405_error_handler(self, client):
        """Test 405 method not allowed error handler"""
        response = client.patch('/api')  # PATCH method not allowed on /api
        assert response.status_code == 405
        result = json.loads(response.data)
        assert 'error' in result
        assert 'not allowed' in result['error'].lower()
