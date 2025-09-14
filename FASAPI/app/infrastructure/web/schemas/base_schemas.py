"""
Base schemas for web layer.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    class Config:
        from_attributes = True
        use_enum_values = True


class BaseEntitySchema(BaseSchema):
    """Base schema for entities with common fields."""

    id: UUID = Field(..., description="Entity unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    version: int = Field(..., description="Entity version")
