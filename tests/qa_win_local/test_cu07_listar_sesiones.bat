@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-07: Listar Sesiones
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-07: Listar Sesiones
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

echo.
echo === Tests de Listado de Sesiones ===
echo.

REM TEST 1: Listar sesiones sin filtros
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Listar sesiones ^(GET /sesiones-mesas^)...

curl -s "%API_URL%/api/v1/sesiones-mesas" ^
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

REM TEST 2: Validar estructura de respuesta paginada
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Validar estructura de respuesta paginada...

python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print('OK' if 'items' in data and 'total' in data else 'FAIL')" > "%TEMP_STATUS%"
set /p VALIDATION=<"%TEMP_STATUS%"

if "!VALIDATION!"=="OK" (
    echo %GREEN%OK PASS%NC% - Campos items y total presentes
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Estructura incorrecta
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 3: Listar sesiones con paginación
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Listar sesiones con paginacion ^(limit=5^)...

curl -s "%API_URL%/api/v1/sesiones-mesas?skip=0&limit=5" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    REM Validar que limit funciona
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(len(data.get('items', [])))" > "%TEMP_STATUS%"
    set /p ITEMS_COUNT=<"%TEMP_STATUS%"
    
    if !ITEMS_COUNT! LEQ 5 (
        echo Items retornados: !ITEMS_COUNT! ^<= 5
    )
) else (
    echo %RED%X FAIL%NC% - Expected: 200, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 4: Filtrar por estado activo
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Filtrar por estado activo...

curl -s "%API_URL%/api/v1/sesiones-mesas?estado=activo" ^
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

REM TEST 5: Filtrar por mesa específica
echo Obteniendo ID de mesa para filtro...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i

if defined MESA_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Filtrar por ID de mesa...
    
    curl -s "%API_URL%/api/v1/sesiones-mesas?id_mesa=%MESA_ID%" ^
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

REM TEST 6: Validar campos requeridos
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Validar campos requeridos en sesiones...

curl -s "%API_URL%/api/v1/sesiones-mesas?limit=1" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%"

python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); item=data['items'][0] if data.get('items') and len(data['items']) > 0 else {}; print('OK' if 'id' in item and 'id_mesa' in item and 'estado' in item else 'FAIL')" > "%TEMP_STATUS%"
set /p VALIDATION=<"%TEMP_STATUS%"

if "!VALIDATION!"=="OK" (
    echo %GREEN%OK PASS%NC% - Campos: id, id_mesa, estado
    set /a PASSED_TESTS+=1
) else (
    echo %RED%X FAIL%NC% - Faltan campos requeridos
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
