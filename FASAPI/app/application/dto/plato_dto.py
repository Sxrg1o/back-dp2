"""Plato DTOs for menu application layer."""

from decimal import Decimal
from typing import Dict, Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.application.dto.item_dto import InformacionNutricionalDTO


class RecetaIngredienteDTO(BaseModel):
    """DTO for recipe ingredients."""
    
    ingrediente_id: UUID = Field(..., description="Ingredient ID")
    cantidad: float = Field(..., gt=0, description="Required quantity (positive)")
    
    @validator('cantidad')
    def validate_cantidad(cls, v):
        """Validate ingredient quantity is positive."""
        if v <= 0:
            raise ValueError("Ingredient quantity must be positive")
        return v


class CreatePlatoDTO(BaseModel):
    """DTO for creating dishes."""
    
    # Base Item fields
    nombre: str = Field(..., min_length=1, max_length=200, description="Dish name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Dish description")
    precio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Dish price (positive)")
    informacion_nutricional: InformacionNutricionalDTO = Field(..., description="Nutritional information")
    tiempo_preparacion: int = Field(..., ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: int = Field(..., ge=0, description="Current stock (non-negative)")
    stock_minimo: int = Field(..., ge=0, description="Minimum stock (non-negative)")
    etiquetas: Set[EtiquetaItem] = Field(default_factory=set, description="Item labels")
    activo: bool = Field(True, description="Whether dish is active")
    
    # Plato-specific fields
    tipo_plato: EtiquetaPlato = Field(..., description="Dish type")
    receta: Dict[UUID, float] = Field(default_factory=dict, description="Recipe ingredients (ingredient_id -> quantity)")
    instrucciones: Optional[str] = Field(None, max_length=2000, description="Cooking instructions")
    porciones: int = Field(1, gt=0, description="Number of portions (positive)")
    dificultad: Optional[str] = Field(None, pattern="^(facil|medio|dificil)$", description="Difficulty level")
    chef_recomendado: Optional[str] = Field(None, max_length=200, description="Recommended chef")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate dish name is not empty."""
        if not v or not v.strip():
            raise ValueError("Dish name cannot be empty")
        return v.strip()
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('receta')
    def validate_receta(cls, v):
        """Validate recipe ingredients and quantities."""
        if v:
            for ingrediente_id, cantidad in v.items():
                if cantidad <= 0:
                    raise ValueError("Recipe quantities must be positive")
        return v
    
    @validator('instrucciones')
    def validate_instrucciones(cls, v):
        """Validate cooking instructions if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('dificultad')
    def validate_dificultad(cls, v):
        """Validate difficulty level."""
        if v is not None and v not in ["facil", "medio", "dificil"]:
            raise ValueError("Difficulty must be 'facil', 'medio', or 'dificil'")
        return v
    
    @validator('chef_recomendado')
    def validate_chef_recomendado(cls, v):
        """Validate recommended chef if provided."""
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


class UpdatePlatoDTO(BaseModel):
    """DTO for updating dishes."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, min_length=1, max_length=200, description="Dish name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Dish description")
    precio: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Dish price (positive)")
    informacion_nutricional: Optional[InformacionNutricionalDTO] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: Optional[int] = Field(None, ge=0, description="Current stock (non-negative)")
    stock_minimo: Optional[int] = Field(None, ge=0, description="Minimum stock (non-negative)")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether dish is active")
    
    # Plato-specific fields
    tipo_plato: Optional[EtiquetaPlato] = Field(None, description="Dish type")
    receta: Optional[Dict[UUID, float]] = Field(None, description="Recipe ingredients (ingredient_id -> quantity)")
    instrucciones: Optional[str] = Field(None, max_length=2000, description="Cooking instructions")
    porciones: Optional[int] = Field(None, gt=0, description="Number of portions (positive)")
    dificultad: Optional[str] = Field(None, pattern="^(facil|medio|dificil)$", description="Difficulty level")
    chef_recomendado: Optional[str] = Field(None, max_length=200, description="Recommended chef")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate dish name is not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Dish name cannot be empty")
        return v.strip() if v else v
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('receta')
    def validate_receta(cls, v):
        """Validate recipe ingredients and quantities."""
        if v:
            for ingrediente_id, cantidad in v.items():
                if cantidad <= 0:
                    raise ValueError("Recipe quantities must be positive")
        return v
    
    @validator('instrucciones')
    def validate_instrucciones(cls, v):
        """Validate cooking instructions if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('dificultad')
    def validate_dificultad(cls, v):
        """Validate difficulty level."""
        if v is not None and v not in ["facil", "medio", "dificil"]:
            raise ValueError("Difficulty must be 'facil', 'medio', or 'dificil'")
        return v
    
    @validator('chef_recomendado')
    def validate_chef_recomendado(cls, v):
        """Validate recommended chef if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        use_enum_values = True


class PlatoResponseDTO(BaseModel):
    """DTO for dish responses."""
    
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
    tipo_plato: EtiquetaPlato
    receta: Dict[UUID, float]
    instrucciones: Optional[str]
    porciones: int
    dificultad: Optional[str]
    chef_recomendado: Optional[str]
    
    class Config:
        use_enum_values = True
        from_attributes = True


class AgregarIngredienteRecetaDTO(BaseModel):
    """DTO for adding ingredient to recipe."""
    
    ingrediente_id: UUID = Field(..., description="Ingredient ID")
    cantidad: float = Field(..., gt=0, description="Required quantity (positive)")
    
    @validator('cantidad')
    def validate_cantidad(cls, v):
        """Validate ingredient quantity is positive."""
        if v <= 0:
            raise ValueError("Ingredient quantity must be positive")
        return v


class ActualizarIngredienteRecetaDTO(BaseModel):
    """DTO for updating ingredient quantity in recipe."""
    
    nueva_cantidad: float = Field(..., gt=0, description="New quantity (positive)")
    
    @validator('nueva_cantidad')
    def validate_nueva_cantidad(cls, v):
        """Validate new ingredient quantity is positive."""
        if v <= 0:
            raise ValueError("New ingredient quantity must be positive")
        return v