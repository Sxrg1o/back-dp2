@echo off
REM Comandos rapidos para usar con Anaconda Prompt
REM Copia y pega estos comandos en Anaconda Prompt

echo ========================================
echo COMANDOS PARA ANACONDA PROMPT
echo ========================================
echo.
echo 1. NAVEGAR AL PROYECTO:
echo    cd E:\PROYECTOS\DP2\V6\back-dp2
echo.
echo 2. CREAR ENTORNO (solo primera vez):
echo    conda env create -f environment.yml
echo.
echo 3. ACTIVAR ENTORNO:
echo    conda activate back-dp2
echo.
echo 4. EJECUTAR TESTS:
echo    pytest
echo    pytest --cov=src
echo.
echo 5. INICIAR SERVIDOR:
echo    uvicorn src.main:app --reload
echo.
echo 6. DESACTIVAR ENTORNO:
echo    conda deactivate
echo.
echo 7. ACTUALIZAR ENTORNO:
echo    conda env update -f environment.yml --prune
echo.
echo 8. LISTAR ENTORNOS:
echo    conda env list
echo.
echo ========================================
echo.
pause
