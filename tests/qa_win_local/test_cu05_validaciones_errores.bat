@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-05: Validaciones y Errores
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-05: Validaciones y Errores
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

echo === Tests de Validacion de Mesa ===
echo.

REM TEST 1: Mesa inexistente
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Mesa inexistente debe retornar 400...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"01INVALID000000000000000000\", \"productos\": [{\"id_producto\": \"01TEST0000000000000000000\", \"cantidad\": 1}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="404" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 400, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM Obtener mesa válida para tests
echo Obteniendo mesa valida...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i

if not defined MESA_ID (
    echo %RED%ERROR: No se encontro mesa valida%NC%
    goto :cleanup
)
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%
echo.

echo === Tests de Validacion de Productos ===
echo.

REM TEST 2: Producto inexistente
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Producto inexistente debe retornar 400...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%MESA_ID%\", \"productos\": [{\"id_producto\": \"01INVALID000000000000000000\", \"cantidad\": 1}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="404" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 400, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM Obtener producto válido
echo Obteniendo producto valido...
curl -s "%API_URL%/api/v1/productos-menu?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') else '')"') do set PRODUCTO_ID=%%i
echo %GREEN%OK - Producto ID: %PRODUCTO_ID%%NC%
echo.

echo === Tests de Validacion de Cantidad ===
echo.

REM TEST 3: Cantidad = 0
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cantidad 0 debe retornar 400 o 422...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%MESA_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": 0}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="422" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 400 or 422, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 4: Cantidad negativa
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cantidad negativa debe retornar 400 o 422...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%MESA_ID%\", \"productos\": [{\"id_producto\": \"%PRODUCTO_ID%\", \"cantidad\": -1}]}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="422" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Expected: 400 or 422, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 5: Array de productos vacío
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Array de productos vacio debe retornar 400 o 422...

curl -s -X POST "%API_URL%/api/v1/pedidos" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_sesion_mesa\": \"%MESA_ID%\", \"productos\": []}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="400" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
) else if "%STATUS_CODE%"=="422" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
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
