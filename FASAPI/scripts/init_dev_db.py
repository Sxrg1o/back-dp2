#!/usr/bin/env python3
"""
Script to initialize development database with sample data.
"""
import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import async_session_maker, engine
from app.infrastructure.persistence.models.base import Base
from app.infrastructure.persistence.models.item_model import ItemModel
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.models.plato_model import PlatoModel
from app.infrastructure.persistence.models.bebida_model import BebidaModel
from datetime import datetime


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully!")


async def create_sample_data():
    """Create sample data for testing."""
    async with async_session_maker() as session:
        # Sample Items
        items = [
            ItemModel(
                nombre="Tomate",
                descripcion="Tomate fresco orgánico",
                precio=2.50,
                activo=True,
                stock_actual=100,
                stock_minimo=10,
                tiempo_preparacion=5,
                tipo="item",
                etiquetas=["fresco", "orgánico", "vegano"],
                informacion_nutricional={
                    "calorias": 18,
                    "proteinas": 0.9,
                    "azucares": 2.6,
                    "grasas": 0.2,
                    "carbohidratos": 3.9,
                    "fibra": 1.2,
                    "sodio": 5,
                    "vitamina_c": "28mg", 
                    "potasio": "237mg"
                }
            ),
            ItemModel(
                nombre="Pollo",
                descripcion="Pechuga de pollo fresca",
                precio=8.99,
                activo=True,
                stock_actual=50,
                stock_minimo=5,
                tiempo_preparacion=20,
                tipo="item",
                etiquetas=["proteína", "bajo en grasa"],
                informacion_nutricional={
                    "calorias": 165,
                    "proteinas": 31,
                    "azucares": 0,
                    "grasas": 3.6,
                    "carbohidratos": 0,
                    "fibra": 0,
                    "sodio": 74,
                    "vitamina_b6": "0.5mg", 
                    "niacina": "8.5mg"
                }
            )
        ]
        
        # Sample Ingredientes
        ingredientes = [
            IngredienteModel(
                nombre="Cebolla",
                descripcion="Cebolla blanca fresca",
                precio=1.20,
                activo=True,
                stock_actual=80,
                stock_minimo=15,
                tiempo_preparacion=5,
                tipo="ingrediente",
                etiquetas=["fresco", "local", "orgánico"],
                informacion_nutricional={"fibra": "1.7g", "vitamina_c": "7.4mg"},
                tipo_ingrediente="vegetal",
                peso_unitario=1000.0,  # 1kg en gramos
                unidad_medida="kg",
                fecha_vencimiento=datetime(2024, 12, 31),
                proveedor="Verduras del Campo"
            )
        ]
        
        # Sample Platos
        platos = [
            PlatoModel(
                nombre="Ensalada César",
                descripcion="Ensalada fresca con pollo y aderezo césar",
                precio=12.99,
                activo=True,
                stock_actual=25,
                stock_minimo=5,
                tiempo_preparacion=15,
                tipo="plato",
                etiquetas=["saludable", "proteína"],
                informacion_nutricional={"calorias": 350, "proteinas": "25g"},
                tipo_plato="ensalada",
                receta={"lechuga": 200, "pollo": 150, "aderezo": 50},  # gramos
                instrucciones="1. Lavar lechuga\n2. Cortar pollo\n3. Mezclar ingredientes",
                porciones=1,
                dificultad="Fácil",
                chef_recomendado="Chef Mario"
            )
        ]
        
        # Sample Bebidas
        bebidas = [
            BebidaModel(
                nombre="Agua Mineral",
                descripcion="Agua mineral natural",
                precio=2.50,
                activo=True,
                stock_actual=100,
                stock_minimo=20,
                tiempo_preparacion=1,
                tipo="bebida",
                etiquetas=["natural", "sin calorías"],
                informacion_nutricional={"sodio": "5mg", "calcio": "20mg"},
                volumen=500.0,
                contenido_alcohol=0.0,
                temperatura_servicio="Fría",
                tipo_bebida="Sin alcohol",
                marca="AquaPura",
                origen="Nacional"
            )
        ]
        
        # Add all items to session
        session.add_all(items + ingredientes + platos + bebidas)
        await session.commit()
        
        print("✅ Sample data created successfully!")
        print(f"   - {len(items)} items")
        print(f"   - {len(ingredientes)} ingredientes")
        print(f"   - {len(platos)} platos")
        print(f"   - {len(bebidas)} bebidas")


async def main():
    """Main function."""
    print("🚀 Initializing development database...")
    
    try:
        await create_tables()
        await create_sample_data()
        print("\n🎉 Development database initialized successfully!")
        print("\nYou can now:")
        print("1. Start the server: make dev")
        print("2. Visit http://localhost:8000/docs")
        print("3. Test the endpoints!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)