#!/usr/bin/env python3
"""
Script para debuggear el repositorio real.
"""

def test_real_repository():
    """Prueba el repositorio real."""
    print("🔍 DEBUGGING REPOSITORIO REAL")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from infrastructure.repositories.item_repository_impl import ItemRepositoryImpl
        from application.services.item_service import ItemService
        from infrastructure.repositories.item_repository_impl import PlatoRepositoryImpl, BebidaRepositoryImpl
        
        print("\n1. Obteniendo sesión de base de datos...")
        db = next(get_db())
        
        print("\n1.1. Creando tablas...")
        from infrastructure.db import create_tables
        create_tables()
        
        print("\n2. Creando repositorios...")
        item_repo = ItemRepositoryImpl(db)
        plato_repo = PlatoRepositoryImpl(db)
        bebida_repo = BebidaRepositoryImpl(db)
        
        print("\n3. Creando servicio...")
        service = ItemService(item_repo, plato_repo, bebida_repo)
        
        print("\n4. Probando get_all_items()...")
        items = service.get_all_items()
        
        print(f"   - Número de ítems: {len(items)}")
        
        for i, item in enumerate(items):
            print(f"   - Ítem {i+1}:")
            print(f"     - Tipo: {getattr(item, 'tipo', 'NOT_FOUND')}")
            print(f"     - get_tipo(): {item.get_tipo()}")
            print(f"     - Descripción: {item.descripcion}")
            print(f"     - hasattr(item, 'tipo'): {hasattr(item, 'tipo')}")
            
            if i >= 2:  # Solo mostrar los primeros 3
                break
        
        print("\n5. Probando get_all_items_with_ingredientes()...")
        items_with_ing = service.get_all_items_with_ingredientes()
        
        print(f"   - Número de ítems con ingredientes: {len(items_with_ing)}")
        
        for i, item in enumerate(items_with_ing):
            print(f"   - Ítem {i+1}:")
            print(f"     - Tipo: {item.get('tipo', 'NOT_FOUND')}")
            print(f"     - Descripción: {item.get('descripcion', 'NOT_FOUND')}")
            
            if i >= 2:  # Solo mostrar los primeros 3
                break
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_repository()
