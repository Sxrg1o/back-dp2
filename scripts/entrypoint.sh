#!/bin/bash

# Script de entrada para el contenedor Docker
# Ejecuta la inicialización de la base de datos antes de iniciar la aplicación

set -e

echo "🚀 Iniciando contenedor..."

# Ejecutar inicialización de la base de datos
echo "🔧 Ejecutando inicialización de base de datos..."
python scripts/init_database.py

# Iniciar la aplicación
echo "🌐 Iniciando aplicación FastAPI..."
exec "$@"
