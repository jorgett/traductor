#!/bin/bash

# Traductor Chat - Inicio automático (Linux/Mac)
# Desarrollado por Jorge Toledo

echo "=========================================="
echo "  Traductor Chat - Offline Translation"
echo "  Desarrollado por Jorge Toledo"
echo "=========================================="
echo ""

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "ERROR: Python no esta instalado. Por favor instala Python 3.11+ primero."
    exit 1
fi

# Verificar si las dependencias están instaladas
if ! python -c "import flask, transformers, torch" &> /dev/null; then
    echo "INFO: Instalando dependencias..."
    pip install -r requirements.txt
fi

# Verificar si hay modelos descargados
if [ ! -d "data/opus-mt-en-es" ] || [ ! -d "data/opus-mt-es-en" ]; then
    echo "INFO: Descargando modelos de traduccion..."
    python download_model.py --source en --target es
    python download_model.py --source es --target en
fi

echo "=========================================="
echo "  Iniciando servidor..."
echo "  Chat: http://localhost:5000"
echo "  API:  http://localhost:5000/api"
echo "=========================================="
echo "Para detener el servidor, presiona Ctrl+C"
echo ""

# Iniciar la aplicación
python app.py
