"""
Servicio para la gestión de pedidos en el sistema.
"""

from typing import List, Tuple
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.pedidos.pedido_repository import PedidoRepository
from src.models.pedidos.pedido_model import PedidoModel
from src.api.schemas.pedido_schema import (
    PedidoCreate,
    PedidoUpdate,
    PedidoResponse,
    PedidoSummary,
    PedidoList,
)
from src.business_logic.exceptions.pedido_exceptions import (
    PedidoValidationError,
    PedidoNotFoundError,
    PedidoConflictError,
)
from src.core.enums.pedido_enums import EstadoPedido


class PedidoService:
    """Servicio para la gestión de pedidos en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con pedidos, incluyendo validaciones, transformaciones y manejo de excepciones.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa el servicio con una sesión de base de datos."""
        self.repository = PedidoRepository(session)
        self.session = session

    async def create_pedido(self, pedido_data: PedidoCreate) -> PedidoResponse:
        """Crea un nuevo pedido en el sistema."""
        try:
            # Validar que el subtotal no sea negativo
            if pedido_data.subtotal < 0:
                raise PedidoValidationError("El subtotal no puede ser negativo")

            # Crear modelo de pedido desde los datos
            pedido = PedidoModel(
                id_mesa=pedido_data.id_mesa,
                numero_pedido=pedido_data.numero_pedido,
                estado=pedido_data.estado or EstadoPedido.PENDIENTE,
                subtotal=pedido_data.subtotal or Decimal("0.00"),
                impuestos=pedido_data.impuestos or Decimal("0.00"),
                descuentos=pedido_data.descuentos or Decimal("0.00"),
                total=pedido_data.total or Decimal("0.00"),
                notas_cliente=pedido_data.notas_cliente,
                notas_cocina=pedido_data.notas_cocina,
            )

            # Persistir en la base de datos
            created_pedido = await self.repository.create(pedido)

            # Convertir y retornar como esquema de respuesta
            return PedidoResponse.model_validate(created_pedido)
        except IntegrityError:
            raise PedidoConflictError(
                f"Error al crear el pedido: posible conflicto con número de pedido"
            )

    async def get_pedido_by_id(self, pedido_id: str) -> PedidoResponse:
        """Obtiene un pedido por su ID."""
        pedido = await self.repository.get_by_id(pedido_id)

        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        return PedidoResponse.model_validate(pedido)

    async def get_pedido_by_id_with_productos(self, pedido_id: str) -> "PedidoConProductosResponse":
        """Obtiene un pedido por su ID con todos sus productos."""
        from src.api.schemas.pedido_schema import PedidoConProductosResponse
        from src.api.schemas.pedido_producto_schema import PedidoProductoResponse

        pedido = await self.repository.get_by_id_with_productos(pedido_id)

        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Convertir pedido_productos a schemas de respuesta
        pedido_productos = [
            PedidoProductoResponse.model_validate(p) for p in pedido.pedido_productos
        ]

        response = PedidoResponse.model_validate(pedido)
        return PedidoConProductosResponse(
            **response.model_dump(),
            pedido_productos=pedido_productos
        )

    async def update_pedido(
        self, pedido_id: str, pedido_data: PedidoUpdate
    ) -> PedidoResponse:
        """Actualiza un pedido existente."""
        # Verificar que existe
        existing_pedido = await self.repository.get_by_id(pedido_id)
        if not existing_pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Convertir a dict y filtrar valores None
        update_dict = {k: v for k, v in pedido_data.model_dump().items() if v is not None}

        if not update_dict:
            return PedidoResponse.model_validate(existing_pedido)

        # Actualizar en la base de datos
        updated_pedido = await self.repository.update(pedido_id, **update_dict)

        if not updated_pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        return PedidoResponse.model_validate(updated_pedido)

    async def delete_pedido(self, pedido_id: str) -> bool:
        """Elimina un pedido."""
        existing_pedido = await self.repository.get_by_id(pedido_id)
        if not existing_pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        return await self.repository.delete(pedido_id)

    async def get_pedidos(
        self, skip: int = 0, limit: int = 100, id_mesa: str = None, estado: str = None
    ) -> PedidoList:
        """Obtiene una lista paginada de pedidos."""
        # Validar parámetros de paginación
        if skip < 0:
            raise PedidoValidationError("El parámetro 'skip' debe ser mayor o igual a 0")
        if limit <= 0 or limit > 500:
            raise PedidoValidationError(
                "El parámetro 'limit' debe estar entre 1 y 500"
            )

        pedidos, total = await self.repository.get_all(skip, limit, id_mesa, estado)

        # Convertir a resúmenes
        summaries = [PedidoSummary.model_validate(pedido) for pedido in pedidos]

        return PedidoList(items=summaries, total=total)

    async def update_estado(
        self, pedido_id: str, nuevo_estado: EstadoPedido
    ) -> PedidoResponse:
        """Actualiza el estado de un pedido."""
        pedido = await self.repository.get_by_id(pedido_id)

        if not pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        # Actualizar timestamp según el estado
        now = datetime.now()
        update_data = {"estado": nuevo_estado}

        if nuevo_estado == EstadoPedido.CONFIRMADO:
            update_data["fecha_confirmado"] = now
        elif nuevo_estado == EstadoPedido.EN_PREPARACION:
            update_data["fecha_en_preparacion"] = now
        elif nuevo_estado == EstadoPedido.LISTO:
            update_data["fecha_listo"] = now
        elif nuevo_estado == EstadoPedido.ENTREGADO:
            update_data["fecha_entregado"] = now
        elif nuevo_estado == EstadoPedido.CANCELADO:
            update_data["fecha_cancelado"] = now

        updated_pedido = await self.repository.update(pedido_id, **update_data)

        if not updated_pedido:
            raise PedidoNotFoundError(f"No se encontró el pedido con ID {pedido_id}")

        return PedidoResponse.model_validate(updated_pedido)

