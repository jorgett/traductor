# Script para ejecutar todas las pruebas del proyecto Traductor Chat

Write-Host "🧪 Ejecutando todas las pruebas de Traductor Chat..." -ForegroundColor Cyan

# Verificar que Python está disponible
Write-Host "`n🐍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "   Instala Python desde: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Verificar si hay un entorno virtual y activarlo
Write-Host "`n📦 Verificando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✅ Entorno virtual encontrado, activando..." -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  No se encontró entorno virtual. Instalando dependencias globalmente..." -ForegroundColor Yellow
    # Instalar dependencias si es necesario
    pip install -r requirements.txt
}

# Ejecutar tests con pytest
Write-Host "`n🧪 Ejecutando pytest..." -ForegroundColor Blue
pytest -v --cov=. --cov-report=html --cov-report=term-missing

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Fallos en las pruebas" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Todas las pruebas completadas exitosamente!" -ForegroundColor Green

# Test de integración con Docker (opcional)
$runDocker = Read-Host "`n🐳 ¿Ejecutar test de integración con Docker? (y/N)"
if ($runDocker -eq "y" -or $runDocker -eq "Y") {
    Write-Host "`n🚀 Iniciando servicios con Docker..." -ForegroundColor Yellow
    
    # Construir y ejecutar en segundo plano
    docker-compose up -d --build
    
    # Esperar a que el servicio esté listo
    Write-Host "⏳ Esperando a que el servicio esté listo..." -ForegroundColor Blue
    $maxAttempts = 30
    $attempt = 0
    
    do {
        Start-Sleep -Seconds 2
        $attempt++
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5000/api" -TimeoutSec 5 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Servicio está funcionando" -ForegroundColor Green
                break
            }
        } catch {
            Write-Host "." -NoNewline -ForegroundColor Yellow
        }
    } while ($attempt -lt $maxAttempts)
    
    if ($attempt -ge $maxAttempts) {
        Write-Host "`n❌ El servicio no respondió en tiempo esperado" -ForegroundColor Red
        docker-compose down
        exit 1
    }
    
    # Test básico de la API
    Write-Host "`n🧪 Probando API de traducción..." -ForegroundColor Blue
    try {
        $testPayload = @{
            source = "en"
            target = "es"
            text = "Hello world"
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "http://localhost:5000/translate" -Method POST -Body $testPayload -ContentType "application/json"
        
        if ($response.translated_text) {
            Write-Host "✅ API de traducción funciona correctamente" -ForegroundColor Green
            Write-Host "   Traducción: '$($response.translated_text)'" -ForegroundColor Cyan
        } else {
            Write-Host "❌ La API no devolvió una traducción válida" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error al probar la API: $_" -ForegroundColor Red
    }
    
    Write-Host "`n🛑 Deteniendo servicios..." -ForegroundColor Yellow
    docker-compose down
}

Write-Host "`n🎉 Tests completados!" -ForegroundColor Green
if (Test-Path "htmlcov") {
    Write-Host "📊 Reporte de cobertura disponible en: htmlcov/index.html" -ForegroundColor Cyan
}
