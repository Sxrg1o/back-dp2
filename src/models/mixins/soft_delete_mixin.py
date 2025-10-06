"""
Soft delete mixin for logical deletion of records.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class SoftDeleteMixin:
    """Mixin to add soft delete functionality to models."""

    @declared_attr
    def deleted_at(cls):
        """Soft delete timestamp."""
        return Column(
            DateTime,
            nullable=True,
            default=None,
            comment="Soft delete timestamp"
        )

    @declared_attr
    def is_deleted(cls):
        """Soft delete flag."""
        return Column(
            Boolean,
            default=False,
            nullable=False,
            comment="Soft delete flag"
        )

    def soft_delete(self):
        """Mark record as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restore soft deleted record."""
        self.is_deleted = False
        self.deleted_at = None