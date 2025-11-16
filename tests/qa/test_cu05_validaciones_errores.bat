@echo off
REM ============================================================================
REM Script de pruebas para Caso de Uso 5: Validaciones y errores (Windows)
REM Autor: Kevin Antonio Navarro Carrera
REM Equipo: QA/SEG
REM Modulo: Pedidos - Backend
REM Fecha: 2025-10-29
REM Adaptado para Windows desde Bash
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuración de colores (usando caracteres ASCII)
set "GREEN=[32m"
set "RED=[31m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "NC=[0m"

REM Configuración
if "%API_URL%"=="" (
    set "API_URL=http://localhost:8000"
)

if "%VERBOSE%"=="" (
    set "VERBOSE=false"
)

echo.
echo ==========================================
echo   CU-05: Validaciones y Errores
echo ==========================================
echo.
echo Configuracion:
echo   API Base URL: %API_URL%
echo   Ambiente: Local (Windows)
echo   Verbose: %VERBOSE%
echo.

REM Verificar disponibilidad de la API
echo Verificando API en %API_URL%...
curl -s -f "%API_URL%/docs" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %RED%X API no disponible en %API_URL%%NC%
    echo.
    echo Por favor, asegurate de que:
    echo   1. El servidor esta corriendo en %API_URL%
    echo   2. Te encuentras en el entorno virtual correcto
    echo.
    echo Para iniciar el servidor localmente, ejecuta:
    echo   cd back-dp2 ^&^& python -m uvicorn src.main:app --reload
    echo.
    exit /b 1
)
echo %GREEN%OK - API disponible%NC%
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
REM Tests de Validación de Mesa
REM ============================================================================
echo === Tests de Validacion de Mesa ===
echo.

REM TC-001: Crear pedido con mesa inexistente (formato inválido detectado por schema)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Mesa inexistente debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"01INVALID000000000000000000\",\"items\":[{\"id_producto\":\"01JTEST0000000000000000000\",\"cantidad\":1,\"precio_unitario\":25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM TC-002: Crear pedido con mesa vacía
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Mesa vacia debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"\",\"items\":[{\"id_producto\":\"01JTEST0000000000000000000\",\"cantidad\":1,\"precio_unitario\":25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

echo.
echo === Tests de Validacion de Productos ===
echo.

REM Obtener mesa válida para tests
echo Obteniendo mesa para tests...
curl -s "%API_URL%/api/v1/mesas?skip=0&limit=1" > mesa_response.json 2>&1
for /f "tokens=2 delims=:," %%a in ('findstr /C:"\"id\"" mesa_response.json') do (
    set MESA_ID=%%a
    set MESA_ID=!MESA_ID:"=!
    set MESA_ID=!MESA_ID: =!
    goto :mesa_found
)
:mesa_found
if "%MESA_ID%"=="" (
    echo %YELLOW%Advertencia: No se encontro mesa valida%NC%
    set MESA_ID=01JMESA0000000000000000000
) else (
    echo %GREEN%OK ^(%MESA_ID%^)%NC%
)

