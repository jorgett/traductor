# Traductor Chat - Offline Translation

**Desarrollado por Jorge Toledo**

Una interfaz web moderna para traducción offline usando modelos de Hugging Face.

## 🚀 Inicio Rápido

### Con Docker (Recomendado):
```powershell
# Modo desarrollo (con setup automático)
.\start-development.ps1

# Modo producción (con setup automático)
.\start-production.ps1
```

### Manual:
```bash
pip install -r requirements.txt
python download_model.py --source en --target es
python app.py
```

Luego abre: **http://localhost:5000**

> **💡 Nota:** Los scripts detectan automáticamente si es la primera ejecución y configuran todo lo necesario (.env, modelos, etc.)

## Estructura del Proyecto

```
.
├── app.py                      # API REST con Flask + Interfaz Web
├── translator.py               # Clase Translator para gestión de modelos
├── download_model.py           # Utilidad para descargar modelos
├── config.py                   # Configuración del proyecto
├── requirements.txt            # Dependencias del proyecto
├── Dockerfile                  # Imagen Docker
├── docker-compose.yml          # Orquestación de contenedores
├── pytest.ini                 # Configuración de tests
├── start-production.ps1        # Script inicio producción (con setup automático)
├── start-development.ps1       # Script inicio desarrollo (con setup automático)
├── stop-services.ps1           # Script para detener servicios
├── cleanup.ps1                 # Script limpieza completa
├── check-docker.ps1            # Diagnóstico Docker
├── run-tests.ps1               # Ejecutar todas las pruebas
├── templates/chat.html         # Interfaz de chat
├── static/style.css           # Estilos CSS
├── static/script.js           # JavaScript del chat
├── test/                       # Tests del proyecto
├── data/                       # Directorio de modelos
└── README.md                   # Este archivo
```

## Instalación

### Con Docker (Recomendado)

1. **Verificar Docker (opcional):**
```powershell
.\check-docker.ps1
```

2. **Iniciar aplicación:**
```powershell
# Desarrollo (configuración automática en primera ejecución)
.\start-development.ps1

# Producción (configuración automática en primera ejecución)
.\start-production.ps1
```

### Instalación Manual

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Descargar modelos:**
```bash
python download_model.py --source en --target es
python download_model.py --source es --target en
```

3. **Iniciar la aplicación:**
```bash
python app.py
```

## 💬 Interfaz de Chat

### ✨ Características:
- **🎨 Diseño moderno**: Interfaz elegante y responsiva
- **⚡ Traducción en tiempo real**: Resultados instantáneos
- **🔄 Intercambio de idiomas**: Cambio rápido entre idiomas
- **📱 Compatible con móviles**: Funciona en cualquier dispositivo
- **💬 Historial de chat**: Mantiene todas las traducciones
- **🚫 Funciona offline**: No requiere conexión a internet

### 🚀 Uso:
1. Abre http://localhost:5000
2. Selecciona idiomas de origen y destino
3. Escribe tu texto y presiona "Traducir"
4. ¡Disfruta de la traducción instantánea!

## 🔧 API REST

También puedes usar la API directamente:

```bash
# Traducir texto
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"source": "en", "target": "es", "text": "Hello world!"}'
```

**Endpoints disponibles:**
- `GET /api` - Health check
- `GET /supported_languages` - Idiomas soportados  
- `POST /translate` - Traducir texto
- `POST /translate/batch` - Traducir múltiples textos

## 🐳 Docker

### Scripts de Gestión

```powershell
# Iniciar en desarrollo (setup automático)
.\start-development.ps1

# Iniciar en producción (setup automático)
.\start-production.ps1

# Detener servicios
.\stop-services.ps1

# Limpieza completa
.\cleanup.ps1

# Verificar Docker
.\check-docker.ps1

# Ejecutar tests
.\run-tests.ps1
```

### Comandos Manuales

```bash
# Construir y ejecutar
docker-compose up --build

# En segundo plano
docker-compose up -d --build

# Detener
docker-compose down

# O manualmente
docker build -t traductor-chat .
docker run -p 5000:5000 -v $(pwd)/data:/app/data traductor-chat
```

## 🧪 Testing

### Ejecutar todas las pruebas:
```powershell
.\run-tests.ps1
```

### Comandos manuales:
```bash
# Tests unitarios
pytest -v

# Con cobertura
pytest --cov=. --cov-report=html

# Test específico
pytest test/test_app.py -v
```

Los reportes de cobertura se generan en `htmlcov/index.html`.

## 🌍 Modelos Disponibles

Puedes descargar modelos para diferentes pares de idiomas:

```bash
# Más idiomas disponibles
python download_model.py --source fr --target en  # Francés a Inglés
python download_model.py --source de --target es  # Alemán a Español
python download_model.py --source it --target en  # Italiano a Inglés
```

Ver todos los modelos en: https://huggingface.co/Helsinki-NLP

## 📄 Licencia

Este proyecto utiliza modelos de [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) disponibles bajo licencias abiertas.

---

**© 2025 Jorge Toledo** - Traducción offline simple y efectiva