# Script para iniciar Traductor Chat en modo PRODUCCIÓN
Write-Host "🚀 Iniciando Traductor Chat en modo PRODUCCIÓN..." -ForegroundColor Green
Write-Host ""

# Detectar si es la primera vez (setup automático)
$isFirstTime = -not (Test-Path ".env") -or -not (Test-Path "data") -or (docker images | Select-String "traductor").Count -eq 0

if ($isFirstTime) {
    Write-Host "🔧 Primera ejecución detectada. Configurando proyecto..." -ForegroundColor Cyan
    Write-Host ""
}

# Verificar si Docker está ejecutándose correctamente
Write-Host "🐳 Verificando Docker..." -ForegroundColor Yellow
$dockerRunning = $false
try {
    docker info >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
        Write-Host "✅ Docker está funcionando correctamente" -ForegroundColor Green
    }
} catch {
    $dockerRunning = $false
}

if (-not $dockerRunning) {
    Write-Host "❌ Docker no está ejecutándose correctamente. Por favor:" -ForegroundColor Red
    Write-Host "  1. Cierra Docker Desktop completamente" -ForegroundColor Yellow
    Write-Host "  2. Reinicia tu computadora" -ForegroundColor Yellow
    Write-Host "  3. Inicia Docker Desktop y espera a que esté completamente iniciado" -ForegroundColor Yellow
    Write-Host "  4. Intenta ejecutar este script nuevamente" -ForegroundColor Yellow
    Write-Host "  5. O ejecuta .\check-docker.ps1 para diagnóstico completo" -ForegroundColor Yellow
    exit 1
}

# Verificar/crear archivo .env
Write-Host "📝 Verificando configuración..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Archivo .env creado desde .env.example" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  No hay archivo .env.example, continuando con configuración por defecto." -ForegroundColor Blue
    }
} else {
    Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green
}

# Verificar/crear directorio data
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" -Force >$null
    Write-Host "✅ Directorio 'data' creado" -ForegroundColor Green
} else {
    Write-Host "✅ Directorio 'data' encontrado" -ForegroundColor Green
}

# Verificar modelos si es primera vez
if ($isFirstTime) {
    Write-Host "🤖 Verificando modelos de traducción..." -ForegroundColor Yellow
    $modelsExist = $false
    if (Test-Path "data") {
        $modelDirs = Get-ChildItem -Path "data" -Directory | Where-Object { $_.Name -like "*opus-mt*" }
        if ($modelDirs.Count -gt 0) {
            $modelsExist = $true
            Write-Host "✅ Modelos encontrados:" -ForegroundColor Green
            foreach ($model in $modelDirs) {
                Write-Host "   - $($model.Name)" -ForegroundColor Cyan
            }
        }
    }

    if (-not $modelsExist) {
        Write-Host "⚠️  No se encontraron modelos de traducción" -ForegroundColor Yellow
        Write-Host "📥 Descargando modelos básicos para producción..." -ForegroundColor Blue
        try {
            python download_model.py --source en --target es
            python download_model.py --source es --target en
            Write-Host "✅ Modelos básicos descargados" -ForegroundColor Green
        } catch {
            Write-Host "❌ Error descargando modelos. La aplicación puede no funcionar correctamente." -ForegroundColor Red
            Write-Host "   Ejecuta manualmente: python download_model.py --source en --target es" -ForegroundColor Yellow
        }
    }
}

Write-Host "🐳 Construyendo y ejecutando contenedores en modo producción..." -ForegroundColor Blue

# Limpiar contenedores existentes si hay alguno para evitar conflictos
Write-Host "🧹 Limpiando ambiente previo..." -ForegroundColor Yellow
docker-compose down --volumes 2>$null

# Verificar si hay contenedores antigüos y eliminarlos
Write-Host "🔍 Verificando contenedores antiguos..." -ForegroundColor Yellow
docker ps -a | Where-Object {$_ -match 'traductor-chat|traductor'} | ForEach-Object {
    $containerId = ($_ -split "\s+")[0]
    if ($containerId -match "^[0-9a-f]+$") {
        Write-Host "   Eliminando contenedor $containerId" -ForegroundColor Yellow
        docker rm -f $containerId >$null 2>&1
    }
}

# Verificar si hay imágenes antigüas y eliminarlas
Write-Host "🔍 Verificando imágenes antiguas..." -ForegroundColor Yellow
docker images | Where-Object {$_ -match 'traductor-chat|traductor'} | ForEach-Object {
    $imageId = ($_ -split "\s+")[2]
    if ($imageId -match "^[0-9a-f]+$") {
        Write-Host "   Eliminando imagen $imageId" -ForegroundColor Yellow
        docker rmi -f $imageId >$null 2>&1
    }
}

# Construir imágenes explícitamente primero
Write-Host "🏗️ Construyendo imágenes..." -ForegroundColor Yellow
docker-compose build --no-cache

# Si la construcción fue exitosa, mostrar información y luego iniciar los contenedores
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 Traductor Chat está ejecutándose en modo producción:" -ForegroundColor Green
    Write-Host "   Aplicación: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "   API Health: http://localhost:5000/api" -ForegroundColor Cyan
    Write-Host "   API Translate: http://localhost:5000/translate" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Iniciando contenedores... Presiona Ctrl+C para detener." -ForegroundColor Yellow
    docker-compose up
} else {
    Write-Host "❌ Error al construir contenedores. Por favor revisa los logs anteriores." -ForegroundColor Red
    exit 1
}
