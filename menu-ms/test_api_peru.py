#!/usr/bin/env python3
"""
Script para probar la API con datos peruanos usando requests.
"""

import requests
import json
from decimal import Decimal

def test_api_peru():
    """Prueba la API con datos peruanos."""
    base_url = "http://localhost:8002"
    
    print("🇵🇪 Probando API con datos peruanos...")
    print("=" * 60)
    
    # Verificar que el servicio esté funcionando
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Servicio funcionando correctamente")
        else:
            print("❌ Servicio no disponible")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servicio. Asegúrate de que esté ejecutándose.")
        return
    
    # Crear un ingrediente peruano
    ingrediente_data = {
        "nombre": "Ají Amarillo",
        "stock": 15.0,
        "peso": 0.05,
        "tipo": "VERDURA"
    }
    
    print("\n🥬 Creando ingrediente peruano...")
    response = requests.post(f"{base_url}/ingredientes/", json=ingrediente_data)
    if response.status_code == 201:
        print("✅ Ingrediente creado correctamente")
        ingrediente = response.json()
        print(f"   ID: {ingrediente['id']}, Nombre: {ingrediente['nombre']}")
    else:
        print(f"❌ Error al crear ingrediente: {response.status_code}")
        print(f"   Respuesta: {response.text}")
    
    # Crear un plato peruano
    plato_data = {
        "descripcion": "Ceviche de Pescado",
        "precio": 28.00,
        "peso": 300.0,
        "tipo": "FONDO",
        "valor_nutricional": "Rico en proteínas, omega-3 y vitamina C",
        "tiempo_preparacion": 20.0,
        "comentarios": "Plato bandera del Perú, pescado fresco marinado en leche de tigre",
        "receta": "Cortar pescado fresco, marinar en limón, ají, cebolla morada y culantro",
        "disponible": True,
        "unidades_disponibles": 15,
        "num_ingredientes": 7,
        "kcal": 250,
        "calorias": 250.0,
        "proteinas": 30.0,
        "azucares": 5.0,
        "etiquetas": ["FRIO", "ACIDO", "SIN_GLUTEN"]
    }
    
    print("\n🍽️ Creando plato peruano...")
    response = requests.post(f"{base_url}/items/platos", json=plato_data)
    if response.status_code == 201:
        print("✅ Plato creado correctamente")
        plato = response.json()
        print(f"   ID: {plato['id']}, Descripción: {plato['descripcion']}")
        print(f"   Precio: S/ {plato['precio']}, Tipo: {plato['tipo']}")
    else:
        print(f"❌ Error al crear plato: {response.status_code}")
        print(f"   Respuesta: {response.text}")
    
    # Crear una bebida peruana
    bebida_data = {
        "descripcion": "Chicha Morada",
        "precio": 6.50,
        "litros": 0.5,
        "alcoholico": False,
        "valor_nutricional": "Rica en antioxidantes y vitamina C",
        "tiempo_preparacion": 15.0,
        "comentarios": "Bebida tradicional de maíz morado",
        "receta": "Cocinar maíz morado con canela y clavo, endulzar y servir frío",
        "disponible": True,
        "unidades_disponibles": 25,
        "num_ingredientes": 3,
        "kcal": 120,
        "calorias": 120.0,
        "proteinas": 1.0,
        "azucares": 28.0,
        "etiquetas": ["FRIO", "SIN_GLUTEN"]
    }
    
    print("\n🥤 Creando bebida peruana...")
    response = requests.post(f"{base_url}/items/bebidas", json=bebida_data)
    if response.status_code == 201:
        print("✅ Bebida creada correctamente")
        bebida = response.json()
        print(f"   ID: {bebida['id']}, Descripción: {bebida['descripcion']}")
        print(f"   Precio: S/ {bebida['precio']}, Litros: {bebida['litros']}L")
    else:
        print(f"❌ Error al crear bebida: {response.status_code}")
        print(f"   Respuesta: {response.text}")
    
    # Listar todos los ítems
    print("\n📋 Listando todos los ítems...")
    response = requests.get(f"{base_url}/items/")
    if response.status_code == 200:
        items = response.json()
        print(f"✅ Total de ítems: {len(items)}")
        for item in items:
            print(f"   - {item['descripcion']} (S/ {item['precio']})")
    else:
        print(f"❌ Error al listar ítems: {response.status_code}")
    
    # Listar todos los ingredientes
    print("\n🥬 Listando todos los ingredientes...")
    response = requests.get(f"{base_url}/ingredientes/")
    if response.status_code == 200:
        ingredientes = response.json()
        print(f"✅ Total de ingredientes: {len(ingredientes)}")
        for ingrediente in ingredientes:
            print(f"   - {ingrediente['nombre']} ({ingrediente['tipo']}) - Stock: {ingrediente['stock']}kg")
    else:
        print(f"❌ Error al listar ingredientes: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Prueba de API completada!")
    print("\n🌐 Endpoints disponibles:")
    print(f"   - GET {base_url}/items/ - Todos los ítems")
    print(f"   - GET {base_url}/ingredientes/ - Todos los ingredientes")
    print(f"   - GET {base_url}/items/platos/entradas - Entradas")
    print(f"   - GET {base_url}/items/platos/principales - Platos principales")
    print(f"   - GET {base_url}/items/platos/postres - Postres")
    print(f"   - GET {base_url}/items/bebidas/alcoholicas - Bebidas alcohólicas")
    print(f"   - GET {base_url}/items/bebidas/no-alcoholicas - Bebidas no alcohólicas")
    print(f"   - GET {base_url}/docs - Documentación de la API")

if __name__ == "__main__":
    test_api_peru()
