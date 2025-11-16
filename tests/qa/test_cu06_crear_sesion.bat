@echo off
REM ============================================================================
REM Script de pruebas para Caso de Uso 6: Crear sesión (Windows)
REM Autor: Kevin Antonio Navarro Carrera
REM Equipo: QA/SEG
REM Modulo: Sesiones - Backend
REM Fecha: 2025-10-29
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuración
if "%API_URL%"=="" (
    set "API_URL=http://localhost:8000"
)

if "%VERBOSE%"=="" (
    set "VERBOSE=false"
)

echo.
echo ==========================================
echo   CU-06: Crear Sesion
echo ==========================================
echo.
echo Configuracion:
echo   API Base URL: %API_URL%
echo   Ambiente: Local (Windows)
echo.

REM Verificar disponibilidad de la API
echo Verificando API en %API_URL%...
curl -s -f "%API_URL%/docs" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] API no disponible en %API_URL%
    echo.
    echo Por favor, asegurate de que:
    echo   1. El servidor esta corriendo en %API_URL%
    echo   2. Te encuentras en el entorno virtual correcto
    echo.
    exit /b 1
)
echo [OK] API disponible
echo.

REM Información de git
for /f "delims=" %%i in ('git rev-parse --short HEAD 2^>nul') do set COMMIT_HASH=%%i
if "%COMMIT_HASH%"=="" set COMMIT_HASH=N/A

for /f "delims=" %%i in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set RAMA=%%i
if "%RAMA%"=="" set RAMA=N/A

echo Commit: %COMMIT_HASH%
echo Rama: %RAMA%
echo Fecha: %date% %time%
echo.

REM Contadores
set TOTAL_TESTS=0
set PASSED_TESTS=0
set FAILED_TESTS=0

REM ============================================================================
REM Preparación: Obtener ID de local
REM ============================================================================
echo === Preparacion: Obtener ID de local ===
echo.

echo Obteniendo ID de local...
curl -s "%API_URL%/api/v1/locales?limit=1" > local_response.json 2>&1
for /f "tokens=2 delims=:," %%a in ('findstr /C:"\"id\"" local_response.json') do (
    set LOCAL_ID=%%a
    set LOCAL_ID=!LOCAL_ID:"=!
    set LOCAL_ID=!LOCAL_ID: =!
    goto :local_found
)
:local_found

if "%LOCAL_ID%"=="" (
    echo [ERROR] No se encontraron locales
    del local_response.json 2>nul
    exit /b 1
)
echo [OK] Local ID: %LOCAL_ID%
echo.

REM ============================================================================
REM Tests de Creación de Sesión
REM ============================================================================
echo === Tests de Creacion de Sesion ===
echo.

REM TC-001: Crear sesión nueva
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Crear sesion nueva...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/sesiones/" ^
-H "Content-Type: application/json" ^
-d "{\"id_local\":\"%LOCAL_ID%\",\"estado\":\"activo\",\"id_domotica\":\"TEST-DOM-001\"}" > sesion_response_full.txt 2>&1

for /f %%i in (sesion_response_full.txt) do set STATUS=%%i
if "%STATUS%"=="201" (
    echo [PASS] Status: %STATUS%
    set /a PASSED_TESTS+=1
    
    REM Guardar respuesta sin el código de estado
    type sesion_response_full.txt | findstr /V "201" > sesion_response.json
    
    REM Extraer ID de sesión
    for /f "tokens=2 delims=:," %%a in ('findstr /C:"\"id\"" sesion_response.json') do (
        set SESION_ID=%%a
        set SESION_ID=!SESION_ID:"=!
        set SESION_ID=!SESION_ID: =!
        goto :sesion_id_found
    )
    :sesion_id_found
) else (
    echo [FAIL] Expected: 201, Got: %STATUS%
    set /a FAILED_TESTS+=1
)

REM TC-002: Validar que la sesión tiene ID generado (ULID)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Validar que sesion tiene ID generado (ULID)...
if defined SESION_ID (
    set ID_LEN=0
    set STR=!SESION_ID!
    :len_loop
    if defined STR (
        set STR=!STR:~1!
        set /a ID_LEN+=1
        goto :len_loop
    )
    if !ID_LEN! EQU 26 (
        echo [PASS] ID: !SESION_ID!
        set /a PASSED_TESTS+=1
    ) else (
        echo [FAIL] ID invalido o longitud incorrecta
        set /a FAILED_TESTS+=1
    )
) else (
    echo [FAIL] No se pudo obtener ID
    set /a FAILED_TESTS+=1
)

