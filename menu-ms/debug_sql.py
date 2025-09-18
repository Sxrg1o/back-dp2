#!/usr/bin/env python3
"""
Script para debuggear directamente con SQL.
"""

def test_sql_direct():
    """Prueba directamente con SQL."""
    print("🔍 DEBUGGING CON SQL DIRECTO")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from sqlalchemy import text
        
        print("\n1. Obteniendo sesión de base de datos...")
        db = next(get_db())
        
        print("\n2. Consultando tabla items directamente...")
        result = db.execute(text("SELECT id, descripcion, tipo FROM items LIMIT 5"))
        items = result.fetchall()
        
        print(f"   - Número de ítems en BD: {len(items)}")
        for item in items:
            print(f"     - ID: {item[0]}, Descripción: {item[1]}, Tipo: {item[2]}")
        
        print("\n3. Consultando tabla platos...")
        result = db.execute(text("SELECT id, peso, tipo_plato FROM platos LIMIT 5"))
        platos = result.fetchall()
        
        print(f"   - Número de platos en BD: {len(platos)}")
        for plato in platos:
            print(f"     - ID: {plato[0]}, Peso: {plato[1]}, Tipo: {plato[2]}")
        
        print("\n4. Consultando tabla bebidas...")
        result = db.execute(text("SELECT id, litros, alcoholico FROM bebidas LIMIT 5"))
        bebidas = result.fetchall()
        
        print(f"   - Número de bebidas en BD: {len(bebidas)}")
        for bebida in bebidas:
            print(f"     - ID: {bebida[0]}, Litros: {bebida[1]}, Alcohólico: {bebida[2]}")
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sql_direct()
