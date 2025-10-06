"""
Product repository for menu product operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from src.models.menu.producto_model import ProductoModel
from src.repositories.base_repository import BaseRepository


class ProductoRepository(BaseRepository[ProductoModel]):
    """Product repository with specific product operations."""

    def __init__(self):
        super().__init__(ProductoModel)

    async def get_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        available_only: bool = True
    ) -> List[ProductoModel]:
        """
        Get products by category.

        Args:
            db: Database session
            category_id: Category ID
            available_only: Filter only available products

        Returns:
            List of products
        """
        query = (
            select(self.model)
            .options(
                selectinload(self.model.categoria),
                selectinload(self.model.alergenos),
                selectinload(self.model.opciones)
            )
            .where(self.model.id_categoria == category_id)
        )

        if available_only:
            query = query.where(self.model.disponible == True)

        result = await db.execute(query.order_by(self.model.nombre))
        return result.scalars().all()

    async def search_products(
        self,
        db: AsyncSession,
        search_term: str,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        available_only: bool = True
    ) -> List[ProductoModel]:
        """
        Search products with various filters.

        Args:
            db: Database session
            search_term: Search term for name and description
            category_id: Optional category filter
            min_price: Minimum price filter
            max_price: Maximum price filter
            available_only: Filter only available products

        Returns:
            List of matching products
        """
        query = (
            select(self.model)
            .options(
                selectinload(self.model.categoria),
                selectinload(self.model.alergenos)
            )
        )

        # Text search
        if search_term:
            search_filter = or_(
                self.model.nombre.ilike(f"%{search_term}%"),
                self.model.descripcion.ilike(f"%{search_term}%")
            )
            query = query.where(search_filter)

        # Category filter
        if category_id:
            query = query.where(self.model.id_categoria == category_id)

        # Price filters
        if min_price is not None:
            query = query.where(self.model.precio_base >= min_price)
        if max_price is not None:
            query = query.where(self.model.precio_base <= max_price)

        # Availability filter
        if available_only:
            query = query.where(self.model.disponible == True)

        result = await db.execute(query.order_by(self.model.nombre))
        return result.scalars().all()

    async def get_featured_products(self, db: AsyncSession) -> List[ProductoModel]:
        """
        Get featured products.

        Args:
            db: Database session

        Returns:
            List of featured products
        """
        result = await db.execute(
            select(self.model)
            .options(
                selectinload(self.model.categoria),
                selectinload(self.model.alergenos)
            )
            .where(
                and_(
                    self.model.destacado == True,
                    self.model.disponible == True
                )
            )
            .order_by(self.model.nombre)
        )
        return result.scalars().all()

    async def get_products_with_allergen(
        self,
        db: AsyncSession,
        allergen_id: int
    ) -> List[ProductoModel]:
        """
        Get products containing a specific allergen.

        Args:
            db: Database session
            allergen_id: Allergen ID

        Returns:
            List of products with the allergen
        """
        result = await db.execute(
            select(self.model)
            .join(self.model.alergenos)
            .where(self.model.alergenos.any(id_alergeno=allergen_id))
            .options(
                selectinload(self.model.categoria),
                selectinload(self.model.alergenos)
            )
        )
        return result.scalars().all()

    async def update_availability(
        self,
        db: AsyncSession,
        product_id: int,
        available: bool
    ) -> Optional[ProductoModel]:
        """
        Update product availability.

        Args:
            db: Database session
            product_id: Product ID
            available: Availability status

        Returns:
            Updated product or None
        """
        return await self.update(db, product_id, disponible=available)

    async def get_products_by_price_range(
        self,
        db: AsyncSession,
        min_price: float,
        max_price: float
    ) -> List[ProductoModel]:
        """
        Get products within a price range.

        Args:
            db: Database session
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of products in price range
        """
        result = await db.execute(
            select(self.model)
            .where(
                and_(
                    self.model.precio_base >= min_price,
                    self.model.precio_base <= max_price,
                    self.model.disponible == True
                )
            )
            .options(selectinload(self.model.categoria))
            .order_by(self.model.precio_base)
        )
        return result.scalars().all()