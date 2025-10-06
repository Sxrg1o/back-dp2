"""
Timestamp mixin for automatic created_at and updated_at fields.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """Mixin to add timestamp fields to models."""

    @declared_attr
    def created_at(cls):
        """Created timestamp."""
        return Column(
            DateTime,
            default=func.now(),
            server_default=func.now(),
            nullable=False,
            comment="Record creation timestamp"
        )

    @declared_attr
    def updated_at(cls):
        """Updated timestamp."""
        return Column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now(),
            server_onupdate=func.now(),
            nullable=False,
            comment="Record last update timestamp"
        )