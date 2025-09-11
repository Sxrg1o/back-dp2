"""SQLAlchemy adapter for ItemRepositoryPort."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from app.domain.entities.item import Item
from app.domain.repositories.item_repository import ItemRepositoryPort
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.models.item_model import ItemModel
from app.infrastructure.persistence.mappers.item_mapper import ItemMapper
from app.infrastructure.persistence.repositories.base_repository import BaseSQLAlchemyRepository


class SqlAlchemyItemRepository(BaseSQLAlchemyRepository[Item, ItemModel], ItemRepositoryPort):
    """SQLAlchemy adapter for Item repository operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize SQLAlchemy Item repository.
        
        Args:
            session: SQLAlchemy async session
        """
        super().__init__(session, ItemModel, ItemMapper())
    
    async def get_by_id(self, item_id: UUID) -> Optional[Item]:
        """Get item by ID."""
        model = await self._get_by_id(item_id)
        return self.mapper.to_entity(model) if model else None
    
    async def get_available_items(self) -> List[Item]:
        """Get all available items."""
        stmt = select(ItemModel).where(
            and_(
                ItemModel.activo == True,
                ItemModel.stock_actual > 0,
                ItemModel.stock_actual > ItemModel.stock_minimo
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_category(self, etiqueta: EtiquetaItem) -> List[Item]:
        """Get items by category/label."""
        stmt = select(ItemModel).where(
            ItemModel.etiquetas.contains([etiqueta.value])
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_all(self) -> List[Item]:
        """Get all items regardless of availability."""
        models = await self._get_all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_name(self, name: str) -> Optional[Item]:
        """Get item by name."""
        stmt = select(ItemModel).where(ItemModel.nombre == name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None
    
    async def get_low_stock_items(self) -> List[Item]:
        """Get items with low stock (at or below minimum)."""
        stmt = select(ItemModel).where(
            ItemModel.stock_actual <= ItemModel.stock_minimo
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_price_range(self, min_price: float, max_price: float) -> List[Item]:
        """Get items within price range."""
        stmt = select(ItemModel).where(
            and_(
                ItemModel.precio >= min_price,
                ItemModel.precio <= max_price
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def save(self, item: Item) -> Item:
        """Save item (create or update)."""
        model = self.mapper.to_model(item)
        saved_model = await self._save(model)
        return self.mapper.to_entity(saved_model)
    
    async def delete(self, item_id: UUID) -> bool:
        """Delete item by ID."""
        return await self._delete_by_id(item_id)
    
    async def exists_by_id(self, item_id: UUID) -> bool:
        """Check if item exists by ID."""
        return await self._exists_by_id(item_id)
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if item exists by name."""
        stmt = select(ItemModel.id).where(ItemModel.nombre == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def count_total(self) -> int:
        """Count total number of items."""
        return await self._count_all()
    
    async def count_available(self) -> int:
        """Count available items."""
        stmt = select(ItemModel.id).where(
            and_(
                ItemModel.activo == True,
                ItemModel.stock_actual > 0,
                ItemModel.stock_actual > ItemModel.stock_minimo
            )
        )
        result = await self.session.execute(stmt)
        return len(result.scalars().all())