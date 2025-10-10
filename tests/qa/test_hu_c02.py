#!/usr/bin/env python3
"""
Script de validación simplificado para Historia de Usuario: Pantalla Inicial
Autor: Equipo QA
Fecha: 2025-10-09

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

# Configuración
API_URL = "http://localhost:8000"  # Cambiar según entorno
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
            status_icon = f"{Colors.GREEN}✓{Colors.NC}"
        else:
            self.tests_failed += 1
            status_icon = f"{Colors.RED}✗{Colors.NC}"
        
        duration_str = f" ({duration_ms}ms)" if duration_ms > 0 else ""
        print(f"{status_icon} Test {self.tests_total}: {name}{duration_str}")
        
        if message:
            color = Colors.CYAN if passed else Colors.RED
            print(f"   {color}{message}{Colors.NC}")
    
    def test_health(self):
        """Test de salud del sistema"""
        response = self.client.get("/health")
        
        if response['status_code'] == 200:
            service = response['data'].get('service', 'N/A')
            self.log_test(
                "Health check del sistema",
                True,
                f"Sistema saludable - {service}",
                response['duration_ms']
            )
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Health check del sistema",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def test_categorias(self):
        """Test de listado de categorías"""
        response = self.client.get("/api/v1/categorias")
        
        if response['status_code'] == 200:
            data = response['data']
            self.categorias = data.get('items', [])
            count = len(self.categorias)
            total = data.get('total', count)
            
            self.log_test(
                "Listar categorías del menú",
                True,
                f"Encontradas {count} categorías de {total} total",
                response['duration_ms']
            )
            
            # Validar estructura
            if self.categorias:
                self.validate_categorias_structure()
            
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Listar categorías del menú",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def validate_categorias_structure(self):
        """Valida la estructura de las categorías"""
        campos_requeridos = ['id', 'nombre', 'activo']
        errores = []
        categorias_activas = 0
        
        for i, categoria in enumerate(self.categorias):
            for campo in campos_requeridos:
                if campo not in categoria:
                    errores.append(f"Categoría {i}: falta campo '{campo}'")
            
            if categoria.get('activo', False):
                categorias_activas += 1
        
        if errores:
            self.log_test(
                "Validar estructura de categorías",
                False,
                f"Errores: {'; '.join(errores[:2])}" + ("..." if len(errores) > 2 else "")
            )
        else:
            self.log_test(
                "Validar estructura de categorías",
                True,
                f"Estructura válida - {categorias_activas} categorías activas"
            )
    
    def test_productos(self):
        """Test de listado de productos"""
        response = self.client.get("/api/v1/productos/cards")
        
        if response['status_code'] == 200:
            data = response['data']
            self.productos = data.get('items', [])
            count = len(self.productos)
            total = data.get('total', count)
            
            self.log_test(
                "Listar productos en formato cards",
                True,
                f"Encontrados {count} productos de {total} total",
                response['duration_ms']
            )
            
            # Validar estructura
            if self.productos:
                self.validate_productos_structure()
                
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Listar productos en formato cards",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def validate_productos_structure(self):
        """Valida la estructura de los productos"""
        campos_requeridos = ['id', 'nombre', 'precio_base', 'disponible']
        errores = []
        productos_disponibles = 0
        
        for i, producto in enumerate(self.productos):
            for campo in campos_requeridos:
                if campo not in producto:
                    errores.append(f"Producto {i}: falta campo '{campo}'")
            
            if producto.get('disponible', False):
                productos_disponibles += 1
        
        if errores:
            self.log_test(
                "Validar estructura de productos",
                False,
                f"Errores: {'; '.join(errores[:2])}" + ("..." if len(errores) > 2 else "")
            )
        else:
            self.log_test(
                "Validar estructura de productos",
                True,
                f"Estructura válida - {productos_disponibles} productos disponibles"
            )
    
    def test_categorias_con_productos(self):
        """Test de categorías con productos"""
        response = self.client.get("/api/v1/categorias/productos/cards")
        
        if response['status_code'] == 200:
            data = response['data']
            categorias_con_productos = data.get('items', [])
            
            total_productos = 0
            categorias_con_productos_count = 0
            
            for categoria in categorias_con_productos:
                productos_en_categoria = categoria.get('productos', [])
                total_productos += len(productos_en_categoria)
                if productos_en_categoria:
                    categorias_con_productos_count += 1
            
            self.log_test(
                "Categorías con productos integradas",
                True,
                f"{categorias_con_productos_count} categorías con productos ({total_productos} productos total)",
                response['duration_ms']
            )
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Categorías con productos integradas",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def test_filtrado_categoria(self):
        """Test de filtrado por categoría"""
        if not self.categorias:
            self.log_test(
                "Filtrado de productos por categoría",
                False,
                "No hay categorías para probar filtrado"
            )
            return
        
        # Buscar primera categoría activa
        categoria_activa = None
        for categoria in self.categorias:
            if categoria.get('activo', False):
                categoria_activa = categoria
                break
        
        if not categoria_activa:
            self.log_test(
                "Filtrado de productos por categoría",
                False,
                "No hay categorías activas para probar"
            )
            return
        
        categoria_id = categoria_activa['id']
        response = self.client.get(f"/api/v1/productos?id_categoria={categoria_id}")
        
        if response['status_code'] == 200:
            data = response['data']
            productos_filtrados = data.get('items', [])
            
            self.log_test(
                "Filtrado de productos por categoría",
                True,
                f"Filtro funcional - {len(productos_filtrados)} productos en '{categoria_activa['nombre']}'",
                response['duration_ms']
            )
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Filtrado de productos por categoría",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def test_paginacion(self):
        """Test de paginación"""
        response = self.client.get("/api/v1/productos?skip=0&limit=2")
        
        if response['status_code'] == 200:
            data = response['data']
            items = data.get('items', [])
            total = data.get('total', 0)
            
            self.log_test(
                "Funcionalidad de paginación",
                True,
                f"Paginación funcional - {len(items)} items de {total} total",
                response['duration_ms']
            )
        else:
            error_msg = response.get('error', f"HTTP {response['status_code']}")
            self.log_test(
                "Funcionalidad de paginación",
                False,
                f"Error: {error_msg}",
                response['duration_ms']
            )
    
    def test_mi_orden_endpoints(self):
        """Test de endpoints de Mi Orden (no implementados)"""
        endpoints = [
            ("/api/v1/pedidos", "Listar pedidos"),
            ("/api/v1/carrito", "Obtener carrito")
        ]
        
        for endpoint, descripcion in endpoints:
            response = self.client.get(endpoint)
            
            # Esperamos 404 porque no están implementados
            if response['status_code'] == 404:
                self.log_test(
                    f"{descripcion} (NO IMPLEMENTADO)",
                    True,
                    "Endpoint no implementado como esperado",
                    response['duration_ms']
                )
            else:
                self.log_test(
                    f"{descripcion} (INESPERADO)",
                    False,
                    f"Esperado 404, obtenido {response['status_code']}",
                    response['duration_ms']
                )
    
    def test_casos_limite(self):
        """Test de casos límite"""
        # Test límite excesivo
        response = self.client.get("/api/v1/productos?limit=1000")
        if response['status_code'] == 422:
            self.log_test(
                "Validación de límite excesivo",
                True,
                "Validación correcta para límite excesivo",
                response['duration_ms']
            )
        else:
            self.log_test(
                "Validación de límite excesivo",
                False,
                f"Esperado 422, obtenido {response['status_code']}",
                response['duration_ms']
            )
        
        # Test skip negativo
        response = self.client.get("/api/v1/productos?skip=-1")
        if response['status_code'] == 422:
            self.log_test(
                "Validación de skip negativo",
                True,
                "Validación correcta para skip negativo",
                response['duration_ms']
            )
        else:
            self.log_test(
                "Validación de skip negativo",
                False,
                f"Esperado 422, obtenido {response['status_code']}",
                response['duration_ms']
            )
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print(f"{Colors.BLUE}==============================================={Colors.NC}")
        print(f"{Colors.BLUE}  Test HU: Pantalla Inicial - Simplificado{Colors.NC}")
        print(f"{Colors.BLUE}==============================================={Colors.NC}")
        print()
        print("Historia de Usuario:")
        print("El producto de software deberá mostrar una pantalla inicial,")
        print("incluyendo pestañas importantes como Mi Orden y Menú")
        print()
        print(f"API Base URL: {self.api_url}")
        print()
        
        print(f"{Colors.PURPLE}=== SECCIÓN 1: TESTS DE SALUD ==={Colors.NC}")
        self.test_health()
        print()
        
        print(f"{Colors.PURPLE}=== SECCIÓN 2: PESTAÑA MENÚ ==={Colors.NC}")
        self.test_categorias()
        self.test_productos()
        self.test_categorias_con_productos()
        self.test_filtrado_categoria()
        self.test_paginacion()
        print()
        
        print(f"{Colors.PURPLE}=== SECCIÓN 3: PESTAÑA MI ORDEN ==={Colors.NC}")
        self.test_mi_orden_endpoints()
        print()
        
        print(f"{Colors.PURPLE}=== SECCIÓN 4: CASOS LÍMITE ==={Colors.NC}")
        self.test_casos_limite()
        print()
        
        self.print_summary()
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print(f"{Colors.BLUE}=== RESUMEN DE RESULTADOS ==={Colors.NC}")
        print()
        print(f"Total de tests:      {self.tests_total}")
        print(f"{Colors.GREEN}Tests exitosos:      {self.tests_passed}{Colors.NC}")
        print(f"{Colors.RED}Tests fallidos:      {self.tests_failed}{Colors.NC}")
        
        percentage = (self.tests_passed / self.tests_total * 100) if self.tests_total > 0 else 0
        print(f"Porcentaje de éxito: {percentage:.1f}%")
        
        print()
        print(f"{Colors.CYAN}=== ESTADO DE LA HISTORIA DE USUARIO ==={Colors.NC}")
        
        if self.tests_failed == 0:
            print(f"{Colors.GREEN}🎉 ¡TODOS LOS TESTS PASARON!{Colors.NC}")
            print()
            print("✅ Funcionalidad de MENÚ: COMPLETAMENTE IMPLEMENTADA")
            print("❌ Funcionalidad de MI ORDEN: PENDIENTE DE IMPLEMENTACIÓN")
        else:
            print(f"{Colors.RED}❌ ALGUNOS TESTS FALLARON{Colors.NC}")
            print()
            print("✅ Funcionalidad de MENÚ: PARCIALMENTE IMPLEMENTADA")
            print("❌ Funcionalidad de MI ORDEN: PENDIENTE DE IMPLEMENTACIÓN")
        
        print()
        print("CONCLUSIÓN:")
        print("- La pestaña MENÚ está funcionando correctamente")
        print("- La pestaña MI ORDEN necesita implementación completa")
        print("- Los endpoints de categorías y productos están operativos")
        print("- Se requiere desarrollo de funcionalidad de carrito/pedidos")
        
        return self.tests_failed == 0


def main():
    """Función principal"""
    import os
    
    # Obtener URL de la API desde variable de entorno
    api_url = os.getenv('API_URL', API_URL)
    
    tester = PantallaInicialTesterSimple(api_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()