"""
Repositorio para la gestión de pedidos en el sistema.
"""

from typing import Optional, List, Tuple
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel


class PedidoRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de pedidos.

    Proporciona acceso a la capa de persistencia para las operaciones
    relacionadas con los pedidos en el sistema, siguiendo el patrón Repository.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa el repositorio con una sesión de base de datos."""
        self.session = session

    async def create(self, pedido: PedidoModel) -> PedidoModel:
        """Crea un nuevo pedido en la base de datos."""
        try:
            self.session.add(pedido)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(pedido)
            return pedido
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, pedido_id: str) -> Optional[PedidoModel]:
        """Obtiene un pedido por su identificador único."""
        query = select(PedidoModel).where(PedidoModel.id == pedido_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id_with_productos(self, pedido_id: str) -> Optional[PedidoModel]:
        """Obtiene un pedido por su ID con todos sus productos cargados."""
        query = (
            select(PedidoModel)
            .where(PedidoModel.id == pedido_id)
            .options(
                selectinload(PedidoModel.pedido_productos)
                .selectinload(PedidoProductoModel.producto)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_mesa(self, mesa_id: str) -> List[PedidoModel]:
        """Obtiene todos los pedidos de una mesa específica."""
        query = select(PedidoModel).where(PedidoModel.id_mesa == mesa_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_numero_pedido(self, numero_pedido: str) -> Optional[PedidoModel]:
        """Obtiene un pedido por su número de pedido."""
        query = select(PedidoModel).where(PedidoModel.numero_pedido == numero_pedido)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, pedido_id: str) -> bool:
        """Elimina un pedido de la base de datos por su ID."""
        try:
            stmt = delete(PedidoModel).where(PedidoModel.id == pedido_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update(self, pedido_id: str, **kwargs) -> Optional[PedidoModel]:
        """Actualiza un pedido existente con los valores proporcionados."""
        try:
            valid_fields = {
                k: v for k, v in kwargs.items() if hasattr(PedidoModel, k) and k != "id"
            }

            if not valid_fields:
                return await self.get_by_id(pedido_id)

            stmt = (
                update(PedidoModel)
                .where(PedidoModel.id == pedido_id)
                .values(**valid_fields)
                .returning(PedidoModel)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()

            updated_pedido = result.scalars().first()
            if not updated_pedido:
                return None

            await self.session.refresh(updated_pedido)
            return updated_pedido
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(
        self, skip: int = 0, limit: int = 100, id_mesa: Optional[str] = None, estado: Optional[str] = None
    ) -> Tuple[List[PedidoModel], int]:
        """Obtiene todos los pedidos con paginación y filtros opcionales."""
        try:
            query = select(PedidoModel)

            if id_mesa is not None:
                query = query.where(PedidoModel.id_mesa == id_mesa)

            if estado is not None:
                query = query.where(PedidoModel.estado == estado)

            count_query = select(func.count()).select_from(query.subquery())
            total_result = await self.session.execute(count_query)
            total = total_result.scalar() or 0

            query = query.order_by(PedidoModel.fecha_creacion.desc()).offset(skip).limit(limit)

            result = await self.session.execute(query)
            pedidos = result.scalars().all()

            return list(pedidos), total
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

