"""
Script para verificar qué endpoints están disponibles en el servidor
"""

import requests

def check_endpoints():
    """Verificar endpoints disponibles."""
    
    base_url = "https://back-dp2.onrender.com"
    
    endpoints = [
        '/api/v1/roles',
        '/api/v1/categorias', 
        '/api/v1/alergenos',
        '/api/v1/productos',
        '/api/v1/tipos-opciones',
        '/api/v1/producto-opciones',
        '/api/v1/productos-alergenos',
        '/api/v1/seed/status',
        '/api/v1/seed/execute'
    ]
    
    print("🔍 Verificando endpoints disponibles:")
    print("="*50)
    
    available_endpoints = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}?limit=1", timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {endpoint}: {status}")
                available_endpoints.append(endpoint)
            elif status == 404:
                print(f"❌ {endpoint}: {status} (No encontrado)")
            else:
                print(f"⚠️ {endpoint}: {status}")
                
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
    
    print("\n" + "="*50)
    print(f"📊 Endpoints disponibles: {len(available_endpoints)}/{len(endpoints)}")
    
    return available_endpoints

if __name__ == "__main__":
    check_endpoints()
