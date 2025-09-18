#!/usr/bin/env python3
"""
Script para debuggear el método to_domain().
"""

from infrastructure.models.item_model import ItemModel, BebidaModel
from decimal import Decimal

def test_to_domain():
    """Prueba el método to_domain() directamente."""
    print("🔍 DEBUGGING MÉTODO to_domain()")
    print("="*50)
    
    # Crear un modelo de bebida simulado
    print("\n1. Creando BebidaModel simulado...")
    
    # Simular los datos que vienen de la base de datos
    class MockBebidaModel:
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
        
        def to_domain(self):
            """Método to_domain simplificado para prueba."""
            from domain.entities import Bebida
            from domain.entities.enums import EtiquetaItem
            
            # Convertir etiquetas
            etiquetas = [EtiquetaItem(etiqueta.etiqueta) for etiqueta in self.etiquetas]
            
            return Bebida(
                id=self.id,
                valor_nutricional=self.valor_nutricional or "",
                precio=self.precio,
                tiempo_preparacion=self.tiempo_preparacion,
                comentarios=self.comentarios or "",
                receta=self.receta or "",
                disponible=self.disponible,
                unidades_disponibles=self.unidades_disponibles,
                num_ingredientes=self.num_ingredientes,
                kcal=self.kcal,
                calorias=self.calorias,
                proteinas=self.proteinas,
                azucares=self.azucares,
                descripcion=self.descripcion,
                etiquetas=etiquetas,
                litros=self.litros,
                alcoholico=self.alcoholico
            )
    
    mock_model = MockBebidaModel()
    
    print(f"   - mock_model.tipo: {mock_model.tipo}")
    
    # Probar to_domain
    print("\n2. Probando to_domain()...")
    try:
        bebida = mock_model.to_domain()
        print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
        print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
        print(f"   - bebida.__dict__: {bebida.__dict__}")
        
        # Probar con Pydantic
        print("\n3. Probando con Pydantic...")
        from infrastructure.handlers.dtos import ItemResponseDTO
        dto = ItemResponseDTO.model_validate(bebida)
        print(f"   - DTO creado exitosamente: {dto.tipo}")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_to_domain()
