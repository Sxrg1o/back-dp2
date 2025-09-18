@echo off
echo 🛑 Deteniendo todos los microservicios de Domótica...
echo.

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo 🔍 Verificando servicios activos...
docker-compose ps

echo.
set /p choice="¿Detener todos los servicios? (s/n): "
if /i "%choice%" neq "s" (
    echo Operación cancelada
    pause
    exit /b 0
)

echo.
echo 🛑 Deteniendo servicios...
docker-compose down

echo.
echo 🧹 Limpiando contenedores y volúmenes...
docker-compose down -v

echo.
echo ✅ Todos los servicios han sido detenidos
echo 🗑️ Volúmenes eliminados
echo.

pause
