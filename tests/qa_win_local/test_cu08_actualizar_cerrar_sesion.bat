@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Test CU-08: Actualizar y Cerrar Sesión
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   CU-08: Actualizar y Cerrar Sesion
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

echo === Preparacion: Crear sesion de prueba ===
echo.

REM Obtener mesa
echo Obteniendo ID de mesa...
curl -s "%API_URL%/api/v1/mesas?limit=1" -o "%TEMP_RESPONSE%"
for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data['items'][0]['id'] if data.get('items') and len(data['items']) > 0 else '')"') do set MESA_ID=%%i
echo %GREEN%OK - Mesa ID: %MESA_ID%%NC%

REM Crear sesión de prueba
echo Creando sesion de prueba...
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

echo.
echo === Tests de Actualizacion de Sesion ===
echo.

REM TEST 1: Actualizar número de personas
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Actualizar numero_personas a 4...

curl -s -X PATCH "%API_URL%/api/v1/sesiones-mesas/!SESION_ID!" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"numero_personas\": 4}" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    REM Validar el cambio
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('numero_personas', 0))" > "%TEMP_STATUS%"
    set /p NUM_PERSONAS=<"%TEMP_STATUS%"
    
    if "!NUM_PERSONAS!"=="4" (
        echo Numero de personas actualizado correctamente: !NUM_PERSONAS!
    )
) else (
    echo %RED%X FAIL%NC% - Expected: 200, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 2: Cambiar estado a INACTIVO (si aplica en tu API)
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cambiar estado a inactivo...

curl -s -X PATCH "%API_URL%/api/v1/sesiones-mesas/!SESION_ID!" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -H "Content-Type: application/json" ^
    -d "{\"estado\": \"inactivo\"}" ^
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

echo === Tests de Cerrar Sesion ===
echo.

REM TEST 3: Cerrar sesión
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Cerrar sesion ^(endpoint de cierre^)...

curl -s -X POST "%API_URL%/api/v1/sesiones-mesas/!SESION_ID!/cerrar" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    echo %GREEN%OK PASS%NC% - Status: %STATUS_CODE%
    set /a PASSED_TESTS+=1
    
    REM Validar que está cerrada
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('estado', ''))" > "%TEMP_STATUS%"
    set /p ESTADO=<"%TEMP_STATUS%"
    
    if "!ESTADO!"=="cerrado" (
        echo Estado verificado: cerrado
    ) else if "!ESTADO!"=="finalizado" (
        echo Estado verificado: finalizado
    )
) else (
    echo %RED%X FAIL%NC% - Expected: 200, Got: %STATUS_CODE%
    set /a FAILED_TESTS+=1
)
echo.

REM TEST 4: Verificar sesión cerrada
set /a TOTAL_TESTS+=1
echo TC-!TOTAL_TESTS!: Verificar que la sesion esta cerrada...

curl -s "%API_URL%/api/v1/sesiones-mesas/!SESION_ID!" ^
    -H "Authorization: Bearer %ACCESS_TOKEN%" ^
    -o "%TEMP_RESPONSE%" ^
    -w "%%{http_code}" > "%TEMP_STATUS%"

set /p STATUS_CODE=<"%TEMP_STATUS%"

if "%STATUS_CODE%"=="200" (
    python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); estado=data.get('estado', ''); print('OK' if estado in ['cerrado', 'finalizado'] else 'FAIL')" > "%TEMP_STATUS%"
    set /p VALIDATION=<"%TEMP_STATUS%"
    
    if "!VALIDATION!"=="OK" (
        echo %GREEN%OK PASS%NC% - Sesion cerrada correctamente
        set /a PASSED_TESTS+=1
    ) else (
        echo %RED%X FAIL%NC% - Sesion no esta cerrada
        set /a FAILED_TESTS+=1
    )
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
    set EXIT_CODE=1
) else (
    set EXIT_CODE=0
)

:cleanup
if exist "%TEMP_RESPONSE%" del /f /q "%TEMP_RESPONSE%" >nul 2>&1
if exist "%TEMP_STATUS%" del /f /q "%TEMP_STATUS%" >nul 2>&1
exit /b %EXIT_CODE%
