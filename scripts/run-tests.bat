@echo off
REM Script para ejecutar tests en Windows
REM Uso: run-tests.bat [opciones]

echo 🧪 Ejecutando Tests - API de Gestión de Restaurante
echo ==================================================

REM Verificar que estamos en el directorio correcto
if not exist "app\main.py" (
    echo ❌ Error: No se encontró app\main.py
    echo 💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto
    pause
    exit /b 1
)

REM Verificar si el entorno virtual está activado
if not defined VIRTUAL_ENV (
    echo ⚠️  Advertencia: No se detectó entorno virtual activado
    echo 💡 Se recomienda activar el entorno virtual antes de ejecutar tests
    echo.
)

REM Ejecutar el runner de tests con los argumentos pasados
python tests\run_tests.py %*

REM Pausar para ver resultados
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Algunos tests fallaron
) else (
    echo.
    echo ✅ Todos los tests pasaron exitosamente
)

pause
