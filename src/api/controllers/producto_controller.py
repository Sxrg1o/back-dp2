"""
Endpoints para gestión de productos.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
    ProductoList,
)
from src.business_logic.exceptions.producto_exceptions import (
    ProductoValidationError,
    ProductoNotFoundError,
    ProductoConflictError,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto en el sistema con los datos proporcionados.",
)
async def create_producto(
    producto_data: ProductoCreate, session: AsyncSession = Depends(get_database_session)
) -> ProductoResponse:
    """
    Crea un nuevo producto en el sistema.
    
    Args:
        producto_data: Datos del producto a crear.
        session: Sesión de base de datos.

    Returns:
        El producto creado con todos sus datos.

    Raises:
        HTTPException:
            - 409: Si ya existe un producto con el mismo nombre.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_service = ProductoService(session)
        return await producto_service.create_producto(producto_data)
    except ProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un producto por ID",
    description="Obtiene los detalles de un producto específico por su ID.",
)
async def get_producto(
    producto_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> ProductoResponse:
    """
    Obtiene un producto específico por su ID.

    Args:
        producto_id: ID del producto a buscar.
        session: Sesión de base de datos.

    Returns:
        El producto encontrado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el producto.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_service = ProductoService(session)
        return await producto_service.get_producto_by_id(producto_id)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "",
    response_model=ProductoList,
    status_code=status.HTTP_200_OK,
    summary="Listar productos",
    description="Obtiene una lista paginada de productos.",
)
async def list_productos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(
        100, gt=0, le=500, description="Número máximo de registros a retornar"
    ),
    session: AsyncSession = Depends(get_database_session),
) -> ProductoList:
    """
    Obtiene una lista paginada de productos.
    
    Args:
        skip: Número de registros a omitir (offset), por defecto 0.
        limit: Número máximo de registros a retornar, por defecto 100.
        session: Sesión de base de datos.

    Returns:
        Lista paginada de productos y el número total de registros.

    Raises:
        HTTPException:
            - 400: Si los parámetros de paginación son inválidos.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_service = ProductoService(session)
        return await producto_service.get_productos(skip, limit)
    except ProductoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un producto",
    description="Actualiza los datos de un producto existente.",
)
async def update_producto(
    producto_id: UUID,
    producto_data: ProductoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> ProductoResponse:
    """
    Actualiza un producto existente.

    Args:
        producto_id: ID del producto a actualizar.
        producto_data: Datos del producto a actualizar.
        session: Sesión de base de datos.

    Returns:
        El producto actualizado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el producto.
            - 409: Si hay un conflicto (e.g., nombre duplicado).
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_service = ProductoService(session)
        return await producto_service.update_producto(producto_id, producto_data)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un producto",
    description="Elimina un producto existente del sistema.",
)
async def delete_producto(
    producto_id: UUID, session: AsyncSession = Depends(get_database_session)
) -> None:
    """
    Elimina un producto existente.

    Args:
        producto_id: ID del producto a eliminar.
        session: Sesión de base de datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el producto.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        producto_service = ProductoService(session)
        result = await producto_service.delete_producto(producto_id)
        # No es necesario verificar el resultado aquí ya que delete_producto
        # lanza ProductoNotFoundError si no encuentra el producto
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )
