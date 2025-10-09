"""
Script simple para ejecutar el seed en el servidor online
URL: https://back-dp2.onrender.com/
"""

import requests
import json
import time

def execute_seed():
    """Ejecutar el seed de datos en el servidor online."""
    
    base_url = "https://back-dp2.onrender.com"
    
    print("🚀 EJECUTANDO SEED EN SERVIDOR ONLINE")
    print(f"🌐 URL: {base_url}")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Headers para las peticiones
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # 1. Verificar estado del seed
        print("\n📋 Verificando estado del seed...")
        response = requests.get(f"{base_url}/api/v1/seed/status", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            has_data = data.get('has_data', False)
            
            if has_data:
                print("✅ La base de datos ya contiene datos de seed")
                print("📊 Datos existentes:")
                for key, value in data.items():
                    print(f"   {key}: {value}")
                return True
            else:
                print("📝 La base de datos está vacía, ejecutando seed...")
        else:
            print(f"⚠️ No se pudo verificar el estado (Status: {response.status_code})")
            print("🔄 Procediendo con la ejecución del seed...")
        
        # 2. Ejecutar el seed
        print("\n🌱 Ejecutando seed de datos...")
        seed_data = {"force": False}
        
        response = requests.post(
            f"{base_url}/api/v1/seed/execute", 
            headers=headers, 
            json=seed_data
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            if result.get('success', False):
                print("✅ Seed ejecutado exitosamente!")
                print(f"⏱️ Tiempo de ejecución: {result.get('execution_time', 0):.2f} segundos")
                print(f"📝 Mensaje: {result.get('message', 'Sin mensaje')}")
                
                # Mostrar datos creados
                data_created = result.get('data_created', {})
                if data_created:
                    print("\n📊 Datos creados:")
                    for tipo, cantidad in data_created.items():
                        print(f"   {tipo}: {cantidad} registros")
                
                return True
            else:
                print("❌ El seed falló")
                print(f"📝 Mensaje: {result.get('message', 'Sin mensaje')}")
                return False
        else:
            print(f"❌ Error al ejecutar seed (Status: {response.status_code})")
            print(f"📝 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verify_data():
    """Verificar que los datos se crearon correctamente."""
    
    base_url = "https://back-dp2.onrender.com"
    headers = {'Accept': 'application/json'}
    
    print("\n🔍 Verificando datos creados...")
    
    endpoints = {
        'Roles': '/api/v1/roles?limit=5',
        'Categorías': '/api/v1/categorias?limit=5',
        'Alérgenos': '/api/v1/alergenos?limit=5',
        'Productos': '/api/v1/productos?limit=5',
        'Tipos de Opciones': '/api/v1/tipos-opciones?limit=5',
        'Opciones de Productos': '/api/v1/producto-opciones?limit=5',
        'Relaciones Producto-Alérgeno': '/api/v1/productos-alergenos?limit=5'
    }
    
    results = {}
    
    for nombre, endpoint in endpoints.items():
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                items = data.get('items', [])
                
                results[nombre] = {
                    'success': True,
                    'total': total,
                    'items': len(items)
                }
                
                print(f"✅ {nombre}: {total} registros totales")
                
                # Mostrar algunos ejemplos
                if items:
                    print(f"   Ejemplos:")
                    for item in items[:3]:
                        if 'nombre' in item:
                            print(f"     - {item['nombre']}")
                        elif 'codigo' in item:
                            print(f"     - {item['codigo']} ({item.get('nombre', 'Sin nombre')})")
                        else:
                            print(f"     - {item.get('id', 'Sin ID')}")
            else:
                results[nombre] = {'success': False, 'error': f"Status {response.status_code}"}
                print(f"❌ {nombre}: Error {response.status_code}")
                
        except Exception as e:
            results[nombre] = {'success': False, 'error': str(e)}
            print(f"❌ {nombre}: Error - {e}")
    
    return results

def main():
    """Función principal."""
    
    # Ejecutar seed
    seed_success = execute_seed()
    
    if seed_success:
        # Esperar un poco para que se complete
        print("\n⏳ Esperando a que se complete el proceso...")
        time.sleep(3)
        
        # Verificar datos
        verification_results = verify_data()
        
        # Resumen final
        print("\n" + "="*60)
        print("📊 RESUMEN FINAL")
        print("="*60)
        
        successful_verifications = sum(1 for result in verification_results.values() if result.get('success', False))
        total_verifications = len(verification_results)
        
        print(f"🌱 Seed ejecutado: {'✅ Exitoso' if seed_success else '❌ Falló'}")
        print(f"🔍 Verificaciones: {successful_verifications}/{total_verifications} exitosas")
        
        if successful_verifications == total_verifications:
            print("\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
            print("✅ Todos los datos del seed están disponibles en el servidor")
        else:
            print(f"\n⚠️ Proceso completado con advertencias")
            print(f"❌ {total_verifications - successful_verifications} verificaciones fallaron")
    else:
        print("\n❌ El seed falló, no se pueden verificar los datos")

if __name__ == "__main__":
    main()
