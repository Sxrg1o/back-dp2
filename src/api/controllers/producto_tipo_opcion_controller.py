"""
Endpoints para gestión de opciones de productos por tipo.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.pedidos.producto_tipo_opcion_service import ProductoTipoOpcionService
from src.api.schemas.producto_tipo_opcion_schema import (
    ProductoTipoOpcionCreate,
    ProductoTipoOpcionResponse,
    ProductoTipoOpcionUpdate,
    ProductoTipoOpcionList,
)
from src.business_logic.exceptions.producto_tipo_opcion_exceptions import (
    ProductoTipoOpcionValidationError,
    ProductoTipoOpcionNotFoundError,
    ProductoTipoOpcionConflictError,
)

router = APIRouter(prefix="/producto-tipo-opciones", tags=["Producto Tipo Opciones"])


@router.post(
    "",
    response_model=ProductoTipoOpcionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva opción de producto por tipo",
    description="Crea una nueva opción de producto por tipo en el sistema con los datos proporcionados.",
)
async def create_producto_tipo_opcion(
    producto_tipo_opcion_data: ProductoTipoOpcionCreate, session: AsyncSession = Depends(get_database_session)
) -> ProductoTipoOpcionResponse:
    """
    Crea una nueva opción de producto en el sistema.
    
    Args:
        producto_opcion_data: Datos de la opción de producto a crear.
        session: Sesión de base de datos.

    Returns:
        La opción de producto creada con todos sus datos.

    Raises:
        HTTPException:
            - 409: Si ya existe una opción de producto con el mismo nombre.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_tipo_opcion_service = ProductoTipoOpcionService(session)
        return await producto_tipo_opcion_service.create_producto_tipo_opcion(producto_tipo_opcion_data)
    except ProductoTipoOpcionConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{producto_tipo_opcion_id}",
    response_model=ProductoTipoOpcionResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una opción de producto por tipo por ID",
    description="Obtiene los detalles de una opción de producto por tipo específica por su ID.",
)
async def get_producto_tipo_opcion(
    producto_tipo_opcion_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> ProductoTipoOpcionResponse:
    """
    Obtiene una opción de producto específica por su ID.

    Args:
        producto_opcion_id: ID de la opción de producto a buscar.
        session: Sesión de base de datos.

    Returns:
        La opción de producto encontrada con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra la opción de producto.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_tipo_opcion_service = ProductoTipoOpcionService(session)
        return await producto_tipo_opcion_service.get_producto_tipo_opcion_by_id(producto_tipo_opcion_id)
    except ProductoTipoOpcionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "",
    response_model=ProductoTipoOpcionList,
    status_code=status.HTTP_200_OK,
    summary="Listar opciones de productos por tipo",
    description="Obtiene una lista paginada de opciones de productos por tipo.",
)
async def list_producto_tipo_opciones(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(
        100, gt=0, le=500, description="Número máximo de registros a retornar"
    ),
    session: AsyncSession = Depends(get_database_session),
) -> ProductoTipoOpcionList:
    """
    Obtiene una lista paginada de opciones de productos.
    
    Args:
        skip: Número de registros a omitir (offset), por defecto 0.
        limit: Número máximo de registros a retornar, por defecto 100.
        session: Sesión de base de datos.

    Returns:
        Lista paginada de opciones de productos y el número total de registros.

    Raises:
        HTTPException:
            - 400: Si los parámetros de paginación son inválidos.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_tipo_opcion_service = ProductoTipoOpcionService(session)
        return await producto_tipo_opcion_service.get_producto_tipo_opciones(skip, limit)
    except ProductoTipoOpcionValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{producto_tipo_opcion_id}",
    response_model=ProductoTipoOpcionResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una opción de producto por tipo",
    description="Actualiza los datos de una opción de producto por tipo existente.",
)
async def update_producto_tipo_opcion(
    producto_tipo_opcion_id: UUID,
    producto_tipo_opcion_data: ProductoTipoOpcionUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> ProductoTipoOpcionResponse:
    """
    Actualiza una opción de producto existente.

    Args:
        producto_opcion_id: ID de la opción de producto a actualizar.
        producto_opcion_data: Datos de la opción de producto a actualizar.
        session: Sesión de base de datos.

    Returns:
        La opción de producto actualizada con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra la opción de producto.
            - 409: Si hay un conflicto (e.g., nombre duplicado).
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_tipo_opcion_service = ProductoTipoOpcionService(session)
        return await producto_tipo_opcion_service.update_producto_tipo_opcion(producto_tipo_opcion_id, producto_tipo_opcion_data)
    except ProductoTipoOpcionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductoTipoOpcionConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{producto_tipo_opcion_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una opción de producto por tipo",
    description="Elimina una opción de producto por tipo existente del sistema.",
)
async def delete_producto_tipo_opcion(
    producto_tipo_opcion_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> None:
    """
    Elimina una opción de producto existente.

    Args:
        producto_opcion_id: ID de la opción de producto a eliminar.
        session: Sesión de base de datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra la opción de producto.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_tipo_opcion_service = ProductoTipoOpcionService(session)
        result = await producto_tipo_opcion_service.delete_producto_tipo_opcion(producto_tipo_opcion_id)
        # No es necesario verificar el resultado aquí ya que delete_producto_tipo_opcion
        # lanza ProductoTipoOpcionNotFoundError si no encuentra la opción
    except ProductoTipoOpcionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )
