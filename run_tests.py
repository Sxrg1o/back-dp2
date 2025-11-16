#!/usr/bin/env python3
"""
Script simple para ejecutar tests QA en ambiente local.
NO requiere dependencias externas, solo Python y bash.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_api_available(url: str = "http://localhost:8000", retries: int = 3) -> bool:
    """Verifica si la API está disponible usando urllib (sin dependencias externas)."""
    import urllib.request
    import urllib.error
    
    print(f"Verificando API en {url}...")
    
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(f"{url}/docs", timeout=3) as response:
                if response.status == 200:
                    print("OK: API disponible")
                    return True
        except Exception as e:
            error_msg = str(e)[:40]
            print(f"  Intento {attempt}/{retries} fallo: {error_msg}")
            if attempt < retries:
                time.sleep(1)
    
    return False

def main():
    """Función principal."""
    print("=" * 60)
    print("  Tests QA - Ambiente Local")
    print("=" * 60)
    print()
    
    # Argumentos
    api_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("--port="):
            port = sys.argv[1].split("=")[1]
            api_url = f"http://localhost:{port}"
        elif sys.argv[1] == "--port" and len(sys.argv) > 2:
            api_url = f"http://localhost:{sys.argv[2]}"
    
    # Verificar que la API está disponible
    if not check_api_available(api_url):
        print()
        print("ERROR: La API no está disponible")
        print()
        print("Asegúrate de tener el servidor corriendo en otra terminal:")
        print("  python -m uvicorn src.main:app --reload")
        print()
        return 1
    
    # Navegar a la carpeta correcta
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Preparar variables de entorno
    env = os.environ.copy()
    env["API_URL"] = api_url
    
    print()
    print("Ejecutando tests...")
    print()
    
    # Ejecutar el script bash
    script_path = project_root / "tests" / "qa" / "test_cu05_validaciones_errores.sh"
    
    try:
        result = subprocess.run(
            ["bash", str(script_path)],
            env=env
        )
        return result.returncode
    except FileNotFoundError:
        print(f"ERROR: No se encontró {script_path}")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
