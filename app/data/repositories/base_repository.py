"""
Base repository class with common CRUD operations.
"""

from typing import List, Optional, Generic, TypeVar, Type, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from app.data.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model type.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    async def create(self, db: AsyncSession, **kwargs) -> ModelType:
        """
        Create a new record.

        Args:
            db: Database session
            **kwargs: Model fields

        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Get record by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            Model instance or None
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        """
        Get all records with optional filtering and pagination.

        Args:
            db: Database session
            skip: Records to skip
            limit: Maximum records to return
            **filters: Additional filters

        Returns:
            List of model instances
        """
        query = select(self.model)

        # Apply filters
        for field, value in filters.items():
            if hasattr(self.model, field) and value is not None:
                query = query.where(getattr(self.model, field) == value)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        id: int,
        **kwargs
    ) -> Optional[ModelType]:
        """
        Update record by ID.

        Args:
            db: Database session
            id: Record ID
            **kwargs: Fields to update

        Returns:
            Updated model instance or None
        """
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(db, id)

        await db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await db.commit()

        return await self.get_by_id(db, id)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """
        Delete record by ID.

        Args:
            db: Database session
            id: Record ID

        Returns:
            True if deleted, False if not found
        """
        result = await db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await db.commit()
        return result.rowcount > 0

    async def count(self, db: AsyncSession, **filters) -> int:
        """
        Count records with optional filtering.

        Args:
            db: Database session
            **filters: Additional filters

        Returns:
            Record count
        """
        query = select(func.count(self.model.id))

        # Apply filters
        for field, value in filters.items():
            if hasattr(self.model, field) and value is not None:
                query = query.where(getattr(self.model, field) == value)

        result = await db.execute(query)
        return result.scalar()

    async def exists(self, db: AsyncSession, **filters) -> bool:
        """
        Check if record exists with given filters.

        Args:
            db: Database session
            **filters: Filters to apply

        Returns:
            True if exists, False otherwise
        """
        count = await self.count(db, **filters)
        return count > 0

    async def get_with_relations(
        self,
        db: AsyncSession,
        id: int,
        relations: List[str] = None
    ) -> Optional[ModelType]:
        """
        Get record by ID with eager loading of relations.

        Args:
            db: Database session
            id: Record ID
            relations: List of relation names to load

        Returns:
            Model instance with loaded relations or None
        """
        query = select(self.model).where(self.model.id == id)

        if relations:
            for relation in relations:
                if hasattr(self.model, relation):
                    query = query.options(selectinload(getattr(self.model, relation)))

        result = await db.execute(query)
        return result.scalar_one_or_none()