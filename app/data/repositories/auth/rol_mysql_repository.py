"""
Rol repository for MySQL restaurant_dp2 schema.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload

from app.data.models.auth.rol_model import RolModel


class RolMySQLRepository:
    """Rol repository for existing MySQL schema."""

    async def create_rol(
        self,
        db: AsyncSession,
        nombre: str,
        descripcion: Optional[str] = None
    ) -> RolModel:
        """
        Create a new rol.

        Args:
            db: Database session
            nombre: Role name
            descripcion: Role description (optional)

        Returns:
            Created rol
        """
        stmt = insert(RolModel).values(
            nombre=nombre,
            descripcion=descripcion
        )
        result = await db.execute(stmt)
        await db.commit()

        # Get the created record
        rol_id = result.inserted_primary_key[0]
        return await self.get_by_id(db, rol_id)

    async def get_by_id(self, db: AsyncSession, rol_id: int) -> Optional[RolModel]:
        """
        Get rol by ID.

        Args:
            db: Database session
            rol_id: Rol ID

        Returns:
            Rol or None
        """
        stmt = select(RolModel).where(RolModel.id_rol == rol_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nombre(self, db: AsyncSession, nombre: str) -> Optional[RolModel]:
        """
        Get rol by name.

        Args:
            db: Database session
            nombre: Role name

        Returns:
            Rol or None
        """
        stmt = select(RolModel).where(RolModel.nombre == nombre)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[RolModel]:
        """
        Get all roles with pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of roles
        """
        stmt = select(RolModel).offset(skip).limit(limit).order_by(RolModel.id_rol)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_rol(
        self,
        db: AsyncSession,
        rol_id: int,
        **kwargs
    ) -> Optional[RolModel]:
        """
        Update rol.

        Args:
            db: Database session
            rol_id: Rol ID
            **kwargs: Fields to update

        Returns:
            Updated rol or None
        """
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(db, rol_id)

        stmt = (
            update(RolModel)
            .where(RolModel.id_rol == rol_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()

        return await self.get_by_id(db, rol_id)

    async def delete_rol(self, db: AsyncSession, rol_id: int) -> bool:
        """
        Delete rol.

        Args:
            db: Database session
            rol_id: Rol ID

        Returns:
            True if deleted, False if not found
        """
        stmt = delete(RolModel).where(RolModel.id_rol == rol_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def exists_nombre(self, db: AsyncSession, nombre: str, exclude_id: int = None) -> bool:
        """
        Check if role name exists.

        Args:
            db: Database session
            nombre: Role name to check
            exclude_id: Rol ID to exclude from check

        Returns:
            True if name exists, False otherwise
        """
        stmt = select(RolModel.id_rol).where(RolModel.nombre == nombre)

        if exclude_id:
            stmt = stmt.where(RolModel.id_rol != exclude_id)

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_roles(self, db: AsyncSession) -> int:
        """
        Count total roles.

        Args:
            db: Database session

        Returns:
            Number of roles
        """
        from sqlalchemy import func

        stmt = select(func.count(RolModel.id_rol))
        result = await db.execute(stmt)
        return result.scalar()