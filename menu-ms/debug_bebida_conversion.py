#!/usr/bin/env python3
"""
Script para debuggear la conversión de bebidas específicamente.
"""

def test_bebida_conversion():
    """Prueba la conversión de bebidas específicamente."""
    print("🔍 DEBUGGING CONVERSIÓN DE BEBIDAS")
    print("="*50)
    
    try:
        from domain.entities import Bebida
        from decimal import Decimal
        
        print("\n1. Creando Bebida directamente...")
        bebida = Bebida(
            id=5,
            descripcion="Chicha Morada",
            precio=Decimal('6.50'),
            litros=Decimal('0.500'),
            alcoholico=False
        )
        
        print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
        print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
        print(f"   - bebida.__dict__: {bebida.__dict__}")
        
        print("\n2. Probando con Pydantic...")
        try:
            from infrastructure.handlers.dtos import ItemResponseDTO
            dto = ItemResponseDTO.model_validate(bebida)
            print(f"   - DTO creado exitosamente: {dto.tipo}")
        except Exception as e:
            print(f"   - Error Pydantic: {e}")
        
        print("\n3. Probando serialización...")
        try:
            import json
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
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bebida_conversion()
