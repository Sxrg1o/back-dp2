#!/usr/bin/env python3
"""
Script para debuggear el endpoint específico que falla.
"""

import requests
import json

def test_failing_endpoint():
    """Prueba el endpoint que está fallando."""
    print("🔍 DEBUGGING ENDPOINT QUE FALLA")
    print("="*50)
    
    base_url = "http://localhost:8002"
    
    print("\n1. Probando /items/ (que falla)...")
    try:
        response = requests.get(f"{base_url}/items/")
        print(f"   - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   - Error: {response.text}")
        else:
            data = response.json()
            print(f"   - Datos: {len(data)} elementos")
            if data:
                print(f"   - Primer elemento: {data[0]}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    print("\n2. Probando /items/with-ingredientes (que funciona)...")
    try:
        response = requests.get(f"{base_url}/items/with-ingredientes")
        print(f"   - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Datos: {len(data)} elementos")
            if data:
                print(f"   - Primer elemento: {data[0]}")
        else:
            print(f"   - Error: {response.text}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    print("\n3. Probando /items/1 (que funciona)...")
    try:
        response = requests.get(f"{base_url}/items/1")
        print(f"   - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Datos: {data}")
        else:
            print(f"   - Error: {response.text}")
    except Exception as e:
        print(f"   - Error: {e}")

if __name__ == "__main__":
    test_failing_endpoint()
