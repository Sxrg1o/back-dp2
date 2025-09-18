#!/usr/bin/env python3
"""
Script simple para crear datos peruanos usando la API REST.
"""

import requests
import json

def create_peru_data():
    """Crea datos peruanos usando la API REST."""
    base_url = "http://localhost:8002"
    
    print("🇵🇪 Creando datos peruanos via API...")
    print("=" * 60)
    
    # Verificar que el servicio esté funcionando
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Servicio no disponible")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servicio. Asegúrate de que esté ejecutándose.")
        return
    
    print("✅ Servicio funcionando correctamente")
    
    # Datos de ingredientes peruanos
    ingredientes = [
        {"nombre": "Ají Amarillo", "stock": 15.0, "peso": 0.05, "tipo": "VERDURA"},
        {"nombre": "Rocoto", "stock": 8.0, "peso": 0.03, "tipo": "VERDURA"},
        {"nombre": "Cebolla Morada", "stock": 20.0, "peso": 0.2, "tipo": "VERDURA"},
        {"nombre": "Culantro", "stock": 12.0, "peso": 0.01, "tipo": "VERDURA"},
        {"nombre": "Papa Amarilla", "stock": 30.0, "peso": 0.3, "tipo": "VERDURA"},
        {"nombre": "Pollo Criollo", "stock": 15.0, "peso": 1.2, "tipo": "CARNE"},
        {"nombre": "Pescado de Mar", "stock": 12.0, "peso": 0.6, "tipo": "CARNE"},
        {"nombre": "Lúcuma", "stock": 8.0, "peso": 0.2, "tipo": "FRUTA"},
        {"nombre": "Chirimoya", "stock": 6.0, "peso": 0.3, "tipo": "FRUTA"},
        {"nombre": "Maracuyá", "stock": 7.0, "peso": 0.15, "tipo": "FRUTA"}
    ]
    
    # Crear ingredientes
    print("\n🥬 Creando ingredientes peruanos...")
    ingredientes_creados = 0
    for ingrediente in ingredientes:
        try:
            response = requests.post(f"{base_url}/ingredientes/", json=ingrediente)
            if response.status_code == 201:
                ingredientes_creados += 1
                print(f"   ✅ {ingrediente['nombre']}")
            else:
                print(f"   ❌ {ingrediente['nombre']} - Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {ingrediente['nombre']} - Error: {str(e)}")
    
    print(f"✅ {ingredientes_creados}/{len(ingredientes)} ingredientes creados")
    
    # Datos de platos peruanos
    platos = [
        {
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
        },
        {
            "descripcion": "Lomo Saltado",
            "precio": 32.50,
            "peso": 350.0,
            "tipo": "FONDO",
            "valor_nutricional": "Alto en proteínas, carbohidratos y vitaminas",
            "tiempo_preparacion": 25.0,
            "comentarios": "Fusión peruano-china, lomo de res salteado con verduras",
            "receta": "Saltear lomo con cebolla, tomate, ají amarillo, servir con papas fritas y arroz",
            "disponible": True,
            "unidades_disponibles": 10,
            "num_ingredientes": 8,
            "kcal": 580,
            "calorias": 580.0,
            "proteinas": 35.0,
            "azucares": 12.0,
            "etiquetas": ["CALIENTE", "CON_GLUTEN"]
        },
        {
            "descripcion": "Causa Limeña de Pollo",
            "precio": 18.50,
            "peso": 250.0,
            "tipo": "ENTRADA",
            "valor_nutricional": "Rica en carbohidratos, proteínas y vitaminas A y C",
            "tiempo_preparacion": 30.0,
            "comentarios": "Plato tradicional de la gastronomía peruana",
            "receta": "Cocinar papa amarilla, hacer puré, mezclar con ají amarillo, rellenar con pollo deshilachado",
            "disponible": True,
            "unidades_disponibles": 12,
            "num_ingredientes": 6,
            "kcal": 320,
            "calorias": 320.0,
            "proteinas": 18.0,
            "azucares": 8.0,
            "etiquetas": ["FRIO", "SIN_GLUTEN"]
        },
        {
            "descripcion": "Suspiro a la Limeña",
            "precio": 12.00,
            "peso": 150.0,
            "tipo": "POSTRE",
            "valor_nutricional": "Rico en azúcares y grasas",
            "tiempo_preparacion": 30.0,
            "comentarios": "Postre tradicional de Lima, manjar blanco con merengue",
            "receta": "Preparar manjar blanco, cubrir con merengue italiano, espolvorear canela",
            "disponible": True,
            "unidades_disponibles": 10,
            "num_ingredientes": 5,
            "kcal": 380,
            "calorias": 380.0,
            "proteinas": 8.0,
            "azucares": 45.0,
            "etiquetas": ["FRIO", "CON_GLUTEN"]
        }
    ]
    
    # Crear platos
    print("\n🍽️ Creando platos peruanos...")
    platos_creados = 0
    for plato in platos:
        try:
            response = requests.post(f"{base_url}/items/platos", json=plato)
            if response.status_code == 201:
                platos_creados += 1
                print(f"   ✅ {plato['descripcion']} - S/ {plato['precio']}")
            else:
                print(f"   ❌ {plato['descripcion']} - Error: {response.status_code}")
                print(f"      Respuesta: {response.text}")
        except Exception as e:
            print(f"   ❌ {plato['descripcion']} - Error: {str(e)}")
    
    print(f"✅ {platos_creados}/{len(platos)} platos creados")
    
    # Datos de bebidas peruanas
    bebidas = [
        {
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
        },
        {
            "descripcion": "Pisco Sour",
            "precio": 18.00,
            "litros": 0.2,
            "alcoholico": True,
            "valor_nutricional": "Cóctel nacional del Perú",
            "tiempo_preparacion": 8.0,
            "comentarios": "Cóctel emblemático con pisco, limón y clara de huevo",
            "receta": "Mezclar pisco, jugo de limón, jarabe de goma y clara de huevo, batir con hielo",
            "disponible": True,
            "unidades_disponibles": 15,
            "num_ingredientes": 5,
            "kcal": 200,
            "calorias": 200.0,
            "proteinas": 2.0,
            "azucares": 8.0,
            "etiquetas": ["FRIO", "ACIDO"]
        },
        {
            "descripcion": "Inca Kola",
            "precio": 4.50,
            "litros": 0.5,
            "alcoholico": False,
            "valor_nutricional": "Bebida gaseosa con sabor a hierba luisa",
            "tiempo_preparacion": 0.0,
            "comentarios": "La bebida nacional del Perú",
            "receta": "Servir fría",
            "disponible": True,
            "unidades_disponibles": 30,
            "num_ingredientes": 1,
            "kcal": 150,
            "calorias": 150.0,
            "proteinas": 0.0,
            "azucares": 35.0,
            "etiquetas": ["FRIO"]
        }
    ]
    
    # Crear bebidas
    print("\n🥤 Creando bebidas peruanas...")
    bebidas_creadas = 0
    for bebida in bebidas:
        try:
            response = requests.post(f"{base_url}/items/bebidas", json=bebida)
            if response.status_code == 201:
                bebidas_creadas += 1
                print(f"   ✅ {bebida['descripcion']} - S/ {bebida['precio']}")
            else:
                print(f"   ❌ {bebida['descripcion']} - Error: {response.status_code}")
                print(f"      Respuesta: {response.text}")
        except Exception as e:
            print(f"   ❌ {bebida['descripcion']} - Error: {str(e)}")
    
    print(f"✅ {bebidas_creadas}/{len(bebidas)} bebidas creadas")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 ¡Datos peruanos creados exitosamente!")
    print(f"📊 Resumen: {ingredientes_creados} ingredientes, {platos_creados} platos, {bebidas_creadas} bebidas")
    
    # Mostrar datos creados
    print("\n📋 Datos disponibles en la API:")
    
    # Listar ítems
    response = requests.get(f"{base_url}/items/")
    if response.status_code == 200:
        items = response.json()
        print(f"\n🍽️ Ítems del menú ({len(items)}):")
        for item in items:
            print(f"   - {item['descripcion']} (S/ {item['precio']})")
    
    # Listar ingredientes
    response = requests.get(f"{base_url}/ingredientes/")
    if response.status_code == 200:
        ingredientes = response.json()
        print(f"\n🥬 Ingredientes ({len(ingredientes)}):")
        for ingrediente in ingredientes:
            print(f"   - {ingrediente['nombre']} ({ingrediente['tipo']}) - Stock: {ingrediente['stock']}kg")
    
    print(f"\n🌐 Documentación de la API: {base_url}/docs")

if __name__ == "__main__":
    create_peru_data()
