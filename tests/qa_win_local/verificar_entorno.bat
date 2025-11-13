@echo off
setlocal

REM ============================================
REM Verificar Entorno para Tests de QA
REM ============================================

echo.
echo ==========================================
echo   VERIFICACION DE ENTORNO
echo ==========================================
echo.

set /a CHECKS_PASSED=0
set /a CHECKS_FAILED=0

REM Check 1: Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [91m  X Python NO esta instalado[0m
    echo      Descarga desde: https://www.python.org/
    set /a CHECKS_FAILED+=1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [92m  OK !PYTHON_VERSION![0m
    set /a CHECKS_PASSED+=1
)

REM Check 2: Verificar curl
echo [2/5] Verificando curl...
curl --version >nul 2>&1
if errorlevel 1 (
    echo [91m  X curl NO esta instalado[0m
    echo      Viene incluido en Windows 10+ o descarga desde: https://curl.se/windows/
    set /a CHECKS_FAILED+=1
) else (
    for /f "tokens=1,2" %%i in ('curl --version ^| findstr /C:"curl"') do set CURL_VERSION=%%i %%j
    echo [92m  OK !CURL_VERSION![0m
    set /a CHECKS_PASSED+=1
)

REM Check 3: Verificar servidor backend
echo [3/5] Verificando servidor backend...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/docs > %TEMP%\status.txt 2>nul
set /p SERVER_STATUS=<%TEMP%\status.txt
del %TEMP%\status.txt >nul 2>&1

if "%SERVER_STATUS%"=="200" (
    echo [92m  OK Servidor respondiendo en http://localhost:8000[0m
    set /a CHECKS_PASSED+=1
) else (
    echo [91m  X Servidor NO esta respondiendo en http://localhost:8000[0m
    echo      Inicia el servidor con:
    echo        cd e:\PROYECTOS\DP2\V8\back-dp2
    echo        venv\Scripts\activate
    echo        python src\main.py
    set /a CHECKS_FAILED+=1
)

REM Check 4: Verificar credenciales de prueba
echo [4/5] Verificando credenciales de prueba...
curl -s -X POST "http://localhost:8000/api/v1/auth/login" ^
    -H "Content-Type: application/json" ^
    -d "{\"email\": \"test@test.com\", \"password\": \"test123\"}" ^
    -o %TEMP%\login_test.json 2>nul

python -c "import json; f=open(r'%TEMP%\login_test.json'); data=json.load(f); print('OK' if data.get('access_token') else 'FAIL')" > %TEMP%\login_status.txt 2>nul
set /p LOGIN_STATUS=<%TEMP%\login_status.txt
del %TEMP%\login_test.json >nul 2>&1
del %TEMP%\login_status.txt >nul 2>&1

if "%LOGIN_STATUS%"=="OK" (
    echo [92m  OK Credenciales de prueba funcionando[0m
    set /a CHECKS_PASSED+=1
) else (
    echo [91m  X Credenciales de prueba NO funcionan[0m
    echo      Usuario: test@test.com / Contrasena: test123
    echo      Ejecuta el script de seed si es necesario
    set /a CHECKS_FAILED+=1
)

REM Check 5: Verificar datos de prueba (mesas)
echo [5/5] Verificando datos de prueba...
curl -s "http://localhost:8000/api/v1/mesas?limit=1" -o %TEMP%\mesas_test.json 2>nul
python -c "import json; f=open(r'%TEMP%\mesas_test.json'); data=json.load(f); print('OK' if data.get('items') and len(data['items']) > 0 else 'FAIL')" > %TEMP%\mesas_status.txt 2>nul
set /p MESAS_STATUS=<%TEMP%\mesas_status.txt
del %TEMP%\mesas_test.json >nul 2>&1
del %TEMP%\mesas_status.txt >nul 2>&1

if "%MESAS_STATUS%"=="OK" (
    echo [92m  OK Datos de prueba disponibles[0m
    set /a CHECKS_PASSED+=1
) else (
    echo [91m  X Datos de prueba NO disponibles[0m
    echo      Ejecuta: python scripts\seed_cevicheria_data.py
    set /a CHECKS_FAILED+=1
)

echo.
echo ==========================================
echo   RESUMEN
echo ==========================================
echo Verificaciones pasadas: %CHECKS_PASSED%/5
echo Verificaciones fallidas: %CHECKS_FAILED%/5
echo ==========================================
echo.

if %CHECKS_FAILED% GTR 0 (
    echo [91mEl entorno NO esta listo para ejecutar tests[0m
    echo [93mCorrige los errores indicados arriba[0m
    exit /b 1
) else (
    echo [92mEl entorno esta listo para ejecutar tests![0m
    echo.
    echo Ejecuta los tests con:
    echo   run_all_tests.bat
    echo.
    echo O tests individuales:
    echo   test_cu01_crear_pedido_simple.bat
    echo   test_cu02_crear_pedido_con_opciones.bat
    echo   test_cu03_listar_pedidos.bat
    exit /b 0
)
