import pytest
import json
import os
from unittest.mock import patch, MagicMock

class TestIntegration:
    """Integration tests for the translation application"""
    
    @patch('app.translator')
    def test_full_translation_workflow(self, mock_translator, client):
        """Test complete workflow: check languages -> translate"""
        # Mock the translator for this test
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate.return_value = "Hola mundo"
        
        # 1. Check supported languages
        response = client.get('/supported_languages')
        assert response.status_code == 200
        
        langs_data = json.loads(response.data)
        assert 'supported_pairs' in langs_data
        assert ['en', 'es'] in langs_data['supported_pairs']
        
        # 2. Perform translation
        translate_data = {
            'source': 'en',
            'target': 'es',
            'text': 'Hello world'
        }
        
        response = client.post('/translate',
                             data=json.dumps(translate_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert result['translated_text'] == "Hola mundo"
        
    @patch('subprocess.run')
    @patch('os.path.exists')
    @patch('shutil.rmtree')
    def test_model_download_and_delete_workflow(self, mock_rmtree, mock_exists, mock_subprocess, client):
        """Test model download and delete workflow"""
        # Mock successful download
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Model downloaded"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        # Mock model exists for deletion
        mock_exists.return_value = True
        
        # 1. Download model
        download_data = {
            'source': 'en',
            'target': 'fr'
        }
        
        response = client.post('/download_model',
                             data=json.dumps(download_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        
        # 2. Delete model
        delete_data = {
            'source': 'en',
            'target': 'fr'
        }
        
        response = client.post('/delete_model',
                             data=json.dumps(delete_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        
    @patch('app.translator')
    def test_batch_translation_workflow(self, mock_translator, client):
        """Test batch translation workflow"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate_batch.return_value = [
            "Hola mundo",
            "Adiós mundo",
            "Buenas noches"
        ]
        
        # Perform batch translation
        batch_data = {
            'source': 'en',
            'target': 'es',
            'texts': [
                'Hello world',
                'Goodbye world',
                'Good night'
            ]
        }
        
        response = client.post('/translate/batch',
                             data=json.dumps(batch_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert result['count'] == 3
        assert len(result['results']) == 3
        
        # Verify each translation pair
        for i, translation_pair in enumerate(result['results']):
            assert 'original' in translation_pair
            assert 'translation' in translation_pair
            assert translation_pair['original'] == batch_data['texts'][i]
            
    def test_error_handling_chain(self, client):
        """Test error handling across the application"""
        # 1. Test invalid JSON
        response = client.post('/translate',
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
        
        # 2. Test missing fields
        response = client.post('/translate',
                             data=json.dumps({'source': 'en'}),
                             content_type='application/json')
        assert response.status_code == 400
        
        # 3. Test empty text
        response = client.post('/translate',
                             data=json.dumps({
                                 'source': 'en',
                                 'target': 'es',
                                 'text': ''
                             }),
                             content_type='application/json')
        assert response.status_code == 400
        
        # 4. Test non-existent endpoint
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
    @patch('app.translator')
    def test_concurrent_requests_simulation(self, mock_translator, client):
        """Simulate concurrent requests to test thread safety"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate.return_value = "Translated text"
        
        # Simulate multiple concurrent requests
        responses = []
        for i in range(5):
            data = {
                'source': 'en',
                'target': 'es',
                'text': f'Text number {i}'
            }
            response = client.post('/translate',
                                 data=json.dumps(data),
                                 content_type='application/json')
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            result = json.loads(response.data)
            assert result['success'] is True
            
    def test_api_endpoints_accessibility(self, client):
        """Test that all API endpoints are accessible"""
        # Test GET endpoints
        get_endpoints = [
            ('/', 302),  # Redirects to /chat
            ('/api', 200),
            ('/health', 200),
            ('/supported_languages', 200),
            ('/models', 200),
            ('/chat', 200)
        ]
        
        for endpoint, expected_status in get_endpoints:
            response = client.get(endpoint)
            assert response.status_code == expected_status, f"Endpoint {endpoint} failed"
            
    @patch('app.translator')
    def test_response_format_consistency(self, mock_translator, client):
        """Test that API responses have consistent format"""
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        mock_translator.translate.return_value = "Hola"
        
        # Test successful translation response format
        response = client.post('/translate',
                             data=json.dumps({
                                 'source': 'en',
                                 'target': 'es',
                                 'text': 'Hello'
                             }),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        
        # Check required fields
        required_fields = ['source_language', 'target_language', 'original_text', 'translated_text', 'success']
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
            
        # Test error response format
        response = client.post('/translate',
                             data=json.dumps({
                                 'source': 'en',
                                 'target': 'es',
                                 'text': ''  # Empty text should cause error
                             }),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        
    @patch('app.translator')
    def test_api_info_structure(self, mock_translator, client):
        """Test API info endpoint provides complete information"""
        mock_translator.get_loaded_models.return_value = ['en-es']
        mock_translator.get_supported_langs.return_value = [['en', 'es']]
        
        response = client.get('/api')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        required_fields = ['status', 'message', 'loaded_models', 'supported_languages']
        
        for field in required_fields:
            assert field in data, f"API info missing field: {field}"
            
        assert data['status'] == 'healthy'
        assert isinstance(data['loaded_models'], list)
        assert isinstance(data['supported_languages'], list)
