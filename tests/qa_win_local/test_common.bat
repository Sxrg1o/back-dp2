@echo off
REM ============================================
REM Funciones comunes para tests QA - Windows
REM Autor: Adaptado para Windows
REM ============================================

REM Este archivo contiene funciones auxiliares para los tests
REM No se ejecuta directamente, se incluye en otros scripts

REM Configuración por defecto
if not defined API_URL set API_URL=http://localhost:8000
if not defined QA_EMAIL set QA_EMAIL=test@test.com
if not defined QA_PASSWORD set QA_PASSWORD=test123
if not defined VERBOSE set VERBOSE=false

REM Archivo temporal para respuestas
set TEMP_RESPONSE=%TEMP%\qa_response_%RANDOM%.json
set TEMP_HEADERS=%TEMP%\qa_headers_%RANDOM%.txt

REM Colores simulados con echo (limitado en cmd)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "NC=[0m"

REM Variable global para el token
set ACCESS_TOKEN=

goto :eof

REM ============================================
REM Función: get_auth_token
REM Obtiene token de autenticación
REM ============================================
:get_auth_token
    echo Obteniendo token de autenticacion...
    
    curl -s -X POST "%API_URL%/api/v1/auth/login" ^
        -H "Content-Type: application/json" ^
        -d "{\"email\": \"%QA_EMAIL%\", \"password\": \"%QA_PASSWORD%\"}" ^
        -o "%TEMP_RESPONSE%" ^
        -w "%%{http_code}" > "%TEMP_HEADERS%"
    
    REM Extraer token usando Python
    for /f "delims=" %%i in ('python -c "import json; f=open('%TEMP_RESPONSE%'); data=json.load(f); print(data.get('access_token', ''))"') do set ACCESS_TOKEN=%%i
    
    if defined ACCESS_TOKEN (
        echo %GREEN%OK - Token obtenido%NC%
        exit /b 0
    ) else (
        echo %RED%ERROR - No se pudo obtener token%NC%
        type "%TEMP_RESPONSE%"
        exit /b 1
    )
goto :eof

REM ============================================
REM Función: curl_with_auth
REM Ejecuta curl con autenticación
REM Uso: call :curl_with_auth <url> <method> <data>
REM ============================================
:curl_with_auth
    if defined ACCESS_TOKEN (
        curl -s -H "Authorization: Bearer %ACCESS_TOKEN%" %*
    ) else (
        curl -s %*
    )
goto :eof

REM ============================================
REM Función: check_prerequisites
REM Verifica que las herramientas necesarias estén instaladas
REM ============================================
:check_prerequisites
    echo Verificando prerequisitos...
    
    REM Verificar curl
    curl --version >nul 2>&1
    if errorlevel 1 (
        echo %RED%ERROR: curl no esta instalado%NC%
        echo Instala curl desde https://curl.se/windows/
        exit /b 1
    )
    
    REM Verificar Python
    python --version >nul 2>&1
    if errorlevel 1 (
        echo %RED%ERROR: Python no esta instalado%NC%
        echo Instala Python desde https://www.python.org/
        exit /b 1
    )
    
    echo %GREEN%OK - Prerequisitos verificados%NC%
    exit /b 0
goto :eof

REM ============================================
REM Función: cleanup_temp_files
REM Limpia archivos temporales
REM ============================================
:cleanup_temp_files
    if exist "%TEMP_RESPONSE%" del /f /q "%TEMP_RESPONSE%" >nul 2>&1
    if exist "%TEMP_HEADERS%" del /f /q "%TEMP_HEADERS%" >nul 2>&1
goto :eof
