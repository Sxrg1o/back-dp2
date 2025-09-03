"""
Mesa (Table) schemas.
"""
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseEntitySchema


class MesaBase(BaseModel):
    """Base mesa schema."""
    
    numero: int = Field(..., description="Table number")
    nombre: str = Field(..., max_length=100, description="Table name")
    capacidad: int = Field(..., gt=0, description="Table capacity")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Table location")
    descripcion: Optional[str] = Field(None, description="Table description")
    activa: bool = Field(True, description="Whether the table is active")


class MesaCreate(MesaBase):
    """Schema for creating a mesa."""
    pass


class MesaUpdate(BaseModel):
    """Schema for updating a mesa."""
    
    nombre: Optional[str] = Field(None, max_length=100)
    numero: Optional[int] = None
    capacidad: Optional[int] = Field(None, gt=0)
    ubicacion: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


class MesaResponse(MesaBase, BaseEntitySchema):
    """Schema for mesa response."""
    pass


class MesaListResponse(BaseModel):
    """Schema for mesa list item."""
    
    numero: int
    nombre: str
    capacidad: int
    ubicacion: Optional[str]
    activa: bool
    
    class Config:
        from_attributes = True