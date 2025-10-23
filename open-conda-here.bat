@echo off
REM Abre Anaconda Prompt en este directorio con el entorno activado
REM Doble clic en este archivo para trabajar rapidamente

REM Buscar Conda
set "CONDA_PATHS=%USERPROFILE%\miniconda3 %USERPROFILE%\anaconda3 C:\ProgramData\miniconda3 C:\ProgramData\anaconda3"

set "CONDA_ROOT="
for %%P in (%CONDA_PATHS%) do (
    if exist "%%P\Scripts\activate.bat" (
        set "CONDA_ROOT=%%P"
        goto :found
    )
)

:notfound
echo [ERROR] No se encontro Conda
pause
exit /b 1

:found
REM Iniciar nueva ventana de CMD con Conda activado
start "Back-DP2 Conda" cmd /K ""%CONDA_ROOT%\Scripts\activate.bat" "%CONDA_ROOT%" && cd /D "%~dp0" && conda activate back-dp2 && echo Entorno 'back-dp2' activado && echo. && echo Comandos utiles: && echo   pytest           - Ejecutar tests && echo   pytest --cov=src - Tests con cobertura && echo   uvicorn src.main:app --reload - Iniciar servidor && echo."
