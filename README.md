# Traductor Chat - Offline Translation

**Desarrollado por Jorge Toledo**

Una interfaz web moderna para traducción offline usando modelos de Hugging Face.

## 🚀 Inicio Rápido

### Windows:
```bash
start.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

Luego abre: **http://localhost:5000**

## Estructura del Proyecto

```
.
├── app.py                      # API REST con Flask + Interfaz Web
├── translator.py               # Clase Translator para gestión de modelos
├── download_model.py           # Utilidad para descargar modelos
├── config.py                   # Configuración del proyecto
├── requirements.txt            # Dependencias del proyecto
├── start.bat / start.sh        # Scripts de inicio automático
├── Dockerfile                  # Imagen Docker
├── docker-compose.yml          # Orquestación de contenedores
├── templates/chat.html         # Interfaz de chat
├── static/style.css           # Estilos CSS
├── static/script.js           # JavaScript del chat
├── data/                       # Directorio de modelos
└── README.md                   # Este archivo
```

## Instalación

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
start.bat  # Windows
./start.sh # Linux/Mac
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

```bash
# Construir y ejecutar
docker-compose up --build

# O manualmente
docker build -t traductor-chat .
docker run -p 5000:5000 -v $(pwd)/data:/app/data traductor-chat
```

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