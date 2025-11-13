@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Script para ejecutar todos los tests de QA
REM Autor: Adaptado para Windows
REM ============================================

echo ==========================================
echo   EJECUTAR TODOS LOS TESTS DE QA
echo ==========================================
echo.
echo API Base URL: http://localhost:8000
echo Fecha: %DATE% %TIME%
echo.

REM Verificar prerequisitos
echo Verificando prerequisitos...
curl --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: curl no esta instalado
    echo Instala curl desde https://curl.se/windows/
    exit /b 1
)

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Instala Python desde https://www.python.org/
    exit /b 1
)

echo OK - Prerequisitos verificados
echo.

REM Verificar que el servidor esté corriendo
echo Verificando conexion al servidor...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/docs > %TEMP%\status.txt
set /p SERVER_STATUS=<%TEMP%\status.txt
del %TEMP%\status.txt

if not "%SERVER_STATUS%"=="200" (
    echo ERROR: El servidor no esta respondiendo en http://localhost:8000
    echo Por favor, inicia el servidor antes de ejecutar los tests:
    echo.
    echo   cd e:\PROYECTOS\DP2\V8\back-dp2
    echo   venv\Scripts\activate
    echo   python src\main.py
    echo.
    exit /b 1
)
echo OK - Servidor respondiendo
echo.

REM Contadores globales
set /a TOTAL_SCRIPTS=0
set /a PASSED_SCRIPTS=0
set /a FAILED_SCRIPTS=0

REM Array para almacenar resultados
set "RESULTS="

REM ============================================
REM Ejecutar cada test
REM ============================================
echo ==========================================
echo   EJECUTANDO TESTS
echo ==========================================
echo.

REM Test CU-01
set /a TOTAL_SCRIPTS+=1
echo [1/13] Ejecutando Test CU-01: Crear Pedido Simple...
call test_cu01_crear_pedido_simple.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-01: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-01: PASS; "
)
echo.

REM Test CU-02
set /a TOTAL_SCRIPTS+=1
echo [2/13] Ejecutando Test CU-02: Crear Pedido con Opciones...
call test_cu02_crear_pedido_con_opciones.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-02: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-02: PASS; "
)
echo.

REM Test CU-03
set /a TOTAL_SCRIPTS+=1
echo [3/13] Ejecutando Test CU-03: Listar Pedidos...
call test_cu03_listar_pedidos.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-03: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-03: PASS; "
)
echo.

REM Test CU-04
set /a TOTAL_SCRIPTS+=1
echo [4/13] Ejecutando Test CU-04: Cambiar Estado Pedido...
call test_cu04_cambiar_estado_pedido.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-04: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-04: PASS; "
)
echo.

REM Test CU-05
set /a TOTAL_SCRIPTS+=1
echo [5/13] Ejecutando Test CU-05: Validaciones y Errores...
call test_cu05_validaciones_errores.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-05: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-05: PASS; "
)
echo.

REM Test CU-06
set /a TOTAL_SCRIPTS+=1
echo [6/13] Ejecutando Test CU-06: Crear Sesion...
call test_cu06_crear_sesion.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-06: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-06: PASS; "
)
echo.

REM Test CU-07
set /a TOTAL_SCRIPTS+=1
echo [7/13] Ejecutando Test CU-07: Listar Sesiones...
call test_cu07_listar_sesiones.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-07: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-07: PASS; "
)
echo.

REM Test CU-08
set /a TOTAL_SCRIPTS+=1
echo [8/13] Ejecutando Test CU-08: Actualizar y Cerrar Sesion...
call test_cu08_actualizar_cerrar_sesion.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-08: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!CU-08: PASS; "
)
echo.

REM Test HU-C02
set /a TOTAL_SCRIPTS+=1
echo [9/13] Ejecutando Test HU-C02: Pantalla Inicial ^(Python^)...
python test_hu_c02.py
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C02: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C02: PASS; "
)
echo.

REM Test HU-C07 API
set /a TOTAL_SCRIPTS+=1
echo [10/13] Ejecutando Test HU-C07: Opciones de Productos API...
call test_hu_c07_api.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C07-API: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C07-API: PASS; "
)
echo.

REM Test HU-C07 Precios
set /a TOTAL_SCRIPTS+=1
echo [11/13] Ejecutando Test HU-C07: Precios ^(Python^)...
python test_hu_c07_precios.py
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C07-PRECIOS: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C07-PRECIOS: PASS; "
)
echo.

REM Test HU-C08
set /a TOTAL_SCRIPTS+=1
echo [12/13] Ejecutando Test HU-C08: Comentarios...
call test_hu_c08_comentarios.bat
if errorlevel 1 (
    set /a FAILED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C08: FAIL; "
) else (
    set /a PASSED_SCRIPTS+=1
    set "RESULTS=!RESULTS!HU-C08: PASS; "
)
echo.

REM ============================================
REM Resumen final
REM ============================================
echo ==========================================
echo   RESUMEN FINAL DE TODOS LOS TESTS
echo ==========================================
echo.
echo Resultados individuales:
echo !RESULTS!
echo.
echo Total de scripts ejecutados: !TOTAL_SCRIPTS!
echo Scripts que pasaron: !PASSED_SCRIPTS!
echo Scripts que fallaron: !FAILED_SCRIPTS!
echo ==========================================
echo.

if !FAILED_SCRIPTS! GTR 0 (
    echo [91mAlgunos tests fallaron - Revisa los detalles arriba[0m
    exit /b 1
) else (
    echo [92mTodos los tests pasaron exitosamente[0m
    exit /b 0
)
