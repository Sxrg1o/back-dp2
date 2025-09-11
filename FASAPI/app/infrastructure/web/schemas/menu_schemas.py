"""
Menu API schemas for web layer.
"""
from decimal import Decimal
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseEntitySchema, BaseSchema
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato


class InformacionNutricionalSchema(BaseModel):
    """Schema for nutritional information."""
    
    calorias: int = Field(..., ge=0, description="Calories")
    proteinas: float = Field(..., ge=0, description="Proteins in grams")
    azucares: float = Field(..., ge=0, description="Sugars in grams")
    grasas: Optional[float] = Field(None, ge=0, description="Fats in grams")
    carbohidratos: Optional[float] = Field(None, ge=0, description="Carbohydrates in grams")
    fibra: Optional[float] = Field(None, ge=0, description="Fiber in grams")
    sodio: Optional[float] = Field(None, ge=0, description="Sodium in milligrams")
    
    class Config:
        from_attributes = True


class ItemBaseSchema(BaseModel):
    """Base schema for menu items."""
    
    nombre: str = Field(..., description="Item name")
    descripcion: Optional[str] = Field(None, description="Item description")
    precio: Decimal = Field(..., description="Item price")
    informacion_nutricional: InformacionNutricionalSchema = Field(..., description="Nutritional information")
    tiempo_preparacion: int = Field(..., description="Preparation time in minutes")
    stock_actual: int = Field(..., description="Current stock")
    stock_minimo: int = Field(..., description="Minimum stock")
    etiquetas: Set[EtiquetaItem] = Field(default_factory=set, description="Item labels")
    activo: bool = Field(..., description="Whether item is active")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class ItemCreateSchema(ItemBaseSchema):
    """Schema for creating menu items."""
    pass


class ItemUpdateSchema(BaseModel):
    """Schema for updating menu items."""
    
    nombre: Optional[str] = Field(None, description="Item name")
    descripcion: Optional[str] = Field(None, description="Item description")
    precio: Optional[Decimal] = Field(None, description="Item price")
    informacion_nutricional: Optional[InformacionNutricionalSchema] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, description="Preparation time in minutes")
    stock_actual: Optional[int] = Field(None, description="Current stock")
    stock_minimo: Optional[int] = Field(None, description="Minimum stock")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether item is active")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class ItemResponseSchema(ItemBaseSchema, BaseEntitySchema):
    """Schema for item responses."""
    pass


class ItemListResponseSchema(BaseModel):
    """Schema for item list responses."""
    
    id: UUID
    nombre: str
    precio: Decimal
    stock_actual: int
    activo: bool
    etiquetas: Set[EtiquetaItem]
    
    class Config:
        from_attributes = True
        use_enum_values = True