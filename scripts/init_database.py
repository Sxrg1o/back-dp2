"""
Script de inicialización de la base de datos para Docker.
Este script se ejecuta al iniciar el contenedor para asegurar que la BD esté poblada.
"""

import asyncio
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.database import BaseModel
from src.models.menu.categoria_model import CategoriaModel
from scripts.seed_cevicheria_data import CevicheriaSeeder
from sqlalchemy import select, func


def get_database_url() -> str:
    """
    Obtiene la URL de la base de datos desde variables de entorno o usa SQLite por defecto.
    
    Returns:
        str: URL de conexión a la base de datos
    """
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Fallback para Docker
        database_url = "sqlite+aiosqlite:///./app.db"
    
    return database_url


async def init_database():
    """
    Inicializa la base de datos creando las tablas y ejecutando el seed si es necesario.
    """
    database_url = get_database_url()
    print(f"🔧 Inicializando base de datos: {database_url}")
    
    # Crear engine
    engine = create_async_engine(database_url, echo=False)
    
    try:
        # Crear tablas si no existen
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        print("✅ Tablas creadas/verificadas correctamente")
        
        # Verificar si la BD está vacía
        async_session = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            # Contar categorías existentes
            query = select(func.count(CategoriaModel.id))
            result = await session.execute(query)
            count = result.scalar()
            
            print(f"📊 Categorías encontradas: {count}")
            
            if count == 0:
                print("🌱 Base de datos vacía detectada. Ejecutando seed...")
                
                # Ejecutar seed
                seeder = CevicheriaSeeder(session)
                await seeder.seed_all()
                await session.commit()
                
                print("✅ Seed completado exitosamente!")
            else:
                print(f"✅ Base de datos ya contiene datos ({count} categorías). Skip seed.")
                
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    print("="*60)
    print("   INICIALIZACIÓN DE BASE DE DATOS - DOCKER")
    print("="*60)
    asyncio.run(init_database())

