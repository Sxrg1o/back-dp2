"""SQLAlchemy adapter for IngredienteRepositoryPort."""

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, update

from app.domain.entities.ingrediente import Ingrediente
from app.domain.repositories.ingrediente_repository import IngredienteRepositoryPort
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.mappers.ingrediente_mapper import IngredienteMapper
from app.infrastructure.persistence.repositories.base_repository import BaseSQLAlchemyRepository


class SqlAlchemyIngredienteRepository(BaseSQLAlchemyRepository[Ingrediente, IngredienteModel], IngredienteRepositoryPort):
    """SQLAlchemy adapter for Ingrediente repository operations."""
    
    def __init__(self, session: AsyncSession):
        """Initialize SQLAlchemy Ingrediente repository.
        
        Args:
            session: SQLAlchemy async session
        """
        super().__init__(session, IngredienteModel, IngredienteMapper())
    
    async def get_by_id(self, ingrediente_id: UUID) -> Optional[Ingrediente]:
        """Get ingredient by ID."""
        model = await self._get_by_id(ingrediente_id)
        return self.mapper.to_entity(model) if model else None
    
    async def get_by_type(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """Get ingredients by type."""
        stmt = select(IngredienteModel).where(
            IngredienteModel.tipo_ingrediente == tipo.value
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_all(self) -> List[Ingrediente]:
        """Get all ingredients."""
        models = await self._get_all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_available(self) -> List[Ingrediente]:
        """Get available ingredients."""
        now = datetime.utcnow()
        stmt = select(IngredienteModel).where(
            and_(
                IngredienteModel.activo == True,
                IngredienteModel.stock_actual > 0,
                or_(
                    IngredienteModel.fecha_vencimiento.is_(None),
                    IngredienteModel.fecha_vencimiento > now
                )
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def check_stock(self, ingrediente_id: UUID) -> int:
        """Check current stock of ingredient."""
        stmt = select(IngredienteModel.stock_actual).where(
            IngredienteModel.id == ingrediente_id
        )
        result = await self.session.execute(stmt)
        stock = result.scalar_one_or_none()
        return stock if stock is not None else 0
    
    async def update_stock(self, ingrediente_id: UUID, new_stock: int) -> Ingrediente:
        """Update ingredient stock."""
        stmt = update(IngredienteModel).where(
            IngredienteModel.id == ingrediente_id
        ).values(
            stock_actual=new_stock,
            updated_at=datetime.utcnow()
        ).returning(IngredienteModel)
        
        result = await self.session.execute(stmt)
        await self.session.commit()
        model = result.scalar_one()
        return self.mapper.to_entity(model)
    
    async def get_by_supplier(self, proveedor: str) -> List[Ingrediente]:
        """Get ingredients by supplier."""
        stmt = select(IngredienteModel).where(
            IngredienteModel.proveedor == proveedor
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_expiring_soon(self, days_ahead: int = 3) -> List[Ingrediente]:
        """Get ingredients expiring within specified days."""
        future_date = datetime.utcnow() + timedelta(days=days_ahead)
        stmt = select(IngredienteModel).where(
            and_(
                IngredienteModel.fecha_vencimiento.is_not(None),
                IngredienteModel.fecha_vencimiento <= future_date,
                IngredienteModel.fecha_vencimiento > datetime.utcnow()
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_expired(self) -> List[Ingrediente]:
        """Get expired ingredients."""
        now = datetime.utcnow()
        stmt = select(IngredienteModel).where(
            and_(
                IngredienteModel.fecha_vencimiento.is_not(None),
                IngredienteModel.fecha_vencimiento <= now
            )
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_low_stock(self) -> List[Ingrediente]:
        """Get ingredients with low stock."""
        stmt = select(IngredienteModel).where(
            IngredienteModel.stock_actual <= IngredienteModel.stock_minimo
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def get_by_name(self, name: str) -> Optional[Ingrediente]:
        """Get ingredient by name."""
        stmt = select(IngredienteModel).where(IngredienteModel.nombre == name)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self.mapper.to_entity(model) if model else None
    
    async def get_by_unit_measure(self, unidad_medida: str) -> List[Ingrediente]:
        """Get ingredients by unit of measure."""
        stmt = select(IngredienteModel).where(
            IngredienteModel.unidad_medida == unidad_medida
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self.mapper.to_entity(model) for model in models]
    
    async def save(self, ingrediente: Ingrediente) -> Ingrediente:
        """Save ingredient (create or update)."""
        model = self.mapper.to_model(ingrediente)
        saved_model = await self._save(model)
        return self.mapper.to_entity(saved_model)
    
    async def delete(self, ingrediente_id: UUID) -> bool:
        """Delete ingredient by ID."""
        return await self._delete_by_id(ingrediente_id)
    
    async def exists_by_id(self, ingrediente_id: UUID) -> bool:
        """Check if ingredient exists by ID."""
        return await self._exists_by_id(ingrediente_id)
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if ingredient exists by name."""
        stmt = select(IngredienteModel.id).where(IngredienteModel.nombre == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def bulk_update_stock(self, stock_updates: dict[UUID, int]) -> List[Ingrediente]:
        """Update stock for multiple ingredients."""
        updated_entities = []
        
        for ingrediente_id, new_stock in stock_updates.items():
            updated_entity = await self.update_stock(ingrediente_id, new_stock)
            updated_entities.append(updated_entity)
        
        return updated_entities
    
    async def get_total_weight_by_type(self, tipo: EtiquetaIngrediente) -> float:
        """Get total weight of ingredients by type."""
        stmt = select(
            func.sum(IngredienteModel.stock_actual * IngredienteModel.peso_unitario)
        ).where(
            IngredienteModel.tipo_ingrediente == tipo.value
        )
        result = await self.session.execute(stmt)
        total_weight = result.scalar()
        return float(total_weight) if total_weight else 0.0