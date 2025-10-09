"""
Endpoints para gestión del seed de la base de datos.
"""

import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.core.database import get_database_session
from src.api.schemas.seed_schema import SeedResponse, SeedResult
from src.models.menu.categoria_model import CategoriaModel
from scripts.seed_cevicheria_data import CevicheriaSeeder

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post(
    "/execute",
    response_model=SeedResponse,
    status_code=status.HTTP_200_OK,
    summary="Ejecutar seed de la base de datos",
    description="Ejecuta el script de seed para poblar la base de datos con datos iniciales de la cevichería.",
)
async def execute_seed(
    force: bool = False,
    session: AsyncSession = Depends(get_database_session)
) -> SeedResponse:
    """
    Ejecuta el seed de la base de datos.
    
    Args:
        force: Si es True, ejecuta el seed aunque ya existan datos.
        session: Sesión de base de datos.

    Returns:
        Resultado de la ejecución del seed con estadísticas detalladas.

    Raises:
        HTTPException:
            - 409: Si ya existen datos y force=False.
            - 500: Si ocurre un error interno del servidor.
    """
    start_time = time.time()
    timestamp = datetime.now().isoformat()
    
    try:
        # Verificar si ya existen datos
        if not force:
            query = select(func.count(CategoriaModel.id))
            result = await session.execute(query)
            count = result.scalar()
            
            if count > 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existen {count} categorías en la base de datos. Use force=true para sobrescribir."
                )
        
        # Ejecutar el seed
        seeder = CevicheriaSeeder(session)
        await seeder.seed_all()
        
        # Commit de los cambios
        await session.commit()
        
        execution_time = time.time() - start_time
        
        # Preparar respuesta
        result = SeedResult(
            success=True,
            message="Seed ejecutado exitosamente",
            data_created={
                "roles": len(seeder.roles),
                "categorias": len(seeder.categorias),
                "alergenos": len(seeder.alergenos),
                "productos": len(seeder.productos),
                "tipos_opciones": len(seeder.tipos_opciones),
                "productos_opciones": len(seeder.productos_opciones)
            },
            execution_time=round(execution_time, 2)
        )
        
        return SeedResponse(
            status="success",
            result=result,
            timestamp=timestamp
        )
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        
        result = SeedResult(
            success=False,
            message=f"Error al ejecutar seed: {str(e)}",
            data_created={},
            execution_time=round(execution_time, 2)
        )
        
        return SeedResponse(
            status="error",
            result=result,
            timestamp=timestamp
        )


@router.get(
    "/status",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Verificar estado del seed",
    description="Verifica si la base de datos ya contiene datos de seed.",
)
async def get_seed_status(
    session: AsyncSession = Depends(get_database_session)
) -> dict:
    """
    Verifica el estado actual del seed en la base de datos.
    
    Args:
        session: Sesión de base de datos.

    Returns:
        Estado actual de los datos en la base de datos.
    """
    try:
        # Contar registros por tipo
        from src.models.auth.rol_model import RolModel
        from src.models.menu.alergeno_model import AlergenoModel
        from src.models.menu.producto_model import ProductoModel
        from src.models.pedidos.tipo_opciones_model import TipoOpcionModel
        from src.models.pedidos.producto_opcion_model import ProductoOpcionModel
        
        counts = {}
        
        # Contar roles
        query = select(func.count(RolModel.id))
        result = await session.execute(query)
        counts["roles"] = result.scalar()
        
        # Contar categorías
        query = select(func.count(CategoriaModel.id))
        result = await session.execute(query)
        counts["categorias"] = result.scalar()
        
        # Contar alérgenos
        query = select(func.count(AlergenoModel.id))
        result = await session.execute(query)
        counts["alergenos"] = result.scalar()
        
        # Contar productos
        query = select(func.count(ProductoModel.id))
        result = await session.execute(query)
        counts["productos"] = result.scalar()
        
        # Contar tipos de opciones
        query = select(func.count(TipoOpcionModel.id))
        result = await session.execute(query)
        counts["tipos_opciones"] = result.scalar()
        
        # Contar opciones de productos
        query = select(func.count(ProductoOpcionModel.id))
        result = await session.execute(query)
        counts["productos_opciones"] = result.scalar()
        
        # Determinar si la BD está poblada
        total_records = sum(counts.values())
        is_populated = total_records > 0
        
        return {
            "is_populated": is_populated,
            "total_records": total_records,
            "counts": counts,
            "message": "Base de datos poblada" if is_populated else "Base de datos vacía"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar estado del seed: {str(e)}"
        )
