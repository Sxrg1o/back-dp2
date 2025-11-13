@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-01: Crear Pedido Completo Simple
REM Autor: Adaptado para Windows
REM Equipo: QA/SEG
REM Modulo: Pedidos - Backend
REM ============================================

echo ==========================================
echo   CU-01: Crear Pedido Completo Simple
echo ==========================================
echo.

REM Configuración
if not defined API_URL set API_URL=http://localhost:8000
if not defined VERBOSE set VERBOSE=false

echo API Base URL: %API_URL%
echo Fecha: %DATE% %TIME%
echo.

REM Contadores
set /a TOTAL_TESTS=0
set /a PASSED_TESTS=0
set /a FAILED_TESTS=0

REM Archivos temporales
set TEMP_RESPONSE=%TEMP%\qa_response_%RANDOM%.json
set TEMP_STATUS=%TEMP%\qa_status_%RANDOM%.txt

REM Colores
set "GREEN=[92m"
set "RED=[91m"
set "NC=[0m"

REM ============================================
REM Paso 1: Obtener token de autenticación
REM ============================================
echo === Preparacion: Obtener IDs necesarios ===
echo.

set QA_EMAIL=test@test.com
set QA_PASSWORD=test123

echo Obteniendo token de autenticacion...
curl -s -X POST "%API_URL%/api/v1/auth/login" ^
    -H "Content-Type: application/json" ^
    -d "{\"email\": \"%QA_EMAIL%\", \"password\": \"%QA_PASSWORD%\"}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('access_token', ''))"') do set ACCESS_TOKEN=%%i

if not defined ACCESS_TOKEN (
    echo %RED%ERROR: No se pudo obtener token%NC%
    type "%TEMP_RESPONSE%"
    goto :cleanup
)
echo %GREEN%OK - Token obtenido%NC%

REM ============================================
REM Paso 2: Obtener ID de usuario
REM ============================================
echo Obteniendo ID de usuario...
curl -s "%API_URL%/api/v1/auth/me" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set USER_ID=%%i

if not defined USER_ID (
    echo %RED%ERROR: No se pudo obtener ID de usuario%NC%
    goto :cleanup
)
echo %GREEN%OK - User ID: %USER_ID%%NC%

REM ============================================
REM Paso 3: Obtener ID de mesa
REM ============================================
echo Obteniendo ID de mesa...
curl -s "%API_URL%/api/v1/mesas?limit=1" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i

if not defined MESA_ID (
    echo %RED%ERROR: No se encontraron mesas%NC%
    goto :cleanup
)
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%

REM ============================================
REM Paso 4: Crear sesión de mesa
REM ============================================
echo Creando sesion de mesa...
curl -s -X POST "%API_URL%/api/v1/sesiones-mesas" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_mesa\": \"%MESA_ID%\", \"numero_personas\": 2}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set SESION_ID=%%i

if not defined SESION_ID (
    echo %RED%ERROR: No se pudo crear sesion%NC%
    type "%TEMP_RESPONSE%"
    goto :cleanup
)
echo %GREEN%OK - Sesion ID: %SESION_ID%%NC%

REM ============================================
REM Paso 5: Obtener productos disponibles
REM ============================================
echo Obteniendo productos disponibles...
curl -s "%API_URL%/api/v1/productos-menu?limit=5" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set PRODUCTO_ID=%%i

if not defined PRODUCTO_ID (
    echo %RED%ERROR: No se encontraron productos%NC%
    goto :cleanup
)
echo %GREEN%OK - Producto ID: %PRODUCTO_ID%%NC%

echo.
echo === Ejecutando Tests ===
echo.

REM ============================================
REM TEST 1: Crear pedido simple
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido simple...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 1}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="201" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    REM Guardar ID del pedido creado
    for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set PEDIDO_ID=%%i
    echo Pedido creado con ID: !PEDIDO_ID!
) else (
    echo %RED%X FAIL%NC% - Expected: 201, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
    if "%VERBOSE%"=="true" type "%TEMP_RESPONSE%"
)
echo.

REM ============================================
REM TEST 2: Verificar pedido creado
REM ============================================
if defined PEDIDO_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Verificar pedido creado...
    
    curl -s "%API_URL%/api/v1/pedidos/!PEDIDO_ID!" ^
        -H "Authorization: Bearer %ACCESS_TOKEN%" ^
        -o "%TEMP_RESPONSE%" ^
        -w "%%{http_code}" > "%TEMP_STATUS%"
    
    set /p STATUS_CODE=<"%TEMP_STATUS%"
    
    if "!STATUS_CODE!"=="200" (
        echo %GREEN%OK PASS%NC% - Status: !STATUS_CODE!
        set /a PASSED_TESTS+=1
    ) else (
        echo %RED%X FAIL%NC% - Expected: 200, Got: !STATUS_CODE!
        set /a FAILED_TESTS+=1
    )
    echo.
)

REM ============================================
REM TEST 3: Listar pedidos de la sesión
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Listar pedidos de la sesion...

curl -s "%API_URL%/api/v1/pedidos?id_sesion_mesa=%SESION_ID%" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 200, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM ============================================
REM Resumen
REM ============================================
echo ==========================================
echo   RESUMEN DE TESTS
echo ==========================================
echo Total de tests: !TOTAL_TESTS!
echo Tests pasados: !PASSED_TESTS!
echo Tests fallados: !FAILED_TESTS!
echo ==========================================

if !FAILED_TESTS! GTR 0 (
    echo %RED%Algunos tests fallaron%NC%
    set EXIT_CODE=1
) else (
    echo %GREEN%Todos los tests pasaron%NC%
    set EXIT_CODE=0
)

REM ============================================
REM Limpieza
REM ============================================
:cleanup
if exist "%TEMP_RESPONSE%" del /f /q "%TEMP_RESPONSE%" >nul 2>&1
if exist "%TEMP_STATUS%" del /f /q "%TEMP_STATUS%" >nul 2>&1

echo.
echo Tests completados.
exit /b %EXIT_CODE%
