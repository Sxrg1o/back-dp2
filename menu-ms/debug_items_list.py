#!/usr/bin/env python3
"""
Script para verificar la lista de ítems usando el servidor.
"""

import requests
import json

def test_items_list():
    """Verifica la lista de ítems usando el servidor."""
    print("🔍 VERIFICANDO LISTA DE ÍTEMS CON SERVIDOR")
    print("="*50)
    
    base_url = "http://localhost:8002"
    
    print("\n1. Probando /items/with-ingredientes (que funciona)...")
    try:
        response = requests.get(f"{base_url}/items/with-ingredientes")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Número de ítems: {len(data)}")
            for i, item in enumerate(data):
                print(f"     - ID: {item['id']}, Descripción: {item['descripcion']}, Tipo: {item['tipo']}")
                if i >= 4:  # Solo mostrar los primeros 5
                    break
        else:
            print(f"   - Error: {response.text}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    print("\n2. Probando ítems individuales...")
    for item_id in [1, 2, 3, 4, 5, 6, 7, 8]:
        try:
            response = requests.get(f"{base_url}/items/{item_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"   - ID {item_id}: {data['descripcion']} (Tipo: {data['tipo']})")
            elif response.status_code == 404:
                print(f"   - ID {item_id}: No encontrado")
            else:
                print(f"   - ID {item_id}: Error {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   - ID {item_id}: Error - {e}")

if __name__ == "__main__":
    test_items_list()
