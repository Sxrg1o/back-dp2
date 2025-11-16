@echo off
REM Script para ejecutar tests QA en ambiente local (Windows)
REM Uso: run_tests_local.bat [puerto]
REM Ejemplo: run_tests_local.bat 8001
REM
REM IMPORTANTE: Asegúrate de tener el servidor corriendo en otra terminal:
REM   python -m uvicorn src.main:app --reload

setlocal enabledelayedexpansion

REM Configuración
set DEFAULT_PORT=8000

REM Argumentos
if "%1"=="" (
    set PORT=%DEFAULT_PORT%
) else (
    set PORT=%1
)

set API_URL=http://localhost:%PORT%

echo.
echo ==========================================
echo   Ejecutor de Tests QA - Ambiente Local
echo ==========================================
echo.
echo Configuración:
echo   URL API: %API_URL%
echo   Puerto: %PORT%
echo.
echo IMPORTANTE: Asegúrate de que el servidor está corriendo.
echo   Terminal 1: python -m uvicorn src.main:app --reload
echo.

REM Verificar que curl está disponible (necesario para los tests)
where curl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ADVERTENCIA] curl no está instalado en PATH
    echo Los tests requieren curl. Instala Git for Windows o WSL.
    echo.
)

REM Verificar que python está disponible
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Obtener el directorio actual (debería ser back-dp2)
cd /d %~dp0..\..\..\back-dp2 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No se pudo navegar al directorio del proyecto
    cd /d ..\..
)

echo.
echo Ejecutando tests...
echo.

REM Usar PowerShell para ejecutar bash con variables de entorno
powershell -NoProfile -Command "$ErrorActionPreference='Continue'; $env:API_URL='%API_URL%'; bash tests/qa/test_cu05_validaciones_errores.sh; exit $LASTEXITCODE"

set TEST_RESULT=%ERRORLEVEL%

echo.
if %TEST_RESULT% EQU 0 (
    echo [OK] Todos los tests pasaron ✓
) else (
    if %TEST_RESULT% EQU 1 (
        echo [FALLO] Algunos tests fallaron
    ) else (
        echo [ERROR] Código de error: %TEST_RESULT%
    )
    echo.
    echo Opciones:
    echo   1. Usa Python (más confiable): python tests/qa/run_tests_local.py --port %PORT%
    echo   2. Asegúrate de tener curl en PATH (Git Bash o WSL)
    echo   3. Verifica que el servidor esté corriendo
echo.
)

pause
exit /b %TEST_RESULT%
