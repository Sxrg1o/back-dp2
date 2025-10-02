"""
Utilidades comunes para todos los tests del proyecto.
"""
import sys
import os
from typing import Dict, Any, List, Optional
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

class TestBase:
    """Clase base para todos los tests con utilidades comunes"""
    
    def __init__(self):
        self.client = TestClient(app)
        self.base_url = ""
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Realiza una petición HTTP y retorna la respuesta como diccionario.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint a llamar
            **kwargs: Argumentos adicionales para la petición
        
        Returns:
            Dict con la respuesta de la API
        """
        response = getattr(self.client, method.lower())(endpoint, **kwargs)
        return {
            'status_code': response.status_code,
            'data': response.json() if response.content else None,
            'headers': dict(response.headers)
        }
    
    def assert_success_response(self, response: Dict[str, Any], expected_status: int = 200):
        """Verifica que la respuesta sea exitosa"""
        assert response['status_code'] == expected_status, \
            f"Expected status {expected_status}, got {response['status_code']}"
        assert response['data'] is not None, "Response data should not be None"
    
    def assert_error_response(self, response: Dict[str, Any], expected_status: int = 400):
        """Verifica que la respuesta sea un error"""
        assert response['status_code'] == expected_status, \
            f"Expected error status {expected_status}, got {response['status_code']}"
    
    def print_test_result(self, test_name: str, success: bool, details: str = ""):
        """Imprime el resultado de un test de forma consistente"""
        status = "OK" if success else "ERROR"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")

class TestRunner:
    """Runner centralizado para ejecutar tests por módulo o todos"""
    
    def __init__(self):
        self.modules = {
            'menu_y_carta': {
                'name': 'Menu y Carta',
                'path': 'tests/menu_y_carta',
                'test_file': 'test_endpoints.py',
                'description': 'Tests del módulo de gestión de menú y carta'
            },
            'gestion_pedidos': {
                'name': 'Gestión de Pedidos',
                'path': 'tests/gestion_pedidos', 
                'test_file': 'test_endpoints.py',
                'description': 'Tests del módulo de gestión de pedidos'
            }
        }
    
    def run_module_tests(self, module_name: str) -> Dict[str, Any]:
        """
        Ejecuta tests de un módulo específico.
        
        Args:
            module_name: Nombre del módulo a ejecutar
        
        Returns:
            Dict con resultados de la ejecución
        """
        if module_name not in self.modules:
            raise ValueError(f"Módulo '{module_name}' no encontrado. Módulos disponibles: {list(self.modules.keys())}")
        
        module_info = self.modules[module_name]
        print(f" Ejecutando tests del módulo: {module_info['name']}")
        print(f" Ruta: {module_info['path']}")
        print("=" * 60)
        
        try:
            # Importar y ejecutar el módulo de tests
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            module_path = f"tests.{module_name}.test_endpoints"
            
            # Importar el módulo dinámicamente
            import importlib
            test_module = importlib.import_module(module_path)
            
            # Ejecutar la función run_all_tests del módulo
            if hasattr(test_module, 'run_all_tests'):
                test_module.run_all_tests()
                return {'success': True, 'module': module_name}
            else:
                return {'success': False, 'error': f"No se encontró función run_all_tests en {module_path}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Ejecuta todos los tests de todos los módulos.
        
        Returns:
            Dict con resultados de la ejecución
        """
        print(" Ejecutando todos los tests del proyecto")
        print("=" * 60)
        
        results = {}
        total_success = 0
        total_modules = len(self.modules)
        
        for module_name in self.modules:
            print(f"\n Módulo: {self.modules[module_name]['name']}")
            print("-" * 40)
            
            result = self.run_module_tests(module_name)
            results[module_name] = result
            
            if result['success']:
                total_success += 1
                print(f"OK {self.modules[module_name]['name']} - Tests completados")
            else:
                print(f"ERROR {self.modules[module_name]['name']} - Error: {result.get('error', 'Desconocido')}")
        
        print("\n" + "=" * 60)
        print(f" Resumen Final:")
        print(f"OK Módulos exitosos: {total_success}/{total_modules}")
        print(f"ERROR Módulos con errores: {total_modules - total_success}/{total_modules}")
        print(f" Tasa de éxito: {(total_success / total_modules) * 100:.1f}%")
        
        return {
            'success': total_success == total_modules,
            'total_modules': total_modules,
            'successful_modules': total_success,
            'results': results
        }
    
    def list_modules(self) -> None:
        """Lista todos los módulos de tests disponibles"""
        print(" Módulos de tests disponibles:")
        print("=" * 40)
        
        for module_name, info in self.modules.items():
            print(f"🔹 {module_name}")
            print(f"   Nombre: {info['name']}")
            print(f"   Descripción: {info['description']}")
            print(f"   Ruta: {info['path']}")
            print()

def create_test_data() -> Dict[str, Any]:
    """
    Crea datos de prueba comunes para todos los tests.
    
    Returns:
        Dict con datos de prueba
    """
    return {
        'test_orden': {
            'mesa_id': 1,
            'comentarios': 'Orden de prueba',
            'mesero_ids': [1]
        },
        'test_item_orden': {
            'item_id': 1,
            'cantidad': 2,
            'comentarios': 'Sin cebolla'
        },
        'test_mesero': {
            'nombre': 'Test Mesero',
            'activo': True
        },
        'test_mesa': {
            'nombre': 'Mesa Test',
            'capacidad': 4,
            'tipo': 'FAMILIAR',
            'ubicacion': 'Interior'
        }
    }
