"""
Base model class with common functionality.
"""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from src.models.mixins.timestamp_mixin import TimestampMixin

# Create the base class
Base = declarative_base()


class BaseModel(Base, TimestampMixin):
    """Base model class with common fields and functionality."""

    __abstract__ = True

    @declared_attr
    def id(cls):
        """Primary key for all models."""
        return Column(
            Integer,
            primary_key=True,
            autoincrement=True,
            comment="Primary key"
        )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        return f"<{class_name}(id={getattr(self, 'id', 'None')})>"