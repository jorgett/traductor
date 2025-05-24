class TranslatorChat {
    constructor() {
        this.messagesContainer = document.getElementById('messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.sourceLang = document.getElementById('source-lang');
        this.targetLang = document.getElementById('target-lang');
        this.swapButton = document.getElementById('swap-languages');
        this.charCount = document.getElementById('char-count');
        
        // Download elements
        this.downloadSource = document.getElementById('download-source');
        this.downloadTarget = document.getElementById('download-target');
        this.downloadButton = document.getElementById('download-model');
        this.downloadStatus = document.getElementById('download-status');
        
        this.initializeEventListeners();
        this.loadSupportedLanguages();
    }

    initializeEventListeners() {
        // Enviar mensaje
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enviar con Enter (pero permitir Shift+Enter para nueva línea)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Contador de caracteres
        this.messageInput.addEventListener('input', () => {
            this.updateCharCounter();
        });

        // Intercambiar idiomas
        this.swapButton.addEventListener('click', () => {
            this.swapLanguages();
        });

        // Auto-resize del textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });

        // Download model functionality
        this.downloadSource.addEventListener('change', () => {
            this.updateDownloadButton();
        });

        this.downloadTarget.addEventListener('change', () => {
            this.updateDownloadButton();
        });

        this.downloadButton.addEventListener('click', () => {
            this.downloadModel();
        });
    }    async loadSupportedLanguages() {
        try {
            const response = await fetch('/supported_languages');
            const data = await response.json();
            
            if (data.supported_pairs) {
                this.updateLanguageOptions(data.supported_pairs);
                this.updateAvailableModels(data.supported_pairs);
                this.updateDownloadOptions(data.supported_pairs);
            }
        } catch (error) {
            console.error('Error loading supported languages:', error);
        }
    }

    updateAvailableModels(supportedPairs) {
        const modelsContainer = document.getElementById('available-models');
        
        if (supportedPairs.length === 0) {
            modelsContainer.innerHTML = '<div class="loading">No hay modelos descargados</div>';
            return;
        }

        modelsContainer.innerHTML = '';
          supportedPairs.forEach(([source, target]) => {
            const modelItem = document.createElement('div');
            modelItem.className = 'model-item';
            
            const langNames = {
                'en': 'Inglés',
                'es': 'Español',
                'fr': 'Francés',
                'de': 'Alemán',
                'it': 'Italiano',
                'pt': 'Portugués',
                'ru': 'Ruso',
                'zh': 'Chino',
                'ja': 'Japonés',
                'ko': 'Coreano',
                'ar': 'Árabe',
                'hi': 'Hindi'
            };
            
            const sourceName = langNames[source] || source.toUpperCase();
            const targetName = langNames[target] || target.toUpperCase();
            
            modelItem.innerHTML = `
                <div class="model-info">
                    <span class="model-pair">${sourceName} → ${targetName}</span>
                    <small class="model-code">(${source}-${target})</small>
                </div>
                <button class="delete-model-btn" data-source="${source}" data-target="${target}" title="Eliminar modelo">
                    <span class="delete-icon">🗑️</span>
                </button>
            `;
            
            // Add delete functionality
            const deleteBtn = modelItem.querySelector('.delete-model-btn');
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteModel(source, target);
            });
            
            modelsContainer.appendChild(modelItem);
        });
    }

    updateLanguageOptions(supportedPairs) {
        const languages = {
            'en': 'Inglés',
            'es': 'Español',
            'fr': 'Francés',
            'de': 'Alemán',
            'it': 'Italiano',
            'pt': 'Portugués',
            'ru': 'Ruso',
            'zh': 'Chino',
            'ja': 'Japonés',
            'ko': 'Coreano'
        };

        // Obtener idiomas únicos de los pares soportados
        const availableLanguages = new Set();
        supportedPairs.forEach(([source, target]) => {
            availableLanguages.add(source);
            availableLanguages.add(target);
        });

        // Limpiar opciones actuales
        this.sourceLang.innerHTML = '';
        this.targetLang.innerHTML = '';

        // Agregar opciones disponibles
        availableLanguages.forEach(langCode => {
            const langName = languages[langCode] || langCode.toUpperCase();
            
            const sourceOption = new Option(langName, langCode);
            const targetOption = new Option(langName, langCode);
            
            this.sourceLang.appendChild(sourceOption);
            this.targetLang.appendChild(targetOption);
        });

        // Establecer valores por defecto si están disponibles
        if (availableLanguages.has('en')) {
            this.sourceLang.value = 'en';
        }
        if (availableLanguages.has('es')) {
            this.targetLang.value = 'es';
        }
    }

    updateCharCounter() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = count;
        
        if (count > 900) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 800) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }

    swapLanguages() {
        const sourceValue = this.sourceLang.value;
        const targetValue = this.targetLang.value;
        
        this.sourceLang.value = targetValue;
        this.targetLang.value = sourceValue;
    }

    async sendMessage() {
        const text = this.messageInput.value.trim();
        if (!text) return;

        const sourceLang = this.sourceLang.value;
        const targetLang = this.targetLang.value;

        if (sourceLang === targetLang) {
            this.showError('Por favor selecciona idiomas diferentes para la traducción.');
            return;
        }

        // Mostrar mensaje del usuario
        this.addMessage(text, 'user');
        
        // Limpiar input
        this.messageInput.value = '';
        this.updateCharCounter();
        this.messageInput.style.height = 'auto';

        // Mostrar estado de carga
        this.setLoading(true);

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source: sourceLang,
                    target: targetLang,
                    text: text
                })
            });

            const data = await response.json();

            if (data.success) {
                // Mostrar traducción
                this.addMessage(data.translated_text, 'bot');
            } else {
                this.showError(data.error || 'Error en la traducción');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error de conexión. Verifica que la API esté funcionando.');
        } finally {
            this.setLoading(false);
        }
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('es-ES', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageDiv.innerHTML = `
            <div class="message-content">${this.escapeHtml(content)}</div>
            <div class="message-time">${timeString}</div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();

        // Remover error después de 5 segundos
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    setLoading(loading) {
        if (loading) {
            this.sendButton.classList.add('loading');
            this.sendButton.disabled = true;
        } else {
            this.sendButton.classList.remove('loading');
            this.sendButton.disabled = false;
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateDownloadButton() {
        const source = this.downloadSource.value;
        const target = this.downloadTarget.value;
        
        // Enable button only if both languages are selected and different
        const isValid = source && target && source !== target;
        this.downloadButton.disabled = !isValid;
        
        if (isValid) {
            this.downloadButton.querySelector('.download-text').textContent = `Descargar ${source.toUpperCase()} → ${target.toUpperCase()}`;
        } else {
            this.downloadButton.querySelector('.download-text').textContent = 'Descargar Modelo';
        }
    }

    async downloadModel() {
        const source = this.downloadSource.value;
        const target = this.downloadTarget.value;
        
        if (!source || !target || source === target) {
            this.showDownloadStatus('Por favor selecciona idiomas válidos', 'error');
            return;
        }

        // Show loading state
        this.downloadButton.disabled = true;
        this.downloadButton.querySelector('.download-text').style.display = 'none';
        this.downloadButton.querySelector('.download-spinner').style.display = 'inline';
        this.showDownloadStatus('Descargando modelo... Esto puede tomar varios minutos.', 'info');

        try {
            const response = await fetch('/download_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source: source,
                    target: target
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.showDownloadStatus('¡Modelo descargado exitosamente!', 'success');
                // Reload supported languages to include the new model
                await this.loadSupportedLanguages();
                // Reset download form
                this.downloadSource.value = '';
                this.downloadTarget.value = '';
            } else {
                this.showDownloadStatus(data.message || 'Error al descargar el modelo', 'error');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showDownloadStatus('Error de conexión al descargar el modelo', 'error');
        } finally {
            // Reset button state
            this.downloadButton.disabled = false;
            this.downloadButton.querySelector('.download-text').style.display = 'inline';
            this.downloadButton.querySelector('.download-spinner').style.display = 'none';
            this.updateDownloadButton();
        }
    }

    async deleteModel(source, target) {
        // Show confirmation dialog
        const sourceName = this.getLanguageName(source);
        const targetName = this.getLanguageName(target);
        
        if (!confirm(`¿Estás seguro de que quieres eliminar el modelo ${sourceName} → ${targetName}?\n\nEsta acción no se puede deshacer.`)) {
            return;
        }

        try {
            const response = await fetch('/delete_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source: source,
                    target: target
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.showDownloadStatus(`Modelo ${sourceName} → ${targetName} eliminado exitosamente`, 'success');
                // Reload supported languages to update the models list
                await this.loadSupportedLanguages();
            } else {
                this.showDownloadStatus(data.error || 'Error al eliminar el modelo', 'error');
            }
        } catch (error) {
            console.error('Delete error:', error);
            this.showDownloadStatus('Error de conexión al eliminar el modelo', 'error');
        }
    }

    getLanguageName(code) {
        const langNames = {
            'en': 'Inglés',
            'es': 'Español',
            'fr': 'Francés',
            'de': 'Alemán',
            'it': 'Italiano',
            'pt': 'Portugués',
            'ru': 'Ruso',
            'zh': 'Chino',
            'ja': 'Japonés',
            'ko': 'Coreano',
            'ar': 'Árabe',
            'hi': 'Hindi'
        };
        return langNames[code] || code.toUpperCase();
    }

    showDownloadStatus(message, type) {
        this.downloadStatus.textContent = message;
        this.downloadStatus.className = `download-status ${type}`;
        
        // Clear status after 10 seconds for success/error messages
        if (type !== 'info') {
            setTimeout(() => {
                this.downloadStatus.textContent = '';
                this.downloadStatus.className = 'download-status';
            }, 10000);
        }
    }

    updateDownloadOptions(supportedPairs) {
        const allLanguages = {
            'en': 'Inglés',
            'es': 'Español',
            'fr': 'Francés',
            'de': 'Alemán',
            'it': 'Italiano',
            'pt': 'Portugués',
            'ru': 'Ruso',
            'zh': 'Chino',
            'ja': 'Japonés',
            'ko': 'Coreano',
            'ar': 'Árabe',
            'hi': 'Hindi',
            'nl': 'Holandés',
            'sv': 'Sueco',
            'da': 'Danés',
            'no': 'Noruego',
            'fi': 'Finlandés'
        };

        // Get languages that already have models
        const existingPairs = new Set();
        supportedPairs.forEach(([source, target]) => {
            existingPairs.add(`${source}-${target}`);
        });

        // Clear current options
        this.downloadSource.innerHTML = '<option value="">Seleccionar idioma origen</option>';
        this.downloadTarget.innerHTML = '<option value="">Seleccionar idioma destino</option>';

        // Add all available languages to download dropdowns
        Object.entries(allLanguages).forEach(([code, name]) => {
            const sourceOption = new Option(name, code);
            const targetOption = new Option(name, code);
            
            this.downloadSource.appendChild(sourceOption);
            this.downloadTarget.appendChild(targetOption);
        });
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    new TranslatorChat();
});
