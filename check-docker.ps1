# Herramienta de diagnóstico para Docker
Write-Host "🔍 Iniciando diagnóstico de Docker..." -ForegroundColor Cyan
Write-Host ""

# 1. Comprobar si Docker está instalado
Write-Host "1️⃣ Comprobando instalación de Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker instalado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# 2. Comprobar si Docker está en ejecución
Write-Host ""
Write-Host "2️⃣ Comprobando si Docker está en ejecución..." -ForegroundColor Yellow
try {
    docker info >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker está ejecutándose correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker está instalado pero no se está ejecutando" -ForegroundColor Red
        Write-Host "   Inicia Docker Desktop y espera a que se inicialice completamente" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error al comprobar el estado de Docker" -ForegroundColor Red
    Write-Host "   Mensaje de error: $_" -ForegroundColor Red
    exit 1
}

# 3. Comprobar conectividad del daemon Docker
Write-Host ""
Write-Host "3️⃣ Comprobando conectividad del daemon Docker..." -ForegroundColor Yellow
try {
    docker ps >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ El daemon de Docker responde correctamente" -ForegroundColor Green
    } else {
        Write-Host "❌ El daemon de Docker no responde correctamente" -ForegroundColor Red
        Write-Host "   Reinicia Docker Desktop" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error al conectar con el daemon de Docker" -ForegroundColor Red
    Write-Host "   Mensaje de error: $_" -ForegroundColor Red
    exit 1
}

# 4. Comprobar si docker-compose está disponible
Write-Host ""
Write-Host "4️⃣ Comprobando disponibilidad de docker-compose..." -ForegroundColor Yellow
try {
    $dockerComposeVersion = docker-compose --version
    Write-Host "✅ docker-compose disponible: $dockerComposeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ docker-compose no está disponible" -ForegroundColor Red
    Write-Host "   Asegúrate de que Docker Desktop está actualizado" -ForegroundColor Red
    exit 1
}

# 5. Comprobar espacio disponible
Write-Host ""
Write-Host "5️⃣ Comprobando espacio disponible..." -ForegroundColor Yellow
$drive = Get-PSDrive C
$freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
if ($freeSpaceGB -lt 5) {
    Write-Host "⚠️ Poco espacio disponible en disco: $freeSpaceGB GB" -ForegroundColor Yellow
    Write-Host "   Se recomiendan al menos 5 GB libres para Docker" -ForegroundColor Yellow
} else {
    Write-Host "✅ Espacio disponible suficiente: $freeSpaceGB GB" -ForegroundColor Green
}

# Resultado final
Write-Host ""
Write-Host "✅ Diagnóstico completado: Docker está listo para usar" -ForegroundColor Green
Write-Host "   Ahora puedes ejecutar ./start-development.ps1 para iniciar la aplicación" -ForegroundColor Cyan
