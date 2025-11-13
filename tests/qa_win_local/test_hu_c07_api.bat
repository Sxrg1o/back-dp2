@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test HU-C07: Opciones de Productos
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   Test HU-C07: Opciones de Productos
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

echo === Tests de Endpoints ===
echo.

REM TEST 1: Health check
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: Health check del backend...

curl -s "%API_URL%/health" ^
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

REM TEST 2: Listar productos
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: GET /productos-menu ^(listar productos^)...

curl -s "%API_URL%/api/v1/productos-menu?skip=0&limit=10" ^
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

REM TEST 3: Listar categorías
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: GET /categorias ^(listar categorias^)...

curl -s "%API_URL%/api/v1/categorias?skip=0&limit=10" ^
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

REM TEST 4: Listar tipos de opciones
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: GET /tipos-opciones ^(listar tipos de opciones^)...

curl -s "%API_URL%/api/v1/tipos-opciones?skip=0&limit=50" ^
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

echo === Tests de Validacion de Campos ===
echo.

REM TEST 5: Validar campo opciones en productos
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: Validar que productos tienen campo opciones...

curl -s "%API_URL%/api/v1/productos-menu?skip=0&limit=10" -o "%TEMP_RESPONSE%"

python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print('OK' if any('opciones' in item for item in data.get('items', [])) else 'FAIL')" > "%TEMP_STATUS%"
set /p VALIDATION=<"%TEMP_STATUS%"

if "!VALIDATION!"=="OK" (
    echo %GREEN%OK PASS%NC% - Campo opciones presente en productos
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Campo opciones no encontrado
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 6: Validar estructura de tipos de opciones
set /a TOTAL_TESTS+=1
echo Test !TOTAL_TESTS!: Validar estructura de tipos de opciones...

curl -s "%API_URL%/api/v1/tipos-opciones?limit=1" -o "%TEMP_RESPONSE%"

python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); item=data['items'][0] if data.get('items') and len(data['items']) > 0 else {}; print('OK' if 'id' in item and 'nombre' in item else 'FAIL')" > "%TEMP_STATUS%"
set /p VALIDATION=<"%TEMP_STATUS%"

if "!VALIDATION!"=="OK" (
    echo %GREEN%OK PASS%NC% - Campos id y nombre presentes
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Estructura incorrecta
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 7: Obtener opciones de un producto específico
echo Obteniendo ID de producto con opciones...
curl -s "%API_URL%/api/v1/productos-menu?limit=20" -o "%TEMP_RESPONSE%"

python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); items=data.get('items',[]); prod=[p for p in items if p.get('opciones')]; print(prod[0]['id'] if prod else '')" > "%TEMP_STATUS%"
set /p PRODUCTO_ID=<"%TEMP_STATUS%"

if defined PRODUCTO_ID (
    set /a TOTAL_TESTS+=1
    echo Test !TOTAL_TESTS!: GET /productos/{id}/opciones...
    
    curl -s "%API_URL%/api/v1/productos/!PRODUCTO_ID!/opciones" ^
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
