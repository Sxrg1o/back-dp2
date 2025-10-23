@echo off
REM Script para configurar entorno Conda sin necesidad de PATH
REM Ejecutar con: setup-conda.bat

echo === Buscando instalacion de Conda ===

REM Buscar Conda en ubicaciones comunes
set "CONDA_PATHS=%USERPROFILE%\miniconda3 %USERPROFILE%\anaconda3 C:\ProgramData\miniconda3 C:\ProgramData\anaconda3 %LOCALAPPDATA%\miniconda3 %LOCALAPPDATA%\anaconda3"

set "CONDA_EXE="
for %%P in (%CONDA_PATHS%) do (
    if exist "%%P\Scripts\conda.exe" (
        set "CONDA_EXE=%%P\Scripts\conda.exe"
        set "CONDA_ROOT=%%P"
        goto :found
    )
)

:notfound
echo [ERROR] No se encontro instalacion de Conda
echo.
echo Busque manualmente Anaconda Prompt en el menu de inicio
echo y ejecute desde ahi: cd %~dp0 ^& .\setup-conda.ps1
echo.
pause
exit /b 1

:found
echo [OK] Conda encontrado en: %CONDA_ROOT%
echo.

REM Inicializar Conda para esta sesion
call "%CONDA_ROOT%\Scripts\activate.bat" "%CONDA_ROOT%"

REM Verificar version
echo Verificando version...
call conda --version
echo.

REM Crear entorno
echo Creando entorno 'back-dp2'...
call conda env create -f environment.yml

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Entorno creado exitosamente
    echo.
    echo === Proximos pasos ===
    echo 1. Abre 'Anaconda Prompt' desde el menu de inicio
    echo 2. Navega al proyecto: cd %~dp0
    echo 3. Activa el entorno: conda activate back-dp2
    echo 4. Ejecuta tests: pytest
    echo 5. Inicia servidor: uvicorn src.main:app --reload
) else (
    echo.
    echo [ERROR] Hubo un problema al crear el entorno
    echo Intenta manualmente desde Anaconda Prompt:
    echo   conda env create -f environment.yml
)

echo.
pause
