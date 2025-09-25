#!/usr/bin/env python3
"""
Script de configuración para el proyecto Menu API
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(e.stderr)
        return False

def main():
    """Función principal de configuración"""
    print("🚀 Configurando Menu API...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detectado")
    
    # Crear entorno virtual
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creando entorno virtual"):
            sys.exit(1)
    else:
        print("✅ Entorno virtual ya existe")
    
    # Determinar comando de activación según el SO
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Instalar dependencias
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias"):
        sys.exit(1)
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    if not run_command(f"{pip_cmd} list", "Listando paquetes instalados"):
        sys.exit(1)
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Activar entorno virtual:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Ejecutar la aplicación:")
    print("   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    print("3. Visitar la documentación:")
    print("   http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
