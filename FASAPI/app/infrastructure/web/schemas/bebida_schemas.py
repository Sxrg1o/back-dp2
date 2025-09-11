"""
Bebida API schemas for web layer.
"""
from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseEntitySchema
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.web.schemas.menu_schemas import InformacionNutricionalSchema, ItemBaseSchema


class BebidaBaseSchema(ItemBaseSchema):
    """Base schema for beverages."""
    
    volumen: float = Field(..., description="Volume in milliliters")
    contenido_alcohol: float = Field(..., description="Alcohol content percentage")
    temperatura_servicio: Optional[str] = Field(None, description="Service temperature")
    tipo_bebida: Optional[str] = Field(None, description="Beverage type")
    marca: Optional[str] = Field(None, description="Brand name")
    origen: Optional[str] = Field(None, description="Origin")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class BebidaCreateSchema(BebidaBaseSchema):
    """Schema for creating beverages."""
    pass


class BebidaUpdateSchema(BaseModel):
    """Schema for updating beverages."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, description="Beverage name")
    descripcion: Optional[str] = Field(None, description="Beverage description")
    precio: Optional[Decimal] = Field(None, description="Beverage price")
    informacion_nutricional: Optional[InformacionNutricionalSchema] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, description="Preparation time in minutes")
    stock_actual: Optional[int] = Field(None, description="Current stock")
    stock_minimo: Optional[int] = Field(None, description="Minimum stock")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether beverage is active")
    
    # Bebida-specific fields
    volumen: Optional[float] = Field(None, description="Volume in milliliters")
    contenido_alcohol: Optional[float] = Field(None, description="Alcohol content percentage")
    temperatura_servicio: Optional[str] = Field(None, description="Service temperature")
    tipo_bebida: Optional[str] = Field(None, description="Beverage type")
    marca: Optional[str] = Field(None, description="Brand name")
    origen: Optional[str] = Field(None, description="Origin")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class BebidaResponseSchema(BebidaBaseSchema, BaseEntitySchema):
    """Schema for beverage responses."""
    pass


class BebidaListResponseSchema(BaseModel):
    """Schema for beverage list responses."""
    
    id: UUID
    nombre: str
    precio: Decimal
    volumen: float
    contenido_alcohol: float
    stock_actual: int
    activo: bool
    
    class Config:
        from_attributes = True
        use_enum_values = True