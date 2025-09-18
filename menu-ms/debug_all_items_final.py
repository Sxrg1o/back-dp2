#!/usr/bin/env python3
"""
Script final para verificar todos los ítems en la base de datos.
"""

def test_all_items_final():
    """Verifica todos los ítems en la base de datos."""
    print("🔍 VERIFICANDO TODOS LOS ÍTEMS FINAL")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from sqlalchemy import text
        
        print("\n1. Obteniendo sesión de base de datos...")
        db = next(get_db())
        
        print("\n2. Consultando todos los ítems...")
        result = db.execute(text("SELECT id, descripcion, tipo FROM items ORDER BY id"))
        items = result.fetchall()
        
        print(f"   - Número de ítems: {len(items)}")
        for item in items:
            print(f"     - ID: {item[0]}, Descripción: {item[1]}, Tipo: {item[2]}")
        
        print("\n3. Consultando todos los platos...")
        result = db.execute(text("SELECT id, peso, tipo_plato FROM platos ORDER BY id"))
        platos = result.fetchall()
        
        print(f"   - Número de platos: {len(platos)}")
        for plato in platos:
            print(f"     - ID: {plato[0]}, Peso: {plato[1]}, Tipo: {plato[2]}")
        
        print("\n4. Consultando todas las bebidas...")
        result = db.execute(text("SELECT id, litros, alcoholico FROM bebidas ORDER BY id"))
        bebidas = result.fetchall()
        
        print(f"   - Número de bebidas: {len(bebidas)}")
        for bebida in bebidas:
            print(f"     - ID: {bebida[0]}, Litros: {bebida[1]}, Alcohólico: {bebida[2]}")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_items_final()
