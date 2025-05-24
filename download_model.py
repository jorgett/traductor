import os
import argparse 
import urllib.error
from urllib.request import urlretrieve
from urllib.parse import urljoin
from config import *

parser = argparse.ArgumentParser(description='Download Hugging Face translation models')
parser.add_argument('--source', type=str, required=True, help='source language code (e.g., en)')
parser.add_argument('--target', type=str, required=True, help='target language code (e.g., es)')

def download_language_model(source, target):
    """Download a translation model from Hugging Face S3"""
    model = f"opus-mt-{source}-{target}"
    model_dir = os.path.join(MODEL_PATH, model)
    
    print(f">>> Downloading data for {source} to {target} model...")
    
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    success = True
    for filename in FILENAMES:
        try:            # Construct the URL properly
            file_url = f"{HUGGINGFACE_S3_BASE_URL}/{model}/{filename}"
            local_path = os.path.join(model_dir, filename)
            
            print(f"Downloading {filename}...")
            print(f"URL: {file_url}")
            
            urlretrieve(file_url, local_path)
            print(f"[OK] {filename} downloaded successfully")
            
        except urllib.error.HTTPError as e:
            print(f"[ERROR] Error downloading {filename}: {e}")
            print("Error retrieving model from url. Please confirm model exists.")
            success = False
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error downloading {filename}: {e}")
            success = False
            break
    
    if success:
        print(f"[SUCCESS] Model {model} download complete!")
    else:
        # Clean up incomplete download
        if os.path.exists(model_dir):
            import shutil
            shutil.rmtree(model_dir)
            print(f"Cleaned up incomplete download directory: {model_dir}")

if __name__ == "__main__":
    args = parser.parse_args()
    download_language_model(args.source, args.target)
