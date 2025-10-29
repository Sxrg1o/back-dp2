"""
Script para limpiar pedidos de prueba antes de ejecutar tests.
"""

import sqlite3
import os

def cleanup_test_pedidos():
    """Elimina pedidos de prueba de la base de datos."""
    db_path = "./app.db"
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Eliminar pedidos de prueba del día actual
        import datetime
        today = datetime.datetime.now().strftime("%Y%m%d")
        pattern = f"{today}-MTEST%"
        
        cursor.execute("DELETE FROM pedido_opcion WHERE id_pedido_producto IN (SELECT id FROM pedido_producto WHERE id_pedido IN (SELECT id FROM pedido WHERE numero_pedido LIKE ?))", (pattern,))
        cursor.execute("DELETE FROM pedido_producto WHERE id_pedido IN (SELECT id FROM pedido WHERE numero_pedido LIKE ?)", (pattern,))
        cursor.execute("DELETE FROM pedido WHERE numero_pedido LIKE ?", (pattern,))
        
        conn.commit()
        
        # Contar cuántos se eliminaron
        cursor.execute("SELECT COUNT(*) FROM pedido WHERE numero_pedido LIKE ?", (pattern,))
        remaining = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Pedidos de prueba eliminados")
        print(f"   Patrón: {pattern}")
        print(f"   Pedidos restantes con ese patrón: {remaining}")
        
    except Exception as e:
        print(f"❌ Error al limpiar pedidos: {e}")

if __name__ == "__main__":
    cleanup_test_pedidos()
