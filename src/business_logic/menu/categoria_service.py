"""
Categoria service for business logic related to category management.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.menu.categoria_mysql_repository import CategoriaMySQLRepository
from src.models.menu.categoria_model import CategoriaModel
from src.business_logic.exceptions.base_exceptions import ValidationError, NotFoundError


class CategoriaService:
    """Categoria service for business operations."""

    def __init__(self):
        self.categoria_repo = CategoriaMySQLRepository()

    async def create_categoria(
        self,
        db: AsyncSession,
        nombre: str,
        descripcion: Optional[str] = None,
        orden: int = 0,
        activo: bool = True,
        imagen_path: Optional[str] = None
    ) -> CategoriaModel:
        """Create a new category."""
        # Validate input
        if not nombre or len(nombre.strip()) == 0:
            raise ValidationError("Category name is required")

        if len(nombre) > 100:
            raise ValidationError("Category name must be 100 characters or less")

        # Normalize name
        nombre = nombre.strip().title()

        # Validate order
        if orden < 0:
            raise ValidationError("Order must be a positive number")

        # Check if category name already exists
        existing_categoria = await self.categoria_repo.get_by_nombre(db, nombre)
        if existing_categoria:
            raise ValidationError(f"Category with name '{nombre}' already exists")

        # Create category
        return await self.categoria_repo.create_categoria(
            db=db,
            nombre=nombre,
            descripcion=descripcion.strip() if descripcion else None,
            orden=orden,
            activo=activo,
            imagen_path=imagen_path.strip() if imagen_path else None
        )

    async def get_categoria_by_id(self, db: AsyncSession, categoria_id: int) -> CategoriaModel:
        """Get category by ID."""
        categoria = await self.categoria_repo.get_by_id(db, categoria_id)
        if not categoria:
            raise NotFoundError(f"Category with ID {categoria_id} not found")
        return categoria

    async def list_categorias(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo_only: bool = False,
        order_by_orden: bool = True
    ) -> List[CategoriaModel]:
        """List all categories with pagination."""
        if limit > 100:
            limit = 100  # Enforce maximum limit

        return await self.categoria_repo.get_all(
            db, skip, limit, activo_only, order_by_orden
        )

    async def update_categoria(
        self,
        db: AsyncSession,
        categoria_id: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        orden: Optional[int] = None,
        activo: Optional[bool] = None,
        imagen_path: Optional[str] = None
    ) -> CategoriaModel:
        """Update category."""
        # Check if category exists
        existing_categoria = await self.categoria_repo.get_by_id(db, categoria_id)
        if not existing_categoria:
            raise NotFoundError(f"Category with ID {categoria_id} not found")

        # Validate and prepare update data
        update_data = {}

        if nombre is not None:
            if not nombre or len(nombre.strip()) == 0:
                raise ValidationError("Category name cannot be empty")

            if len(nombre) > 100:
                raise ValidationError("Category name must be 100 characters or less")

            nombre = nombre.strip().title()

            # Check if new name already exists (excluding current category)
            if nombre != existing_categoria.nombre:
                name_exists = await self.categoria_repo.exists_nombre(db, nombre, categoria_id)
                if name_exists:
                    raise ValidationError(f"Category with name '{nombre}' already exists")

            update_data['nombre'] = nombre

        if descripcion is not None:
            update_data['descripcion'] = descripcion.strip() if descripcion else None

        if orden is not None:
            if orden < 0:
                raise ValidationError("Order must be a positive number")
            update_data['orden'] = orden

        if activo is not None:
            update_data['activo'] = activo

        if imagen_path is not None:
            update_data['imagen_path'] = imagen_path.strip() if imagen_path else None

        # Update category
        return await self.categoria_repo.update_categoria(db, categoria_id, **update_data)

    async def delete_categoria(self, db: AsyncSession, categoria_id: int) -> bool:
        """Delete category."""
        # Check if category exists
        existing_categoria = await self.categoria_repo.get_by_id(db, categoria_id)
        if not existing_categoria:
            raise NotFoundError(f"Category with ID {categoria_id} not found")

        return await self.categoria_repo.delete_categoria(db, categoria_id)

    async def initialize_default_categorias(self, db: AsyncSession) -> List[CategoriaModel]:
        """Initialize default categories."""
        default_categorias = [
            ("Entradas", "Aperitivos y entradas para comenzar", 1),
            ("Platos Principales", "Platos fuertes y especialidades", 2),
            ("Postres", "Dulces y postres para finalizar", 3),
            ("Bebidas", "Bebidas frías y calientes", 4),
            ("Ensaladas", "Ensaladas frescas y saludables", 5)
        ]

        created_categorias = []

        for nombre, descripcion, orden in default_categorias:
            try:
                # Check if category already exists
                existing_categoria = await self.categoria_repo.get_by_nombre(db, nombre)
                if not existing_categoria:
                    categoria = await self.create_categoria(db, nombre, descripcion, orden)
                    created_categorias.append(categoria)
                else:
                    created_categorias.append(existing_categoria)
            except ValidationError:
                pass

        return created_categorias