#!/bin/bash
# Script para ejecutar tests en Linux/Mac
# Uso: ./run-tests.sh [opciones]

echo "🧪 Ejecutando Tests - API de Gestión de Restaurante"
echo "=================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: No se encontró app/main.py"
    echo "💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar si el entorno virtual está activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Advertencia: No se detectó entorno virtual activado"
    echo "💡 Se recomienda activar el entorno virtual antes de ejecutar tests"
    echo ""
fi

# Hacer el script ejecutable
chmod +x "$0"

# Ejecutar el runner de tests con los argumentos pasados
python tests/run_tests.py "$@"

# Verificar el resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos los tests pasaron exitosamente"
else
    echo ""
    echo "❌ Algunos tests fallaron"
    exit 1
fi
