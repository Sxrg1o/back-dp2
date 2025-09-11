"""Base mapper interface for entity-model conversion."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from app.infrastructure.persistence.models.base import BaseModel

# Type variables for generic mapper
EntityType = TypeVar('EntityType')
ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseMapper(ABC, Generic[EntityType, ModelType]):
    """Abstract base mapper for entity-model conversion."""
    
    @abstractmethod
    def to_entity(self, model: ModelType) -> EntityType:
        """Convert SQLAlchemy model to domain entity."""
        pass
    
    @abstractmethod
    def to_model(self, entity: EntityType) -> ModelType:
        """Convert domain entity to SQLAlchemy model."""
        pass