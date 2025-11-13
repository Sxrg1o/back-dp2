@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-02: Crear Pedido con Opciones
REM Autor: Adaptado para Windows
REM Equipo: QA/SEG
REM Modulo: Pedidos - Backend
REM ============================================

echo ==========================================
echo   CU-02: Crear Pedido con Opciones
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
    goto :cleanup
)
echo %GREEN%OK - Token obtenido%NC%

REM ============================================
REM Paso 2: Obtener ID de mesa y crear sesión
REM ============================================
echo Obteniendo ID de mesa...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i

if not defined MESA_ID (
    echo %RED%ERROR: No se encontraron mesas%NC%
    goto :cleanup
)
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%

echo Creando sesion de mesa...
curl -s -X POST "%API_URL%/api/v1/sesiones-mesas" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_mesa\": \"%MESA_ID%\", \"numero_personas\": 2}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set SESION_ID=%%i

if not defined SESION_ID (
    echo %RED%ERROR: No se pudo crear sesion%NC%
    goto :cleanup
)
echo %GREEN%OK - Sesion ID: %SESION_ID%%NC%

REM ============================================
REM Paso 3: Obtener producto con opciones
REM ============================================
echo Buscando producto con opciones disponibles...
curl -s "%API_URL%/api/v1/productos-menu?limit=20" -o "%TEMP_RESPONSE%"

REM Buscar producto con opciones usando Python
python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); items=data.get('items',[]); prod=[p for p in items if p.get('opciones')]; print(prod[0]['id'] if prod else '')" > "%TEMP_STATUS%"
set /p PRODUCTO_ID=<"%TEMP_STATUS%"

if not defined PRODUCTO_ID (
    echo %RED%ERROR: No se encontro producto con opciones%NC%
    goto :cleanup
)
echo %GREEN%OK - Producto ID: %PRODUCTO_ID%%NC%

REM Obtener ID de opción
python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); items=data.get('items',[]); prod=[p for p in items if p.get('id')=='%PRODUCTO_ID%']; print(prod[0]['opciones'][0]['id'] if prod and prod[0].get('opciones') else '')" > "%TEMP_STATUS%"
set /p OPCION_ID=<"%TEMP_STATUS%"

if not defined OPCION_ID (
    echo %RED%ERROR: No se encontro opcion para el producto%NC%
    goto :cleanup
)
echo %GREEN%OK - Opcion ID: %OPCION_ID%%NC%

echo.
echo === Ejecutando Tests ===
echo.

REM ============================================
REM TEST 1: Crear pedido con opciones
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido con opciones...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 1, \"opciones_seleccionadas\": [\"%OPCION_ID%\"]}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="201" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set PEDIDO_ID=%%i
    echo Pedido creado con ID: !PEDIDO_ID!
) else (
    echo %RED%X FAIL%NC% - Expected: 201, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
    if "%VERBOSE%"=="true" type "%TEMP_RESPONSE%"
)
echo.

REM ============================================
REM TEST 2: Verificar opciones en el pedido
REM ============================================
if defined PEDIDO_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Verificar opciones en el pedido...
    
    curl -s "%API_URL%/api/v1/pedidos/!PEDIDO_ID!" ^
        -H "Authorization: Bearer %ACCESS_TOKEN%" ^
        -o "%TEMP_RESPONSE%" ^
        -w "%%{http_code}" > "%TEMP_STATUS%"
    
    set /p STATUS_CODE=<"%TEMP_STATUS%"
    
    if "!STATUS_CODE!"=="200" (
        REM Verificar que el pedido tenga opciones
        python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print('OK' if any(prod.get('opciones_seleccionadas') for prod in data.get('productos',[])) else 'FAIL')" > "%TEMP_STATUS%"
        set /p VALIDATION=<"%TEMP_STATUS%"
        
        if "!VALIDATION!"=="OK" (
            echo %GREEN%OK PASS%NC% - Pedido contiene opciones
            set /a PASSED_TESTS+=1
        ) else (
            echo %RED%X FAIL%NC% - Pedido no contiene opciones
            set /a FAILED_TESTS+=1
        )
    ) else (
        echo %RED%X FAIL%NC% - Expected: 200, Got: !STATUS_CODE!
        set /a FAILED_TESTS+=1
    )
    echo.
)

REM ============================================
REM TEST 3: Crear pedido con múltiples opciones
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido con multiples productos y opciones...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 2, \"opciones_seleccionadas\": [\"%OPCION_ID%\"]}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="201" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 201, Got: %STATUS_CODE%
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
