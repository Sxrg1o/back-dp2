"""
Pydantic schemas for Producto (Product) entities.
"""

from typing import Optional, ClassVar, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class ProductoBase(BaseModel):
    """Base schema for Producto."""

    nombre: str = Field(description="Product name", min_length=1, max_length=255)
    descripcion: Optional[str] = Field(
        default=None, description="Product description"
    )
    precio_base: Decimal = Field(description="Base price", gt=0)
    imagen_path: Optional[str] = Field(
        default=None, description="Product image path", max_length=255
    )
    imagen_alt_text: Optional[str] = Field(
        default=None, description="Image alt text", max_length=255
    )


class ProductoCreate(ProductoBase):
    """Schema for creating a new producto."""

    id_categoria: UUID = Field(description="Category ID")


class ProductoUpdate(BaseModel):
    """Schema for updating producto."""

    nombre: Optional[str] = Field(
        default=None, description="Product name", min_length=1, max_length=255
    )
    descripcion: Optional[str] = Field(
        default=None, description="Product description"
    )
    precio_base: Optional[Decimal] = Field(
        default=None, description="Base price", gt=0
    )
    imagen_path: Optional[str] = Field(
        default=None, description="Product image path", max_length=255
    )
    imagen_alt_text: Optional[str] = Field(
        default=None, description="Image alt text", max_length=255
    )
    id_categoria: Optional[UUID] = Field(
        default=None, description="Category ID"
    )
    disponible: Optional[bool] = Field(
        default=None, description="Product availability"
    )
    destacado: Optional[bool] = Field(
        default=None, description="Featured product"
    )


class ProductoResponse(ProductoBase):
    """Schema for producto responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: UUID = Field(description="Product ID")
    id_categoria: UUID = Field(description="Category ID")
    disponible: bool = Field(description="Indicates if the product is available")
    destacado: bool = Field(description="Indicates if the product is featured")
    fecha_creacion: Optional[datetime] = Field(
        default=None, description="Creation timestamp"
    )
    fecha_modificacion: Optional[datetime] = Field(
        default=None, description="Last modification timestamp"
    )
    
    
class ProductoSummary(BaseModel):
    """Schema for summarized producto information in lists."""
    
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
    
    id: UUID = Field(description="Product ID")
    nombre: str = Field(description="Product name")
    precio_base: Decimal = Field(description="Base price")
    disponible: bool = Field(description="Indicates if the product is available")


class ProductoList(BaseModel):
    """Schema for paginated list of products."""
    
    items: List[ProductoSummary]
    total: int = Field(description="Total number of products")

