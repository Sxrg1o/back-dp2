@echo off
echo 🚀 Iniciando todos los microservicios de Domótica...
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está en el PATH
    echo Por favor instala Docker Desktop desde https://docker.com
    pause
    exit /b 1
)

REM Verificar si Docker Compose está disponible
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está disponible
    echo Por favor instala Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker y Docker Compose están disponibles
echo.

REM Mostrar información de los servicios
echo 📋 Servicios que se van a iniciar:
echo    👤 Users MS    - http://localhost:8001
echo    🍽️ Menu MS     - http://localhost:8002
echo.

REM Preguntar si continuar
set /p choice="¿Continuar? (s/n): "
if /i "%choice%" neq "s" (
    echo Operación cancelada
    pause
    exit /b 0
)

echo.
echo 🔧 Construyendo imágenes...
docker-compose build

echo.
echo 🚀 Iniciando servicios...
docker-compose up -d

echo.
echo ✅ Servicios iniciados correctamente!
echo.
echo 📚 Documentación disponible en:
echo    👤 Users MS:  http://localhost:8001/docs
echo    🍽️ Menu MS:   http://localhost:8002/docs
echo.
echo 🔍 Health Checks:
echo    👤 Users MS:  http://localhost:8001/health
echo    🍽️ Menu MS:   http://localhost:8002/health
echo.
echo 🛠️ Comandos útiles:
echo    Ver logs:     docker-compose logs -f
echo    Detener:      docker-compose down
echo    Reiniciar:    docker-compose restart
echo    Estado:       docker-compose ps
echo.

REM Mostrar estado de los servicios
echo 📊 Estado de los servicios:
docker-compose ps

echo.
echo Presiona cualquier tecla para ver los logs en tiempo real...
pause >nul

REM Mostrar logs
docker-compose logs -f

