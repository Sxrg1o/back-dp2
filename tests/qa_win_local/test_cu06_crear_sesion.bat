@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-06: Crear Sesión
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-06: Crear Sesion
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

echo === Preparacion: Obtener ID de mesa ===
echo.

echo Obteniendo ID de mesa...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i

if not defined MESA_ID (
    echo %RED%ERROR: No se encontraron mesas%NC%
    goto :cleanup
)
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%

echo.
echo === Tests de Creacion de Sesion ===
echo.

REM TEST 1: Crear sesión nueva
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear sesion nueva...

curl -s -X POST "%API_URL%/api/v1/sesiones-mesas" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_mesa\": \"%MESA_ID%\", \"numero_personas\": 2}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="201" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id', ''))"') do set SESION_ID=%%i
    echo Sesion creada con ID: !SESION_ID!
) else (
    echo %RED%X FAIL%NC% - Expected: 201, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 2: Validar ID de sesión (ULID)
if defined SESION_ID (
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Validar que sesion tiene ID generado ^(ULID^)...
    
    set ID_LENGTH=0
    set "SESION_ID_STR=!SESION_ID!"
    for /l %%i in (0,1,30) do if "!SESION_ID_STR:~%%i,1!" neq "" set /a ID_LENGTH+=1
    
    if !ID_LENGTH! EQU 26 (
        echo %GREEN%OK PASS%NC% - ID: !SESION_ID!
        set /a PASSED_TESTS+=1
    ) else (
        echo %RED%X FAIL%NC% - ID invalido o vacio
        set /a FAILED_TESTS+=1
    )
    echo.
    
    REM TEST 3: Validar estado inicial es ACTIVO
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Validar que estado es activo...
    
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('estado', ''))" > "%TEMP_STATUS%"
    set /p ESTADO=<"%TEMP_STATUS%"
    
    if "!ESTADO!"=="activo" (
        echo %GREEN%OK PASS%NC% - Estado: !ESTADO!
        set /a PASSED_TESTS+=1
    ) else (
        echo %RED%X FAIL%NC% - Esperado: activo, Obtenido: !ESTADO!
        set /a FAILED_TESTS+=1
    )
    echo.
    
    REM TEST 4: Validar id_mesa correcto
    set /a TOTAL_TESTS+=1
    echo TC-!TOTAL_TESTS!: Validar que id_mesa es correcto...
    
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('id_mesa', ''))" > "%TEMP_STATUS%"
    set /p ID_MESA_RESP=<"%TEMP_STATUS%"
    
    if "!ID_MESA_RESP!"=="%MESA_ID%" (
        echo %GREEN%OK PASS%NC% - ID Mesa: !ID_MESA_RESP!
        set /a PASSED_TESTS+=1
    ) else (
        echo %RED%X FAIL%NC% - Esperado: %MESA_ID%, Obtenido: !ID_MESA_RESP!
        set /a FAILED_TESTS+=1
    )
    echo.
)

REM TEST 5: Crear sesión con número de personas
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Crear sesion con numero_personas=4...

curl -s -X POST "%API_URL%/api/v1/sesiones-mesas" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"id_mesa\": \"%MESA_ID%\", \"numero_personas\": 4}" ^
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
    set EXIT_CODE=1
) else (
    set EXIT_CODE=0
)

:cleanup
if exist "%TEMP_RESPONSE%" del /f /q "%TEMP_RESPONSE%" >nul 2>&1
if exist "%TEMP_STATUS%" del /f /q "%TEMP_STATUS%" >nul 2>&1
exit /b %EXIT_CODE%
