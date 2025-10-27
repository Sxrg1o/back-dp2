"""
Repositorio para la gestión de pedido_producto en el sistema.
"""

from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.menu.producto_model import ProductoModel


class PedidoProductoRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de pedido_producto.

    Proporciona acceso a la capa de persistencia para las operaciones
    relacionadas con los items de productos en pedidos.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio con una sesión de base de datos."""
        self.session = session

    async def create(self, pedido_producto: PedidoProductoModel) -> PedidoProductoModel:
        """Crea un nuevo pedido_producto en la base de datos."""
        try:
            self.session.add(pedido_producto)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(pedido_producto)
            return pedido_producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, pedido_producto_id: str) -> Optional[PedidoProductoModel]:
        """Obtiene un pedido_producto por su identificador único."""
        query = select(PedidoProductoModel).where(PedidoProductoModel.id == pedido_producto_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_with_producto(self, pedido_producto_id: str) -> Optional[PedidoProductoModel]:
        """Obtiene un pedido_producto por su ID con información del producto."""
        query = (
            select(PedidoProductoModel)
            .where(PedidoProductoModel.id == pedido_producto_id)
            .options(selectinload(PedidoProductoModel.producto))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_pedido(self, pedido_id: str) -> List[PedidoProductoModel]:
        """Obtiene todos los items de un pedido específico."""
        query = select(PedidoProductoModel).where(PedidoProductoModel.id_pedido == pedido_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_pedido_with_productos(self, pedido_id: str) -> List[PedidoProductoModel]:
        """Obtiene todos los items de un pedido con información de productos."""
        query = (
            select(PedidoProductoModel)
            .where(PedidoProductoModel.id_pedido == pedido_id)
            .options(selectinload(PedidoProductoModel.producto))
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete(self, pedido_producto_id: str) -> bool:
        """Elimina un pedido_producto de la base de datos por su ID."""
        try:
            stmt = delete(PedidoProductoModel).where(PedidoProductoModel.id == pedido_producto_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def delete_by_pedido(self, pedido_id: str) -> int:
        """Elimina todos los items de un pedido específico."""
        try:
            stmt = delete(PedidoProductoModel).where(PedidoProductoModel.id_pedido == pedido_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(self, pedido_producto_id: str, **kwargs) -> Optional[PedidoProductoModel]:
        """Actualiza un pedido_producto existente con los valores proporcionados."""
        try:
            valid_fields = {
                k: v for k, v in kwargs.items() if hasattr(PedidoProductoModel, k) and k != "id"
            }

            if not valid_fields:
                return await self.get_by_id(pedido_producto_id)

            stmt = (
                update(PedidoProductoModel)
                .where(PedidoProductoModel.id == pedido_producto_id)
                .values(**valid_fields)
                .returning(PedidoProductoModel)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_pedido_producto = result.scalars().first()
            if not updated_pedido_producto:
                return None

            await self.session.refresh(updated_pedido_producto)
            return updated_pedido_producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[PedidoProductoModel], int]:
        """Obtiene todos los pedido_producto con paginación."""
        try:
            query = select(PedidoProductoModel)

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.session.execute(count_query)
            total = total_result.scalar() or 0

            query = query.offset(skip).limit(limit)

            result = await self.session.execute(query)
            pedido_productos = result.scalars().all()

            return list(pedido_productos), total
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def batch_insert(self, pedido_productos: List[PedidoProductoModel]) -> List[PedidoProductoModel]:
        """Crea múltiples pedido_producto en una sola operación."""
        if not pedido_productos:
            return []

        try:
            self.session.add_all(pedido_productos)
            await self.session.flush()
            await self.session.commit()

            for pedido_producto in pedido_productos:
                await self.session.refresh(pedido_producto)

            return pedido_productos
        except SQLAlchemyError:
            await self.session.rollback()
            raise

