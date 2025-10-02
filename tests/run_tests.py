#!/usr/bin/env python3
"""
Runner centralizado para ejecutar todos los tests del proyecto.
Permite ejecutar tests por módulo o todos los tests.
"""
import sys
import os
import argparse
from typing import Dict, Any

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.utils import TestRunner

def main():
    """Función principal del runner de tests"""
    parser = argparse.ArgumentParser(
        description="Runner de tests para el proyecto API de Gestión de Restaurante",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python tests/run_tests.py                    # Ejecutar todos los tests
  python tests/run_tests.py --module menu      # Ejecutar solo tests de menú
  python tests/run_tests.py --module pedidos   # Ejecutar solo tests de pedidos
  python tests/run_tests.py --list             # Listar módulos disponibles
  python tests/run_tests.py --verbose          # Ejecutar con salida detallada
        """
    )
    
    parser.add_argument(
        '--module', '-m',
        choices=['menu', 'pedidos', 'all'],
        default='all',
        help='Módulo de tests a ejecutar (default: all)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Listar módulos de tests disponibles'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Ejecutar con salida detallada'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Ejecutar con salida mínima'
    )
    
    args = parser.parse_args()
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("app/main.py"):
        print("ERROR Error: No se encontró app/main.py")
        print(" Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return 1
    
    runner = TestRunner()
    
    # Listar módulos si se solicita
    if args.list:
        runner.list_modules()
        return 0
    
    # Configurar nivel de verbosidad
    if args.quiet:
        # Redirigir stdout para salida mínima
        import io
        sys.stdout = io.StringIO()
    
    print("Sistema de Tests - API de Gestion de Restaurante")
    print("=" * 60)
    
    try:
        if args.module == 'all':
            # Ejecutar todos los tests
            result = runner.run_all_tests()
            
            if result['success']:
                print("\n ¡Todos los tests pasaron exitosamente!")
                return 0
            else:
                print(f"\n  {result['total_modules'] - result['successful_modules']} módulo(s) fallaron")
                return 1
                
        else:
            # Ejecutar tests de un módulo específico
            module_map = {
                'menu': 'menu_y_carta',
                'pedidos': 'gestion_pedidos'
            }
            
            module_name = module_map[args.module]
            result = runner.run_module_tests(module_name)
            
            if result['success']:
                print(f"\n ¡Tests del módulo {module_name} completados exitosamente!")
                return 0
            else:
                print(f"\nERROR Error en módulo {module_name}: {result.get('error', 'Desconocido')}")
                return 1
                
    except KeyboardInterrupt:
        print("\n\n  Ejecución interrumpida por el usuario")
        return 130
    except Exception as e:
        print(f"\nERROR Error inesperado: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
