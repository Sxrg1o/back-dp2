"""
Pydantic schemas for Categoria (Category) entities.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    """Base schema for Categoria."""
    nombre: str = Field(..., description="Category name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Category description")
    orden: int = Field(default=0, description="Display order", ge=0)
    activo: bool = Field(default=True, description="Active status")
    imagen_path: Optional[str] = Field(None, description="Image path", max_length=255)


class CategoriaCreate(CategoriaBase):
    """Schema for creating a new categoria."""
    pass


class CategoriaUpdate(BaseModel):
    """Schema for updating categoria."""
    nombre: Optional[str] = Field(None, description="Category name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Category description")
    orden: Optional[int] = Field(None, description="Display order", ge=0)
    activo: Optional[bool] = Field(None, description="Active status")
    imagen_path: Optional[str] = Field(None, description="Image path", max_length=255)


class CategoriaResponse(CategoriaBase):
    """Schema for categoria responses."""
    id_categoria: int = Field(..., description="Category ID")
    fecha_creacion: Optional[datetime] = Field(None, description="Creation timestamp")
    fecha_modificacon: Optional[datetime] = Field(None, description="Last modification timestamp")

    class Config:
        from_attributes = True


class CategoriaSummary(BaseModel):
    """Schema for categoria summary (minimal data)."""
    id_categoria: int = Field(..., description="Category ID")
    nombre: str = Field(..., description="Category name")
    orden: int = Field(..., description="Display order")

    class Config:
        from_attributes = True