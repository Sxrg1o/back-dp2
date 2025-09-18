#!/usr/bin/env python3
"""
Script final para debuggear el método to_domain() del modelo.
"""

def test_model_to_domain_final():
    """Prueba final del método to_domain() del modelo."""
    print("🔍 DEBUGGING MÉTODO to_domain() FINAL")
    print("="*50)
    
    try:
        from domain.entities import Bebida
        from decimal import Decimal
        
        print("\n1. Simulando el método to_domain() del ItemModel...")
        
        # Simular los datos que vienen de la base de datos
        class MockItemModel:
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
                """Método to_domain exacto del ItemModel."""
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
        
        mock_model = MockItemModel()
        
        print("\n2. Ejecutando to_domain()...")
        bebida = mock_model.to_domain()
        
        if bebida:
            print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
            print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
            print(f"   - bebida.__dict__: {bebida.__dict__}")
            
            print("\n3. Probando acceso directo:")
            print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
            print(f"   - bebida.tipo: {bebida.tipo}")
            
            print("\n4. Probando con vars():")
            bebida_vars = vars(bebida)
            print(f"   - 'tipo' in bebida_vars: {'tipo' in bebida_vars}")
            print(f"   - bebida_vars['tipo']: {bebida_vars.get('tipo', 'NOT_FOUND')}")
            
        else:
            print("   - Error: No se pudo crear la bebida")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_to_domain_final()