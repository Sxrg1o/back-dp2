#!/usr/bin/env python3
"""
Script final para capturar el error completo del endpoint que falla.
"""

import requests
import json
import traceback

def test_final_error_final():
    """Captura el error final del endpoint que falla."""
    print("🔍 CAPTURANDO ERROR FINAL")
    print("="*50)
    
    base_url = "http://localhost:8002"
    
    print("\n1. Probando /items/ con captura de error...")
    try:
        response = requests.get(f"{base_url}/items/", timeout=10)
        print(f"   - Status Code: {response.status_code}")
        print(f"   - Headers: {dict(response.headers)}")
        
        if response.status_code == 500:
            try:
                error_data = response.json()
                print(f"   - Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   - Error Text: {response.text}")
        else:
            data = response.json()
            print(f"   - Datos: {len(data)} elementos")
            if data:
                print(f"   - Primer elemento: {json.dumps(data[0], indent=2)}")
                
    except requests.exceptions.RequestException as e:
        print(f"   - Error de conexión: {e}")
    except Exception as e:
        print(f"   - Error inesperado: {e}")
        traceback.print_exc()
    
    print("\n2. Probando /items/with-ingredientes para comparar...")
    try:
        response = requests.get(f"{base_url}/items/with-ingredientes", timeout=10)
        print(f"   - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   - Datos: {len(data)} elementos")
            if data:
                print(f"   - Primer elemento: {json.dumps(data[0], indent=2)}")
        else:
            print(f"   - Error: {response.text}")
                
    except Exception as e:
        print(f"   - Error: {e}")

if __name__ == "__main__":
    test_final_error_final()
