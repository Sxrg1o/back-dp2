#!/usr/bin/env python3
"""
Script rápido para probar los endpoints principales del microservicio de menú.
"""

import requests
import json
from typing import Dict, Any

def quick_test():
    """Prueba rápida de los endpoints principales."""
    base_url = "http://localhost:8002"
    
    print("🚀 PRUEBA RÁPIDA DE ENDPOINTS")
    print("="*50)
    
    # Lista de endpoints a probar
    endpoints = [
        ("GET", "/health", "Health Check"),
        ("GET", "/", "Root"),
        ("GET", "/info", "Info del servicio"),
        ("GET", "/docs", "Documentación"),
        ("GET", "/ingredientes/", "Listar ingredientes"),
        ("GET", "/items/", "Listar ítems"),
        ("GET", "/items/with-ingredientes", "Ítems con ingredientes"),
        ("GET", "/ingredientes/verduras", "Verduras"),
        ("GET", "/ingredientes/carnes", "Carnes"),
        ("GET", "/items/platos/entradas", "Entradas"),
        ("GET", "/items/bebidas/alcoholicas", "Bebidas alcohólicas"),
    ]
    
    results = {"ok": [], "error": []}
    
    for method, endpoint, description in endpoints:
        try:
            print(f"\n🔍 {description}...")
            url = f"{base_url}{endpoint}"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ OK ({response.status_code})")
                
                # Mostrar información adicional
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"   📊 {len(data)} elementos")
                    elif isinstance(data, dict):
                        print(f"   📊 {len(data)} campos")
                except:
                    print(f"   📄 Respuesta de texto")
                
                results["ok"].append(endpoint)
            else:
                print(f"   ❌ Error {response.status_code}")
                results["error"].append(f"{endpoint} ({response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Sin conexión")
            results["error"].append(f"{endpoint} (sin conexión)")
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")
            results["error"].append(f"{endpoint} ({str(e)[:30]})")
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)
    print(f"✅ Funcionando: {len(results['ok'])}")
    print(f"❌ Con errores: {len(results['error'])}")
    
    if results["ok"]:
        print(f"\n✅ Endpoints OK:")
        for endpoint in results["ok"]:
            print(f"   • {endpoint}")
    
    if results["error"]:
        print(f"\n❌ Endpoints con error:")
        for endpoint in results["error"]:
            print(f"   • {endpoint}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if len(results["error"]) == 0:
        print("   🎉 ¡Todos los endpoints funcionan correctamente!")
    elif len(results["ok"]) > len(results["error"]):
        print("   ⚠️ La mayoría funciona, revisar los que fallan")
    else:
        print("   🚨 Muchos endpoints fallan, verificar el servicio")
    
    print(f"\n🔧 Para diagnóstico completo:")
    print(f"   python test_all_endpoints.py")

if __name__ == "__main__":
    quick_test()