REM TC-003: Crear pedido con producto inexistente (formato inválido detectado por schema)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Producto inexistente debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[{\"id_producto\":\"01INVALID000000000000000000\",\"cantidad\":1,\"precio_unitario\":25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM Obtener producto válido
echo Obteniendo producto para tests...
curl -s "%API_URL%/api/v1/productos?skip=0&limit=1" > producto_response.json 2>&1
for /f "tokens=2 delims=:," %%a in ('findstr /C:"\"id\"" producto_response.json') do (
    set PRODUCTO_ID=%%a
    set PRODUCTO_ID=!PRODUCTO_ID:"=!
    set PRODUCTO_ID=!PRODUCTO_ID: =!
    goto :producto_found
)
:producto_found
if "%PRODUCTO_ID%"=="" (
    echo %YELLOW%Advertencia: No se encontro producto valido%NC%
    set PRODUCTO_ID=01JPRODUCTO00000000000000000
) else (
    echo %GREEN%OK ^(%PRODUCTO_ID%^)%NC%
)

echo.
echo === Tests de Validacion de Cantidad ===
echo.

REM TC-004: Cantidad = 0 debe fallar
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Cantidad = 0 debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[{\"id_producto\":\"%PRODUCTO_ID%\",\"cantidad\":0,\"precio_unitario\":25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM TC-005: Cantidad negativa debe fallar
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Cantidad negativa debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[{\"id_producto\":\"%PRODUCTO_ID%\",\"cantidad\":-5,\"precio_unitario\":25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

echo.
echo === Tests de Validacion de Precio ===
echo.

REM TC-006: Precio = 0 debe fallar
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Precio = 0 debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[{\"id_producto\":\"%PRODUCTO_ID%\",\"cantidad\":1,\"precio_unitario\":0,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM TC-007: Precio negativo debe fallar
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Precio negativo debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[{\"id_producto\":\"%PRODUCTO_ID%\",\"cantidad\":1,\"precio_unitario\":-25.50,\"opciones\":[]}]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

echo.
echo === Tests de Validacion de Items Vacios ===
echo.

REM TC-008: Items vacío debe fallar
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: Items vacio debe retornar 422...
curl -s -w "%%{http_code}" -X POST "%API_URL%/api/v1/pedidos/completo" ^
-H "Content-Type: application/json" ^
-d "{\"id_mesa\":\"%MESA_ID%\",\"items\":[]}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

echo.
echo === Tests de Validacion de Pedido Inexistente ===
echo.

REM TC-009: GET pedido inexistente
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: GET pedido inexistente debe retornar 404...
curl -s -w "%%{http_code}" "%API_URL%/api/v1/pedidos/01INVALID000000000000000000" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="404" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 404, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM TC-010: PATCH pedido inexistente (formato inválido detectado por schema)
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: PATCH estado de pedido inexistente debe retornar 422...
curl -s -w "%%{http_code}" -X PATCH "%API_URL%/api/v1/pedidos/01INVALID000000000000000000/estado" ^
-H "Content-Type: application/json" ^
-d "{\"estado\":\"CONFIRMADO\"}" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="422" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 422, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM TC-011: DELETE pedido inexistente
set /a TOTAL_TESTS+=1
echo TC-%TOTAL_TESTS%: DELETE pedido inexistente debe retornar 404...
curl -s -w "%%{http_code}" -X DELETE "%API_URL%/api/v1/pedidos/01INVALID000000000000000000" > temp_response.txt 2>&1
for /f %%i in (temp_response.txt) do set STATUS=%%i
if "%STATUS%"=="404" (
    echo %GREEN%PASS%NC% ^(Status: %STATUS%^)
    set /a PASSED_TESTS+=1
) else (
    echo %RED%FAIL%NC% ^(Expected: 404, Got: %STATUS%^)
    set /a FAILED_TESTS+=1
)

REM Limpiar archivos temporales
del temp_response.txt mesa_response.json producto_response.json 2>nul

echo.
echo ==========================================
echo   Resumen de Tests
echo ==========================================
echo Total:  %TOTAL_TESTS%
echo Pasados: %GREEN%%PASSED_TESTS%%NC%
echo Fallidos: %RED%%FAILED_TESTS%%NC%

set /a PORCENTAJE=(%PASSED_TESTS% * 100) / %TOTAL_TESTS%
echo Exito: %BLUE%%PORCENTAJE%%%NC%
echo.

if %FAILED_TESTS% EQU 0 (
    echo %GREEN%Todos los tests pasaron%NC%
    exit /b 0
) else (
    echo %RED%Algunos tests fallaron%NC%
    echo.
    echo Instrucciones para ejecutar en LOCAL:
    echo   1. Abre una terminal en la carpeta 'back-dp2'
    echo   2. Activa el entorno virtual: venv\Scripts\activate
    echo   3. Ejecuta el servidor: python -m uvicorn src.main:app --reload
    echo   4. En otra terminal, ejecuta este script:
    echo      tests\qa\test_cu05_validaciones_errores.bat
    exit /b 1
)
