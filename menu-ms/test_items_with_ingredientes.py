#!/usr/bin/env python3
"""
Script de prueba para el endpoint de ítems con ingredientes.
"""

import requests
import json
from typing import Dict, Any

def test_items_with_ingredientes():
    """Prueba el endpoint de ítems con ingredientes."""
    base_url = "http://localhost:8002"
    
    print("🍽️ Probando endpoint de ítems con ingredientes...")
    print("=" * 60)
    
    try:
        # Verificar que el servicio esté funcionando
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Servicio no disponible")
            return
        print("✅ Servicio funcionando correctamente")
        
        # Probar el endpoint de ítems con ingredientes
        print("\n📋 Obteniendo ítems con ingredientes...")
        response = requests.get(f"{base_url}/items/with-ingredientes")
        
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Se obtuvieron {len(items)} ítems con ingredientes")
            
            # Mostrar información detallada
            for item in items:
                print(f"\n🍽️ {item['descripcion']} (ID: {item['id']})")
                print(f"   💰 Precio: S/ {item['precio']}")
                print(f"   🏷️ Tipo: {item['tipo']}")
                print(f"   📦 Disponible: {'Sí' if item['disponible'] else 'No'}")
                print(f"   🏷️ Etiquetas: {', '.join(item.get('etiquetas', []))}")
                
                # Mostrar ingredientes
                ingredientes = item.get('ingredientes', [])
                if ingredientes:
                    print(f"   🥬 Ingredientes ({len(ingredientes)}):")
                    for ing in ingredientes:
                        cantidad = ing.get('cantidad', 1.0)
                        print(f"      - {ing['nombre']} ({ing['tipo']}) - Cantidad: {cantidad}")
                else:
                    print("   🥬 Sin ingredientes asociados")
                
                # Mostrar campos específicos según el tipo
                if item['tipo'] == 'PLATO':
                    peso = item.get('peso', 0)
                    tipo_plato = item.get('tipo_plato', 'FONDO')
                    print(f"   ⚖️ Peso: {peso}g")
                    print(f"   🍽️ Tipo de plato: {tipo_plato}")
                elif item['tipo'] == 'BEBIDA':
                    litros = item.get('litros', 0)
                    alcoholico = item.get('alcoholico', False)
                    print(f"   🥤 Volumen: {litros}L")
                    print(f"   🍺 Alcohólica: {'Sí' if alcoholico else 'No'}")
                
                print("   " + "-" * 40)
            
            # Mostrar estadísticas
            print(f"\n📊 Estadísticas:")
            platos = [item for item in items if item['tipo'] == 'PLATO']
            bebidas = [item for item in items if item['tipo'] == 'BEBIDA']
            print(f"   🍽️ Platos: {len(platos)}")
            print(f"   🥤 Bebidas: {len(bebidas)}")
            
            # Contar ingredientes únicos
            todos_ingredientes = set()
            for item in items:
                for ing in item.get('ingredientes', []):
                    todos_ingredientes.add(ing['nombre'])
            print(f"   🥬 Ingredientes únicos: {len(todos_ingredientes)}")
            
        else:
            print(f"❌ Error al obtener ítems: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servicio. Asegúrate de que esté ejecutándose.")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_performance():
    """Prueba el rendimiento del endpoint."""
    base_url = "http://localhost:8002"
    
    print("\n⚡ Probando rendimiento del endpoint...")
    print("=" * 60)
    
    import time
    
    try:
        # Medir tiempo de respuesta
        start_time = time.time()
        response = requests.get(f"{base_url}/items/with-ingredientes")
        end_time = time.time()
        
        if response.status_code == 200:
            items = response.json()
            response_time = (end_time - start_time) * 1000  # en milisegundos
            
            print(f"✅ Tiempo de respuesta: {response_time:.2f}ms")
            print(f"📊 Ítems procesados: {len(items)}")
            print(f"⚡ Tiempo por ítem: {response_time/len(items):.2f}ms/ítem")
            
            # Verificar que todos los ítems tienen ingredientes cargados
            items_con_ingredientes = [item for item in items if item.get('ingredientes')]
            print(f"🥬 Ítems con ingredientes: {len(items_con_ingredientes)}/{len(items)}")
            
        else:
            print(f"❌ Error en la prueba de rendimiento: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en la prueba de rendimiento: {str(e)}")

def main():
    """Función principal."""
    print("🚀 Prueba del Endpoint de Ítems con Ingredientes")
    print("=" * 60)
    
    # Prueba básica
    test_items_with_ingredientes()
    
    # Prueba de rendimiento
    test_performance()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas!")
    print("\n💡 Para usar la API:")
    print("   GET /items/with-ingredientes - Lista todos los ítems con ingredientes")
    print("   GET /items/ - Lista ítems sin ingredientes (más rápido)")
    print("   GET /docs - Documentación completa de la API")

if __name__ == "__main__":
    main()
