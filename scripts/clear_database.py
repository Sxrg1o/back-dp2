"""
Script para limpiar todos los datos de la base de datos.

ADVERTENCIA: Este script eliminará TODOS los datos de la base de datos.
Usar solo en desarrollo/testing.

Ejecutar con:
    python -m scripts.clear_database
"""
import asyncio
import sys
import os
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.database import BaseModel


def get_database_url() -> str:
    """Obtiene la URL de la BD desde .env"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        database_url = "sqlite+aiosqlite:///app.db"
    
    return database_url


async def clear_all_data():
    """Elimina todos los datos de todas las tablas."""
    
    database_url = get_database_url()
    engine = create_async_engine(database_url, echo=False)
    
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        print("🗑️  Eliminando datos de todas las tablas...\n")
        
        try:
            # Deshabilitar verificación de foreign keys temporalmente (SQLite)
            await session.execute(text("PRAGMA foreign_keys = OFF"))
            
            # Obtener todas las tablas (en orden correcto para evitar FK errors)
            tables = [
                "producto_alergeno",  # Primero las tablas con FK
                "producto",
                "alergeno",
                "categoria",
                "usuario",
                "rol",
            ]
            
            deleted_counts = {}
            
            for table in tables:
                try:
                    # Contar registros antes de eliminar
                    result = await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count_before = result.scalar()
                    
                    if count_before is not None and count_before > 0:
                        # Eliminar todos los registros
                        await session.execute(text(f"DELETE FROM {table}"))
                        deleted_counts[table] = count_before
                        print(f"   ✓ {table}: {count_before} registro(s) eliminado(s)")
                    else:
                        deleted_counts[table] = 0
                        print(f"   - {table}: vacío")
                        
                except Exception as e:
                    print(f"   ⚠️  {table}: {str(e)}")
                    deleted_counts[table] = 0
            
            # Resetear autoincrement solo si sqlite_sequence existe
            try:
                await session.execute(text("DELETE FROM sqlite_sequence"))
                print(f"   ✓ Autoincrement reseteado")
            except Exception:
                # sqlite_sequence no existe, ignorar
                pass
            
            # Reactivar verificación de foreign keys
            await session.execute(text("PRAGMA foreign_keys = ON"))
            
            await session.commit()
            
            print("\n" + "="*60)
            print("✅ Base de datos limpiada exitosamente")
            print("="*60)
            print(f"   Total de registros eliminados: {sum(deleted_counts.values())}")
            print("="*60)
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error al limpiar la base de datos: {str(e)}")
            raise
        finally:
            await engine.dispose()


async def drop_all_tables():
    """Elimina todas las tablas de la base de datos."""
    
    database_url = get_database_url()
    engine = create_async_engine(database_url, echo=False)
    
    async with engine.begin() as conn:
        print("🗑️  Eliminando todas las tablas...\n")
        await conn.run_sync(BaseModel.metadata.drop_all)
        print("   ✓ Todas las tablas eliminadas\n")
    
    await engine.dispose()


async def recreate_tables():
    """Recrea todas las tablas vacías."""
    
    database_url = get_database_url()
    engine = create_async_engine(database_url, echo=False)
    
    async with engine.begin() as conn:
        print("🔨 Recreando tablas...\n")
        await conn.run_sync(BaseModel.metadata.create_all)
        print("   ✓ Tablas recreadas\n")
    
    await engine.dispose()


async def main():
    """Función principal con opciones de limpieza."""
    
    database_url = get_database_url()
    
    print("="*60)
    print("   LIMPIEZA DE BASE DE DATOS")
    print("="*60)
    print(f"\n📊 Base de datos: {database_url}\n")
    print("Seleccione una opción:")
    print("  1. Limpiar datos (mantener estructura de tablas)")
    print("  2. Eliminar y recrear tablas (reset completo)")
    print("  3. Cancelar")
    print("="*60)
    
    opcion = input("\nOpción [1-3]: ").strip()
    
    if opcion == "1":
        confirmacion = input("\n⚠️  ¿Estás seguro de eliminar TODOS los datos? (si/no): ").strip().lower()
        if confirmacion in ["si", "s", "yes", "y"]:
            await clear_all_data()
        else:
            print("\n❌ Operación cancelada")
    
    elif opcion == "2":
        confirmacion = input("\n⚠️  ¿Estás seguro de ELIMINAR y RECREAR todas las tablas? (si/no): ").strip().lower()
        if confirmacion in ["si", "s", "yes", "y"]:
            await drop_all_tables()
            await recreate_tables()
            print("="*60)
            print("✅ Base de datos recreada exitosamente")
            print("="*60)
        else:
            print("\n❌ Operación cancelada")
    
    elif opcion == "3":
        print("\n❌ Operación cancelada")
    
    else:
        print("\n❌ Opción inválida")


if __name__ == "__main__":
    asyncio.run(main())