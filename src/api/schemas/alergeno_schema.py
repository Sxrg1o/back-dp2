"""
Pydantic schemas for Alergeno (Allergen) entities.
"""

from typing import Optional, ClassVar, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from src.core.enums.alergeno_enums import NivelRiesgo


class AlergenoBase(BaseModel):
    """Base schema for Alergeno."""

    nombre: str = Field(description="Allergen name", min_length=1, max_length=100)
    descripcion: Optional[str] = Field(
        default=None, description="Allergen description"
    )
    icono: Optional[str] = Field(
        default=None, description="Icon or emoji for UI", max_length=50
    )
    nivel_riesgo: NivelRiesgo = Field(
        default=NivelRiesgo.MEDIO, description="Risk level of the allergen"
    )


class AlergenoCreate(AlergenoBase):
    """Schema for creating a new alergeno."""

    pass


class AlergenoUpdate(BaseModel):
    """Schema for updating alergeno."""

    nombre: Optional[str] = Field(
        default=None, description="Allergen name", min_length=1, max_length=100
    )
    descripcion: Optional[str] = Field(
        default=None, description="Allergen description"
    )
    icono: Optional[str] = Field(
        default=None, description="Icon or emoji for UI", max_length=50
    )
    nivel_riesgo: Optional[NivelRiesgo] = Field(
        default=None, description="Risk level of the allergen"
    )


class AlergenoResponse(AlergenoBase):
    """Schema for alergeno responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Allergen ID")
    activo: bool = Field(description="Indicates if the allergen is active")
    fecha_creacion: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    fecha_modificacion: Optional[datetime] = Field(
        default=None, description="Last modification timestamp"
    )


class AlergenoSummary(BaseModel):
    """Schema for summarized alergeno information in lists."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Allergen ID")
    nombre: str = Field(description="Allergen name")
    nivel_riesgo: NivelRiesgo = Field(description="Risk level of the allergen")
    activo: bool = Field(description="Indicates if the allergen is active")


class AlergenoList(BaseModel):
    """Schema for paginated list of allergens."""

    items: List[AlergenoSummary]
    total: int = Field(description="Total number of allergens")
