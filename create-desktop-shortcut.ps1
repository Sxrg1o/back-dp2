# Script para crear acceso directo en el escritorio
# Ejecutar una vez: .\create-desktop-shortcut.ps1

Write-Host "Creando acceso directo en el escritorio..." -ForegroundColor Cyan

# Buscar Conda
$condaPaths = @(
    "$env:USERPROFILE\miniconda3",
    "$env:USERPROFILE\anaconda3",
    "C:\ProgramData\miniconda3",
    "C:\ProgramData\anaconda3"
)

$condaRoot = $null
foreach ($path in $condaPaths) {
    if (Test-Path "$path\Scripts\activate.bat") {
        $condaRoot = $path
        break
    }
}

if (-not $condaRoot) {
    Write-Host "ERROR: No se encontro Conda" -ForegroundColor Red
    exit 1
}

# Crear acceso directo
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktop\Back-DP2 Conda.lnk"
$projectPath = $PSScriptRoot

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/K `"$condaRoot\Scripts\activate.bat`" `"$condaRoot`" && cd /D `"$projectPath`" && conda activate back-dp2"
$Shortcut.WorkingDirectory = $projectPath
$Shortcut.Description = "Abre Anaconda Prompt en el proyecto Back-DP2"
$Shortcut.Save()

Write-Host "OK Acceso directo creado: $shortcutPath" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes hacer doble clic en 'Back-DP2 Conda' en tu escritorio" -ForegroundColor Yellow
Write-Host "para abrir el entorno directamente." -ForegroundColor Yellow
