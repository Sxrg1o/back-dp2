"""
Mesa repository for data access operations.
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mesa import Mesa
from app.repositories.base import BaseRepository
from app.schemas.mesa import MesaCreate, MesaUpdate


class MesaRepository(BaseRepository[Mesa, MesaCreate, MesaUpdate]):
    """Repository for Mesa operations."""
    
    def __init__(self):
        super().__init__(Mesa)
    
    async def get_by_numero(self, db: AsyncSession, numero: int) -> Optional[Mesa]:
        """Get mesa by table number."""
        result = await db.execute(
            select(Mesa).where(Mesa.numero == numero)
        )
        return result.scalar_one_or_none()
    
    async def get_active_mesas(self, db: AsyncSession) -> List[Mesa]:
        """Get all active mesas."""
        result = await db.execute(
            select(Mesa).where(Mesa.activa == True).order_by(Mesa.numero)
        )
        return result.scalars().all()
    
    async def get_by_capacidad_range(
        self,
        db: AsyncSession,
        min_capacidad: int,
        max_capacidad: int
    ) -> List[Mesa]:
        """Get mesas by capacity range."""
        result = await db.execute(
            select(Mesa).where(
                Mesa.capacidad >= min_capacidad,
                Mesa.capacidad <= max_capacidad,
                Mesa.activa == True
            ).order_by(Mesa.numero)
        )
        return result.scalars().all()


# Create repository instance
mesa_repository = MesaRepository()