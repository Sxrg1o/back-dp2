#!/usr/bin/env python3
"""
Script auxiliar para ejecutar tests QA en ambiente local.
Facilita la ejecución del script de tests bash desde Python.

Uso:
    python tests/qa/run_tests_local.py
    python tests/qa/run_tests_local.py --port 8001
    python tests/qa/run_tests_local.py --url http://localhost:8001
    python tests/qa/run_tests_local.py --verbose
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import urllib.error


class LocalTestRunner:
    """Ejecutor de tests locales para QA."""
    
    def __init__(self, api_url: str = "http://localhost:8000", verbose: bool = False):
        self.api_url = api_url
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent
        self.script_path = self.project_root / "tests" / "qa" / "test_cu05_validaciones_errores.sh"
    
    def check_api_available(self, timeout: int = 5, max_retries: int = 3) -> bool:
        """Verifica si la API está disponible."""
        print(f"Verificando disponibilidad de API en {self.api_url}...")
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(f"{self.api_url}/docs", timeout=timeout)
                if response.status_code == 200:
                    print(f"✓ API disponible")
                    return True
            except requests.exceptions.RequestException as e:
                print(f"  Intento {attempt}/{max_retries} falló: {e}")
                if attempt < max_retries:
                    time.sleep(1)
        
        print("✗ API no disponible")
        return False
    
    def get_api_port(self) -> int:
        """Extrae el puerto de la URL."""
        parsed = urlparse(self.api_url)
        return parsed.port or 8000
    
    def run_tests(self) -> int:
        """Ejecuta el script de tests."""
        
        # Verificar que el script existe
        if not self.script_path.exists():
            print(f"✗ Error: Script no encontrado en {self.script_path}")
            return 1
        
        # Hacer el script ejecutable
        os.chmod(self.script_path, 0o755)
        
        # Preparar variables de ambiente
        env = os.environ.copy()
        env["API_URL"] = self.api_url
        if self.verbose:
            env["VERBOSE"] = "true"
        
        # Cambiar al directorio del proyecto
        original_cwd = os.getcwd()
        os.chdir(self.project_root)
        
        try:
            print(f"\nEjecutando tests desde: {self.project_root}")
            print(f"Script: {self.script_path}")
            print(f"API URL: {self.api_url}")
            print(f"Verbose: {self.verbose}\n")
            
            # Ejecutar el script
            result = subprocess.run(
                ["bash", str(self.script_path)],
                env=env,
                capture_output=False
            )
            
            return result.returncode
        
        except Exception as e:
            print(f"✗ Error ejecutando tests: {e}")
            return 1
        
        finally:
            os.chdir(original_cwd)
    
    def main(self) -> int:
        """Función principal."""
        print("=" * 50)
        print("  Ejecutor de Tests QA - Ambiente Local")
        print("=" * 50)
        print()
        
        # Verificar disponibilidad de API
        if not self.check_api_available():
            print()
            print("Instrucciones para iniciar la API:")
            print()
            print("1. Navega a la carpeta back-dp2:")
            print("   cd back-dp2")
            print()
            print("2. Activa el entorno virtual:")
            print("   # En Windows:")
            print("   .\\venv\\Scripts\\Activate.ps1")
            print("   # En Linux/Mac:")
            print("   source venv/bin/activate")
            print()
            print("3. Ejecuta el servidor:")
            port = self.get_api_port()
            print(f"   python -m uvicorn src.main:app --reload --port {port}")
            print()
            return 1
        
        # Ejecutar tests
        print()
        return self.run_tests()


def main():
    """Punto de entrada."""
    parser = argparse.ArgumentParser(
        description="Ejecutor de tests QA en ambiente local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python tests/qa/run_tests_local.py
  python tests/qa/run_tests_local.py --port 8001
  python tests/qa/run_tests_local.py --url http://localhost:8001
  python tests/qa/run_tests_local.py --verbose
  python tests/qa/run_tests_local.py --port 8001 --verbose
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
        help="Puerto de la API (default: 8000, ignora --url)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Modo verbose (muestra respuestas completas)"
    )
    
    args = parser.parse_args()
    
    # Determinar URL
    if args.port:
        api_url = f"http://localhost:{args.port}"
    elif args.url:
        api_url = args.url
    else:
        api_url = "http://localhost:8000"
    
    # Crear ejecutor y correr tests
    runner = LocalTestRunner(api_url=api_url, verbose=args.verbose)
    return runner.main()


if __name__ == "__main__":
    sys.exit(main())
