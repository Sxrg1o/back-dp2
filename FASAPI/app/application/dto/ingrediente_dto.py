"""Ingrediente DTOs for menu application layer."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.application.dto.item_dto import InformacionNutricionalDTO


class CreateIngredienteDTO(BaseModel):
    """DTO for creating ingredients."""
    
    # Base Item fields
    nombre: str = Field(..., min_length=1, max_length=200, description="Ingredient name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Ingredient description")
    precio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Ingredient price (positive)")
    informacion_nutricional: InformacionNutricionalDTO = Field(..., description="Nutritional information")
    tiempo_preparacion: int = Field(..., ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: int = Field(..., ge=0, description="Current stock (non-negative)")
    stock_minimo: int = Field(..., ge=0, description="Minimum stock (non-negative)")
    etiquetas: Set[EtiquetaItem] = Field(default_factory=set, description="Item labels")
    activo: bool = Field(True, description="Whether ingredient is active")
    
    # Ingrediente-specific fields
    tipo: EtiquetaIngrediente = Field(..., description="Ingredient type")
    peso_unitario: float = Field(..., gt=0, description="Unit weight in grams (positive)")
    unidad_medida: str = Field(..., min_length=1, max_length=50, description="Unit of measure")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Expiration date")
    proveedor: Optional[str] = Field(None, max_length=200, description="Supplier name")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate ingredient name is not empty."""
        if not v or not v.strip():
            raise ValueError("Ingredient name cannot be empty")
        return v.strip()
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('unidad_medida')
    def validate_unidad_medida(cls, v):
        """Validate unit of measure is not empty."""
        if not v or not v.strip():
            raise ValueError("Unit of measure cannot be empty")
        return v.strip()
    
    @validator('fecha_vencimiento')
    def validate_fecha_vencimiento(cls, v):
        """Validate expiration date is in the future."""
        if v is not None and v <= datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
        return v
    
    @validator('proveedor')
    def validate_proveedor(cls, v):
        """Validate supplier name if provided."""
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


class UpdateIngredienteDTO(BaseModel):
    """DTO for updating ingredients."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, min_length=1, max_length=200, description="Ingredient name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Ingredient description")
    precio: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Ingredient price (positive)")
    informacion_nutricional: Optional[InformacionNutricionalDTO] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: Optional[int] = Field(None, ge=0, description="Current stock (non-negative)")
    stock_minimo: Optional[int] = Field(None, ge=0, description="Minimum stock (non-negative)")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether ingredient is active")
    
    # Ingrediente-specific fields
    tipo: Optional[EtiquetaIngrediente] = Field(None, description="Ingredient type")
    peso_unitario: Optional[float] = Field(None, gt=0, description="Unit weight in grams (positive)")
    unidad_medida: Optional[str] = Field(None, min_length=1, max_length=50, description="Unit of measure")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Expiration date")
    proveedor: Optional[str] = Field(None, max_length=200, description="Supplier name")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate ingredient name is not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Ingredient name cannot be empty")
        return v.strip() if v else v
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('unidad_medida')
    def validate_unidad_medida(cls, v):
        """Validate unit of measure is not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Unit of measure cannot be empty")
        return v.strip() if v else v
    
    @validator('fecha_vencimiento')
    def validate_fecha_vencimiento(cls, v):
        """Validate expiration date is in the future."""
        if v is not None and v <= datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
        return v
    
    @validator('proveedor')
    def validate_proveedor(cls, v):
        """Validate supplier name if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        use_enum_values = True


class IngredienteResponseDTO(BaseModel):
    """DTO for ingredient responses."""
    
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
    tipo: EtiquetaIngrediente
    peso_unitario: float
    unidad_medida: str
    fecha_vencimiento: Optional[datetime]
    proveedor: Optional[str]
    
    class Config:
        use_enum_values = True
        from_attributes = True


class StockUpdateDTO(BaseModel):
    """DTO for stock updates."""
    
    cantidad: int = Field(..., gt=0, description="Quantity to add or remove (positive)")
    operacion: str = Field(..., pattern="^(aumentar|reducir)$", description="Operation: 'aumentar' or 'reducir'")
    
    @validator('operacion')
    def validate_operacion(cls, v):
        """Validate operation type."""
        if v not in ["aumentar", "reducir"]:
            raise ValueError("Operation must be 'aumentar' or 'reducir'")
        return v