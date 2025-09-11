"""Base repository adapter with common SQLAlchemy operations."""

from typing import TypeVar, Generic, Optional, List, Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload

from app.infrastructure.persistence.models.base import BaseModel
from app.infrastructure.persistence.mappers.base_mapper import BaseMapper

# Type variables
EntityType = TypeVar('EntityType')
ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseSQLAlchemyRepository(Generic[EntityType, ModelType]):
    """Base repository adapter with common SQLAlchemy operations."""
    
    def __init__(
        self,
        session: AsyncSession,
        model_class: Type[ModelType],
        mapper: BaseMapper[EntityType, ModelType]
    ):
        """Initialize base repository.
        
        Args:
            session: SQLAlchemy async session
            model_class: SQLAlchemy model class
            mapper: Entity-model mapper
        """
        self.session = session
        self.model_class = model_class
        self.mapper = mapper
    
    async def _get_by_id(self, entity_id: UUID) -> Optional[ModelType]:
        """Get model by ID."""
        stmt = select(self.model_class).where(self.model_class.id == entity_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def _get_all(self) -> List[ModelType]:
        """Get all models."""
        stmt = select(self.model_class)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def _save(self, model: ModelType) -> ModelType:
        """Save model to database."""
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def _delete_by_id(self, entity_id: UUID) -> bool:
        """Delete model by ID."""
        stmt = delete(self.model_class).where(self.model_class.id == entity_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
    
    async def _exists_by_id(self, entity_id: UUID) -> bool:
        """Check if model exists by ID."""
        stmt = select(func.count(self.model_class.id)).where(self.model_class.id == entity_id)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count > 0
    
    async def _count_all(self) -> int:
        """Count all models."""
        stmt = select(func.count(self.model_class.id))
        result = await self.session.execute(stmt)
        return result.scalar()