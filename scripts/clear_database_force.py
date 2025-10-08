"""
Script para limpiar la base de datos SIN confirmación.
¡USAR CON PRECAUCIÓN!

Ejecutar con:
    python -m scripts.clear_database_force
"""
import asyncio
import sys
import os
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


def get_database_url() -> str:
    """Obtiene la URL de la BD desde .env"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        database_url = "sqlite+aiosqlite:///instance/restaurant.db"
    
    print(f"📊 Usando BD: {database_url}\n")
    return database_url


async def clear_now() -> None:
    """Limpia la BD inmediatamente sin confirmación."""
    
    database_url = get_database_url()
    engine = create_async_engine(database_url, echo=False)
    
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        print("🗑️  Limpiando base de datos...")
        
        await session.execute(text("PRAGMA foreign_keys = OFF"))
        
        tables = ["producto_alergeno", "producto", "alergeno", "categoria", "rol"]
        total: int = 0
        
        for table in tables:
            try:
                # Contar registros
                result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                
                if count is not None and count > 0:
                    # Eliminar registros
                    await session.execute(text(f"DELETE FROM {table}"))
                    total += count
                    print(f"   ✓ {table}: {count} registros eliminados")
                else:
                    print(f"   - {table}: vacío")
                
            except Exception as e:
                # Si la tabla no existe, continuar
                print(f"   ⚠️  {table}: {str(e)}")
        
        # Resetear autoincrement solo si sqlite_sequence existe
        try:
            await session.execute(text("DELETE FROM sqlite_sequence"))
            print(f"   ✓ Autoincrement reseteado")
        except Exception:
            # sqlite_sequence no existe, ignorar
            pass
        
        await session.execute(text("PRAGMA foreign_keys = ON"))
        await session.commit()
        
        print(f"\n✅ {total} registros eliminados en total")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(clear_now())