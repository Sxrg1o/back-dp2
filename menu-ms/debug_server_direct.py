#!/usr/bin/env python3
"""
Script para debuggear directamente con el servidor.
"""

import requests
import json

def test_server_direct():
    """Prueba directamente con el servidor."""
    print("🔍 DEBUGGING SERVIDOR DIRECTO")
    print("="*50)
    
    base_url = "http://localhost:8002"
    
    print("\n1. Probando /items/with-ingredientes (que funciona)...")
    try:
        response = requests.get(f"{base_url}/items/with-ingredientes")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Número de ítems: {len(data)}")
            
            # Buscar bebidas
            bebidas = [item for item in data if item.get('tipo') == 'BEBIDA']
            print(f"   - Número de bebidas: {len(bebidas)}")
            
            for bebida in bebidas[:3]:  # Solo las primeras 3
                print(f"     - ID: {bebida['id']}, Descripción: {bebida['descripcion']}, Tipo: {bebida['tipo']}")
        else:
            print(f"   - Error: {response.text}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    print("\n2. Probando /items/ (que falla)...")
    try:
        response = requests.get(f"{base_url}/items/")
        print(f"   - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   - Error: {response.text}")
        else:
            data = response.json()
            print(f"   - Datos: {len(data)} elementos")
    except Exception as e:
        print(f"   - Error: {e}")
    
    print("\n3. Probando bebidas individuales...")
    for item_id in [5, 6, 7, 8]:
        try:
            response = requests.get(f"{base_url}/items/{item_id}")
            print(f"   - ID {item_id}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"     - Error: {response.text}")
        except Exception as e:
            print(f"   - ID {item_id}: Error - {e}")

if __name__ == "__main__":
    test_server_direct()
