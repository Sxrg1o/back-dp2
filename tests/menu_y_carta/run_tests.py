#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del módulo Menu y Carta
"""

import sys
import os

# Agregar el directorio raíz al path para importar la app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_menu_y_carta_tests():
    """Ejecuta todos los tests del módulo Menu y Carta"""
    print("🧪 Test Suite - Módulo Menu y Carta")
    print("=" * 50)
    
    try:
        # Importar y ejecutar los tests
        from test_menu_y_carta_all_endpoints import run_all_tests
        run_all_tests()
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de estar en el directorio correcto")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("🍽️  Tests del Módulo Menu y Carta")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app/main.py"):
        print("❌ Error: No se encontró app/main.py")
        print("💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return 1
    
    # Ejecutar tests
    if not run_menu_y_carta_tests():
        return 1
    
    print("\n🎉 ¡Tests del módulo Menu y Carta completados!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
