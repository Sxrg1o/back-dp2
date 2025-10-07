@echo off
echo Instalando dependencias para Windows...
echo.

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias específicas para Windows
pip install -r requirements-windows.txt

echo.
echo Instalacion completada para Windows!
echo.
echo Para ejecutar la aplicacion:
echo   uvicorn src.main:app --reload
echo.
pause
