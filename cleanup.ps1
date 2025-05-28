# Script para limpiar y resetear Traductor Chat
Write-Host "🧹 Limpiando contenedores de Traductor Chat..." -ForegroundColor Yellow
Write-Host ""

# Detener y eliminar contenedores
Write-Host "⏹️  Deteniendo contenedores..." -ForegroundColor Blue
docker-compose down --remove-orphans 2>$null

# Eliminar volúmenes
Write-Host "🗑️  Eliminando volúmenes..." -ForegroundColor Blue
docker-compose down -v 2>$null

# Limpiar imágenes no utilizadas
Write-Host "🖼️  Limpiando imágenes no utilizadas..." -ForegroundColor Blue
docker image prune -f 2>$null

Write-Host ""
Write-Host "✅ Limpieza completada." -ForegroundColor Green
Write-Host "Para un reset completo (¡CUIDADO!), ejecuta:" -ForegroundColor Yellow
Write-Host "   docker system prune -a --volumes" -ForegroundColor Red
