"""
Pydantic schemas for category-related operations.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    """Base category schema."""

    nombre: str = Field(..., min_length=2, max_length=100, description="Category name")
    descripcion: Optional[str] = Field(None, max_length=500, description="Category description")
    orden: int = Field(0, ge=0, description="Display order")
    activo: bool = Field(True, description="Active status")
    imagen_path: Optional[str] = Field(None, max_length=255, description="Image path")


class CategoriaCreate(CategoriaBase):
    """Schema for creating a category."""
    pass


class CategoriaUpdate(BaseModel):
    """Schema for updating a category."""

    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    orden: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None
    imagen_path: Optional[str] = Field(None, max_length=255)


class CategoriaResponse(CategoriaBase):
    """Schema for category response."""

    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CategoriaWithProductCount(CategoriaResponse):
    """Schema for category with product count."""

    product_count: int = Field(0, description="Number of products in category")