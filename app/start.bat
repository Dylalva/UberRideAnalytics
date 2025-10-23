@echo off
echo ========================================
echo   Uber Ride Analytics - Flask App
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Ejecutar setup
echo.
echo Ejecutando configuracion...
python setup.py

REM Iniciar aplicacion
echo.
echo Iniciando aplicacion Flask...
echo La aplicacion estara disponible en: http://localhost:5000
echo.
python app.py

pause
