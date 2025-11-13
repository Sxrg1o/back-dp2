@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-04: Cambiar Estado de Pedido
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-04: Cambiar Estado de Pedido
echo ==========================================
echo.

if not defined API_URL set API_URL=http://localhost:8000
if not defined VERBOSE set VERBOSE=false

echo API Base URL: %API_URL%
echo Fecha: %DATE% %TIME%
echo.

set /a TOTAL_TESTS=0
set /a PASSED_TESTS=0
set /a FAILED_TESTS=0

set TEMP_RESPONSE=%TEMP%\qa_response_%RANDOM%.json
set TEMP_STATUS=%TEMP%\qa_status_%RANDOM%.txt

set "GREEN=[92m"
set "RED=[91m"
set "NC=[0m"

REM ============================================
REM Preparación: Crear pedido de prueba
REM ============================================
echo === Preparacion: Crear pedido de prueba ===
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
echo %GREEN%OK%NC%

REM Obtener ID de usuario
echo Obteniendo ID de usuario...
curl -s "%API_URL%/api/v1/auth/me" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set USER_ID=%%i
echo %GREEN%OK - User ID: %USER_ID%%NC%

REM Obtener mesa
echo Obteniendo ID de mesa...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%

REM Crear sesión
echo Creando sesion de mesa...
curl -s -X POST "%API_URL%/api/v1/sesiones-mesas" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_mesa\": \"%MESA_ID%\", \"numero_personas\": 2}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set SESION_ID=%%i
echo %GREEN%OK - Sesion ID: %SESION_ID%%NC%

REM Obtener producto
echo Obteniendo producto...
curl -s "%API_URL%/api/v1/productos-menu?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set PRODUCTO_ID=%%i
echo %GREEN%OK - Producto ID: %PRODUCTO_ID%%NC%

REM Crear pedido de prueba
echo Creando pedido de prueba...
curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 1}], \"notas_cliente\": \"Test cambio de estado\"}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set PEDIDO_ID=%%i

if not defined PEDIDO_ID (
    echo %RED%ERROR: No se pudo crear pedido%NC%
    goto :cleanup
)
echo %GREEN%OK - Pedido ID: %PEDIDO_ID%%NC%

echo.
echo === Ejecutando Tests ===
echo.

REM ============================================
REM TEST 1: Cambiar estado a EN_PREPARACION
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cambiar estado a EN_PREPARACION...

curl -s -X PATCH "%API_URL%/api/v1/pedidos/!PEDIDO_ID!/estado" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"estado\": \"en_preparacion\"}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    REM Validar que el estado cambió
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print('OK' if data.get('estado')=='en_preparacion' else 'FAIL')" > "%TEMP_STATUS%"
    set /p VALIDATION=<"%TEMP_STATUS%"
    
    if "!VALIDATION!"=="OK" (
        echo Estado verificado: en_preparacion
    )
) else (
    echo %RED%X FAIL%NC% - Expected: 200, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM ============================================
REM TEST 2: Cambiar estado a LISTO
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cambiar estado a LISTO...

curl -s -X PATCH "%API_URL%/api/v1/pedidos/!PEDIDO_ID!/estado" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"estado\": \"listo\"}" ^
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
REM TEST 3: Cambiar estado a ENTREGADO
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cambiar estado a ENTREGADO...

curl -s -X PATCH "%API_URL%/api/v1/pedidos/!PEDIDO_ID!/estado" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"estado\": \"entregado\"}" ^
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
REM TEST 4: Intentar cambiar a estado inválido
REM ============================================
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Intentar cambiar a estado invalido...

curl -s -X PATCH "%API_URL%/api/v1/pedidos/!PEDIDO_ID!/estado" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"estado\": \"estado_invalido\"}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE% ^(error esperado^)
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="422" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE% ^(error esperado^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 400 or 422, Got: %STATUS_CODE%
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
    set EXIT_CODE=1
) else (
    set EXIT_CODE=0
)

:cleanup
if exist "%TEMP_RESPONSE%" del /f /q "%TEMP_RESPONSE%" >nul 2>&1
if exist "%TEMP_STATUS%" del /f /q "%TEMP_STATUS%" >nul 2>&1
exit /b %EXIT_CODE%
