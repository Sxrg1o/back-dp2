"""SQLAlchemy adapter for BebidaRepositoryPort."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from app.domain.entities.bebida import Bebida
from app.domain.repositories.bebida_repository import BebidaRepositoryPort
from app.infrastructure.persistence.models.bebida_model import BebidaModel
from app.infrastructure.persistence.mappers.bebida_mapper import BebidaMapper
from app.infrastructure.persistence.repositories.base_repository import BaseSQLAlchemyRepository


class SqlAlchemyBebidaRepository(BaseSQLAlchemyRepository[Bebida, BebidaModel], BebidaRepositoryPort):
    """SQLAlchemy adapter for Bebida repository operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize SQLAlchemy Bebida repository.
        
        Args:
            session: SQLAlchemy async session
        """
        super().__init__(session, BebidaModel, BebidaMapper())
    
    async def get_by_id(self, bebida_id: UUID) -> Optional[Bebida]:
        """Get beverage by ID."""
        model = await self._get_by_id(bebida_id)
        return self.mapper.to_entity(model) if model else None
    
    async def get_alcoholic(self) -> List[Bebida]:
        """Get alcoholic beverages."""
        stmt = select(BebidaModel).where(BebidaModel.contenido_alcohol > 0)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_non_alcoholic(self) -> List[Bebida]:
        """Get non-alcoholic beverages."""
        stmt = select(BebidaModel).where(BebidaModel.contenido_alcohol == 0)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_all(self) -> List[Bebida]:
        """Get all beverages."""
        models = await self._get_all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_available(self) -> List[Bebida]:
        """Get available beverages."""
        stmt = select(BebidaModel).where(
            and_(
                BebidaModel.activo == True,
                BebidaModel.stock_actual > 0
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_type(self, tipo_bebida: str) -> List[Bebida]:
        """Get beverages by type."""
        stmt = select(BebidaModel).where(BebidaModel.tipo_bebida == tipo_bebida)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_temperature(self, temperatura_servicio: str) -> List[Bebida]:
        """Get beverages by service temperature."""
        stmt = select(BebidaModel).where(BebidaModel.temperatura_servicio == temperatura_servicio)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_volume_range(self, min_volume: float, max_volume: float) -> List[Bebida]:
        """Get beverages by volume range."""
        stmt = select(BebidaModel).where(
            and_(
                BebidaModel.volumen >= min_volume,
                BebidaModel.volumen <= max_volume
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_alcohol_range(self, min_alcohol: float, max_alcohol: float) -> List[Bebida]:
        """Get beverages by alcohol content range."""
        stmt = select(BebidaModel).where(
            and_(
                BebidaModel.contenido_alcohol >= min_alcohol,
                BebidaModel.contenido_alcohol <= max_alcohol
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_brand(self, marca: str) -> List[Bebida]:
        """Get beverages by brand."""
        stmt = select(BebidaModel).where(BebidaModel.marca == marca)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_origin(self, origen: str) -> List[Bebida]:
        """Get beverages by origin."""
        stmt = select(BebidaModel).where(BebidaModel.origen == origen)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_name(self, name: str) -> Optional[Bebida]:
        """Get beverage by name."""
        stmt = select(BebidaModel).where(BebidaModel.nombre == name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None
    
    async def get_cold_beverages(self) -> List[Bebida]:
        """Get cold beverages."""
        stmt = select(BebidaModel).where(BebidaModel.temperatura_servicio == "fria")
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_hot_beverages(self) -> List[Bebida]:
        """Get hot beverages."""
        stmt = select(BebidaModel).where(BebidaModel.temperatura_servicio == "caliente")
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_standard_volumes(self) -> List[Bebida]:
        """Get beverages with standard volumes."""
        standard_volumes = [200, 250, 330, 355, 500, 750, 1000]
        stmt = select(BebidaModel).where(BebidaModel.volumen.in_(standard_volumes))
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_suitable_for_minors(self) -> List[Bebida]:
        """Get beverages suitable for minors."""
        return await self.get_non_alcoholic()
    
    async def get_by_volume_category(self, categoria: str) -> List[Bebida]:
        """Get beverages by volume category."""
        volume_ranges = {
            "pequeño": (0, 250),
            "mediano": (251, 500),
            "grande": (501, 750),
            "extra_grande": (751, float('inf'))
        }
        
        if categoria not in volume_ranges:
            return []
        
        min_vol, max_vol = volume_ranges[categoria]
        if max_vol == float('inf'):
            stmt = select(BebidaModel).where(BebidaModel.volumen > min_vol)
        else:
            stmt = select(BebidaModel).where(
                and_(
                    BebidaModel.volumen > min_vol,
                    BebidaModel.volumen <= max_vol
                )
            )
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def save(self, bebida: Bebida) -> Bebida:
        """Save beverage (create or update)."""
        model = self.mapper.to_model(bebida)
        saved_model = await self._save(model)
        return self.mapper.to_entity(saved_model)
    
    async def delete(self, bebida_id: UUID) -> bool:
        """Delete beverage by ID."""
        return await self._delete_by_id(bebida_id)
    
    async def exists_by_id(self, bebida_id: UUID) -> bool:
        """Check if beverage exists by ID."""
        return await self._exists_by_id(bebida_id)
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if beverage exists by name."""
        stmt = select(BebidaModel.id).where(BebidaModel.nombre == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def get_most_popular(self, limit: int = 10) -> List[Bebida]:
        """Get most popular beverages."""
        # For now, return active beverages ordered by name
        # In a real implementation, this would use order/sales data
        stmt = select(BebidaModel).where(
            BebidaModel.activo == True
        ).order_by(BebidaModel.nombre).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_low_stock(self) -> List[Bebida]:
        """Get beverages with low stock."""
        stmt = select(BebidaModel).where(
            BebidaModel.stock_actual <= BebidaModel.stock_minimo
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]