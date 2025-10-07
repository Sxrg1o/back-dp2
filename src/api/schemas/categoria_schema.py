"""
Pydantic schemas for Categoria (Category) entities.
"""

from typing import Optional, ClassVar, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CategoriaBase(BaseModel):
    """Base schema for Categoria."""

    nombre: str = Field(description="Category name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(
        default=None, description="Category description"
    )


class CategoriaCreate(CategoriaBase):
    """Schema for creating a new categoria."""

    pass


class CategoriaUpdate(BaseModel):
    """Schema for updating categoria."""

    nombre: Optional[str] = Field(
        default=None, description="Category name", min_length=1, max_length=100
    )
    descripcion: Optional[str] = Field(
        default=None, description="Category description"
    )
    activo: Optional[bool] = Field(
        default=None, description="Indicates if the category is active"
    )


class CategoriaResponse(CategoriaBase):
    """Schema for categoria responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Category ID")
    activo: bool = Field(description="Indicates if the category is active")
    fecha_creacion: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    fecha_modificacion: Optional[datetime] = Field(
        default=None, description="Last modification timestamp"
    )
    
    
class CategoriaSummary(BaseModel):
    """Schema for summarized categoria information in lists."""
    
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
    
    id: UUID = Field(description="Category ID")
    nombre: str = Field(description="Category name")
    activo: bool = Field(description="Indicates if the category is active")


class CategoriaList(BaseModel):
    """Schema for paginated list of categorias."""
    
    items: List[CategoriaSummary]
    total: int = Field(description="Total number of categorias")
