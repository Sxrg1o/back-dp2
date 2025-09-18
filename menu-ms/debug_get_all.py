#!/usr/bin/env python3
"""
Script para debuggear específicamente el método get_all() del repositorio.
"""

def test_get_all_repository():
    """Prueba el método get_all() del repositorio."""
    print("🔍 DEBUGGING MÉTODO get_all() DEL REPOSITORIO")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from infrastructure.repositories.item_repository_impl import ItemRepositoryImpl
        
        print("\n1. Obteniendo sesión de base de datos...")
        db = next(get_db())
        
        print("\n2. Creando repositorio...")
        item_repo = ItemRepositoryImpl(db)
        
        print("\n3. Probando get_all()...")
        items = item_repo.get_all()
        
        print(f"   - Número de ítems: {len(items)}")
        
        for i, item in enumerate(items):
            print(f"\n   - Ítem {i+1}:")
            print(f"     - Tipo: {getattr(item, 'tipo', 'NOT_FOUND')}")
            print(f"     - get_tipo(): {item.get_tipo()}")
            print(f"     - Descripción: {item.descripcion}")
            print(f"     - hasattr(item, 'tipo'): {hasattr(item, 'tipo')}")
            print(f"     - vars(item): {vars(item)}")
            
            if i >= 2:  # Solo mostrar los primeros 3
                break
        
        print("\n4. Probando get_all_with_ingredientes()...")
        items_with_ing = item_repo.get_all_with_ingredientes()
        
        print(f"   - Número de ítems con ingredientes: {len(items_with_ing)}")
        
        for i, item in enumerate(items_with_ing):
            print(f"\n   - Ítem {i+1}:")
            print(f"     - Tipo: {item.get('tipo', 'NOT_FOUND')}")
            print(f"     - Descripción: {item.get('descripcion', 'NOT_FOUND')}")
            
            if i >= 2:  # Solo mostrar los primeros 3
                break
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_get_all_repository()
