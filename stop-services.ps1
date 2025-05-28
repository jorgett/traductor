# Script para parar los servicios de Traductor Chat
Write-Host "⏹️  Parando servicios de Traductor Chat..." -ForegroundColor Yellow
Write-Host ""

# Parar contenedores
Write-Host "🔄 Parando contenedores..." -ForegroundColor Blue
docker-compose down --remove-orphans 2>$null

Write-Host ""
Write-Host "✅ Servicios detenidos." -ForegroundColor Green
Write-Host ""
Write-Host "💡 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   .\start-development.ps1  # Reiniciar en desarrollo" -ForegroundColor Gray
Write-Host "   .\start-production.ps1   # Reiniciar en producción" -ForegroundColor Gray
Write-Host "   .\cleanup.ps1           # Reset completo" -ForegroundColor Gray
