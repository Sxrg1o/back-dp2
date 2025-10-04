"""
Pydantic schemas for allergen-related operations.
"""

from typing import Optional
from pydantic import BaseModel, Field

from app.shared.enums.alergeno_enums import NivelRiesgo, NivelPresencia


class AlergenoBase(BaseModel):
    """Base allergen schema."""

    nombre: str = Field(..., min_length=2, max_length=100, description="Allergen name")
    descripcion: Optional[str] = Field(None, max_length=500, description="Allergen description")
    icono: Optional[str] = Field(None, max_length=100, description="Icon filename or URL")
    nivel_riesgo: NivelRiesgo = Field(NivelRiesgo.MEDIO, description="Risk level")
    activo: bool = Field(True, description="Active status")
    orden: int = Field(0, ge=0, description="Display order")


class AlergenoCreate(AlergenoBase):
    """Schema for creating an allergen."""
    pass


class AlergenoUpdate(BaseModel):
    """Schema for updating an allergen."""

    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    icono: Optional[str] = Field(None, max_length=100)
    nivel_riesgo: Optional[NivelRiesgo] = None
    activo: Optional[bool] = None
    orden: Optional[int] = Field(None, ge=0)


class AlergenoResponse(AlergenoBase):
    """Schema for allergen response."""

    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ProductoAlergenoResponse(BaseModel):
    """Schema for product-allergen association response."""

    alergeno: AlergenoResponse
    nivel_presencia: NivelPresencia
    notas: Optional[str] = None
    activo: bool

    class Config:
        from_attributes = True