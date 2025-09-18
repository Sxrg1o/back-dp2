#!/usr/bin/env python3
"""
Script final para debuggear específicamente el ítem con ID 5.
"""

def test_item_5_final():
    """Prueba final del ítem con ID 5."""
    print("🔍 DEBUGGING ÍTEM CON ID 5 FINAL")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from infrastructure.models.item_model import ItemModel
        from sqlalchemy import text
        
        print("\n1. Obteniendo sesión de base de datos...")
        db = next(get_db())
        
        print("\n2. Consultando ítem con ID 5 directamente...")
        result = db.execute(text("SELECT * FROM items WHERE id = 5"))
        item_data = result.fetchone()
        
        if item_data:
            print(f"   - Datos del ítem: {dict(item_data._mapping)}")
        else:
            print("   - No se encontró el ítem con ID 5")
            return
        
        print("\n3. Consultando bebida con ID 5...")
        result = db.execute(text("SELECT * FROM bebidas WHERE id = 5"))
        bebida_data = result.fetchone()
        
        if bebida_data:
            print(f"   - Datos de la bebida: {dict(bebida_data._mapping)}")
        else:
            print("   - No se encontró la bebida con ID 5")
            return
        
        print("\n4. Creando modelo ItemModel...")
        # Crear un modelo simulado con los datos de la BD
        class MockItemModel:
            def __init__(self, item_data, bebida_data):
                self.id = item_data['id']
                self.valor_nutricional = item_data['valor_nutricional']
                self.precio = item_data['precio']
                self.tiempo_preparacion = item_data['tiempo_preparacion']
                self.comentarios = item_data['comentarios']
                self.receta = item_data['receta']
                self.disponible = item_data['disponible']
                self.unidades_disponibles = item_data['unidades_disponibles']
                self.num_ingredientes = item_data['num_ingredientes']
                self.kcal = item_data['kcal']
                self.calorias = item_data['calorias']
                self.proteinas = item_data['proteinas']
                self.azucares = item_data['azucares']
                self.descripcion = item_data['descripcion']
                self.tipo = item_data['tipo']
                self.litros = bebida_data['litros']
                self.alcoholico = bebida_data['alcoholico']
                self.etiquetas = []
            
            def to_domain(self):
                from domain.entities import Bebida
                from domain.entities.enums import EtiquetaItem
                
                # Convertir etiquetas
                etiquetas = [EtiquetaItem(etiqueta.etiqueta) for etiqueta in self.etiquetas]
                
                if self.tipo == 'BEBIDA':
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
                else:
                    return None
        
        mock_model = MockItemModel(item_data, bebida_data)
        
        print("\n5. Probando to_domain()...")
        bebida = mock_model.to_domain()
        
        if bebida:
            print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
            print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
            print(f"   - bebida.__dict__: {bebida.__dict__}")
            
            # Probar con Pydantic
            print("\n6. Probando con Pydantic...")
            try:
                from infrastructure.handlers.dtos import ItemResponseDTO
                dto = ItemResponseDTO.model_validate(bebida)
                print(f"   - DTO creado exitosamente: {dto.tipo}")
            except Exception as e:
                print(f"   - Error Pydantic: {e}")
        else:
            print("   - Error: No se pudo crear la bebida")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_item_5_final()
