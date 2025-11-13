@echo off
REM ============================================
REM INICIO RAPIDO - Tests QA en Windows Local
REM ============================================

echo.
echo ============================================
echo   TESTS DE QA PARA WINDOWS (LOCAL)
echo ============================================
echo.
echo Este script te ayudara a ejecutar los tests
echo de QA en tu entorno local de Windows.
echo.
echo ============================================
echo   PREREQUISITOS
echo ============================================
echo.
echo 1. Python 3.8+ instalado
echo 2. curl instalado (incluido en Windows 10+)
echo 3. Servidor backend corriendo en localhost:8000
echo.
echo ============================================
echo   PASOS PARA EJECUTAR
echo ============================================
echo.
echo PASO 1: Iniciar el servidor backend
echo   - Abre una terminal nueva
echo   - cd e:\PROYECTOS\DP2\V8\back-dp2
echo   - venv\Scripts\activate
echo   - python src\main.py
echo.
echo PASO 2: Ejecutar los tests (en esta ventana)
echo   - Opcion A: Ejecutar todos los tests
echo     run_all_tests.bat
echo.
echo   - Opcion B: Ejecutar un test individual
echo     test_cu01_crear_pedido_simple.bat
echo     test_cu02_crear_pedido_con_opciones.bat
echo     test_cu03_listar_pedidos.bat
echo.
echo ============================================
echo   VARIABLES DE CONFIGURACION (opcional)
echo ============================================
echo.
echo set API_URL=http://localhost:8000
echo set QA_EMAIL=test@test.com
echo set QA_PASSWORD=test123
echo set VERBOSE=true
echo.
echo ============================================
echo.
pause
