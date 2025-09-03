"""
Mesa service for business logic operations.
"""
import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.models.mesa import Mesa
from app.repositories.mesa_repository import mesa_repository
from app.schemas.mesa import MesaCreate, MesaUpdate
from app.schemas.base import PaginatedResponse, PaginationParams


class MesaService:
    """Service for Mesa business logic."""
    
    def __init__(self):
        self.repository = mesa_repository
    
    async def get_mesa(self, db: AsyncSession, mesa_id: uuid.UUID) -> Mesa:
        """Get mesa by ID."""
        mesa = await self.repository.get(db, id=mesa_id)
        if not mesa:
            raise NotFoundError(f"Mesa with ID {mesa_id} not found")
        return mesa
    
    async def get_mesa_by_numero(self, db: AsyncSession, numero: int) -> Mesa:
        """Get mesa by table number."""
        mesa = await self.repository.get_by_numero(db, numero=numero)
        if not mesa:
            raise NotFoundError(f"Mesa with number {numero} not found")
        return mesa
    
    async def get_mesas(
        self,
        db: AsyncSession,
        pagination: PaginationParams,
        activa: Optional[bool] = None,
        min_capacidad: Optional[int] = None,
        max_capacidad: Optional[int] = None,
    ) -> PaginatedResponse:
        """Get paginated list of mesas with optional filtering."""
        
        # Build filters
        filters = {}
        if activa is not None:
            filters["activa"] = activa
        
        # Handle capacity range filtering
        if min_capacidad is not None or max_capacidad is not None:
            if min_capacidad and max_capacidad:
                mesas = await self.repository.get_by_capacidad_range(
                    db, min_capacidad, max_capacidad
                )
                total = len(mesas)
                # Apply pagination manually for complex queries
                start = pagination.page * pagination.size
                end = start + pagination.size
                mesas = mesas[start:end]
            else:
                # Use regular filtering for single capacity constraint
                if min_capacidad:
                    filters["capacidad"] = min_capacidad
                mesas = await self.repository.get_multi(
                    db,
                    skip=pagination.page * pagination.size,
                    limit=pagination.size,
                    filters=filters,
                    order_by="numero",
                )
                total = await self.repository.count(db, filters=filters)
        else:
            # Regular pagination
            mesas = await self.repository.get_multi(
                db,
                skip=pagination.page * pagination.size,
                limit=pagination.size,
                filters=filters,
                order_by="numero",
            )
            total = await self.repository.count(db, filters=filters)
        
        total_pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResponse(
            content=mesas,
            page=pagination.page,
            size=pagination.size,
            total_elements=total,
            total_pages=total_pages,
            sort=["numero,asc"] if not pagination.sort else [pagination.sort],
        )
    
    async def create_mesa(self, db: AsyncSession, mesa_data: MesaCreate) -> Mesa:
        """Create a new mesa."""
        
        # Check if table number already exists
        existing_mesa = await self.repository.get_by_numero(db, numero=mesa_data.numero)
        if existing_mesa:
            raise ConflictError(f"Mesa with number {mesa_data.numero} already exists")
        
        return await self.repository.create(db, obj_in=mesa_data)
    
    async def update_mesa(
        self,
        db: AsyncSession,
        mesa_id: uuid.UUID,
        mesa_data: MesaUpdate
    ) -> Mesa:
        """Update an existing mesa."""
        
        # Get existing mesa
        mesa = await self.get_mesa(db, mesa_id)
        
        # Check if new table number conflicts with existing one
        if mesa_data.numero is not None and mesa_data.numero != mesa.numero:
            existing_mesa = await self.repository.get_by_numero(db, numero=mesa_data.numero)
            if existing_mesa:
                raise ConflictError(f"Mesa with number {mesa_data.numero} already exists")
        
        return await self.repository.update(db, db_obj=mesa, obj_in=mesa_data)
    
    async def delete_mesa(self, db: AsyncSession, mesa_id: uuid.UUID) -> Mesa:
        """Delete a mesa."""
        
        # Get existing mesa
        mesa = await self.get_mesa(db, mesa_id)
        
        # TODO: Check if mesa has active orders before deletion
        # This would require implementing the Pedido model and repository
        
        return await self.repository.remove(db, id=mesa_id)
    
    async def get_active_mesas(self, db: AsyncSession) -> List[Mesa]:
        """Get all active mesas."""
        return await self.repository.get_active_mesas(db)


# Create service instance
mesa_service = MesaService()