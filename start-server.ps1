# start-server.ps1 - Iniciar servidor Fresh Bowl
# Ejecutar desde la carpeta raíz del proyecto

Write-Host "🥗 Fresh Bowl - Iniciando servidor..." -ForegroundColor Green
Write-Host ""

# Verificar MongoDB
Write-Host "📦 Verificando MongoDB..." -ForegroundColor Yellow
try {
    $mongoCheck = Get-Service -Name "MongoDB" -ErrorAction SilentlyContinue
    if ($mongoCheck -and $mongoCheck.Status -ne "Running") {
        Write-Host "⚠️  MongoDB no está corriendo. Intentando iniciar..." -ForegroundColor Yellow
        Start-Service MongoDB
    }
} catch {
    Write-Host "⚠️  No se detectó MongoDB como servicio. Asegúrate de que esté corriendo." -ForegroundColor Yellow
}

# Ir a carpeta BackEnd
$backendPath = Join-Path $PSScriptRoot "BackEnd"
Set-Location $backendPath

Write-Host ""
Write-Host "🚀 Iniciando servidor FastAPI en http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "📚 Documentación API: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Gray
Write-Host ""

# Iniciar servidor
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
