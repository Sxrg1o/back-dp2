#!/usr/bin/env python3
"""
Script de validación simplificado para Historia de Usuario: Pantalla Inicial
Autor: Equipo QA
Fecha: 2025-10-09
Adaptado para: Windows Local

Versión simplificada que usa solo librerías estándar de Python.

Historia de Usuario:
"El producto de software deberá mostrar una pantalla inicial, incluyendo 
pestañas importantes como Mi Orden (Visualizar pedidos seleccionados) y 
Menú (Visualizar platos por categoría)"
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time
from typing import List, Dict, Any, Optional

# Configuración - LOCALHOST
API_URL = "http://localhost:8000"
TIMEOUT = 30  # segundos

# Colores para output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


class SimpleHTTPClient:
    """Cliente HTTP simple usando urllib"""
    
    def __init__(self, base_url: str, timeout: int = TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """Realiza una petición GET y retorna la respuesta"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                duration_ms = int((time.time() - start_time) * 1000)
                
                data = response.read().decode('utf-8')
                json_data = json.loads(data) if data else {}
                
                return {
                    'status_code': response.getcode(),
                    'data': json_data,
                    'duration_ms': duration_ms
                }
                
        except urllib.error.HTTPError as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                'status_code': e.code,
                'data': {},
                'duration_ms': duration_ms,
                'error': str(e)
            }
        except Exception as e:
            return {
                'status_code': 0,
                'data': {},
                'duration_ms': 0,
                'error': str(e)
            }


