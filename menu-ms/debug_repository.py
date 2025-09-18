#!/usr/bin/env python3
"""
Script para debuggear el repositorio específicamente.
"""

from domain.entities import Bebida
from decimal import Decimal

def test_repository_simulation():
    """Simula exactamente lo que hace el repositorio."""
    print("🔍 DEBUGGING SIMULACIÓN DEL REPOSITORIO")
    print("="*50)
    
    # Simular el método to_domain() del ItemModel
    def to_domain_simulation():
        """Simulación del método to_domain() del ItemModel."""
        from domain.entities import Bebida
        from domain.entities.enums import EtiquetaItem
        
        # Simular datos del modelo
        self_id = 5
        self_valor_nutricional = "Rica en antioxidantes y vitamina C"
        self_precio = Decimal('6.50')
        self_tiempo_preparacion = Decimal('15.0')
        self_comentarios = "Bebida tradicional de maíz morado"
        self_receta = "Cocinar maíz morado con canela y clavo, endulzar y servir frío"
        self_disponible = True
        self_unidades_disponibles = 25
        self_num_ingredientes = 3
        self_kcal = 120
        self_calorias = Decimal('120.0')
        self_proteinas = Decimal('1.0')
        self_azucares = Decimal('28.0')
        self_descripcion = "Chicha Morada"
        self_tipo = 'BEBIDA'
        self_litros = Decimal('0.500')
        self_alcoholico = False
        self_etiquetas = []
        
        # Convertir etiquetas
        etiquetas = [EtiquetaItem(etiqueta.etiqueta) for etiqueta in self_etiquetas]
        
        if self_tipo == 'BEBIDA':
            bebida = Bebida(
                id=self_id,
                valor_nutricional=self_valor_nutricional or "",
                precio=self_precio,
                tiempo_preparacion=self_tiempo_preparacion,
                comentarios=self_comentarios or "",
                receta=self_receta or "",
                disponible=self_disponible,
                unidades_disponibles=self_unidades_disponibles,
                num_ingredientes=self_num_ingredientes,
                kcal=self_kcal,
                calorias=self_calorias,
                proteinas=self_proteinas,
                azucares=self_azucares,
                descripcion=self_descripcion,
                etiquetas=etiquetas,
                litros=self_litros,
                alcoholico=self_alcoholico
            )
            return bebida
        else:
            return None
    
    print("\n1. Ejecutando to_domain_simulation()...")
    bebida = to_domain_simulation()
    
    if bebida:
        print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
        print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
        print(f"   - bebida.__dict__: {bebida.__dict__}")
        
        # Probar acceso directo
        print(f"\n2. Probando acceso directo:")
        print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
        print(f"   - bebida.tipo: {bebida.tipo}")
        
        # Probar con vars()
        print(f"\n3. Usando vars():")
        bebida_vars = vars(bebida)
        print(f"   - 'tipo' in bebida_vars: {'tipo' in bebida_vars}")
        print(f"   - bebida_vars['tipo']: {bebida_vars.get('tipo', 'NOT_FOUND')}")
        
        # Probar serialización JSON
        print(f"\n4. Probando serialización JSON:")
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
            print(f"   - Dict para JSON: {bebida_dict}")
            
        except Exception as e:
            print(f"   - Error en serialización: {e}")
    else:
        print("   - Error: No se pudo crear la bebida")

if __name__ == "__main__":
    test_repository_simulation()
