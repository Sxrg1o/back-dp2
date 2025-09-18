#!/usr/bin/env python3
"""
Script simple para debuggear la conversión de entidades.
"""

from domain.entities import Bebida
from decimal import Decimal

def test_bebida_conversion():
    """Prueba la conversión de Bebida a dict."""
    print("🔍 DEBUGGING CONVERSIÓN DE BEBIDA")
    print("="*50)
    
    # Crear una bebida
    bebida = Bebida(
        id=5,
        descripcion="Chicha Morada",
        precio=Decimal('6.50'),
        litros=Decimal('0.500'),
        alcoholico=False
    )
    
    print(f"1. Bebida creada:")
    print(f"   - bebida.tipo: {bebida.tipo}")
    print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
    
    # Probar conversión a dict
    print(f"\n2. Conversión a dict:")
    bebida_dict = bebida.__dict__.copy()
    print(f"   - bebida_dict: {bebida_dict}")
    
    # Probar acceso al campo tipo
    print(f"\n3. Acceso al campo tipo:")
    print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
    print(f"   - getattr(bebida, 'tipo'): {getattr(bebida, 'tipo', 'NOT_FOUND')}")
    print(f"   - bebida.tipo: {bebida.tipo}")
    
    # Probar con vars()
    print(f"\n4. Usando vars():")
    bebida_vars = vars(bebida)
    print(f"   - 'tipo' in bebida_vars: {'tipo' in bebida_vars}")
    print(f"   - bebida_vars['tipo']: {bebida_vars.get('tipo', 'NOT_FOUND')}")

if __name__ == "__main__":
    test_bebida_conversion()
