#!/usr/bin/env python3
"""
Script de pruebas para Caso de Uso 6: Crear sesión
Autor: Kevin Antonio Navarro Carrera
Equipo: QA/SEG
Modulo: Sesiones - Backend
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
    """Ejecutor de tests para creación de sesiones."""
    
    def __init__(self, api_url: str = "http://localhost:8000", verbose: bool = False):
        self.api_url = api_url.rstrip('/')
        self.verbose = verbose
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.sesion_id = None
        self.local_id = None
        
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
                 endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """Ejecuta un test individual y retorna la respuesta."""
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
                try:
                    return response.json()
                except:
                    return None
            else:
                print(f"{Colors.RED}✗ FAIL{Colors.NC} (Expected: {expected_status}, Got: {status_code})")
                self.failed_tests += 1
                if self.verbose:
                    print(f"  Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"{Colors.RED}✗ ERROR{Colors.NC} ({str(e)})")
            self.failed_tests += 1
            return None
    
    def validate_test(self, test_name: str, condition: bool, expected: str = "", actual: str = ""):
        """Ejecuta una validación sin hacer request HTTP."""
        self.total_tests += 1
        print(f"TC-{self.total_tests:02d}: {test_name}... ", end='')
        
        if condition:
            print(f"{Colors.GREEN}✓ PASS{Colors.NC}", end='')
            if actual:
                print(f" ({actual})")
            else:
                print()
            self.passed_tests += 1
        else:
            print(f"{Colors.RED}✗ FAIL{Colors.NC}", end='')
            if expected and actual:
                print(f" (Expected: {expected}, Got: {actual})")
            else:
                print()
            self.failed_tests += 1
    
    def get_local_id(self) -> Optional[str]:
        """Obtiene un ID de local válido."""
        print("Obteniendo ID de local... ", end='')
        try:
            response = requests.get(f"{self.api_url}/api/v1/locales?limit=1", timeout=10)
            data = response.json()
            if data.get('items') and len(data['items']) > 0:
                local_id = data['items'][0]['id']
                print(f"{Colors.GREEN}✓{Colors.NC} Local ID: {local_id}")
                return local_id
        except Exception as e:
            print(f"{Colors.RED}✗ No se encontraron locales{Colors.NC}")
        
        return None
    
    def run_all_tests(self) -> int:
        """Ejecuta todos los tests."""
        print("\n" + "=" * 42)
        print("  CU-06: Crear Sesión")
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
        
        # === Preparación ===
        print("=== Preparación: Obtener ID de local ===")
        print()
        
        self.local_id = self.get_local_id()
        if not self.local_id:
            print(f"{Colors.RED}Error: No se pudo obtener un local válido{Colors.NC}")
            return 1
        
        print()
        print("=== Tests de Creación de Sesión ===")
        print()
        
        # TC-001: Crear sesión nueva
        sesion_data = self.run_test(
            "Crear sesión nueva",
            201,
            "POST",
            "/api/v1/sesiones/",
            {
                "id_local": self.local_id,
                "estado": "activo",
                "id_domotica": "TEST-DOM-001"
            }
        )
        
        if sesion_data:
            self.sesion_id = sesion_data.get('id')
            
            # TC-002: Validar que la sesión tiene ID generado (ULID)
            self.validate_test(
                "Validar que sesión tiene ID generado (ULID)",
                self.sesion_id is not None and len(self.sesion_id) == 26,
                "ULID de 26 caracteres",
                f"ID: {self.sesion_id}" if self.sesion_id else "ID vacío"
            )
            
            # TC-003: Validar estado inicial es ACTIVO
            estado = sesion_data.get('estado')
            self.validate_test(
                "Validar que estado es activo",
                estado == "activo",
                "activo",
                f"Estado: {estado}"
            )
            
            # TC-004: Validar que tiene id_local correcto
            id_local_resp = sesion_data.get('id_local')
            self.validate_test(
                "Validar que id_local es correcto",
                id_local_resp == self.local_id,
                self.local_id,
                f"ID Local: {id_local_resp}"
            )
            
            # TC-005: Validar que tiene fecha_inicio (no null)
            fecha_inicio = sesion_data.get('fecha_inicio')
            self.validate_test(
                "Validar que fecha_inicio no es null",
                fecha_inicio is not None and fecha_inicio != 'null',
                "timestamp válido",
                f"Fecha inicio: {fecha_inicio}"
            )
            
            # TC-006: Validar que fecha_fin es null (sesión activa)
            fecha_fin = sesion_data.get('fecha_fin')
            self.validate_test(
                "Validar que fecha_fin es null (sesión activa)",
                fecha_fin is None or fecha_fin == 'null',
                "null",
                f"fecha_fin: {fecha_fin}"
            )
        else:
            print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No se pudo crear sesión, saltando validaciones")
        
        print()
        print("=== Tests de Consulta de Sesión ===")
        print()
        
        if self.sesion_id:
            # TC-007: Obtener sesión por ID
            self.run_test(
                "Obtener sesión por ID (GET /sesiones/{id})",
                200,
                "GET",
                f"/api/v1/sesiones/{self.sesion_id}"
            )
        else:
            print(f"{Colors.YELLOW}⚠ SKIP{Colors.NC} - No se pudo crear sesión")
        
        print()
        print("=== Tests de Validación ===")
        print()
        
        # TC-008: Crear sesión con local inexistente (validación de negocio)
        self.run_test(
            "Crear sesión con local inexistente debe retornar 400",
            400,
            "POST",
            "/api/v1/sesiones/",
            {
                "id_local": "01INVALID000000000000000000",
                "estado": "activo",
                "id_domotica": "TEST-DOM-001"
            }
        )
        
        # TC-009: Crear sesión con estado inválido
        self.run_test(
            "Crear sesión con estado inválido debe retornar 422",
            422,
            "POST",
            "/api/v1/sesiones/",
            {
                "id_local": self.local_id,
                "estado": "ESTADO_INVALIDO"
            }
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
            return 1


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Tests de creación de sesiones para CU-06",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python test_cu06_crear_sesion.py
  python test_cu06_crear_sesion.py --url http://localhost:8001
  python test_cu06_crear_sesion.py --verbose
  python test_cu06_crear_sesion.py --port 8001 -v
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
