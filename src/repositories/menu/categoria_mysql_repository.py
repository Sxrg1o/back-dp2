"""
Categoria repository for MySQL restaurant_dp2 schema.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import selectinload

from src.models.menu.categoria_model import CategoriaModel


class CategoriaMySQLRepository:
    """Categoria repository for existing MySQL schema."""

    async def create_categoria(
        self,
        db: AsyncSession,
        nombre: str,
        descripcion: Optional[str] = None,
        orden: int = 0,
        activo: bool = True,
        imagen_path: Optional[str] = None
    ) -> CategoriaModel:
        """
        Create a new categoria.

        Args:
            db: Database session
            nombre: Category name
            descripcion: Category description (optional)
            orden: Display order
            activo: Active status
            imagen_path: Image path (optional)

        Returns:
            Created categoria
        """
        stmt = insert(CategoriaModel).values(
            nombre=nombre,
            descripcion=descripcion,
            orden=orden,
            activo=activo,
            imagen_path=imagen_path
        )
        result = await db.execute(stmt)
        await db.commit()

        # Get the created record
        categoria_id = result.inserted_primary_key[0]
        return await self.get_by_id(db, categoria_id)

    async def get_by_id(self, db: AsyncSession, categoria_id: int) -> Optional[CategoriaModel]:
        """Get categoria by ID."""
        stmt = select(CategoriaModel).where(CategoriaModel.id_categoria == categoria_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, db: AsyncSession, nombre: str) -> Optional[CategoriaModel]:
        """Get categoria by name."""
        stmt = select(CategoriaModel).where(CategoriaModel.nombre == nombre)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo_only: bool = False,
        order_by_orden: bool = True
    ) -> List[CategoriaModel]:
        """Get all categorias with pagination."""
        stmt = select(CategoriaModel)

        if activo_only:
            stmt = stmt.where(CategoriaModel.activo == True)

        if order_by_orden:
            stmt = stmt.order_by(CategoriaModel.orden, CategoriaModel.nombre)
        else:
            stmt = stmt.order_by(CategoriaModel.id_categoria)

        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_categoria(
        self,
        db: AsyncSession,
        categoria_id: int,
        **kwargs
    ) -> Optional[CategoriaModel]:
        """Update categoria."""
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(db, categoria_id)

        stmt = (
            update(CategoriaModel)
            .where(CategoriaModel.id_categoria == categoria_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()

        return await self.get_by_id(db, categoria_id)

    async def delete_categoria(self, db: AsyncSession, categoria_id: int) -> bool:
        """Delete categoria."""
        stmt = delete(CategoriaModel).where(CategoriaModel.id_categoria == categoria_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def exists_nombre(self, db: AsyncSession, nombre: str, exclude_id: int = None) -> bool:
        """Check if category name exists."""
        stmt = select(CategoriaModel.id_categoria).where(CategoriaModel.nombre == nombre)

        if exclude_id:
            stmt = stmt.where(CategoriaModel.id_categoria != exclude_id)

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_categorias(self, db: AsyncSession, activo_only: bool = False) -> int:
        """Count categorias."""
        stmt = select(func.count(CategoriaModel.id_categoria))

        if activo_only:
            stmt = stmt.where(CategoriaModel.activo == True)

        result = await db.execute(stmt)
        return result.scalar()