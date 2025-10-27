"""
Endpoints para gestión de pedido_producto (items de pedido).
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.pedidos.pedido_producto_service import PedidoProductoService
from src.api.schemas.pedido_producto_schema import (
    PedidoProductoCreate,
    PedidoProductoResponse,
    PedidoProductoUpdate,
)
from src.business_logic.exceptions.pedido_producto_exceptions import (
    PedidoProductoValidationError,
    PedidoProductoNotFoundError,
    PedidoProductoConflictError,
)

router = APIRouter(prefix="/pedido-productos", tags=["Pedido Productos"])


@router.post(
    "",
    response_model=PedidoProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo item de pedido",
    description="Crea un nuevo item de producto para un pedido.",
)
async def create_pedido_producto(
    pedido_producto_data: PedidoProductoCreate,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoProductoResponse:
    """Crea un nuevo item de pedido."""
    try:
        pedido_producto_service = PedidoProductoService(session)
        return await pedido_producto_service.create_pedido_producto(pedido_producto_data)
    except PedidoProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{pedido_producto_id}",
    response_model=PedidoProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un item de pedido por ID",
    description="Obtiene los detalles de un item de pedido específico por su ID.",
)
async def get_pedido_producto(
    pedido_producto_id: str, session: AsyncSession = Depends(get_database_session)
) -> PedidoProductoResponse:
    """Obtiene un item de pedido específico por su ID."""
    try:
        pedido_producto_service = PedidoProductoService(session)
        return await pedido_producto_service.get_pedido_producto_by_id(pedido_producto_id)
    except PedidoProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/pedido/{pedido_id}",
    response_model=List[PedidoProductoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener items de un pedido",
    description="Obtiene todos los items de un pedido específico.",
)
async def get_pedido_productos_by_pedido(
    pedido_id: str, session: AsyncSession = Depends(get_database_session)
) -> List[PedidoProductoResponse]:
    """Obtiene todos los items de un pedido específico."""
    try:
        pedido_producto_service = PedidoProductoService(session)
        return await pedido_producto_service.get_pedido_productos_by_pedido(pedido_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{pedido_producto_id}",
    response_model=PedidoProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un item de pedido",
    description="Actualiza los datos de un item de pedido existente.",
)
async def update_pedido_producto(
    pedido_producto_id: str,
    pedido_producto_data: PedidoProductoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoProductoResponse:
    """Actualiza un item de pedido existente."""
    try:
        pedido_producto_service = PedidoProductoService(session)
        return await pedido_producto_service.update_pedido_producto(
            pedido_producto_id, pedido_producto_data
        )
    except PedidoProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PedidoProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{pedido_producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un item de pedido",
    description="Elimina un item de pedido existente del sistema.",
)
async def delete_pedido_producto(
    pedido_producto_id: str, session: AsyncSession = Depends(get_database_session)
) -> None:
    """Elimina un item de pedido existente."""
    try:
        pedido_producto_service = PedidoProductoService(session)
        await pedido_producto_service.delete_pedido_producto(pedido_producto_id)
    except PedidoProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )

