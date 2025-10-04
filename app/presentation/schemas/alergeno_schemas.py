"""
Pydantic schemas for Alergeno (Allergen) entities.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AlergenoBase(BaseModel):
    """Base schema for Alergeno."""
    nombre: str = Field(..., description="Allergen name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Allergen description")
    icono: Optional[str] = Field(None, description="Icon name or emoji", max_length=50)
    nivel_riesgo: str = Field(default="medio", description="Risk level: bajo, medio, alto, critico")
    activo: bool = Field(default=True, description="Active status")
    orden: int = Field(default=0, description="Display order", ge=0)


class AlergenoCreate(AlergenoBase):
    """Schema for creating a new alergeno."""
    pass


class AlergenoUpdate(BaseModel):
    """Schema for updating alergeno."""
    nombre: Optional[str] = Field(None, description="Allergen name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, description="Allergen description")
    icono: Optional[str] = Field(None, description="Icon name or emoji", max_length=50)
    nivel_riesgo: Optional[str] = Field(None, description="Risk level: bajo, medio, alto, critico")
    activo: Optional[bool] = Field(None, description="Active status")
    orden: Optional[int] = Field(None, description="Display order", ge=0)


class AlergenoResponse(AlergenoBase):
    """Schema for alergeno responses."""
    id_alergeno: int = Field(..., description="Allergen ID")
    fecha_creacion: Optional[datetime] = Field(None, description="Creation timestamp")
    fecha_modificacion: Optional[datetime] = Field(None, description="Last modification timestamp")

    class Config:
        from_attributes = True


class AlergenoSummary(BaseModel):
    """Schema for alergeno summary (minimal data)."""
    id_alergeno: int = Field(..., description="Allergen ID")
    nombre: str = Field(..., description="Allergen name")
    icono: Optional[str] = Field(None, description="Icon name or emoji")
    nivel_riesgo: str = Field(..., description="Risk level")

    class Config:
        from_attributes = True


class AlergenoOrdenUpdate(BaseModel):
    """Schema for updating alergeno order."""
    nuevo_orden: int = Field(..., description="New display order", ge=0)


class AlergenoFilter(BaseModel):
    """Schema for filtering alergenos."""
    nivel_riesgo: Optional[str] = Field(None, description="Filter by risk level")
    activo_only: bool = Field(default=False, description="Show only active allergens")
    order_by_orden: bool = Field(default=True, description="Order by display order")