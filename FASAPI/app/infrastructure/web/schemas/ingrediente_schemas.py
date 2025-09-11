"""
Ingrediente API schemas for web layer.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseEntitySchema
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.infrastructure.web.schemas.menu_schemas import InformacionNutricionalSchema, ItemBaseSchema


class IngredienteBaseSchema(ItemBaseSchema):
    """Base schema for ingredients."""
    
    tipo: EtiquetaIngrediente = Field(..., description="Ingredient type")
    peso_unitario: float = Field(..., description="Unit weight in grams")
    unidad_medida: str = Field(..., description="Unit of measure")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Expiration date")
    proveedor: Optional[str] = Field(None, description="Supplier name")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class IngredienteCreateSchema(IngredienteBaseSchema):
    """Schema for creating ingredients."""
    pass


class IngredienteUpdateSchema(BaseModel):
    """Schema for updating ingredients."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, description="Ingredient name")
    descripcion: Optional[str] = Field(None, description="Ingredient description")
    precio: Optional[Decimal] = Field(None, description="Ingredient price")
    informacion_nutricional: Optional[InformacionNutricionalSchema] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, description="Preparation time in minutes")
    stock_actual: Optional[int] = Field(None, description="Current stock")
    stock_minimo: Optional[int] = Field(None, description="Minimum stock")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether ingredient is active")
    
    # Ingrediente-specific fields
    tipo: Optional[EtiquetaIngrediente] = Field(None, description="Ingredient type")
    peso_unitario: Optional[float] = Field(None, description="Unit weight in grams")
    unidad_medida: Optional[str] = Field(None, description="Unit of measure")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Expiration date")
    proveedor: Optional[str] = Field(None, description="Supplier name")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class IngredienteResponseSchema(IngredienteBaseSchema, BaseEntitySchema):
    """Schema for ingredient responses."""
    pass


class IngredienteListResponseSchema(BaseModel):
    """Schema for ingredient list responses."""
    
    id: UUID
    nombre: str
    tipo: EtiquetaIngrediente
    precio: Decimal
    stock_actual: int
    activo: bool
    fecha_vencimiento: Optional[datetime]
    
    class Config:
        from_attributes = True
        use_enum_values = True


class StockUpdateSchema(BaseModel):
    """Schema for stock updates."""
    
    cantidad: int = Field(..., gt=0, description="Quantity to add or remove")
    operacion: str = Field(..., pattern="^(aumentar|reducir)$", description="Operation: 'aumentar' or 'reducir'")
    
    class Config:
        from_attributes = True