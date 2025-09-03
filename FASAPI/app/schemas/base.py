"""
Base schemas with common fields.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common fields."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class BaseEntitySchema(BaseSchema):
    """Base entity schema with audit fields."""
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    version: int


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(default=0, ge=0, description="Page number (0-based)")
    size: int = Field(default=20, ge=1, le=200, description="Page size")
    sort: Optional[str] = Field(default=None, description="Sort field and direction (e.g., 'name,asc')")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    
    content: list
    page: int
    size: int
    total_elements: int
    total_pages: int
    sort: Optional[list[str]] = None
    
    class Config:
        from_attributes = True