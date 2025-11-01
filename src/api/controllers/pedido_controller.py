"""
Endpoints para gestión de pedidos.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.pedidos.pedido_service import PedidoService
from src.api.schemas.pedido_schema import (
    PedidoCreate,
    PedidoResponse,
    PedidoUpdate,
    PedidoList,
    PedidoEstadoUpdate,
    PedidoCompletoCreate,
    PedidoCompletoResponse,
)
from src.business_logic.exceptions.pedido_exceptions import (
    PedidoValidationError,
    PedidoNotFoundError,
    PedidoConflictError,
    PedidoStateTransitionError,
)
from src.core.enums.pedido_enums import EstadoPedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo pedido",
    description="Crea un nuevo pedido en el sistema. El numero_pedido se genera automáticamente.",
)
async def create_pedido(
    pedido_data: PedidoCreate, session: AsyncSession = Depends(get_database_session)
) -> PedidoResponse:
    """
    Crea un nuevo pedido en el sistema.

    Args:
        pedido_data: Datos del pedido a crear.
        session: Sesión de base de datos.

    Returns:
        El pedido creado con todos sus datos.

    Raises:
        HTTPException:
            - 400: Si los datos son inválidos.
            - 409: Si hay un conflicto (e.g., numero_pedido duplicado).
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.create_pedido(pedido_data)
    except PedidoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PedidoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.post(
    "/completo",
    response_model=PedidoCompletoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un pedido completo con items",
    description="Crea un pedido completo con todos sus items en una sola transacción. "
    "El numero_pedido se genera automáticamente y los totales se calculan según los items.",
)
async def create_pedido_completo(
    pedido_data: PedidoCompletoCreate,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoCompletoResponse:
    """
    Crea un pedido completo con sus items en una sola transacción.

    Este endpoint permite al frontend enviar un pedido completo con todos sus items
    y crear todo de forma atómica. Si algún item falla, se deshace toda la operación.

    Args:
        pedido_data: Datos del pedido completo con su lista de items.
        session: Sesión de base de datos.

    Returns:
        El pedido creado con todos sus items y sus datos.

    Raises:
        HTTPException:
            - 400: Si los datos son inválidos, la mesa no existe, o algún producto
                   no existe o no está disponible.
            - 409: Si hay un conflicto de integridad.
            - 500: Si ocurre un error interno del servidor.

    Example:
        ```json
        {
            "id_mesa": "01J123456789ABCDEFGHIJKLMN",
            "items": [
                {
                    "id_producto": "01J234567890ABCDEFGHIJKLMN",
                    "cantidad": 2,
                    "precio_unitario": 25.50,
                    "precio_opciones": 3.00,
                    "notas_personalizacion": "Sin cebolla"
                }
            ],
            "notas_cliente": "Mesa para evento",
            "notas_cocina": "Urgente"
        }
        ```
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.create_pedido_completo(pedido_data)
    except PedidoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
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
    """
    Obtiene un pedido específico por su ID.

    Args:
        pedido_id: ID del pedido a buscar (ULID).
        session: Sesión de base de datos.

    Returns:
        El pedido encontrado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el pedido.
            - 500: Si ocurre un error interno del servidor.
    """
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
    "/numero/{numero_pedido}",
    response_model=PedidoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un pedido por número",
    description="Obtiene los detalles de un pedido específico por su número único.",
)
async def get_pedido_by_numero(
    numero_pedido: str, session: AsyncSession = Depends(get_database_session)
) -> PedidoResponse:
    """
    Obtiene un pedido específico por su número único.

    Args:
        numero_pedido: Número único del pedido a buscar.
        session: Sesión de base de datos.

    Returns:
        El pedido encontrado con todos sus datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el pedido.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.get_pedido_by_numero(numero_pedido)
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
    description="Obtiene una lista paginada de pedidos con filtros opcionales.",
)
async def list_pedidos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(
        100, gt=0, le=500, description="Número máximo de registros a retornar"
    ),
    estado: Optional[EstadoPedido] = Query(
        None, description="Filtrar por estado del pedido"
    ),
    id_mesa: Optional[str] = Query(None, description="Filtrar por ID de mesa"),
    session: AsyncSession = Depends(get_database_session),
) -> PedidoList:
    """
    Obtiene una lista paginada de pedidos.

    Args:
        skip: Número de registros a omitir (offset), por defecto 0.
        limit: Número máximo de registros a retornar, por defecto 100.
        estado: Filtrar por estado del pedido (opcional).
        id_mesa: Filtrar por ID de mesa (opcional).
        session: Sesión de base de datos.

    Returns:
        Lista paginada de pedidos y el número total de registros.

    Raises:
        HTTPException:
            - 400: Si los parámetros de paginación son inválidos.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.get_pedidos(skip, limit, estado, id_mesa)
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
    """
    Actualiza un pedido existente.

    Args:
        pedido_id: ID del pedido a actualizar (ULID).
        pedido_data: Datos del pedido a actualizar.
        session: Sesión de base de datos.

    Returns:
        El pedido actualizado con todos sus datos.

    Raises:
        HTTPException:
            - 400: Si los datos son inválidos.
            - 404: Si no se encuentra el pedido.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.update_pedido(pedido_id, pedido_data)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PedidoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar estado de un pedido",
    description="Cambia el estado de un pedido y actualiza el timestamp correspondiente.",
)
async def cambiar_estado_pedido(
    pedido_id: str,
    estado_data: PedidoEstadoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> PedidoResponse:
    """
    Cambia el estado de un pedido.

    Args:
        pedido_id: ID del pedido a actualizar (ULID).
        estado_data: Nuevo estado del pedido.
        session: Sesión de base de datos.

    Returns:
        El pedido actualizado con todos sus datos.

    Raises:
        HTTPException:
            - 400: Si la transición de estado no es válida.
            - 404: Si no se encuentra el pedido.
            - 500: Si ocurre un error interno del servidor.
    """
    try:
        pedido_service = PedidoService(session)
        return await pedido_service.cambiar_estado(pedido_id, estado_data)
    except PedidoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PedidoStateTransitionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
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
    """
    Elimina un pedido existente.

    Args:
        pedido_id: ID del pedido a eliminar (ULID).
        session: Sesión de base de datos.

    Raises:
        HTTPException:
            - 404: Si no se encuentra el pedido.
            - 500: Si ocurre un error interno del servidor.
    """
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
