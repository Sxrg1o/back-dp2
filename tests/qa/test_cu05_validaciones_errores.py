#!/usr/bin/env python3
"""
Script de pruebas para Caso de Uso 5: Validaciones y errores
Autor: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Modulo: Pedidos - Backend
Fecha: 2025-10-29
Adaptado a Python para compatibilidad multiplataforma
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests no está instalado. Instálalo con: pip install requests")
    sys.exit(1)


class Colors:
    """Códigos de color ANSI para la salida."""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color
    
    @classmethod
    def disable(cls):
        """Desactiva los colores (para Windows sin soporte ANSI)."""
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = cls.NC = ''


class TestRunner:
    """Ejecutor de tests para validaciones de pedidos."""
    
    def __init__(self, api_url: str = "http://localhost:8000", verbose: bool = False):
        self.api_url = api_url.rstrip('/')
        self.verbose = verbose
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def check_api_health(self, max_attempts: int = 3) -> bool:
        """Verifica si la API está disponible."""
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Verificando API en {self.api_url}... ", end='')
                response = requests.get(f"{self.api_url}/docs", timeout=5)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}✓ OK{Colors.NC}")
                    return True
            except Exception as e:
                print(f"{Colors.YELLOW}Intento {attempt}/{max_attempts} falló{Colors.NC}")
                if attempt < max_attempts:
                    import time
                    time.sleep(1)
        
        print(f"{Colors.RED}✗ API no disponible en {self.api_url}{Colors.NC}")
        print("\nPor favor, asegúrate de que:")
        print("  1. El servidor está corriendo en", self.api_url)
        print("  2. Te encuentras en el entorno virtual correcto")
        print("\nPara iniciar el servidor localmente, ejecuta:")
        print("  cd back-dp2 && python -m uvicorn src.main:app --reload")
        return False
    
    def run_test(self, test_name: str, expected_status: int, method: str, 
                 endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> bool:
        """Ejecuta un test individual."""
        self.total_tests += 1
        print(f"TC-{self.total_tests:02d}: {test_name}... ", end='')
        
        try:
            url = f"{self.api_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=json_data, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, json=json_data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, timeout=10)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            status_code = response.status_code
            
            if status_code == expected_status:
                print(f"{Colors.GREEN}✓ PASS{Colors.NC} (Status: {status_code})")
                self.passed_tests += 1
                return True
            else:
                print(f"{Colors.RED}✗ FAIL{Colors.NC} (Expected: {expected_status}, Got: {status_code})")
                self.failed_tests += 1
                if self.verbose:
                    print(f"  Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}✗ ERROR{Colors.NC} ({str(e)})")
            self.failed_tests += 1
            return False
    
    def get_mesa_id(self) -> str:
        """Obtiene un ID de mesa válido."""
        print("Obteniendo mesa para tests... ", end='')
        try:
            response = requests.get(f"{self.api_url}/api/v1/mesas?skip=0&limit=1", timeout=10)
            data = response.json()
            if data.get('items') and len(data['items']) > 0:
                mesa_id = data['items'][0]['id']
                print(f"{Colors.GREEN}OK ({mesa_id}){Colors.NC}")
                return mesa_id
        except Exception as e:
            print(f"{Colors.YELLOW}Advertencia: No se encontró mesa válida{Colors.NC}")
        
        return "01JMESA0000000000000000000"
    
    def get_producto_id(self) -> str:
        """Obtiene un ID de producto válido."""
        print("Obteniendo producto para tests... ", end='')
        try:
            response = requests.get(f"{self.api_url}/api/v1/productos?skip=0&limit=1", timeout=10)
            data = response.json()
            if data.get('items') and len(data['items']) > 0:
                producto_id = data['items'][0]['id']
                print(f"{Colors.GREEN}OK ({producto_id}){Colors.NC}")
                return producto_id
        except Exception as e:
            print(f"{Colors.YELLOW}Advertencia: No se encontró producto válido{Colors.NC}")
        
        return "01JPRODUCTO00000000000000000"
    
    def run_all_tests(self) -> int:
        """Ejecuta todos los tests."""
        print("\n" + "=" * 42)
        print("  CU-05: Validaciones y Errores")
        print("=" * 42)
        print()
        print(f"{Colors.BLUE}Configuración{Colors.NC}")
        print(f"API Base URL: {self.api_url}")
        print("Ambiente: Local")
        print()
        
        # Verificar API
        if not self.check_api_health():
            return 1
        
        # Info de Git
        try:
            commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], 
                                                  stderr=subprocess.DEVNULL).decode().strip()
            rama = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                          stderr=subprocess.DEVNULL).decode().strip()
        except:
            commit_hash = "N/A"
            rama = "N/A"
        
        print(f"Commit: {commit_hash}")
        print(f"Rama: {rama}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # === Tests de Validación de Mesa ===
        print("=== Tests de Validación de Mesa ===")
        print()
        
        # TC-001: Mesa inexistente (formato inválido detectado por schema)
        self.run_test(
            "Mesa inexistente debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": "01INVALID000000000000000000",
                "items": [{
                    "id_producto": "01JTEST0000000000000000000",
                    "cantidad": 1,
                    "precio_unitario": 25.50,
                    "opciones": []
                }]
            }
        )
        
        # TC-002: Mesa vacía
        self.run_test(
            "Mesa vacía debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": "",
                "items": [{
                    "id_producto": "01JTEST0000000000000000000",
                    "cantidad": 1,
                    "precio_unitario": 25.50,
                    "opciones": []
                }]
            }
        )
        
        print()
        print("=== Tests de Validación de Productos ===")
        print()
        
        # Obtener IDs válidos
        mesa_id = self.get_mesa_id()
        
        # TC-003: Producto inexistente (formato inválido detectado por schema)
        self.run_test(
            "Producto inexistente debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": [{
                    "id_producto": "01INVALID000000000000000000",
                    "cantidad": 1,
                    "precio_unitario": 25.50,
                    "opciones": []
                }]
            }
        )
        
        producto_id = self.get_producto_id()
        
        print()
        print("=== Tests de Validación de Cantidad ===")
        print()
        
        # TC-004: Cantidad = 0
        self.run_test(
            "Cantidad = 0 debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": [{
                    "id_producto": producto_id,
                    "cantidad": 0,
                    "precio_unitario": 25.50,
                    "opciones": []
                }]
            }
        )
        
        # TC-005: Cantidad negativa
        self.run_test(
            "Cantidad negativa debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": [{
                    "id_producto": producto_id,
                    "cantidad": -5,
                    "precio_unitario": 25.50,
                    "opciones": []
                }]
            }
        )
        
        print()
        print("=== Tests de Validación de Precio ===")
        print()
        
        # TC-006: Precio = 0
        self.run_test(
            "Precio = 0 debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": [{
                    "id_producto": producto_id,
                    "cantidad": 1,
                    "precio_unitario": 0,
                    "opciones": []
                }]
            }
        )
        
        # TC-007: Precio negativo
        self.run_test(
            "Precio negativo debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": [{
                    "id_producto": producto_id,
                    "cantidad": 1,
                    "precio_unitario": -25.50,
                    "opciones": []
                }]
            }
        )
        
        print()
        print("=== Tests de Validación de Items Vacíos ===")
        print()
        
        # TC-008: Items vacío
        self.run_test(
            "Items vacío debe retornar 422",
            422,
            "POST",
            "/api/v1/pedidos/completo",
            {
                "id_mesa": mesa_id,
                "items": []
            }
        )
        
        print()
        print("=== Tests de Validación de Pedido Inexistente ===")
        print()
        
        # TC-009: GET pedido inexistente
        self.run_test(
            "GET pedido inexistente debe retornar 404",
            404,
            "GET",
            "/api/v1/pedidos/01INVALID000000000000000000"
        )
        
        # TC-010: PATCH pedido inexistente (formato inválido detectado por schema)
        self.run_test(
            "PATCH estado de pedido inexistente debe retornar 422",
            422,
            "PATCH",
            "/api/v1/pedidos/01INVALID000000000000000000/estado",
            {"estado": "CONFIRMADO"}
        )
        
        # TC-011: DELETE pedido inexistente
        self.run_test(
            "DELETE pedido inexistente debe retornar 404",
            404,
            "DELETE",
            "/api/v1/pedidos/01INVALID000000000000000000"
        )
        
        # Resumen
        print()
        print("=" * 42)
        print("  Resumen de Tests")
        print("=" * 42)
        print(f"Total:  {self.total_tests}")
        print(f"Pasados: {Colors.GREEN}{self.passed_tests}{Colors.NC}")
        print(f"Fallidos: {Colors.RED}{self.failed_tests}{Colors.NC}")
        
        porcentaje = (self.passed_tests * 100) // self.total_tests if self.total_tests > 0 else 0
        print(f"Éxito: {Colors.BLUE}{porcentaje}%{Colors.NC}")
        print()
        
        if self.failed_tests == 0:
            print(f"{Colors.GREEN}✓ Todos los tests pasaron{Colors.NC}")
            return 0
        else:
            print(f"{Colors.RED}✗ Algunos tests fallaron{Colors.NC}")
            print()
            print("Instrucciones para ejecutar en LOCAL:")
            print("  1. Abre una terminal en la carpeta 'back-dp2'")
            print("  2. Activa el entorno virtual:")
            print("     Windows: venv\\Scripts\\activate")
            print("     Linux/Mac: source venv/bin/activate")
            print("  3. Ejecuta el servidor: python -m uvicorn src.main:app --reload")
            print("  4. En otra terminal, ejecuta este script:")
            print("     python tests/qa/test_cu05_validaciones_errores.py")
            return 1


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Tests de validaciones para CU-05 (Pedidos)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python test_cu05_validaciones_errores.py
  python test_cu05_validaciones_errores.py --url http://localhost:8001
  python test_cu05_validaciones_errores.py --verbose
  python test_cu05_validaciones_errores.py --port 8001 -v
        """
    )
    
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="URL de la API (default: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Puerto de la API (default: 8000)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verbose (muestra respuestas completas en fallos)"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desactiva los colores en la salida"
    )
    
    args = parser.parse_args()
    
    # Desactivar colores si se solicita
    if args.no_color or os.name == 'nt':
        # En Windows, activar soporte ANSI si está disponible
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            Colors.disable()
    
    # Determinar URL
    api_url = os.environ.get('API_URL')
    if args.port:
        api_url = f"http://localhost:{args.port}"
    elif args.url:
        api_url = args.url
    elif not api_url:
        api_url = "http://localhost:8000"
    
    # Ejecutar tests
    runner = TestRunner(api_url=api_url, verbose=args.verbose)
    return runner.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
