"""
Pydantic schemas for ProductoTipoOpcion (Product Type Option) entities.
"""

from typing import Optional, ClassVar, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class ProductoTipoOpcionBase(BaseModel):
    """Base schema for ProductoTipoOpcion."""

    nombre: str = Field(
        description="Option name (e.g., 'Sin ají', 'Ají suave', 'Con choclo')", 
        min_length=1, 
        max_length=100
    )
    precio_adicional: Decimal = Field(
        default=Decimal("0.00"),
        description="Additional price for this option",
        ge=0
    )
    activo: bool = Field(
        default=True,
        description="Indicates if the option is active"
    )
    orden: Optional[int] = Field(
        default=0,
        description="Display order for the option",
        ge=0
    )


class ProductoTipoOpcionCreate(ProductoTipoOpcionBase):
    """Schema for creating a new producto tipo opcion."""

    id_producto: UUID = Field(description="Product ID")
    id_tipo_opcion: UUID = Field(description="Option type ID")


class ProductoTipoOpcionUpdate(BaseModel):
    """Schema for updating producto tipo opcion."""

    nombre: Optional[str] = Field(
        default=None,
        description="Option name",
        min_length=1,
        max_length=100
    )
    precio_adicional: Optional[Decimal] = Field(
        default=None,
        description="Additional price for this option",
        ge=0
    )
    activo: Optional[bool] = Field(
        default=None,
        description="Indicates if the option is active"
    )
    orden: Optional[int] = Field(
        default=None,
        description="Display order for the option",
        ge=0
    )
    id_producto: Optional[UUID] = Field(
        default=None,
        description="Product ID"
    )
    id_tipo_opcion: Optional[UUID] = Field(
        default=None,
        description="Option type ID"
    )


class ProductoTipoOpcionResponse(ProductoTipoOpcionBase):
    """Schema for producto tipo opcion responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Product option ID")
    id_producto: UUID = Field(description="Product ID")
    id_tipo_opcion: UUID = Field(description="Option type ID")
    fecha_creacion: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    fecha_modificacion: Optional[datetime] = Field(
        default=None, description="Last modification timestamp"
    )


class ProductoTipoOpcionSummary(BaseModel):
    """Schema for summarized producto tipo opcion information in lists."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Product option ID")
    id_producto: UUID = Field(description="Product ID")
    id_tipo_opcion: UUID = Field(description="Option type ID")
    nombre: str = Field(description="Option name")
    precio_adicional: Decimal = Field(description="Additional price")
    activo: bool = Field(description="Indicates if the option is active")
    orden: int = Field(default=0, description="Display order for the option")


class ProductoTipoOpcionList(BaseModel):
    """Schema for paginated list of product type options."""

    items: List[ProductoTipoOpcionSummary]
    total: int = Field(description="Total number of product options")
