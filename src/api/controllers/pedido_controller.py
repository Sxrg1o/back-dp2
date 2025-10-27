"""
Endpoints para gestión de pedidos.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.pedidos.pedido_service import PedidoService
from src.api.schemas.pedido_schema import (
    PedidoCreate,
    PedidoResponse,
    PedidoUpdate,
    PedidoList,
    PedidoConProductosResponse,
)
from src.business_logic.exceptions.pedido_exceptions import (
    PedidoValidationError,
    PedidoNotFoundError,
    PedidoConflictError,
)
from src.core.enums.pedido_enums import EstadoPedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo pedido",
    description="Crea un nuevo pedido en el sistema con los datos proporcionados.",
)
async def create_pedido(
    pedido_data: PedidoCreate, session: AsyncSession = Depends(get_database_session)
) -> PedidoResponse:
    """Crea un nuevo pedido en el sistema."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.create_pedido(pedido_data)
    except PedidoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un pedido por ID",
    description="Obtiene los detalles de un pedido específico por su ID.",
)
async def get_pedido(
    pedido_id: str, session: AsyncSession = Depends(get_database_session)
) -> PedidoResponse:
    """Obtiene un pedido específico por su ID."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.get_pedido_by_id(pedido_id)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{pedido_id}/productos",
    response_model=PedidoConProductosResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener pedido con productos",
    description="Obtiene un pedido con todos sus productos incluidos.",
)
async def get_pedido_con_productos(
    pedido_id: str, session: AsyncSession = Depends(get_database_session)
) -> PedidoConProductosResponse:
    """Obtiene un pedido con todos sus productos."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.get_pedido_by_id_with_productos(pedido_id)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "",
    response_model=PedidoList,
    status_code=status.HTTP_200_OK,
    summary="Listar pedidos",
    description="Obtiene una lista paginada de pedidos.",
)
async def list_pedidos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(100, gt=0, le=500, description="Número máximo de registros a retornar"),
    id_mesa: str = Query(None, description="Filtrar pedidos por ID de mesa"),
    estado: str = Query(None, description="Filtrar pedidos por estado"),
    session: AsyncSession = Depends(get_database_session),
) -> PedidoList:
    """Obtiene una lista paginada de pedidos."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.get_pedidos(skip, limit, id_mesa, estado)
    except PedidoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{pedido_id}",
    response_model=PedidoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un pedido",
    description="Actualiza los datos de un pedido existente.",
)
async def update_pedido(
    pedido_id: str,
    pedido_data: PedidoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoResponse:
    """Actualiza un pedido existente."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.update_pedido(pedido_id, pedido_data)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PedidoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{pedido_id}/estado",
    response_model=PedidoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar estado de un pedido",
    description="Actualiza el estado de un pedido existente.",
)
async def update_pedido_estado(
    pedido_id: str,
    nuevo_estado: EstadoPedido,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoResponse:
    """Actualiza el estado de un pedido existente."""
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.update_estado(pedido_id, nuevo_estado)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un pedido",
    description="Elimina un pedido existente del sistema.",
)
async def delete_pedido(
    pedido_id: str, session: AsyncSession = Depends(get_database_session)
) -> None:
    """Elimina un pedido existente."""
    try:
        pedido_service = PedidoService(session)
        await pedido_service.delete_pedido(pedido_id)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )

