"""
Script para probar directamente los endpoints de productos
para ver qué está devolviendo realmente.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi.testclient import TestClient
from src.main import app

def test_productos_directo():
    """Prueba directa de los endpoints de productos."""
    print("=" * 60)
    print("🔍 PRUEBA DIRECTA DE ENDPOINTS DE PRODUCTOS")
    print("=" * 60)
    
    client = TestClient(app)
    
    # 1. Probar endpoint principal de productos
    print("\n1️⃣ Probando /api/v1/productos...")
    response = client.get("/api/v1/productos?skip=0&limit=100")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Estructura de respuesta: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        
        if isinstance(data, dict) and 'items' in data:
            productos = data['items']
            print(f"   Número de productos: {len(productos)}")
            
            if productos:
                print("   Primeros 2 productos:")
                for i, producto in enumerate(productos[:2], 1):
                    print(f"     {i}. Nombre: {producto.get('nombre', 'N/A')}")
                    print(f"        Precio: {producto.get('precio_base', producto.get('precio', 'N/A'))}")
                    print(f"        Disponible: {producto.get('disponible', 'N/A')}")
                    print(f"        ID: {producto.get('id', 'N/A')}")
        else:
            print(f"   Respuesta completa: {data}")
    else:
        print(f"   Error: {response.text}")
    
    # 2. Probar endpoint de cards
    print("\n2️⃣ Probando /api/v1/productos/cards...")
    response = client.get("/api/v1/productos/cards?limit=10")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Estructura de respuesta: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        
        if isinstance(data, dict) and 'items' in data:
            productos = data['items']
            print(f"   Número de productos: {len(productos)}")
            
            if productos:
                print("   Primeros 2 productos:")
                for i, producto in enumerate(productos[:2], 1):
                    print(f"     {i}. Nombre: {producto.get('nombre', 'N/A')}")
                    print(f"        Precio: {producto.get('precio_base', producto.get('precio', 'N/A'))}")
                    print(f"        Disponible: {producto.get('disponible', 'N/A')}")
        else:
            print(f"   Respuesta completa: {data}")
    else:
        print(f"   Error: {response.text}")
    
    # 3. Probar mesas para comparar
    print("\n3️⃣ Probando /api/v1/mesas para comparar...")
    response = client.get("/api/v1/mesas?limit=10")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'items' in data:
            mesas = data['items']
            print(f"   Número de mesas: {len(mesas)}")
    else:
        print(f"   Error: {response.text}")


if __name__ == "__main__":
    test_productos_directo()
