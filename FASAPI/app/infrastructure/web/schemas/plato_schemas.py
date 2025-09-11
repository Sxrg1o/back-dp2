"""
Plato API schemas for web layer.
"""
from decimal import Decimal
from typing import Dict, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseEntitySchema
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.infrastructure.web.schemas.menu_schemas import InformacionNutricionalSchema, ItemBaseSchema


class PlatoBaseSchema(ItemBaseSchema):
    """Base schema for dishes."""
    
    tipo_plato: EtiquetaPlato = Field(..., description="Dish type")
    receta: Dict[UUID, float] = Field(default_factory=dict, description="Recipe ingredients")
    instrucciones: Optional[str] = Field(None, description="Cooking instructions")
    porciones: int = Field(1, description="Number of portions")
    dificultad: Optional[str] = Field(None, description="Difficulty level")
    chef_recomendado: Optional[str] = Field(None, description="Recommended chef")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class PlatoCreateSchema(PlatoBaseSchema):
    """Schema for creating dishes."""
    pass


class PlatoUpdateSchema(BaseModel):
    """Schema for updating dishes."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, description="Dish name")
    descripcion: Optional[str] = Field(None, description="Dish description")
    precio: Optional[Decimal] = Field(None, description="Dish price")
    informacion_nutricional: Optional[InformacionNutricionalSchema] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, description="Preparation time in minutes")
    stock_actual: Optional[int] = Field(None, description="Current stock")
    stock_minimo: Optional[int] = Field(None, description="Minimum stock")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether dish is active")
    
    # Plato-specific fields
    tipo_plato: Optional[EtiquetaPlato] = Field(None, description="Dish type")
    receta: Optional[Dict[UUID, float]] = Field(None, description="Recipe ingredients")
    instrucciones: Optional[str] = Field(None, description="Cooking instructions")
    porciones: Optional[int] = Field(None, description="Number of portions")
    dificultad: Optional[str] = Field(None, description="Difficulty level")
    chef_recomendado: Optional[str] = Field(None, description="Recommended chef")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class PlatoResponseSchema(PlatoBaseSchema, BaseEntitySchema):
    """Schema for dish responses."""
    pass


class PlatoListResponseSchema(BaseModel):
    """Schema for dish list responses."""
    
    id: UUID
    nombre: str
    tipo_plato: EtiquetaPlato
    precio: Decimal
    stock_actual: int
    activo: bool
    porciones: int
    
    class Config:
        from_attributes = True
        use_enum_values = True


class RecetaIngredienteSchema(BaseModel):
    """Schema for recipe ingredients."""
    
    ingrediente_id: UUID = Field(..., description="Ingredient ID")
    cantidad: float = Field(..., gt=0, description="Required quantity")
    
    class Config:
        from_attributes = True


class AgregarIngredienteRecetaSchema(BaseModel):
    """Schema for adding ingredient to recipe."""
    
    ingrediente_id: UUID = Field(..., description="Ingredient ID")
    cantidad: float = Field(..., gt=0, description="Required quantity")
    
    class Config:
        from_attributes = True


class ActualizarIngredienteRecetaSchema(BaseModel):
    """Schema for updating ingredient quantity in recipe."""
    
    nueva_cantidad: float = Field(..., gt=0, description="New quantity")
    
    class Config:
        from_attributes = True