@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-03: Listar Pedidos
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-03: Listar Pedidos
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

echo === Ejecutando Tests ===
echo.

REM TEST 1: Listar todos los pedidos
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Listar todos los pedidos...

curl -s "%API_URL%/api/v1/pedidos" ^
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

REM TEST 2: Listar pedidos con paginación
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Listar pedidos con paginacion...

curl -s "%API_URL%/api/v1/pedidos?limit=5&offset=0" ^
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

REM Resumen
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
