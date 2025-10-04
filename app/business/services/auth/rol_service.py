"""
Rol service for business logic related to role management.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.auth.rol_mysql_repository import RolMySQLRepository
from app.data.models.auth.rol_model import RolModel
from app.business.exceptions.base_exceptions import ValidationError, NotFoundError


class RolService:
    """Rol service for business operations."""

    def __init__(self):
        self.rol_repo = RolMySQLRepository()

    async def create_rol(
        self,
        db: AsyncSession,
        nombre: str,
        descripcion: Optional[str] = None
    ) -> RolModel:
        """
        Create a new role.

        Args:
            db: Database session
            nombre: Role name
            descripcion: Role description

        Returns:
            Created role

        Raises:
            ValidationError: If role name already exists or validation fails
        """
        # Validate input
        if not nombre or len(nombre.strip()) == 0:
            raise ValidationError("Role name is required")

        if len(nombre) > 50:
            raise ValidationError("Role name must be 50 characters or less")

        # Normalize name (trim and title case)
        nombre = nombre.strip().title()

        # Check if role name already exists
        existing_rol = await self.rol_repo.get_by_nombre(db, nombre)
        if existing_rol:
            raise ValidationError(f"Role with name '{nombre}' already exists")

        # Create role
        return await self.rol_repo.create_rol(
            db=db,
            nombre=nombre,
            descripcion=descripcion.strip() if descripcion else None
        )

    async def get_rol_by_id(self, db: AsyncSession, rol_id: int) -> RolModel:
        """
        Get role by ID.

        Args:
            db: Database session
            rol_id: Role ID

        Returns:
            Role

        Raises:
            NotFoundError: If role not found
        """
        rol = await self.rol_repo.get_by_id(db, rol_id)
        if not rol:
            raise NotFoundError(f"Role with ID {rol_id} not found")
        return rol

    async def get_rol_by_nombre(self, db: AsyncSession, nombre: str) -> RolModel:
        """
        Get role by name.

        Args:
            db: Database session
            nombre: Role name

        Returns:
            Role

        Raises:
            NotFoundError: If role not found
        """
        rol = await self.rol_repo.get_by_nombre(db, nombre)
        if not rol:
            raise NotFoundError(f"Role with name '{nombre}' not found")
        return rol

    async def list_roles(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[RolModel]:
        """
        List all roles with pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records

        Returns:
            List of roles
        """
        if limit > 100:
            limit = 100  # Enforce maximum limit

        return await self.rol_repo.get_all(db, skip, limit)

    async def update_rol(
        self,
        db: AsyncSession,
        rol_id: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None
    ) -> RolModel:
        """
        Update role.

        Args:
            db: Database session
            rol_id: Role ID
            nombre: New role name
            descripcion: New role description

        Returns:
            Updated role

        Raises:
            NotFoundError: If role not found
            ValidationError: If validation fails
        """
        # Check if role exists
        existing_rol = await self.rol_repo.get_by_id(db, rol_id)
        if not existing_rol:
            raise NotFoundError(f"Role with ID {rol_id} not found")

        # Validate and prepare update data
        update_data = {}

        if nombre is not None:
            if not nombre or len(nombre.strip()) == 0:
                raise ValidationError("Role name cannot be empty")

            if len(nombre) > 50:
                raise ValidationError("Role name must be 50 characters or less")

            nombre = nombre.strip().title()

            # Check if new name already exists (excluding current role)
            if nombre != existing_rol.nombre:
                name_exists = await self.rol_repo.exists_nombre(db, nombre, rol_id)
                if name_exists:
                    raise ValidationError(f"Role with name '{nombre}' already exists")

            update_data['nombre'] = nombre

        if descripcion is not None:
            update_data['descripcion'] = descripcion.strip() if descripcion else None

        # Update role
        return await self.rol_repo.update_rol(db, rol_id, **update_data)

    async def delete_rol(self, db: AsyncSession, rol_id: int) -> bool:
        """
        Delete role.

        Args:
            db: Database session
            rol_id: Role ID

        Returns:
            True if deleted

        Raises:
            NotFoundError: If role not found
        """
        # Check if role exists
        existing_rol = await self.rol_repo.get_by_id(db, rol_id)
        if not existing_rol:
            raise NotFoundError(f"Role with ID {rol_id} not found")

        # TODO: Check if role is being used by any users before deletion
        # This would require checking the usuario table

        return await self.rol_repo.delete_rol(db, rol_id)

    async def get_roles_count(self, db: AsyncSession) -> int:
        """
        Get total count of roles.

        Args:
            db: Database session

        Returns:
            Number of roles
        """
        return await self.rol_repo.count_roles(db)

    async def initialize_default_roles(self, db: AsyncSession) -> List[RolModel]:
        """
        Initialize default system roles.

        Args:
            db: Database session

        Returns:
            List of created default roles
        """
        default_roles = [
            ("Admin", "Administrador del sistema con acceso completo"),
            ("Mesero", "Personal de servicio en sala"),
            ("Cocina", "Personal de cocina"),
            ("Cliente", "Cliente del restaurante")
        ]

        created_roles = []

        for nombre, descripcion in default_roles:
            try:
                # Check if role already exists
                existing_rol = await self.rol_repo.get_by_nombre(db, nombre)
                if not existing_rol:
                    rol = await self.create_rol(db, nombre, descripcion)
                    created_roles.append(rol)
                else:
                    created_roles.append(existing_rol)
            except ValidationError:
                # Role already exists, skip
                pass

        return created_roles