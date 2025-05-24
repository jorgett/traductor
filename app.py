"""
Traductor Chat - Offline Translation API
Developed by Jorge Toledo

A modern web interface for offline translation using Hugging Face models.
"""

import os
from flask import Flask, request, jsonify, render_template
from translator import Translator
from config import MODEL_PATH

app = Flask(__name__)

# Initialize translator
translator = Translator(MODEL_PATH)

# Configuration
app.config["DEBUG"] = False  # Disabled for cleaner output
app.config["JSON_AS_ASCII"] = False  # Support for non-ASCII characters

@app.route('/', methods=["GET"])
def home():
    """Redirect to chat interface"""
    from flask import redirect, url_for
    return redirect(url_for('chat_interface'))

@app.route('/api', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return jsonify({
        "status": "healthy",
        "message": "Machine translation service is up and running.",
        "loaded_models": translator.get_loaded_models(),
        "supported_languages": translator.get_supported_langs()
    })

@app.route('/health', methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/lang_routes', methods=["GET"])
def get_lang_routes():
    """Get available target languages for a specific source language"""
    try:
        lang = request.args.get('lang')
        if not lang:
            return jsonify({"error": "Missing 'lang' parameter"}), 400
        
        all_langs = translator.get_supported_langs()
        lang_routes = [route for route in all_langs if route[0] == lang]
        
        return jsonify({
            "source_language": lang,
            "available_targets": lang_routes,
            "count": len(lang_routes)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    """Get all supported language pairs"""
    try:
        langs = translator.get_supported_langs()
        
        # Group by source language for better organization
        grouped_langs = {}
        for source, target in langs:
            if source not in grouped_langs:
                grouped_langs[source] = []
            grouped_langs[source].append(target)
        
        return jsonify({
            "supported_pairs": langs,
            "grouped_by_source": grouped_langs,
            "total_pairs": len(langs)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=["POST"])
def translate_text():
    """Translate text from source to target language"""
    try:
        # Validate JSON payload
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        # Extract required fields
        source = request.json.get('source')
        target = request.json.get('target')
        text = request.json.get('text')
        
        # Validate required fields
        if not all([source, target, text]):
            return jsonify({
                "error": "Missing required fields. Need: source, target, text"
            }), 400
        
        # Validate text is not empty
        if not text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Check if language pair is supported
        supported_langs = translator.get_supported_langs()
        if [source, target] not in supported_langs:
            return jsonify({
                "error": f"Language pair '{source}-{target}' not supported",
                "supported_pairs": supported_langs
            }), 400
        # Perform translation
        translation = translator.translate(source, target, text)
        
        # Check if translation failed (translation is always a string)
        if isinstance(translation, str) and (translation.startswith("Model directory not found") or translation.startswith("Error")):
            return jsonify({"error": translation}), 500
        
        return jsonify({
            "source_language": source,
            "target_language": target,
            "original_text": text,
            "translated_text": translation,
            "success": True
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/translate/batch', methods=["POST"])
def translate_batch():
    """Translate multiple texts at once"""
    try:
        # Validate JSON payload
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        # Extract required fields
        source = request.json.get('source')
        target = request.json.get('target')
        texts = request.json.get('texts')
        
        # Validate required fields
        if not all([source, target, texts]):
            return jsonify({
                "error": "Missing required fields. Need: source, target, texts"
            }), 400
        
        # Validate texts is a list
        if not isinstance(texts, list):
            return jsonify({"error": "Field 'texts' must be a list"}), 400
        
        # Validate texts are not empty
        if not texts or len(texts) == 0:
            return jsonify({"error": "Texts list cannot be empty"}), 400
        
        # Validate individual texts
        valid_texts = [text for text in texts if text and text.strip()]
        if len(valid_texts) != len(texts):
            return jsonify({"error": "All texts must be non-empty strings"}), 400
        
        # Check if language pair is supported
        supported_langs = translator.get_supported_langs()
        if [source, target] not in supported_langs:
            return jsonify({
                "error": f"Language pair '{source}-{target}' not supported",
                "supported_pairs": supported_langs
            }), 400
        
        # Perform batch translation
        translations = translator.translate_batch(source, target, texts)
        
        # Create response with paired texts and translations
        results = []
        for original, translated in zip(texts, translations):
            results.append({
                "original": original,
                "translation": translated
            })
        
        return jsonify({
            "source_language": source,
            "target_language": target,
            "results": results,
            "count": len(results),
            "success": True
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/models', methods=["GET"])
def get_models_info():
    """Get information about loaded models"""
    try:
        return jsonify({
            "loaded_models": translator.get_loaded_models(),
            "supported_languages": translator.get_supported_langs(),
            "models_directory": translator.models_dir
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download_model', methods=["POST"])
def download_model():
    """Download a new translation model"""
    try:
        # Validate JSON payload
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        # Extract required fields
        source = request.json.get('source')
        target = request.json.get('target')
        
        # Validate required fields
        if not all([source, target]):
            return jsonify({
                "error": "Missing required fields. Need: source, target"
            }), 400
        
        # Validate languages are different
        if source == target:
            return jsonify({
                "error": "Source and target languages must be different"
            }), 400
        
        # Import download_model function
        import subprocess
        import sys
        
        # Run download_model.py as subprocess
        try:
            result = subprocess.run([
                sys.executable, 'download_model.py', 
                '--source', source, 
                '--target', target
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode == 0:
                # Reload translator to include new model
                global translator
                translator = Translator(MODEL_PATH)
                
                return jsonify({
                    "success": True,
                    "message": f"Model {source}-{target} downloaded successfully",
                    "source_language": source,
                    "target_language": target,
                    "output": result.stdout
                })
            else:
                return jsonify({
                    "success": False,
                    "message": f"Failed to download model: {result.stderr}",
                    "error": result.stderr
                }), 500
                
        except subprocess.TimeoutExpired:
            return jsonify({
                "success": False,
                "message": "Download timeout - model download taking too long",
                "error": "Timeout after 5 minutes"
            }), 500
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error executing download: {str(e)}",
                "error": str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "error": str(e)
        }), 500

@app.route('/delete_model', methods=["POST"])
def delete_model():
    """Delete a translation model"""
    global translator
    try:
        # Validate JSON payload
        if not request.json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        # Extract required fields
        source = request.json.get('source')
        target = request.json.get('target')
        
        # Validate required fields
        if not all([source, target]):
            return jsonify({
                "error": "Missing required fields. Need: source, target"
            }), 400
        
        model_name = f"opus-mt-{source}-{target}"
        model_path = os.path.join(MODEL_PATH, model_name)
        
        # Check if model exists
        if not os.path.exists(model_path):
            return jsonify({
                "error": f"Model {source}-{target} not found"
            }), 404
        
        # Remove model from memory if loaded
        model_key = f"{source}-{target}"
        if model_key in translator.models:
            del translator.models[model_key]
          # Delete model directory
        import shutil
        shutil.rmtree(model_path)
        
        # Reload translator to update available models
        translator = Translator(MODEL_PATH)
        
        return jsonify({
            "success": True,
            "message": f"Model {source}-{target} deleted successfully",
            "source_language": source,
            "target_language": target
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to delete model: {str(e)}"
        }), 500

@app.route('/chat', methods=["GET"])
def chat_interface():
    """Serve the chat interface"""
    return render_template('chat.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("=" * 50)
    print("  Traductor Chat - Offline Translation")
    print("  Desarrollado por Jorge Toledo")
    print("=" * 50)
    print(f"Directorio de modelos: {MODEL_PATH}")
    print(f"Idiomas soportados: {translator.get_supported_langs()}")
    print("Interfaz de chat: http://localhost:5000")
    print("API REST: http://localhost:5000/api")
    print("Presiona Ctrl+C para detener")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=5000, debug=False)
