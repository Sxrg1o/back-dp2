#!/usr/bin/env python3
"""
Script final para debuggar el modelo real de la base de datos.
"""

def test_real_model_final():
    """Prueba final del modelo real de la base de datos."""
    print("🔍 DEBUGGING MODELO REAL FINAL")
    print("="*50)
    
    try:
        from infrastructure.db import get_db
        from infrastructure.models.item_model import ItemModel
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        from infrastructure.db import DATABASE_URL
        
        print("\n1. Creando sesión de base de datos...")
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("\n2. Consultando ítem con ID 5...")
        item_model = db.query(ItemModel).filter(ItemModel.id == 5).first()
        
        if item_model:
            print(f"   - Modelo encontrado: {item_model}")
            print(f"   - Tipo del modelo: {item_model.tipo}")
            print(f"   - hasattr(item_model, 'to_domain'): {hasattr(item_model, 'to_domain')}")
            
            print("\n3. Probando to_domain()...")
            bebida = item_model.to_domain()
            
            if bebida:
                print(f"   - bebida.tipo: {getattr(bebida, 'tipo', 'NOT_FOUND')}")
                print(f"   - bebida.get_tipo(): {bebida.get_tipo()}")
                print(f"   - bebida.__dict__: {bebida.__dict__}")
                
                print("\n4. Probando acceso directo:")
                print(f"   - hasattr(bebida, 'tipo'): {hasattr(bebida, 'tipo')}")
                print(f"   - bebida.tipo: {bebida.tipo}")
                
            else:
                print("   - Error: No se pudo crear la bebida")
        else:
            print("   - No se encontró el modelo con ID 5")
        
        db.close()
        
    except Exception as e:
        print(f"   - Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_model_final()