# Configuration for model downloading
HUGGINGFACE_S3_BASE_URL = "https://s3.amazonaws.com/models.huggingface.co/bert/Helsinki-NLP"
FILENAMES = ["config.json", "pytorch_model.bin", "source.spm", "target.spm", "tokenizer_config.json", "vocab.json"]
MODEL_PATH = "data"


class Config:
    """Application configuration class"""
    
    # Model storage configuration
    MODEL_PATH = MODEL_PATH
    
    # Text processing limits
    MAX_TEXT_LENGTH = 5000
    MAX_BATCH_SIZE = 100
    
    # Supported models configuration
    SUPPORTED_MODELS = {
        'en-es': {
            'name': 'English to Spanish',
            'description': 'Translate from English to Spanish using OPUS-MT model'
        },
        'es-en': {
            'name': 'Spanish to English', 
            'description': 'Translate from Spanish to English using OPUS-MT model'
        },
        'en-fr': {
            'name': 'English to French',
            'description': 'Translate from English to French using OPUS-MT model'
        },
        'fr-en': {
            'name': 'French to English',
            'description': 'Translate from French to English using OPUS-MT model'
        },
        'en-de': {
            'name': 'English to German',
            'description': 'Translate from English to German using OPUS-MT model'
        },
        'de-en': {
            'name': 'German to English',
            'description': 'Translate from German to English using OPUS-MT model'
        },
        'en-it': {
            'name': 'English to Italian',
            'description': 'Translate from English to Italian using OPUS-MT model'
        },
        'it-en': {
            'name': 'Italian to English',
            'description': 'Translate from Italian to English using OPUS-MT model'
        },
        'en-pt': {
            'name': 'English to Portuguese',
            'description': 'Translate from English to Portuguese using OPUS-MT model'
        },
        'pt-en': {
            'name': 'Portuguese to English',
            'description': 'Translate from Portuguese to English using OPUS-MT model'
        }
    }
    
    # Download configuration
    HUGGINGFACE_S3_BASE_URL = HUGGINGFACE_S3_BASE_URL
    FILENAMES = FILENAMES
