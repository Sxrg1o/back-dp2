#!/usr/bin/env python3
"""
Script para verificar que el proyecto está listo para desplegar en Render.
"""
import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_python_syntax(file_path):
    """Verifica que un archivo Python tiene sintaxis correcta"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        print(f"✅ Sintaxis Python OK: {file_path}")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en {file_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  No se pudo verificar {file_path}: {e}")
        return False

def check_imports():
    """Verifica que las importaciones funcionan"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from app.main import app
        print("✅ Importaciones principales funcionan")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def check_requirements():
    """Verifica que requirements.txt tiene las dependencias necesarias"""
    required_packages = ['fastapi', 'uvicorn', 'pydantic']
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        missing = []
        for package in required_packages:
            if package not in content:
                missing.append(package)
        
        if missing:
            print(f"❌ Faltan dependencias en requirements.txt: {missing}")
            return False
        else:
            print("✅ requirements.txt tiene las dependencias necesarias")
            return True
    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {e}")
        return False

def check_endpoints():
    """Verifica que los endpoints principales existen"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from app.main import app
        
        # Verificar endpoints críticos
        critical_endpoints = ['/health', '/docs', '/api/menu/items']
        
        routes = [route.path for route in app.routes]
        missing = []
        
        for endpoint in critical_endpoints:
            if endpoint not in routes:
                missing.append(endpoint)
        
        if missing:
            print(f"❌ Faltan endpoints críticos: {missing}")
            return False
        else:
            print("✅ Endpoints críticos están disponibles")
            return True
    except Exception as e:
        print(f"❌ Error verificando endpoints: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 Verificando proyecto para despliegue en Render...")
    print("=" * 60)
    
    checks = []
    
    # Verificar archivos de configuración
    print("\n📁 Verificando archivos de configuración:")
    checks.append(check_file_exists('requirements.txt', 'Dependencias'))
    checks.append(check_file_exists('Procfile', 'Comando de inicio'))
    checks.append(check_file_exists('runtime.txt', 'Versión de Python'))
    checks.append(check_file_exists('render.yaml', 'Configuración Render'))
    
    # Verificar archivos principales
    print("\n🐍 Verificando archivos principales:")
    checks.append(check_file_exists('app/main.py', 'Punto de entrada'))
    checks.append(check_file_exists('app/__init__.py', 'Paquete app'))
    
    # Verificar sintaxis Python
    print("\n🔧 Verificando sintaxis Python:")
    checks.append(check_python_syntax('app/main.py'))
    
    # Verificar importaciones
    print("\n📦 Verificando importaciones:")
    checks.append(check_imports())
    
    # Verificar dependencias
    print("\n📋 Verificando dependencias:")
    checks.append(check_requirements())
    
    # Verificar endpoints
    print("\n🌐 Verificando endpoints:")
    checks.append(check_endpoints())
    
    # Resumen
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    
    print(f"📊 Resumen: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Proyecto listo para desplegar en Render!")
        print("\n📋 Próximos pasos:")
        print("1. Subir código a GitHub")
        print("2. Crear servicio en Render")
        print("3. Configurar variables de entorno")
        print("4. Desplegar y probar")
        return 0
    else:
        print("❌ Hay problemas que resolver antes del despliegue")
        print("Revisa los errores arriba y corrígelos")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
