#!/usr/bin/env python3
"""
Script para debuggear el problema del campo 'tipo' en las entidades.
"""

from domain.entities import Bebida, Plato, Item
from decimal import Decimal

def test_entidades():
    """Prueba las entidades para verificar el campo tipo."""
    print("🔍 DEBUGGING CAMPO 'TIPO' EN ENTIDADES")
    print("="*50)
    
    # Crear una bebida
    print("\n1. Creando Bebida...")
    bebida = Bebida(
        id=1,
        descripcion="Test Bebida",
        precio=Decimal('10.0'),
        litros=Decimal('0.5'),
        alcoholico=False
    )
    
    print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
    print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
    print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
    print(f"   - dir(bebida): {[attr for attr in dir(bebida) if 'tipo' in attr.lower()]}")
    
    # Crear un plato
    print("\n2. Creando Plato...")
    plato = Plato(
        id=2,
        descripcion="Test Plato",
        precio=Decimal('15.0'),
        peso=Decimal('300.0')
    )
    
    print(f"   - hasattr(plato, 'tipo'): {hasattr(plato, 'tipo')}")
    print(f"   - plato.tipo: {getattr(plato, 'tipo', 'NOT_FOUND')}")
    print(f"   - plato.get_tipo(): {plato.get_tipo()}")
    print(f"   - dir(plato): {[attr for attr in dir(plato) if 'tipo' in attr.lower()]}")
    
    # Probar conversión a dict
    print("\n3. Probando conversión a dict...")
    try:
        bebida_dict = bebida.__dict__
        print(f"   - bebida.__dict__: {bebida_dict}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    # Probar con Pydantic
    print("\n4. Probando con Pydantic...")
    try:
        from infrastructure.handlers.dtos import ItemResponseDTO
        dto = ItemResponseDTO.model_validate(bebida)
        print(f"   - DTO creado exitosamente: {dto}")
    except Exception as e:
        print(f"   - Error Pydantic: {e}")

if __name__ == "__main__":
    test_entidades()
