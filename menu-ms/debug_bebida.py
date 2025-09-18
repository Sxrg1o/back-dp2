#!/usr/bin/env python3
"""
Script para debuggear específicamente el problema con Bebida.
"""

from domain.entities import Bebida
from decimal import Decimal

def test_bebida_from_db():
    """Simula la creación de una bebida desde la base de datos."""
    print("🔍 DEBUGGING BEBIDA DESDE BASE DE DATOS")
    print("="*50)
    
    # Simular los datos que vienen de la base de datos
    print("\n1. Creando Bebida con datos de BD...")
    bebida = Bebida(
        id=5,
        valor_nutricional="Rica en antioxidantes y vitamina C",
        precio=Decimal('6.50'),
        tiempo_preparacion=Decimal('15.0'),
        comentarios="Bebida tradicional de maíz morado",
        receta="Cocinar maíz morado con canela y clavo, endulzar y servir frío",
        disponible=True,
        unidades_disponibles=25,
        num_ingredientes=3,
        kcal=120,
        calorias=Decimal('120.0'),
        proteinas=Decimal('1.0'),
        azucares=Decimal('28.0'),
        descripcion="Chicha Morada",
        etiquetas=[],
        litros=Decimal('0.500'),
        alcoholico=False
    )
    
    print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
    print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
    print(f"   - bebida.__dict__: {bebida.__dict__}")
    
    # Probar serialización
    print("\n2. Probando serialización...")
    try:
        import json
        # Convertir Decimal a float para JSON
        def decimal_converter(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        bebida_dict = {
            'id': bebida.id,
            'tipo': bebida.tipo,
            'descripcion': bebida.descripcion,
            'precio': float(bebida.precio),
            'litros': float(bebida.litros),
            'alcoholico': bebida.alcoholico
        }
        print(f"   - Dict serializado: {bebida_dict}")
        
    except Exception as e:
        print(f"   - Error en serialización: {e}")

if __name__ == "__main__":
    test_bebida_from_db()