class PantallaInicialTesterSimple:
    """Tester simplificado para la pantalla inicial"""
    
    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url
        self.client = SimpleHTTPClient(api_url)
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
        
        # Datos recolectados
        self.categorias = []
        self.productos = []
    
    def log_test(self, name: str, passed: bool, message: str, duration_ms: int = 0):
        """Registra y muestra el resultado de un test"""
        self.tests_total += 1
        
        if passed:
            self.tests_passed += 1
            status = f"{Colors.GREEN}✓ PASS{Colors.NC}"
        else:
            self.tests_failed += 1
            status = f"{Colors.RED}✗ FAIL{Colors.NC}"
        
        duration_str = f" ({duration_ms}ms)" if duration_ms > 0 else ""
        print(f"Test {self.tests_total}: {name}... {status}{duration_str}")
        if message:
            print(f"  {message}")
    
    def test_health_check(self):
        """Test 1: Verificar que el backend está activo"""
        print(f"\n{Colors.CYAN}=== Test 1: Health Check ==={Colors.NC}")
        
        response = self.client.get("/health")
        
        if response['status_code'] == 200:
            self.log_test(
                "Backend está activo",
                True,
                f"API respondiendo en {self.api_url}",
                response['duration_ms']
            )
            return True
        else:
            self.log_test(
                "Backend está activo",
                False,
                f"Error: {response.get('error', 'Unknown')}"
            )
            return False
    
    def test_get_categorias(self):
        """Test 2: Obtener categorías del menú"""
        print(f"\n{Colors.CYAN}=== Test 2: Obtener Categorías ==={Colors.NC}")
        
        response = self.client.get("/api/v1/categorias")
        
        if response['status_code'] == 200:
            data = response['data']
            self.categorias = data.get('items', [])
            
            self.log_test(
                "GET /api/v1/categorias",
                True,
                f"Obtenidas {len(self.categorias)} categorías",
                response['duration_ms']
            )
            
            if self.categorias:
                print(f"\n  Categorías encontradas:")
                for cat in self.categorias[:5]:
                    print(f"    - {cat.get('nombre', 'N/A')}")
                if len(self.categorias) > 5:
                    print(f"    ... y {len(self.categorias) - 5} más")
            
            return True
        else:
            self.log_test(
                "GET /api/v1/categorias",
                False,
                f"Status: {response['status_code']}"
            )
            return False
    
    def test_get_productos(self):
        """Test 3: Obtener productos del menú"""
        print(f"\n{Colors.CYAN}=== Test 3: Obtener Productos ==={Colors.NC}")
        
        response = self.client.get("/api/v1/productos-menu?limit=50")
        
        if response['status_code'] == 200:
            data = response['data']
            self.productos = data.get('items', [])
            
            self.log_test(
                "GET /api/v1/productos-menu",
                True,
                f"Obtenidos {len(self.productos)} productos",
                response['duration_ms']
            )
            
            if self.productos:
                print(f"\n  Productos encontrados:")
                for prod in self.productos[:5]:
                    nombre = prod.get('nombre', 'N/A')
                    precio = prod.get('precio_base', 0)
                    print(f"    - {nombre}: S/{precio}")
                if len(self.productos) > 5:
                    print(f"    ... y {len(self.productos) - 5} más")
            
            return True
        else:
            self.log_test(
                "GET /api/v1/productos-menu",
                False,
                f"Status: {response['status_code']}"
            )
            return False
    
    def test_productos_por_categoria(self):
        """Test 4: Filtrar productos por categoría"""
        print(f"\n{Colors.CYAN}=== Test 4: Productos por Categoría ==={Colors.NC}")
        
        if not self.categorias:
            self.log_test(
                "Filtrar productos por categoría",
                False,
                "No hay categorías disponibles para probar"
            )
            return False
        
        # Probar con la primera categoría
        primera_categoria = self.categorias[0]
        cat_id = primera_categoria.get('id')
        cat_nombre = primera_categoria.get('nombre', 'N/A')
        
        response = self.client.get(f"/api/v1/productos-menu?id_categoria={cat_id}")
        
        if response['status_code'] == 200:
            data = response['data']
            productos_filtrados = data.get('items', [])
            
            self.log_test(
                f"Filtrar por categoría '{cat_nombre}'",
                True,
                f"Encontrados {len(productos_filtrados)} productos",
                response['duration_ms']
            )
            return True
        else:
            self.log_test(
                f"Filtrar por categoría '{cat_nombre}'",
                False,
                f"Status: {response['status_code']}"
            )
            return False
    
    def test_validar_estructura_producto(self):
        """Test 5: Validar estructura de datos de productos"""
        print(f"\n{Colors.CYAN}=== Test 5: Validar Estructura de Productos ==={Colors.NC}")
        
        if not self.productos:
            self.log_test(
                "Validar estructura de productos",
                False,
                "No hay productos disponibles para validar"
            )
            return False
        
        producto = self.productos[0]
        campos_requeridos = ['id', 'nombre', 'precio_base', 'id_categoria']
        campos_faltantes = [campo for campo in campos_requeridos if campo not in producto]
        
        if not campos_faltantes:
            self.log_test(
                "Validar campos requeridos en productos",
                True,
                f"Todos los campos presentes: {', '.join(campos_requeridos)}"
            )
            return True
        else:
            self.log_test(
                "Validar campos requeridos en productos",
                False,
                f"Campos faltantes: {', '.join(campos_faltantes)}"
            )
            return False
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print("="*60)
        print("  Tests de Pantalla Inicial - HU-C02")
        print("="*60)
        print(f"API Base URL: {self.api_url}")
        print()
        
        # Ejecutar tests en orden
        if not self.test_health_check():
            print(f"\n{Colors.RED}El backend no está disponible. Abortando tests.{Colors.NC}")
            return 1
        
        self.test_get_categorias()
        self.test_get_productos()
        self.test_productos_por_categoria()
        self.test_validar_estructura_producto()
        
        # Resumen
        print("\n" + "="*60)
        print("  RESUMEN DE TESTS")
        print("="*60)
        print(f"Total de tests: {self.tests_total}")
        print(f"Tests pasados: {Colors.GREEN}{self.tests_passed}{Colors.NC}")
        print(f"Tests fallados: {Colors.RED}{self.tests_failed}{Colors.NC}")
        print("="*60)
        print()
        
        if self.tests_failed == 0:
            print(f"{Colors.GREEN}✓ Todos los tests pasaron{Colors.NC}")
            return 0
        else:
            print(f"{Colors.RED}✗ Algunos tests fallaron{Colors.NC}")
            return 1


def main():
    """Función principal"""
    tester = PantallaInicialTesterSimple()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
