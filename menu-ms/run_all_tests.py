#!/usr/bin/env python3
"""
Script maestro para ejecutar todas las pruebas del microservicio de menú.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_script(script_name: str, description: str) -> bool:
    """Ejecuta un script de prueba y retorna si fue exitoso."""
    print(f"\n{'='*60}")
    print(f"🧪 EJECUTANDO: {description}")
    print(f"📄 Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errores/Warnings:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ ÉXITO" if success else "❌ FALLO"
        print(f"\n{status} - Código de salida: {result.returncode}")
        
        return success
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - El script tardó demasiado")
        return False
    except FileNotFoundError:
        print(f"❌ ARCHIVO NO ENCONTRADO - {script_name}")
        return False
    except Exception as e:
        print(f"❌ ERROR - {e}")
        return False

def main():
    """Función principal que ejecuta todos los tests."""
    print("🚀 EJECUTOR MAESTRO DE PRUEBAS - MICROSERVICIO DE MENÚ")
    print("="*70)
    print(f"📁 Directorio: {Path.cwd()}")
    print(f"⏰ Inicio: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Lista de scripts a ejecutar en orden
    test_scripts = [
        ("diagnose_db.py", "Diagnóstico de Base de Datos"),
        ("test_service_connectivity.py", "Prueba de Conectividad del Servicio"),
        ("quick_test.py", "Prueba Rápida de Endpoints"),
        ("test_all_endpoints.py", "Prueba Completa de Endpoints"),
    ]
    
    results = {}
    total_scripts = len(test_scripts)
    
    print(f"\n📋 Ejecutando {total_scripts} scripts de prueba...")
    
    for script_name, description in test_scripts:
        success = run_script(script_name, description)
        results[script_name] = success
        
        # Pausa entre scripts
        if script_name != test_scripts[-1][0]:  # No pausar después del último
            print("\n⏳ Esperando 2 segundos antes del siguiente test...")
            time.sleep(2)
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📊 RESUMEN FINAL DE TODAS LAS PRUEBAS")
    print(f"{'='*70}")
    
    successful = sum(1 for success in results.values() if success)
    failed = total_scripts - successful
    
    print(f"📈 Total de scripts: {total_scripts}")
    print(f"✅ Exitosos: {successful}")
    print(f"❌ Fallidos: {failed}")
    print(f"📊 Tasa de éxito: {(successful/total_scripts)*100:.1f}%")
    
    print(f"\n📋 DETALLE POR SCRIPT:")
    for script_name, description in test_scripts:
        status = "✅" if results[script_name] else "❌"
        print(f"   {status} {script_name} - {description}")
    
    # Recomendaciones finales
    print(f"\n💡 RECOMENDACIONES:")
    if failed == 0:
        print("   🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("   ✅ El microservicio está funcionando correctamente")
    elif successful > failed:
        print("   ⚠️ La mayoría de pruebas pasaron")
        print("   🔧 Revisa los scripts que fallaron")
    else:
        print("   🚨 Muchas pruebas fallaron")
        print("   🔧 Verifica que el microservicio esté ejecutándose")
        print("   📚 Revisa la documentación y logs")
    
    print(f"\n🔧 COMANDOS ÚTILES:")
    print("   • Iniciar servicio: python main.py")
    print("   • Cargar datos: python create_peru_data_simple.py")
    print("   • Prueba rápida: python quick_test.py")
    print("   • Diagnóstico: python diagnose_db.py")
    
    print(f"\n⏰ Finalizado: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Código de salida basado en resultados
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
