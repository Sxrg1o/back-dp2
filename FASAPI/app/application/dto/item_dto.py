"""Item DTOs for menu application layer."""

from decimal import Decimal
from typing import List, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.etiqueta_item import EtiquetaItem


class InformacionNutricionalDTO(BaseModel):
    """DTO for nutritional information."""
    
    calorias: int = Field(..., ge=0, description="Calories (non-negative)")
    proteinas: float = Field(..., ge=0, description="Proteins in grams (non-negative)")
    azucares: float = Field(..., ge=0, description="Sugars in grams (non-negative)")
    grasas: Optional[float] = Field(None, ge=0, description="Fats in grams (non-negative)")
    carbohidratos: Optional[float] = Field(None, ge=0, description="Carbohydrates in grams (non-negative)")
    fibra: Optional[float] = Field(None, ge=0, description="Fiber in grams (non-negative)")
    sodio: Optional[float] = Field(None, ge=0, description="Sodium in milligrams (non-negative)")
    
    @validator('calorias', 'proteinas', 'azucares', 'grasas', 'carbohidratos', 'fibra', 'sodio')
    def validate_nutritional_values(cls, v):
        """Validate nutritional values are non-negative."""
        if v is not None and v < 0:
            raise ValueError("Nutritional values cannot be negative")
        return v
    
    @validator('calorias')
    def validate_calorie_consistency(cls, v, values):
        """Validate calorie count consistency with macronutrients."""
        if 'proteinas' in values and 'grasas' in values and 'carbohidratos' in values:
            proteinas = values.get('proteinas', 0)
            grasas = values.get('grasas', 0) or 0
            carbohidratos = values.get('carbohidratos', 0) or 0
            
            # Rough estimate: 4 cal/g protein, 4 cal/g carbs, 9 cal/g fat
            estimated_calories = (proteinas * 4) + (carbohidratos * 4) + (grasas * 9)
            
            # Allow 20% variance for estimation errors
            if estimated_calories > 0 and abs(v - estimated_calories) > (estimated_calories * 0.2):
                raise ValueError("Calorie count doesn't match macronutrient breakdown")
        
        return v


class CreateItemDTO(BaseModel):
    """DTO for creating menu items."""
    
    nombre: str = Field(..., min_length=1, max_length=200, description="Item name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Item description")
    precio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Item price (positive)")
    informacion_nutricional: InformacionNutricionalDTO = Field(..., description="Nutritional information")
    tiempo_preparacion: int = Field(..., ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: int = Field(..., ge=0, description="Current stock (non-negative)")
    stock_minimo: int = Field(..., ge=0, description="Minimum stock (non-negative)")
    etiquetas: Set[EtiquetaItem] = Field(default_factory=set, description="Item labels")
    activo: bool = Field(True, description="Whether item is active")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate item name is not empty."""
        if not v or not v.strip():
            raise ValueError("Item name cannot be empty")
        return v.strip()
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('stock_minimo')
    def validate_stock_minimo(cls, v, values):
        """Validate minimum stock is not greater than current stock."""
        if 'stock_actual' in values and v > values['stock_actual']:
            raise ValueError("Minimum stock cannot be greater than current stock")
        return v
    
    class Config:
        use_enum_values = True


class UpdateItemDTO(BaseModel):
    """DTO for updating menu items."""
    
    nombre: Optional[str] = Field(None, min_length=1, max_length=200, description="Item name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Item description")
    precio: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Item price (positive)")
    informacion_nutricional: Optional[InformacionNutricionalDTO] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: Optional[int] = Field(None, ge=0, description="Current stock (non-negative)")
    stock_minimo: Optional[int] = Field(None, ge=0, description="Minimum stock (non-negative)")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether item is active")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate item name is not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Item name cannot be empty")
        return v.strip() if v else v
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        use_enum_values = True


class ItemResponseDTO(BaseModel):
    """DTO for item responses."""
    
    id: UUID
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    informacion_nutricional: InformacionNutricionalDTO
    tiempo_preparacion: int
    stock_actual: int
    stock_minimo: int
    etiquetas: Set[EtiquetaItem]
    activo: bool
    
    class Config:
        use_enum_values = True
        from_attributes = True