@echo off
echo 🍽️ Iniciando Microservicio de Menú y Carta...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

REM Verificar si el entorno virtual existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
if not exist "venv\Lib\site-packages\fastapi" (
    echo 📥 Instalando dependencias...
    pip install -r requirements.txt
)

REM Crear base de datos si no existe
if not exist "menu.db" (
    echo 🗄️ Inicializando base de datos...
    python -c "from infrastructure.db import create_tables; create_tables()"
)

REM Mostrar información
echo.
echo ✅ Configuración completada
echo 🚀 Iniciando servidor...
echo.
echo 📚 Documentación: http://localhost:8002/docs
echo 🔍 Health Check: http://localhost:8002/health
echo 🛑 Para detener: Ctrl+C
echo.

REM Iniciar el servidor
python main.py

pause
