#!/bin/bash
# Script de configuración para entorno Conda en Linux/Mac
# Ejecutar con: bash setup-conda.sh

echo "=== Configuración del entorno Conda para back-dp2 ==="

# Verificar si Conda está instalado
if ! command -v conda &> /dev/null; then
    echo "✗ Error: Conda no está instalado o no está en el PATH"
    echo "Instala Miniconda o Anaconda desde: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✓ Conda detectado: $(conda --version)"

# Crear el entorno desde environment.yml
echo -e "\nCreando entorno 'back-dp2'..."
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo "✓ Entorno creado exitosamente"
    
    echo -e "\n=== Próximos pasos ==="
    echo "1. Activar el entorno:"
    echo "   conda activate back-dp2"
    echo -e "\n2. Verificar instalación:"
    echo "   python --version"
    echo "   pip list"
    echo -e "\n3. Ejecutar tests:"
    echo "   pytest"
    echo -e "\n4. Iniciar servidor de desarrollo:"
    echo "   uvicorn src.main:app --reload"
else
    echo "✗ Error al crear el entorno"
    echo "Intenta manualmente con: conda env create -f environment.yml"
    exit 1
fi
