#!/usr/bin/env python3
"""
Script para ejecutar tests del módulo Menu y Carta.
Ahora usa la nueva estructura organizada.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    """Función principal - delega al runner centralizado"""
    print("  Tests del Módulo Menu y Carta")
    print("=" * 50)
    print(" Usando el runner centralizado...")
    print()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app/main.py"):
        print("ERROR Error: No se encontró app/main.py")
        print(" Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return 1
    
    try:
        # Importar y usar el runner centralizado
        from tests.utils import TestRunner
        
        runner = TestRunner()
        result = runner.run_module_tests('menu_y_carta')
        
        if result['success']:
            print("\n ¡Tests del módulo Menu y Carta completados!")
            return 0
        else:
            print(f"\nERROR Error: {result.get('error', 'Desconocido')}")
            return 1
            
    except Exception as e:
        print(f"ERROR Error ejecutando tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
