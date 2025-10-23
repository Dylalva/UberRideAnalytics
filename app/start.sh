#!/bin/bash

echo "========================================"
echo "  Uber Ride Analytics - Flask App"
echo "========================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar setup
echo ""
echo "Ejecutando configuración..."
python setup.py

# Iniciar aplicación
echo ""
echo "Iniciando aplicación Flask..."
echo "La aplicación estará disponible en: http://localhost:5000"
echo ""
python app.py
