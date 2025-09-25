#!/usr/bin/env python3
"""
Script para ejecutar todos los tests del módulo de Gestión de Pedidos
"""

import sys
import os

# Agregar el directorio raíz al path para importar la app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_pedidos_tests():
    """Ejecuta todos los tests del módulo de Gestión de Pedidos"""
    print("🧪 Test Suite - Módulo Gestión de Pedidos")
    print("=" * 50)
    
    try:
        # Importar y ejecutar los tests
        from test_pedidos_endpoints import run_all_tests
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
    print("🍽️  Tests del Módulo Gestión de Pedidos")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app/main.py"):
        print("❌ Error: No se encontró app/main.py")
        print("💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return 1
    
    # Ejecutar tests
    if not run_pedidos_tests():
        return 1
    
    print("\n🎉 ¡Tests del módulo Gestión de Pedidos completados!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