REM TC-003: Validar estado inicial es ACTIVO
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Validar que estado es activo...
findstr /C:"\"estado\"" sesion_response.json | findstr /C:"activo" > nul
if %ERRORLEVEL% EQU 0 (
    echo [PASS] Estado: activo
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] Estado no es activo
    set /a FAILED_TESTS+=1
)

REM TC-004: Validar que tiene id_local correcto
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Validar que id_local es correcto...
findstr /C:"%LOCAL_ID%" sesion_response.json > nul
if %ERRORLEVEL% EQU 0 (
    echo [PASS] ID Local correcto
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] ID Local incorrecto
    set /a FAILED_TESTS+=1
)

REM TC-005: Validar que tiene fecha_inicio (no null)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Validar que fecha_inicio no es null...
findstr /C:"\"fecha_inicio\"" sesion_response.json | findstr /V /C:"null" > nul
if %ERRORLEVEL% EQU 0 (
    echo [PASS] fecha_inicio tiene valor
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] fecha_inicio es null
    set /a FAILED_TESTS+=1
)

REM TC-006: Validar que fecha_fin es null (sesión activa)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Validar que fecha_fin es null (sesion activa)...
findstr /C:"\"fecha_fin\"" sesion_response.json | findstr /C:"null" > nul
if %ERRORLEVEL% EQU 0 (
    echo [PASS] fecha_fin: null
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] fecha_fin no es null
    set /a FAILED_TESTS+=1
)

echo.
echo === Tests de Consulta de Sesion ===
echo.

REM TC-007: Obtener sesión por ID
if defined SESION_ID (
    set /a TOTAL_TESTS+=1
    echo TC-%TOTAL_TESTS%: Obtener sesion por ID (GET /sesiones/{id})...
    curl -s -w "%%{http_code}" "%API_URL%/api/v1/sesiones/%SESION_ID%" > temp_get.txt 2>&1
    for /f %%i in (temp_get.txt) do set STATUS=%%i
    if "%STATUS%"=="200" (
        echo [PASS] Status: %STATUS%
        set /a PASSED_TESTS+=1
    ) else (
        echo [FAIL] Expected: 200, Got: %STATUS%
        set /a FAILED_TESTS+=1
    )
    del temp_get.txt 2>nul
) else (
    echo [SKIP] No se pudo crear sesion
)

echo.
echo === Tests de Validacion ===
echo.

REM TC-008: Crear sesión con local inexistente (validación de negocio)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Crear sesion con local inexistente debe retornar 400...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/sesiones/" ^
-H "Content-Type: application/json" ^
-d "{\"id_local\":\"01INVALID000000000000000000\",\"estado\":\"activo\",\"id_domotica\":\"TEST-DOM-001\"}" > temp_invalid_local.txt 2>&1
for /f %%i in (temp_invalid_local.txt) do set STATUS=%%i
if "%STATUS%"=="400" (
    echo [PASS] Status: %STATUS%
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] Expected: 400, Got: %STATUS%
    set /a FAILED_TESTS+=1
)
del temp_invalid_local.txt 2>nul

REM TC-009: Crear sesión con estado inválido
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Crear sesion con estado invalido debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/sesiones/" ^
-H "Content-Type: application/json" ^
-d "{\"id_local\":\"%LOCAL_ID%\",\"estado\":\"ESTADO_INVALIDO\"}" > temp_invalid_estado.txt 2>&1
for /f %%i in (temp_invalid_estado.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo [PASS] Status: %STATUS%
    set /a PASSED_TESTS+=1
) else (
    echo [FAIL] Expected: 422, Got: %STATUS%
    set /a FAILED_TESTS+=1
)
del temp_invalid_estado.txt 2>nul

REM Limpiar archivos temporales
del local_response.json sesion_response.json sesion_response_full.txt 2>nul

echo.
echo ==========================================
echo   Resumen de Tests
echo ==========================================
echo Total:  %TOTAL_TESTS%
echo Pasados: %PASSED_TESTS%
echo Fallidos: %FAILED_TESTS%

set /a PORCENTAJE=(%PASSED_TESTS% * 100) / %TOTAL_TESTS%
echo Exito: %PORCENTAJE%%%
echo.

if %FAILED_TESTS% EQU 0 (
    echo [OK] Todos los tests pasaron
    exit /b 0
) else (
    echo [FAIL] Algunos tests fallaron
    exit /b 1
)
