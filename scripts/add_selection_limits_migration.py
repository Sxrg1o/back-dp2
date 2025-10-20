"""
Script de migración para agregar columnas seleccion_minima y seleccion_maxima
a la tabla tipo_opcion.

Este script agrega las restricciones de selección al modelo TipoOpcionModel.
"""

import asyncio
import logging
from sqlalchemy import text
from src.core.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_selection_columns():
    """
    Agrega las columnas seleccion_minima y seleccion_maxima a tipo_opcion.
    """
    db_manager = DatabaseManager()
    
    try:
        async with db_manager.session() as session:
            logger.info("🔧 Iniciando migración de tipo_opcion...")
            
            # Verificar si las columnas ya existen
            check_query = text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('tipo_opcion') 
                WHERE name IN ('seleccion_minima', 'seleccion_maxima')
            """)
            result = await session.execute(check_query)
            existing_columns = result.scalar()
            
            # if existing_columns >= 2:
            #     logger.info("✅ Las columnas ya existen. Migración no necesaria.")
            #     return
            
            logger.info("📝 Agregando columna seleccion_minima...")
            await session.execute(text("""
                ALTER TABLE tipo_opcion 
                ADD COLUMN seleccion_minima INTEGER NOT NULL DEFAULT 0
            """))
            
            logger.info("📝 Agregando columna seleccion_maxima...")
            await session.execute(text("""
                ALTER TABLE tipo_opcion 
                ADD COLUMN seleccion_maxima INTEGER DEFAULT NULL
            """))
            
            # Actualizar valores por defecto basados en el nombre del tipo
            logger.info("🔄 Configurando valores por defecto...")
            
            # Tamaño: obligatorio, solo uno (minimo=1, maximo=1)
            await session.execute(text("""
                UPDATE tipo_opcion 
                SET seleccion_minima = 1, seleccion_maxima = 1 
                WHERE LOWER(nombre) LIKE '%tamaño%' OR LOWER(nombre) LIKE '%tamano%'
            """))
            
            # Picante/Ají: opcional, solo uno (minimo=0, maximo=1)
            await session.execute(text("""
                UPDATE tipo_opcion 
                SET seleccion_minima = 0, seleccion_maxima = 1 
                WHERE LOWER(nombre) LIKE '%picante%' 
                   OR LOWER(nombre) LIKE '%ají%' 
                   OR LOWER(nombre) LIKE '%aji%'
            """))
            
            # Extras/Adicionales: opcional, sin límite (minimo=0, maximo=NULL)
            await session.execute(text("""
                UPDATE tipo_opcion 
                SET seleccion_minima = 0, seleccion_maxima = NULL 
                WHERE LOWER(nombre) LIKE '%extra%' 
                   OR LOWER(nombre) LIKE '%adicional%'
                   OR LOWER(nombre) LIKE '%agregado%'
            """))
            
            # Acompañamientos: opcional, máximo 3 (minimo=0, maximo=3)
            await session.execute(text("""
                UPDATE tipo_opcion 
                SET seleccion_minima = 0, seleccion_maxima = 3 
                WHERE LOWER(nombre) LIKE '%acompañamiento%' 
                   OR LOWER(nombre) LIKE '%acompanamiento%'
            """))
            
            await session.commit()
            
            logger.info("✅ Migración completada exitosamente!")
            
            # Mostrar estado actual
            logger.info("\n📊 Estado actual de tipos de opciones:")
            result = await session.execute(text("""
                SELECT nombre, seleccion_minima, seleccion_maxima 
                FROM tipo_opcion 
                ORDER BY orden
            """))
            
            for row in result:
                max_str = str(row.seleccion_maxima) if row.seleccion_maxima else "∞"
                logger.info(
                    f"  - {row.nombre}: "
                    f"min={row.seleccion_minima}, max={max_str}"
                )
            
    except Exception as e:
        logger.error(f"❌ Error durante la migración: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


async def main():
    """Punto de entrada principal."""
    logger.info("=" * 60)
    logger.info("MIGRACIÓN: Agregar seleccion_minima y seleccion_maxima")
    logger.info("=" * 60)
    
    await add_selection_columns()
    
    logger.info("\n🎉 Proceso completado!")


if __name__ == "__main__":
    asyncio.run(main())
