"""
Usuario repository for MySQL restaurant_dp2 schema.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload

from app.data.models.auth.usuario_model import UsuarioModel


class UsuarioMySQLRepository:
    """Usuario repository for existing MySQL schema."""

    async def create_usuario(
        self,
        db: AsyncSession,
        id_rol: int,
        email: str,
        password_hash: str,
        nombre: str,
        telefono: Optional[str] = None,
        activo: bool = True
    ) -> UsuarioModel:
        """
        Create a new usuario.

        Args:
            db: Database session
            id_rol: Role ID
            email: User email
            password_hash: Hashed password
            nombre: User name
            telefono: Phone number (optional)
            activo: Active status

        Returns:
            Created usuario
        """
        stmt = insert(UsuarioModel).values(
            id_rol=id_rol,
            email=email,
            password_hash=password_hash,
            nombre=nombre,
            telefono=telefono,
            activo=activo
        )
        result = await db.execute(stmt)
        await db.commit()

        # Get the created record
        usuario_id = result.inserted_primary_key[0]
        return await self.get_by_id(db, usuario_id)

    async def get_by_id(self, db: AsyncSession, usuario_id: int) -> Optional[UsuarioModel]:
        """
        Get usuario by ID.

        Args:
            db: Database session
            usuario_id: Usuario ID

        Returns:
            Usuario or None
        """
        stmt = select(UsuarioModel).where(UsuarioModel.id_usuario == usuario_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[UsuarioModel]:
        """
        Get usuario by email.

        Args:
            db: Database session
            email: User email

        Returns:
            Usuario or None
        """
        stmt = select(UsuarioModel).where(UsuarioModel.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo_only: bool = False
    ) -> List[UsuarioModel]:
        """
        Get all usuarios with pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records
            activo_only: Filter only active users

        Returns:
            List of usuarios
        """
        stmt = select(UsuarioModel)

        if activo_only:
            stmt = stmt.where(UsuarioModel.activo == True)

        stmt = stmt.offset(skip).limit(limit).order_by(UsuarioModel.id_usuario)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_usuario(
        self,
        db: AsyncSession,
        usuario_id: int,
        **kwargs
    ) -> Optional[UsuarioModel]:
        """
        Update usuario.

        Args:
            db: Database session
            usuario_id: Usuario ID
            **kwargs: Fields to update

        Returns:
            Updated usuario or None
        """
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(db, usuario_id)

        stmt = (
            update(UsuarioModel)
            .where(UsuarioModel.id_usuario == usuario_id)
            .values(**update_data)
        )
        await db.execute(stmt)
        await db.commit()

        return await self.get_by_id(db, usuario_id)

    async def delete_usuario(self, db: AsyncSession, usuario_id: int) -> bool:
        """
        Delete usuario.

        Args:
            db: Database session
            usuario_id: Usuario ID

        Returns:
            True if deleted, False if not found
        """
        stmt = delete(UsuarioModel).where(UsuarioModel.id_usuario == usuario_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def deactivate_usuario(self, db: AsyncSession, usuario_id: int) -> Optional[UsuarioModel]:
        """
        Deactivate usuario (soft delete).

        Args:
            db: Database session
            usuario_id: Usuario ID

        Returns:
            Updated usuario or None
        """
        return await self.update_usuario(db, usuario_id, activo=False)

    async def get_by_role(self, db: AsyncSession, id_rol: int) -> List[UsuarioModel]:
        """
        Get usuarios by role.

        Args:
            db: Database session
            id_rol: Role ID

        Returns:
            List of usuarios with the role
        """
        stmt = (
            select(UsuarioModel)
            .where(UsuarioModel.id_rol == id_rol)
            .where(UsuarioModel.activo == True)
            .order_by(UsuarioModel.nombre)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def count_usuarios(self, db: AsyncSession, activo_only: bool = False) -> int:
        """
        Count usuarios.

        Args:
            db: Database session
            activo_only: Count only active users

        Returns:
            Number of usuarios
        """
        from sqlalchemy import func

        stmt = select(func.count(UsuarioModel.id_usuario))

        if activo_only:
            stmt = stmt.where(UsuarioModel.activo == True)

        result = await db.execute(stmt)
        return result.scalar()

    async def exists_email(self, db: AsyncSession, email: str, exclude_id: int = None) -> bool:
        """
        Check if email exists.

        Args:
            db: Database session
            email: Email to check
            exclude_id: Usuario ID to exclude from check

        Returns:
            True if email exists, False otherwise
        """
        stmt = select(UsuarioModel.id_usuario).where(UsuarioModel.email == email)

        if exclude_id:
            stmt = stmt.where(UsuarioModel.id_usuario != exclude_id)

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None