# Script de configuracion para entorno Conda en Windows
# Ejecutar con: .\setup-conda.ps1

Write-Host "=== Configuracion del entorno Conda para back-dp2 ===" -ForegroundColor Green

# Verificar si Conda esta instalado
$condaExists = Get-Command conda -ErrorAction SilentlyContinue

if (-not $condaExists) {
    Write-Host "X Error: Conda no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host "Instala Miniconda o Anaconda desde: https://docs.conda.io/en/latest/miniconda.html" -ForegroundColor Yellow
    exit 1
}

$condaVersion = conda --version 2>&1
Write-Host "OK Conda detectado: $condaVersion" -ForegroundColor Green

# Crear el entorno desde environment.yml
Write-Host "`nCreando entorno 'back-dp2'..." -ForegroundColor Cyan
conda env create -f environment.yml

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Entorno creado exitosamente" -ForegroundColor Green
    
    Write-Host "`n=== Proximos pasos ===" -ForegroundColor Yellow
    Write-Host "1. Activar el entorno:" -ForegroundColor White
    Write-Host "   conda activate back-dp2" -ForegroundColor Cyan
    Write-Host "`n2. Verificar instalacion:" -ForegroundColor White
    Write-Host "   python --version" -ForegroundColor Cyan
    Write-Host "   pip list" -ForegroundColor Cyan
    Write-Host "`n3. Ejecutar tests:" -ForegroundColor White
    Write-Host "   pytest" -ForegroundColor Cyan
    Write-Host "`n4. Iniciar servidor de desarrollo:" -ForegroundColor White
    Write-Host "   uvicorn src.main:app --reload" -ForegroundColor Cyan
}
else {
    Write-Host "X Error al crear el entorno" -ForegroundColor Red
    Write-Host "Intenta manualmente con: conda env create -f environment.yml" -ForegroundColor Yellow
    exit 1
}
