@echo off
echo ===========================================
echo     USERS MICRO SERVICE - Ejecutar
echo ===========================================
echo.

REM Verificar si Docker esta disponible
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Docker no esta disponible. Ejecutando con Python...
    goto :python_mode
)

REM Mostrar opciones al usuario
echo Selecciona una opcion:
echo 1. Ejecutar con Docker Compose (recomendado)
echo 2. Ejecutar directamente con Python
echo 3. Salir
echo.
set /p choice="Ingresa tu eleccion (1-3): "

if "%choice%"=="1" goto :docker_mode
if "%choice%"=="2" goto :python_mode
if "%choice%"=="3" goto :exit

echo Opcion invalida. Ejecutando con Docker por defecto...
goto :docker_mode

:docker_mode
echo.
echo [INFO] Ejecutando users-ms con Docker Compose...
echo [INFO] Puerto: 8501
echo [INFO] Presiona Ctrl+C para detener
echo.
cd /d "%~dp0"
docker-compose up users --build
goto :end

:python_mode
echo.
echo [INFO] Ejecutando users-ms con Python...
echo [INFO] Puerto: 8002 (por defecto)
echo.

REM Cambiar al directorio del microservicio
cd /d "%~dp0users-ms"

REM Verificar si existe entorno virtual
if exist venv (
    echo [INFO] Activando entorno virtual existente...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat

    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
)

echo [INFO] Iniciando servidor...
echo [INFO] Presiona Ctrl+C para detener
echo.
python main.py
goto :end

:exit
echo.
echo [INFO] Saliendo...
goto :end

:end
echo.
echo ===========================================
pause
