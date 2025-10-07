# Script de instalación para Windows
Write-Host "Instalando dependencias para Windows..." -ForegroundColor Green
Write-Host ""

# Activar el entorno virtual
& ".\venv\Scripts\Activate.ps1"

# Instalar dependencias específicas para Windows
pip install -r requirements-windows.txt

Write-Host ""
Write-Host "Instalación completada para Windows!" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "  uvicorn src.main:app --reload" -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para continuar"
