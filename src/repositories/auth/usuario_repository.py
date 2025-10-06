"""
User repository for user-related database operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.auth.usuario_model import UsuarioModel
from src.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[UsuarioModel]):
    """User repository with specific user operations."""

    def __init__(self):
        super().__init__(UsuarioModel)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[UsuarioModel]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: User email

        Returns:
            User model instance or None
        """
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.rol))
            .where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def get_active_users(self, db: AsyncSession) -> list[UsuarioModel]:
        """
        Get all active users.

        Args:
            db: Database session

        Returns:
            List of active users
        """
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.rol))
            .where(self.model.activo == True)
            .order_by(self.model.nombre)
        )
        return result.scalars().all()

    async def get_by_role(self, db: AsyncSession, role_name: str) -> list[UsuarioModel]:
        """
        Get users by role name.

        Args:
            db: Database session
            role_name: Role name

        Returns:
            List of users with the specified role
        """
        result = await db.execute(
            select(self.model)
            .join(self.model.rol)
            .where(self.model.rol.has(nombre=role_name))
            .where(self.model.activo == True)
            .options(selectinload(self.model.rol))
        )
        return result.scalars().all()

    async def update_last_access(self, db: AsyncSession, user_id: int) -> None:
        """
        Update user's last access timestamp.

        Args:
            db: Database session
            user_id: User ID
        """
        from datetime import datetime
        await self.update(db, user_id, ultimo_acceso=datetime.utcnow())

    async def deactivate_user(self, db: AsyncSession, user_id: int) -> Optional[UsuarioModel]:
        """
        Deactivate user (soft delete).

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Updated user or None
        """
        return await self.update(db, user_id, activo=False)