#!/usr/bin/env python3
"""
Script de demostración que muestra cómo usar todos los scripts de prueba.
"""

import subprocess
import sys
import time
import os

def print_header(title: str):
    """Imprime un encabezado con estilo."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step: int, description: str):
    """Imprime un paso numerado."""
    print(f"\n📋 PASO {step}: {description}")
    print("-" * 40)

def run_demo_command(command: str, description: str):
    """Ejecuta un comando de demostración."""
    print(f"\n💻 Comando: {command}")
    print(f"📝 Descripción: {description}")
    print("⏳ Ejecutando...")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Comando ejecutado exitosamente")
            if result.stdout:
                print("📄 Salida:")
                print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        else:
            print("❌ Comando falló")
            if result.stderr:
                print("📄 Error:")
                print(result.stderr[:300] + "..." if len(result.stderr) > 300 else result.stderr)
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Comando tardó demasiado")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal de demostración."""
    print("🎬 DEMOSTRACIÓN DE SCRIPTS DE PRUEBA")
    print("="*60)
    print("Este script demuestra cómo usar todos los scripts de prueba")
    print("del microservicio de menú paso a paso.")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: No se encontró main.py")
        print("💡 Asegúrate de estar en el directorio del microservicio")
        return
    
    print_header("VERIFICACIÓN INICIAL")
    print("🔍 Verificando archivos de prueba...")
    
    test_files = [
        "test_all_endpoints.py",
        "quick_test.py", 
        "diagnose_db.py",
        "test_service_connectivity.py",
        "run_all_tests.py"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - No encontrado")
    
    print_header("DEMOSTRACIÓN PASO A PASO")
    
    print_step(1, "Diagnóstico de Base de Datos")
    print("Primero verificamos si la base de datos está en buen estado...")
    run_demo_command("python diagnose_db.py", "Diagnóstico completo de la base de datos")
    
    print_step(2, "Verificación de Conectividad")
    print("Luego verificamos si el servicio está ejecutándose...")
    run_demo_command("python test_service_connectivity.py", "Prueba de conectividad del servicio")
    
    print_step(3, "Prueba Rápida")
    print("Si el servicio está funcionando, hacemos una prueba rápida...")
    run_demo_command("python quick_test.py", "Prueba rápida de endpoints principales")
    
    print_step(4, "Prueba Completa (Opcional)")
    print("Para un análisis completo, ejecutamos todas las pruebas...")
    print("⚠️ Nota: Este paso puede tardar varios minutos")
    
    response = input("¿Deseas ejecutar la prueba completa? (y/N): ").strip().lower()
    if response in ['y', 'yes', 'sí', 'si']:
        run_demo_command("python test_all_endpoints.py", "Prueba completa de todos los endpoints")
    else:
        print("⏭️ Saltando prueba completa...")
    
    print_header("COMANDOS ÚTILES")
    print("Aquí tienes los comandos más útiles para usar en el futuro:")
    
    commands = [
        ("python quick_test.py", "Prueba rápida de endpoints"),
        ("python diagnose_db.py", "Diagnóstico de base de datos"),
        ("python test_service_connectivity.py", "Verificar conectividad"),
        ("python test_all_endpoints.py", "Prueba completa"),
        ("python run_all_tests.py", "Ejecutar todas las pruebas"),
        ("python main.py", "Iniciar el microservicio"),
        ("python create_peru_data_simple.py", "Cargar datos de prueba"),
    ]
    
    for command, description in commands:
        print(f"   💻 {command:<40} - {description}")
    
    print_header("SOLUCIÓN DE PROBLEMAS COMUNES")
    
    problems = [
        ("Servicio no responde", "python main.py", "Iniciar el microservicio"),
        ("Base de datos vacía", "python create_peru_data_simple.py", "Cargar datos de prueba"),
        ("Endpoints lentos", "python diagnose_db.py", "Verificar base de datos"),
        ("Errores 500", "python test_service_connectivity.py", "Diagnosticar conectividad"),
    ]
    
    for problem, solution, description in problems:
        print(f"   🚨 {problem}")
        print(f"      💡 Solución: {solution}")
        print(f"      📝 {description}")
        print()
    
    print_header("PRÓXIMOS PASOS")
    print("1. 🚀 Inicia el microservicio: python main.py")
    print("2. 🌱 Carga datos de prueba: python create_peru_data_simple.py")
    print("3. 🧪 Ejecuta pruebas: python quick_test.py")
    print("4. 📚 Lee la documentación: README_TESTING.md")
    
    print("\n🎉 ¡Demostración completada!")
    print("💡 Para más información, consulta README_TESTING.md")

if __name__ == "__main__":
    main()
