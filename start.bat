@echo off
chcp 65001 >nul
REM Traductor Chat - Inicio automático (Windows)
REM Desarrollado por Jorge Toledo

echo ==========================================
echo  Traductor Chat - Offline Translation
echo  Desarrollado por Jorge Toledo
echo ==========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado. Por favor instala Python 3.11+ primero.
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
python -c "import flask, transformers, torch" >nul 2>&1
if errorlevel 1 (
    echo INFO: Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar si hay modelos descargados
if not exist "data\opus-mt-en-es" (
    echo INFO: Descargando modelos de traduccion...
    python download_model.py --source en --target es
)

if not exist "data\opus-mt-es-en" (
    echo INFO: Descargando modelos de traduccion...
    python download_model.py --source es --target en
)

echo ==========================================
echo  Iniciando servidor...
echo  Chat: http://localhost:5000
echo  API:  http://localhost:5000/api
echo ==========================================
echo Para detener el servidor, presiona Ctrl+C
echo.

REM Iniciar la aplicación
python app.py

pause
