from typing import Dict

# =========================
# Agente 2: Catálogo (datos)
# =========================

# Ingredientes (id->nombre)
INGREDIENTES: Dict[int, str] = {
    1: "Pescado",
    2: "Limón",
    3: "Cebolla",
    4: "Arroz",
    5: "Mariscos",
    6: "Camarones",
    7: "Pulpo",
    8: "Ají",
    9: "Cilantro",
    10: "Ajo",
}

# Items del menú (IDs como strings y enteros para mapear ambos casos)
ITEMS: Dict[str, dict] = {
    "1": {
        "id": 1,
        "nombre": "Ceviche",
        "tipo": "FONDO",
        "precio": 28.0,
        "stock": 10,
        "disponible": True,
        "tiempo_preparacion": 10,
        "descripcion": "Clásico ceviche peruano con pescado fresco marinado en limón",
        "categoria": "Plato",
        "imagen_url": "https://example.com/ceviche.jpg",
        "ingredientes_ids": [1, 2, 3, 8, 9],
        "etiquetas": ["sin_gluten", "fresco"],
        "kcal": 300,
        "calorias": "300",
        "proteinas": "25",
        "azucares": "3",
        "valor_nutricional": "Alto en proteínas, bajo en carbohidratos",
        "receta": "Pescado fresco cortado en cubos, marinado con limón, cebolla, ají y cilantro",
        "comentarios": "Plato estrella de la casa",
    },
    "2": {
        "id": 2,
        "nombre": "Arroz con mariscos",
        "tipo": "FONDO",
        "precio": 32.0,
        "stock": 4,
        "disponible": True,
        "tiempo_preparacion": 20,
        "descripcion": "Arroz con mariscos mixtos y salsa criolla",
        "categoria": "Plato",
        "imagen_url": "https://example.com/arroz.jpg",
        "ingredientes_ids": [4, 5, 6, 7, 3, 10],
        "etiquetas": ["mariscos", "sustancioso"],
        "kcal": 650,
        "calorias": "650",
        "proteinas": "20",
        "azucares": "5",
        "valor_nutricional": "Rico en proteínas marinas y carbohidratos",
        "receta": "Arroz cocido con mariscos frescos, cebolla, ajo y especias",
        "comentarios": "Ideal para compartir",
    },
    "3": {
        "id": 3,
        "nombre": "Lomo saltado",
        "tipo": "FONDO",
        "precio": 35.0,
        "stock": 8,
        "disponible": True,
        "tiempo_preparacion": 15,
        "descripcion": "Lomo de res salteado con cebolla, tomate y papas fritas",
        "categoria": "Plato",
        "imagen_url": "https://example.com/lomo.jpg",
        "ingredientes_ids": [3, 10, 8],
        "etiquetas": ["carne", "popular"],
        "kcal": 580,
        "calorias": "580",
        "proteinas": "35",
        "azucares": "8",
        "valor_nutricional": "Alto en proteínas, moderado en carbohidratos",
        "receta": "Lomo de res salteado con verduras frescas y papas fritas",
        "comentarios": "Plato tradicional peruano",
    },
}

# Grupos/opciones como catálogo simple:
ACOMPANAMIENTOS: Dict[str, dict] = {
    "a1": {
        "id": "a1", 
        "nombre": "Camote", 
        "precio": 3.0, 
        "categoria": "acompanamiento", 
        "disponible": True, 
        "obligatorio": False, 
        "precio_adicional": 3.0
    },
    "a2": {
        "id": "a2", 
        "nombre": "Choclo",  
        "precio": 2.5, 
        "categoria": "acompanamiento", 
        "disponible": True, 
        "obligatorio": False, 
        "precio_adicional": 2.5
    },
    "a3": {
        "id": "a3", 
        "nombre": "Papas fritas",  
        "precio": 4.0, 
        "categoria": "acompanamiento", 
        "disponible": True, 
        "obligatorio": False, 
        "precio_adicional": 4.0
    },
}

OPCIONES_ADICIONALES: Dict[str, dict] = {
    "o1": {
        "id": "o1", 
        "nombre": "Ají extra", 
        "precio": 1.0, 
        "max_selecciones": 2
    },
    "o2": {
        "id": "o2", 
        "nombre": "Salsa de la casa", 
        "precio": 1.5, 
        "max_selecciones": 1
    },
    "o3": {
        "id": "o3", 
        "nombre": "Cebolla extra", 
        "precio": 0.5, 
        "max_selecciones": 3
    },
}
