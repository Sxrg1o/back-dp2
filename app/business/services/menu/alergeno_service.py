"""
Alergeno service for business logic related to allergen management.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.menu.alergeno_mysql_repository import AlergenoMySQLRepository
from app.data.models.menu.alergeno_model import AlergenoModel
from app.business.exceptions.base_exceptions import ValidationError, NotFoundError


class AlergenoService:
    """Alergeno service for business operations."""

    def __init__(self):
        self.alergeno_repo = AlergenoMySQLRepository()

    # Valid risk levels
    VALID_RISK_LEVELS = ['bajo', 'medio', 'alto', 'critico']

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
        Create a new allergen.

        Args:
            db: Database session
            nombre: Allergen name
            descripcion: Allergen description
            icono: Icon name or emoji
            nivel_riesgo: Risk level
            activo: Active status
            orden: Display order

        Returns:
            Created allergen

        Raises:
            ValidationError: If validation fails
        """
        # Validate input
        if not nombre or len(nombre.strip()) == 0:
            raise ValidationError("Allergen name is required")

        if len(nombre) > 100:
            raise ValidationError("Allergen name must be 100 characters or less")

        # Normalize name (trim and title case)
        nombre = nombre.strip().title()

        # Validate risk level
        if nivel_riesgo not in self.VALID_RISK_LEVELS:
            raise ValidationError(f"Invalid risk level. Must be one of: {', '.join(self.VALID_RISK_LEVELS)}")

        # Validate icon length
        if icono and len(icono) > 50:
            raise ValidationError("Icon must be 50 characters or less")

        # Validate order
        if orden < 0:
            raise ValidationError("Order must be a positive number")

        # Check if allergen name already exists
        existing_alergeno = await self.alergeno_repo.get_by_nombre(db, nombre)
        if existing_alergeno:
            raise ValidationError(f"Allergen with name '{nombre}' already exists")

        # Create allergen
        return await self.alergeno_repo.create_alergeno(
            db=db,
            nombre=nombre,
            descripcion=descripcion.strip() if descripcion else None,
            icono=icono.strip() if icono else None,
            nivel_riesgo=nivel_riesgo,
            activo=activo,
            orden=orden
        )

    async def get_alergeno_by_id(self, db: AsyncSession, alergeno_id: int) -> AlergenoModel:
        """
        Get allergen by ID.

        Args:
            db: Database session
            alergeno_id: Allergen ID

        Returns:
            Allergen

        Raises:
            NotFoundError: If allergen not found
        """
        alergeno = await self.alergeno_repo.get_by_id(db, alergeno_id)
        if not alergeno:
            raise NotFoundError(f"Allergen with ID {alergeno_id} not found")
        return alergeno

    async def get_alergeno_by_nombre(self, db: AsyncSession, nombre: str) -> AlergenoModel:
        """
        Get allergen by name.

        Args:
            db: Database session
            nombre: Allergen name

        Returns:
            Allergen

        Raises:
            NotFoundError: If allergen not found
        """
        alergeno = await self.alergeno_repo.get_by_nombre(db, nombre)
        if not alergeno:
            raise NotFoundError(f"Allergen with name '{nombre}' not found")
        return alergeno

    async def list_alergenos(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo_only: bool = False,
        order_by_orden: bool = True
    ) -> List[AlergenoModel]:
        """
        List all allergens with pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records
            activo_only: Filter only active allergens
            order_by_orden: Order by display order

        Returns:
            List of allergens
        """
        if limit > 100:
            limit = 100  # Enforce maximum limit

        return await self.alergeno_repo.get_all(
            db, skip, limit, activo_only, order_by_orden
        )

    async def list_by_risk_level(
        self,
        db: AsyncSession,
        nivel_riesgo: str,
        activo_only: bool = True
    ) -> List[AlergenoModel]:
        """
        List allergens by risk level.

        Args:
            db: Database session
            nivel_riesgo: Risk level
            activo_only: Filter only active allergens

        Returns:
            List of allergens

        Raises:
            ValidationError: If invalid risk level
        """
        if nivel_riesgo not in self.VALID_RISK_LEVELS:
            raise ValidationError(f"Invalid risk level. Must be one of: {', '.join(self.VALID_RISK_LEVELS)}")

        return await self.alergeno_repo.get_by_nivel_riesgo(db, nivel_riesgo, activo_only)

    async def update_alergeno(
        self,
        db: AsyncSession,
        alergeno_id: int,
        nombre: Optional[str] = None,
        descripcion: Optional[str] = None,
        icono: Optional[str] = None,
        nivel_riesgo: Optional[str] = None,
        activo: Optional[bool] = None,
        orden: Optional[int] = None
    ) -> AlergenoModel:
        """
        Update allergen.

        Args:
            db: Database session
            alergeno_id: Allergen ID
            nombre: New allergen name
            descripcion: New allergen description
            icono: New icon
            nivel_riesgo: New risk level
            activo: New active status
            orden: New display order

        Returns:
            Updated allergen

        Raises:
            NotFoundError: If allergen not found
            ValidationError: If validation fails
        """
        # Check if allergen exists
        existing_alergeno = await self.alergeno_repo.get_by_id(db, alergeno_id)
        if not existing_alergeno:
            raise NotFoundError(f"Allergen with ID {alergeno_id} not found")

        # Validate and prepare update data
        update_data = {}

        if nombre is not None:
            if not nombre or len(nombre.strip()) == 0:
                raise ValidationError("Allergen name cannot be empty")

            if len(nombre) > 100:
                raise ValidationError("Allergen name must be 100 characters or less")

            nombre = nombre.strip().title()

            # Check if new name already exists (excluding current allergen)
            if nombre != existing_alergeno.nombre:
                name_exists = await self.alergeno_repo.exists_nombre(db, nombre, alergeno_id)
                if name_exists:
                    raise ValidationError(f"Allergen with name '{nombre}' already exists")

            update_data['nombre'] = nombre

        if descripcion is not None:
            update_data['descripcion'] = descripcion.strip() if descripcion else None

        if icono is not None:
            if icono and len(icono) > 50:
                raise ValidationError("Icon must be 50 characters or less")
            update_data['icono'] = icono.strip() if icono else None

        if nivel_riesgo is not None:
            if nivel_riesgo not in self.VALID_RISK_LEVELS:
                raise ValidationError(f"Invalid risk level. Must be one of: {', '.join(self.VALID_RISK_LEVELS)}")
            update_data['nivel_riesgo'] = nivel_riesgo

        if activo is not None:
            update_data['activo'] = activo

        if orden is not None:
            if orden < 0:
                raise ValidationError("Order must be a positive number")
            update_data['orden'] = orden

        # Update allergen
        return await self.alergeno_repo.update_alergeno(db, alergeno_id, **update_data)

    async def delete_alergeno(self, db: AsyncSession, alergeno_id: int) -> bool:
        """
        Delete allergen.

        Args:
            db: Database session
            alergeno_id: Allergen ID

        Returns:
            True if deleted

        Raises:
            NotFoundError: If allergen not found
        """
        # Check if allergen exists
        existing_alergeno = await self.alergeno_repo.get_by_id(db, alergeno_id)
        if not existing_alergeno:
            raise NotFoundError(f"Allergen with ID {alergeno_id} not found")

        # TODO: Check if allergen is being used by any products before deletion
        # This would require checking the producto_alergeno table

        return await self.alergeno_repo.delete_alergeno(db, alergeno_id)

    async def deactivate_alergeno(self, db: AsyncSession, alergeno_id: int) -> AlergenoModel:
        """
        Deactivate allergen (soft delete).

        Args:
            db: Database session
            alergeno_id: Allergen ID

        Returns:
            Updated allergen

        Raises:
            NotFoundError: If allergen not found
        """
        alergeno = await self.alergeno_repo.deactivate_alergeno(db, alergeno_id)
        if not alergeno:
            raise NotFoundError(f"Allergen with ID {alergeno_id} not found")
        return alergeno

    async def get_alergenos_count(self, db: AsyncSession, activo_only: bool = False) -> int:
        """
        Get total count of allergens.

        Args:
            db: Database session
            activo_only: Count only active allergens

        Returns:
            Number of allergens
        """
        return await self.alergeno_repo.count_alergenos(db, activo_only)

    async def initialize_default_alergenos(self, db: AsyncSession) -> List[AlergenoModel]:
        """
        Initialize default allergens.

        Args:
            db: Database session

        Returns:
            List of created default allergens
        """
        default_alergenos = [
            ("Gluten", "Proteína presente en trigo, cebada, centeno", "🌾", "alto", 1),
            ("Lactosa", "Azúcar presente en la leche y productos lácteos", "🥛", "medio", 2),
            ("Mariscos", "Crustáceos y moluscos", "🦐", "critico", 3),
            ("Frutos Secos", "Almendras, nueces, avellanas, etc.", "🥜", "alto", 4),
            ("Huevo", "Huevo de gallina y derivados", "🥚", "medio", 5),
            ("Soja", "Soja y productos derivados", "🌱", "medio", 6),
            ("Pescado", "Pescado y productos derivados", "🐟", "alto", 7),
            ("Apio", "Apio y productos derivados", "🥬", "bajo", 8),
            ("Mostaza", "Semillas de mostaza y derivados", "🌿", "bajo", 9),
            ("Sésamo", "Semillas de sésamo y derivados", "🌾", "medio", 10)
        ]

        created_alergenos = []

        for nombre, descripcion, icono, nivel_riesgo, orden in default_alergenos:
            try:
                # Check if allergen already exists
                existing_alergeno = await self.alergeno_repo.get_by_nombre(db, nombre)
                if not existing_alergeno:
                    alergeno = await self.create_alergeno(
                        db, nombre, descripcion, icono, nivel_riesgo, True, orden
                    )
                    created_alergenos.append(alergeno)
                else:
                    created_alergenos.append(existing_alergeno)
            except ValidationError:
                # Allergen already exists, skip
                pass

        return created_alergenos

    async def update_orden(self, db: AsyncSession, alergeno_id: int, nuevo_orden: int) -> AlergenoModel:
        """
        Update display order of allergen.

        Args:
            db: Database session
            alergeno_id: Allergen ID
            nuevo_orden: New order value

        Returns:
            Updated allergen

        Raises:
            NotFoundError: If allergen not found
            ValidationError: If validation fails
        """
        if nuevo_orden < 0:
            raise ValidationError("Order must be a positive number")

        alergeno = await self.alergeno_repo.update_orden(db, alergeno_id, nuevo_orden)
        if not alergeno:
            raise NotFoundError(f"Allergen with ID {alergeno_id} not found")
        return alergeno