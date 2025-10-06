"""
Pydantic schemas for product-related operations.
"""

from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, validator

from src.api.schemas.categoria_schema import CategoriaResponse
from src.api.schemas.alergeno_schema import AlergenoResponse


class ProductoBase(BaseModel):
    """Base product schema."""

    nombre: str = Field(..., min_length=2, max_length=200, description="Product name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Product description")
    precio_base: Decimal = Field(..., ge=0, description="Base price")
    imagen_path: Optional[str] = Field(None, max_length=255, description="Image path")
    imagen_alt_text: Optional[str] = Field(None, max_length=255, description="Image alt text")
    disponible: bool = Field(True, description="Availability status")
    destacado: bool = Field(False, description="Featured status")

    @validator("precio_base")
    def validate_price(cls, v):
        """Validate price format."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        if v > Decimal("999999.99"):
            raise ValueError("Price too high")
        # Check decimal places
        if v.as_tuple().exponent < -2:
            raise ValueError("Price cannot have more than 2 decimal places")
        return v


class ProductoCreate(ProductoBase):
    """Schema for creating a product."""

    id_categoria: int = Field(..., description="Category ID")


class ProductoUpdate(BaseModel):
    """Schema for updating a product."""

    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    precio_base: Optional[Decimal] = Field(None, ge=0)
    id_categoria: Optional[int] = None
    imagen_path: Optional[str] = Field(None, max_length=255)
    imagen_alt_text: Optional[str] = Field(None, max_length=255)
    disponible: Optional[bool] = None
    destacado: Optional[bool] = None

    @validator("precio_base")
    def validate_price(cls, v):
        """Validate price format."""
        if v is not None:
            if v < 0:
                raise ValueError("Price cannot be negative")
            if v > Decimal("999999.99"):
                raise ValueError("Price too high")
            if v.as_tuple().exponent < -2:
                raise ValueError("Price cannot have more than 2 decimal places")
        return v


class ProductoOpcionResponse(BaseModel):
    """Schema for product option response."""

    id: int
    nombre: str
    precio_adicional: Decimal
    activo: bool
    orden: int

    class Config:
        from_attributes = True


class ProductoResponse(ProductoBase):
    """Schema for product response."""

    id: int
    id_categoria: int
    categoria: Optional[CategoriaResponse] = None
    alergenos: List[AlergenoResponse] = []
    opciones: List[ProductoOpcionResponse] = []
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ProductoSearchParams(BaseModel):
    """Schema for product search parameters."""

    search_term: Optional[str] = Field(None, description="Search in name and description")
    category_id: Optional[int] = Field(None, description="Filter by category")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum price")
    available_only: bool = Field(True, description="Show only available products")
    featured_only: bool = Field(False, description="Show only featured products")

    @validator("max_price")
    def validate_price_range(cls, v, values):
        """Validate price range."""
        min_price = values.get("min_price")
        if v is not None and min_price is not None and v < min_price:
            raise ValueError("Maximum price must be greater than minimum price")
        return v


class ProductoPriceCalculation(BaseModel):
    """Schema for product price calculation."""

    product_id: int
    selected_options: List[int] = []


class ProductoPriceResponse(BaseModel):
    """Schema for product price calculation response."""

    product_id: int
    base_price: Decimal
    options_price: Decimal
    final_price: Decimal
    selected_options: List[ProductoOpcionResponse]


class ProductoBulkPriceUpdate(BaseModel):
    """Schema for bulk price updates."""

    updates: List[dict] = Field(..., description="List of price updates")

    @validator("updates")
    def validate_updates(cls, v):
        """Validate update format."""
        if not v:
            raise ValueError("Updates list cannot be empty")

        for update in v:
            if "id" not in update or "precio_base" not in update:
                raise ValueError("Each update must have 'id' and 'precio_base'")

            try:
                price = Decimal(str(update["precio_base"]))
                if price < 0:
                    raise ValueError("Price cannot be negative")
            except (ValueError, TypeError):
                raise ValueError("Invalid price format")

        return v