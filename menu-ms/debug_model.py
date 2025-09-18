#!/usr/bin/env python3
"""
Script para debuggear el modelo directamente.
"""

def test_model_creation():
    """Prueba la creación del modelo directamente."""
    print("🔍 DEBUGGING MODELO DIRECTAMENTE")
    print("="*50)
    
    try:
        from infrastructure.models.item_model import ItemModel, BebidaModel
        from decimal import Decimal
        
        print("\n1. Creando BebidaModel...")
        
        # Crear un modelo de bebida simulado
        class MockBebidaModel(ItemModel):
            def __init__(self):
                self.id = 5
                self.valor_nutricional = "Rica en antioxidantes y vitamina C"
                self.precio = Decimal('6.50')
                self.tiempo_preparacion = Decimal('15.0')
                self.comentarios = "Bebida tradicional de maíz morado"
                self.receta = "Cocinar maíz morado con canela y clavo, endulzar y servir frío"
                self.disponible = True
                self.unidades_disponibles = 25
                self.num_ingredientes = 3
                self.kcal = 120
                self.calorias = Decimal('120.0')
                self.proteinas = Decimal('1.0')
                self.azucares = Decimal('28.0')
                self.descripcion = "Chicha Morada"
                self.tipo = 'BEBIDA'
                self.litros = Decimal('0.500')
                self.alcoholico = False
                self.etiquetas = []
        
        mock_model = MockBebidaModel()
        
        print(f"   - mock_model.tipo: {mock_model.tipo}")
        print(f"   - hasattr(mock_model, 'to_domain'): {hasattr(mock_model, 'to_domain')}")
        
        print("\n2. Probando to_domain()...")
        bebida = mock_model.to_domain()
        
        print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
        print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
        print(f"   - bebida.__dict__: {bebida.__dict__}")
        
        print("\n3. Probando acceso directo:")
        print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
        print(f"   - bebida.tipo: {bebida.tipo}")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_creation()
