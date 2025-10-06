"""
Alergeno repository for MySQL restaurant_dp2 schema.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.orm import selectinload

from src.models.menu.alergeno_model import AlergenoModel


class AlergenoMySQLRepository:
    """Alergeno repository for existing MySQL schema."""

    async def create_alergeno(
        self,
        db: AsyncSession,
        nombre: str,
        descripcion: Optional[str] = None,
        icono: Optional[str] = None,
        nivel_riesgo: str = 'medio',
        activo: bool = True,
        orden: int = 0
    ) -> AlergenoModel:
        """
        Create a new alergeno.

        Args:
            db: Database session
            nombre: Allergen name
            descripcion: Allergen description (optional)
            icono: Icon name or emoji (optional)
            nivel_riesgo: Risk level (bajo, medio, alto, critico)
            activo: Active status
            orden: Display order

        Returns:
            Created alergeno
        """
        stmt = insert(AlergenoModel).values(
            nombre=nombre,
            descripcion=descripcion,
            icono=icono,
            nivel_riesgo=nivel_riesgo,
            activo=activo,
            orden=orden
        )
        result = await db.execute(stmt)
        await db.commit()

        # Get the created record
        alergeno_id = result.inserted_primary_key[0]
        return await self.get_by_id(db, alergeno_id)

    async def get_by_id(self, db: AsyncSession, alergeno_id: int) -> Optional[AlergenoModel]:
        """
        Get alergeno by ID.

        Args:
            db: Database session
            alergeno_id: Alergeno ID

        Returns:
            Alergeno or None
        """
        stmt = select(AlergenoModel).where(AlergenoModel.id_alergeno == alergeno_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, db: AsyncSession, nombre: str) -> Optional[AlergenoModel]:
        """
        Get alergeno by name.

        Args:
            db: Database session
            nombre: Allergen name

        Returns:
            Alergeno or None
        """
        stmt = select(AlergenoModel).where(AlergenoModel.nombre == nombre)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo_only: bool = False,
        order_by_orden: bool = True
    ) -> List[AlergenoModel]:
        """
        Get all alergenos with pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records
            activo_only: Filter only active allergens
            order_by_orden: Order by 'orden' field

        Returns:
            List of alergenos
        """
        stmt = select(AlergenoModel)

        if activo_only:
            stmt = stmt.where(AlergenoModel.activo == True)

        if order_by_orden:
            stmt = stmt.order_by(AlergenoModel.orden, AlergenoModel.nombre)
        else:
            stmt = stmt.order_by(AlergenoModel.id_alergeno)

        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_nivel_riesgo(
        self,
        db: AsyncSession,
        nivel_riesgo: str,
        activo_only: bool = True
    ) -> List[AlergenoModel]:
        """
        Get alergenos by risk level.

        Args:
            db: Database session
            nivel_riesgo: Risk level (bajo, medio, alto, critico)
            activo_only: Filter only active allergens

        Returns:
            List of alergenos
        """
        stmt = select(AlergenoModel).where(AlergenoModel.nivel_riesgo == nivel_riesgo)

        if activo_only:
            stmt = stmt.where(AlergenoModel.activo == True)

        stmt = stmt.order_by(AlergenoModel.orden, AlergenoModel.nombre)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_alergeno(
        self,
        db: AsyncSession,
        alergeno_id: int,
        **kwargs
    ) -> Optional[AlergenoModel]:
        """
        Update alergeno.

        Args:
            db: Database session
            alergeno_id: Alergeno ID
            **kwargs: Fields to update

        Returns:
            Updated alergeno or None
        """
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(db, alergeno_id)

        stmt = (
            update(AlergenoModel)
            .where(AlergenoModel.id_alergeno == alergeno_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()

        return await self.get_by_id(db, alergeno_id)

    async def delete_alergeno(self, db: AsyncSession, alergeno_id: int) -> bool:
        """
        Delete alergeno.

        Args:
            db: Database session
            alergeno_id: Alergeno ID

        Returns:
            True if deleted, False if not found
        """
        stmt = delete(AlergenoModel).where(AlergenoModel.id_alergeno == alergeno_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def deactivate_alergeno(self, db: AsyncSession, alergeno_id: int) -> Optional[AlergenoModel]:
        """
        Deactivate alergeno (soft delete).

        Args:
            db: Database session
            alergeno_id: Alergeno ID

        Returns:
            Updated alergeno or None
        """
        return await self.update_alergeno(db, alergeno_id, activo=False)

    async def exists_nombre(self, db: AsyncSession, nombre: str, exclude_id: int = None) -> bool:
        """
        Check if allergen name exists.

        Args:
            db: Database session
            nombre: Allergen name to check
            exclude_id: Alergeno ID to exclude from check

        Returns:
            True if name exists, False otherwise
        """
        stmt = select(AlergenoModel.id_alergeno).where(AlergenoModel.nombre == nombre)

        if exclude_id:
            stmt = stmt.where(AlergenoModel.id_alergeno != exclude_id)

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_alergenos(self, db: AsyncSession, activo_only: bool = False) -> int:
        """
        Count alergenos.

        Args:
            db: Database session
            activo_only: Count only active allergens

        Returns:
            Number of alergenos
        """
        stmt = select(func.count(AlergenoModel.id_alergeno))

        if activo_only:
            stmt = stmt.where(AlergenoModel.activo == True)

        result = await db.execute(stmt)
        return result.scalar()

    async def update_orden(self, db: AsyncSession, alergeno_id: int, nuevo_orden: int) -> Optional[AlergenoModel]:
        """
        Update display order of alergeno.

        Args:
            db: Database session
            alergeno_id: Alergeno ID
            nuevo_orden: New order value

        Returns:
            Updated alergeno or None
        """
        return await self.update_alergeno(db, alergeno_id, orden=nuevo_orden)