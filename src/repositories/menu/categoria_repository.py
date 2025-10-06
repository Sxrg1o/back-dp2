"""
Category repository for menu category operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.models.menu.categoria_model import CategoriaModel
from src.repositories.base_repository import BaseRepository


class CategoriaRepository(BaseRepository[CategoriaModel]):
    """Category repository with specific category operations."""

    def __init__(self):
        super().__init__(CategoriaModel)

    async def get_active_categories(self, db: AsyncSession) -> List[CategoriaModel]:
        """
        Get all active categories ordered by display order.

        Args:
            db: Database session

        Returns:
            List of active categories
        """
        result = await db.execute(
            select(self.model)
            .where(self.model.activo == True)
            .order_by(self.model.orden, self.model.nombre)
        )
        return result.scalars().all()

    async def get_categories_with_products(self, db: AsyncSession) -> List[CategoriaModel]:
        """
        Get categories with their products loaded.

        Args:
            db: Database session

        Returns:
            List of categories with products
        """
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.productos))
            .where(self.model.activo == True)
            .order_by(self.model.orden, self.model.nombre)
        )
        return result.scalars().all()

    async def update_display_order(
        self,
        db: AsyncSession,
        category_id: int,
        new_order: int
    ) -> Optional[CategoriaModel]:
        """
        Update category display order.

        Args:
            db: Database session
            category_id: Category ID
            new_order: New display order

        Returns:
            Updated category or None
        """
        return await self.update(db, category_id, orden=new_order)