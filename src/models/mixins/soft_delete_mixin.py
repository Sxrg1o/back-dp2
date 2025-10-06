"""
Soft delete mixin for logical deletion of records.
"""

from sqlalchemy.orm import (
    mapped_column,
    declared_attr,
    declarative_mixin,
)
from sqlalchemy import TIMESTAMP, Boolean
from datetime import datetime, timezone


@declarative_mixin
class SoftDeleteMixin:
    """Mixin to add soft delete functionality to models."""

    @declared_attr
    def deleted_at(cls):
        """Soft delete timestamp."""
        return mapped_column(
            TIMESTAMP, nullable=True, default=None, comment="Soft delete timestamp"
        )

    @declared_attr
    def is_deleted(cls):
        """Soft delete flag."""
        return mapped_column(
            Boolean, default=False, nullable=False, comment="Soft delete flag"
        )

    def soft_delete(self):
        """Mark record as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore soft deleted record."""
        self.is_deleted = False
        self.deleted_at = None
