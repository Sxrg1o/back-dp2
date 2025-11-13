@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test HU-C08: Dejar indicación para cocina
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   HU-C08: Dejar indicacion para cocina
echo ==========================================
echo.

if not defined API_URL set API_URL=http://localhost:8000
echo API Base URL: %API_URL%
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
REM Preparación
REM ============================================
echo === Preparacion: Obtener IDs necesarios ===
echo.

REM Obtener token
echo Obteniendo token de autenticacion...
curl -s -X POST "%API_URL%/api/v1/auth/login" ^
    -H "Content-Type: application/json" ^
    -d "{\"email\": \"test@test.com\", \"password\": \"test123\"}" ^
    -o "%TEMP_RESPONSE%"

for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('access_token', ''))"') do set ACCESS_TOKEN=%%i

if not defined ACCESS_TOKEN (
    echo %RED%ERROR: No se pudo obtener token%NC%
    goto :cleanup
)
echo %GREEN%OK%NC%

REM Obtener usuario
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
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') else '')"') do set PRODUCTO_ID=%%i
echo %GREEN%OK - Producto ID: %PRODUCTO_ID%%NC%

echo.
echo === Tests de Comentarios en Pedidos ===
echo.

REM TEST 1: Crear pedido con comentario
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido con notas_cliente...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 1}], \"notas_cliente\": \"Sin picante, por favor\"}" ^
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
)
echo.

REM TEST 2: Verificar que el comentario se guardó
if defined PEDIDO_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Verificar que el comentario se guardo...
    
    curl -s "%API_URL%/api/v1/pedidos/!PEDIDO_ID!" ^
        -H "Authorization: Bearer %ACCESS_TOKEN%" ^
        -o "%TEMP_RESPONSE%"
    
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print('OK' if data.get('notas_cliente') else 'FAIL')" > "%TEMP_STATUS%"
    set /p VALIDATION=<"%TEMP_STATUS%"
    
    if "!VALIDATION!"=="OK" (
        echo %GREEN%OK PASS%NC% - notas_cliente presente
        set /a PASSED_TESTS+=1
        
        REM Mostrar el comentario
        for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('notas_cliente', ''))"') do set NOTAS=%%i
        echo Comentario: !NOTAS!
    ) else (
        echo %RED%X FAIL%NC% - notas_cliente no presente
        set /a FAILED_TESTS+=1
    )
    echo.
)

REM TEST 3: Crear pedido con comentario largo
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido con comentario largo...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%SESION_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 1}], \"notas_cliente\": \"Por favor preparar sin aji, con poca sal, agregar limones extra, y servir bien frio. Gracias!\"}" ^
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

REM TEST 4: Crear pedido sin comentario (opcional)
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear pedido sin comentario ^(campo opcional^)...

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
) else (
    echo %RED%X FAIL%NC% - Expected: 201, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 5: Actualizar comentario de pedido existente
if defined PEDIDO_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Actualizar comentario de pedido existente...
    
    curl -s -X PATCH "%API_URL%/api/v1/pedidos/!PEDIDO_ID!" ^
        -H "Authorization: Bearer %ACCESS_TOKEN%" ^
        -H "Content-Type: application/json" ^
        -d "{\"notas_cliente\": \"Comentario actualizado\"}" ^
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
