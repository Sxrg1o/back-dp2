"""
Servicio para la gestión de pedido_producto en el sistema.
"""

from typing import List
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.pedidos.pedido_producto_repository import PedidoProductoRepository
from src.repositories.menu.producto_repository import ProductoRepository
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.api.schemas.pedido_producto_schema import (
    PedidoProductoCreate,
    PedidoProductoUpdate,
    PedidoProductoResponse,
)
from src.business_logic.exceptions.pedido_producto_exceptions import (
    PedidoProductoValidationError,
    PedidoProductoNotFoundError,
    PedidoProductoConflictError,
)


class PedidoProductoService:
    """Servicio para la gestión de items de pedido en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con items de productos en pedidos, incluyendo validaciones y cálculos de precios.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa el servicio con una sesión de base de datos."""
        self.repository = PedidoProductoRepository(session)
        self.producto_repository = ProductoRepository(session)
        self.session = session

    async def create_pedido_producto(
        self, pedido_producto_data: PedidoProductoCreate
    ) -> PedidoProductoResponse:
        """Crea un nuevo item de pedido."""
        try:
            # Obtener precio del producto
            producto = await self.producto_repository.get_by_id(
                pedido_producto_data.id_producto
            )
            if not producto:
                raise PedidoProductoValidationError(
                    f"No se encontró el producto con ID {pedido_producto_data.id_producto}"
                )

            precio_unitario = pedido_producto_data.precio_unitario or producto.precio_base
            precio_opciones = pedido_producto_data.precio_opciones or Decimal("0.00")
            cantidad = pedido_producto_data.cantidad

            # Calcular subtotal
            subtotal = (precio_unitario * cantidad) + (precio_opciones * cantidad)

            # Crear modelo de pedido_producto
            pedido_producto = PedidoProductoModel(
                id_pedido=pedido_producto_data.id_pedido,
                id_producto=pedido_producto_data.id_producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_opciones=precio_opciones,
                subtotal=subtotal,
                notas_personalizacion=pedido_producto_data.notas_personalizacion,
            )

            # Persistir en la base de datos
            created_pedido_producto = await self.repository.create(pedido_producto)

            # Actualizar total del pedido
            await self._update_pedido_total(pedido_producto_data.id_pedido)

            return PedidoProductoResponse.model_validate(created_pedido_producto)
        except IntegrityError as e:
            raise PedidoProductoConflictError(f"Error al crear el item de pedido: {str(e)}")

    async def get_pedido_producto_by_id(self, pedido_producto_id: str) -> PedidoProductoResponse:
        """Obtiene un item de pedido por su ID."""
        pedido_producto = await self.repository.get_by_id(pedido_producto_id)

        if not pedido_producto:
            raise PedidoProductoNotFoundError(
                f"No se encontró el item de pedido con ID {pedido_producto_id}"
            )

        return PedidoProductoResponse.model_validate(pedido_producto)

    async def update_pedido_producto(
        self, pedido_producto_id: str, pedido_producto_data: PedidoProductoUpdate
    ) -> PedidoProductoResponse:
        """Actualiza un item de pedido."""
        existing_pedido_producto = await self.repository.get_by_id(pedido_producto_id)

        if not existing_pedido_producto:
            raise PedidoProductoNotFoundError(
                f"No se encontró el item de pedido con ID {pedido_producto_id}"
            )

        # Convertir a dict y filtrar valores None
        update_dict = {
            k: v for k, v in pedido_producto_data.model_dump().items() if v is not None
        }

        # Si se actualiza cantidad o precios, recalcular subtotal
        if "cantidad" in update_dict or "precio_unitario" in update_dict or "precio_opciones" in update_dict:
            cantidad = update_dict.get("cantidad", existing_pedido_producto.cantidad)
            precio_unitario = update_dict.get(
                "precio_unitario", existing_pedido_producto.precio_unitario
            )
            precio_opciones = update_dict.get(
                "precio_opciones", existing_pedido_producto.precio_opciones
            )
            update_dict["subtotal"] = (precio_unitario * cantidad) + (precio_opciones * cantidad)

        if not update_dict:
            return PedidoProductoResponse.model_validate(existing_pedido_producto)

        updated_pedido_producto = await self.repository.update(pedido_producto_id, **update_dict)

        # Actualizar total del pedido
        await self._update_pedido_total(existing_pedido_producto.id_pedido)

        if not updated_pedido_producto:
            raise PedidoProductoNotFoundError(
                f"No se encontró el item de pedido con ID {pedido_producto_id}"
            )

        return PedidoProductoResponse.model_validate(updated_pedido_producto)

    async def delete_pedido_producto(self, pedido_producto_id: str) -> bool:
        """Elimina un item de pedido."""
        existing_pedido_producto = await self.repository.get_by_id(pedido_producto_id)

        if not existing_pedido_producto:
            raise PedidoProductoNotFoundError(
                f"No se encontró el item de pedido con ID {pedido_producto_id}"
            )

        pedido_id = existing_pedido_producto.id_pedido
        result = await self.repository.delete(pedido_producto_id)

        # Actualizar total del pedido
        await self._update_pedido_total(pedido_id)

        return result

    async def get_pedido_productos_by_pedido(
        self, pedido_id: str
    ) -> List[PedidoProductoResponse]:
        """Obtiene todos los items de un pedido específico."""
        pedido_productos = await self.repository.get_by_pedido_with_productos(pedido_id)

        return [PedidoProductoResponse.model_validate(p) for p in pedido_productos]

    async def _update_pedido_total(self, pedido_id: str):
        """Actualiza el total de un pedido basado en sus items."""
        from src.repositories.pedidos.pedido_repository import PedidoRepository

        pedido_repo = PedidoRepository(self.session)
        pedido_productos = await self.repository.get_by_pedido(pedido_id)

        subtotal = sum(item.subtotal for item in pedido_productos)
        impuestos = pedido_productos[0].pedido.impuestos if pedido_productos else 0
        descuentos = pedido_productos[0].pedido.descuentos if pedido_productos else 0
        total = subtotal + impuestos - descuentos

        await pedido_repo.update(pedido_id, subtotal=subtotal, total=total)

