@echo off
REM Script para iniciar la aplicación con Docker en Windows

echo 🐳 Iniciando Menu API con Docker...

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado. Por favor instala Docker Desktop primero.
    pause
    exit /b 1
)

REM Verificar si Docker Compose está instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está instalado. Por favor instala Docker Compose primero.
    pause
    exit /b 1
)

REM Procesar argumentos
if "%1"=="dev" (
    echo 🚀 Iniciando en modo desarrollo...
    docker-compose up --build
) else if "%1"=="prod" (
    echo 🚀 Iniciando en modo producción...
    docker-compose -f docker-compose.prod.yml up --build -d
    echo ✅ Aplicación iniciada en http://localhost:8000
    echo 📚 Documentación disponible en http://localhost:8000/docs
) else if "%1"=="build" (
    echo 🔨 Construyendo imagen Docker...
    docker-compose build
) else if "%1"=="stop" (
    echo 🛑 Deteniendo contenedores...
    docker-compose down
) else if "%1"=="logs" (
    echo 📋 Mostrando logs...
    docker-compose logs -f
) else if "%1"=="clean" (
    echo 🧹 Limpiando contenedores e imágenes...
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
    echo ✅ Limpieza completada
) else if "%1"=="help" (
    echo Uso: %0 [opción]
    echo.
    echo Opciones:
    echo   dev     Iniciar en modo desarrollo (con hot reload)
    echo   prod    Iniciar en modo producción
    echo   build   Construir la imagen Docker
    echo   stop    Detener los contenedores
    echo   logs    Mostrar logs de los contenedores
    echo   clean   Limpiar contenedores e imágenes
    echo   help    Mostrar esta ayuda
) else (
    echo 🚀 Iniciando en modo desarrollo (por defecto)...
    docker-compose up --build
)

pause
