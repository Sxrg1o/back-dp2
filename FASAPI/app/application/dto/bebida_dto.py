"""Bebida DTOs for menu application layer."""

from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.application.dto.item_dto import InformacionNutricionalDTO


class CreateBebidaDTO(BaseModel):
    """DTO for creating beverages."""
    
    # Base Item fields
    nombre: str = Field(..., min_length=1, max_length=200, description="Beverage name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Beverage description")
    precio: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Beverage price (positive)")
    informacion_nutricional: InformacionNutricionalDTO = Field(..., description="Nutritional information")
    tiempo_preparacion: int = Field(..., ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: int = Field(..., ge=0, description="Current stock (non-negative)")
    stock_minimo: int = Field(..., ge=0, description="Minimum stock (non-negative)")
    etiquetas: Set[EtiquetaItem] = Field(default_factory=set, description="Item labels")
    activo: bool = Field(True, description="Whether beverage is active")
    
    # Bebida-specific fields
    volumen: float = Field(..., gt=0, description="Volume in milliliters (positive)")
    contenido_alcohol: float = Field(..., ge=0, le=100, description="Alcohol content percentage (0-100)")
    temperatura_servicio: Optional[str] = Field(None, pattern="^(fria|caliente|ambiente)$", description="Service temperature")
    tipo_bebida: Optional[str] = Field(None, max_length=100, description="Beverage type")
    marca: Optional[str] = Field(None, max_length=200, description="Brand name")
    origen: Optional[str] = Field(None, max_length=200, description="Origin")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate beverage name is not empty."""
        if not v or not v.strip():
            raise ValueError("Beverage name cannot be empty")
        return v.strip()
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('contenido_alcohol')
    def validate_contenido_alcohol(cls, v):
        """Validate alcohol content is between 0 and 100."""
        if v < 0 or v > 100:
            raise ValueError("Alcohol content must be between 0 and 100 percent")
        return v
    
    @validator('temperatura_servicio')
    def validate_temperatura_servicio(cls, v):
        """Validate service temperature."""
        if v is not None and v not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Service temperature must be 'fria', 'caliente', or 'ambiente'")
        return v
    
    @validator('tipo_bebida')
    def validate_tipo_bebida(cls, v):
        """Validate beverage type if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('marca')
    def validate_marca(cls, v):
        """Validate brand name if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('origen')
    def validate_origen(cls, v):
        """Validate origin if provided."""
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


class UpdateBebidaDTO(BaseModel):
    """DTO for updating beverages."""
    
    # Base Item fields
    nombre: Optional[str] = Field(None, min_length=1, max_length=200, description="Beverage name")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Beverage description")
    precio: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2, description="Beverage price (positive)")
    informacion_nutricional: Optional[InformacionNutricionalDTO] = Field(None, description="Nutritional information")
    tiempo_preparacion: Optional[int] = Field(None, ge=0, description="Preparation time in minutes (non-negative)")
    stock_actual: Optional[int] = Field(None, ge=0, description="Current stock (non-negative)")
    stock_minimo: Optional[int] = Field(None, ge=0, description="Minimum stock (non-negative)")
    etiquetas: Optional[Set[EtiquetaItem]] = Field(None, description="Item labels")
    activo: Optional[bool] = Field(None, description="Whether beverage is active")
    
    # Bebida-specific fields
    volumen: Optional[float] = Field(None, gt=0, description="Volume in milliliters (positive)")
    contenido_alcohol: Optional[float] = Field(None, ge=0, le=100, description="Alcohol content percentage (0-100)")
    temperatura_servicio: Optional[str] = Field(None, pattern="^(fria|caliente|ambiente)$", description="Service temperature")
    tipo_bebida: Optional[str] = Field(None, max_length=100, description="Beverage type")
    marca: Optional[str] = Field(None, max_length=200, description="Brand name")
    origen: Optional[str] = Field(None, max_length=200, description="Origin")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validate beverage name is not empty."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Beverage name cannot be empty")
        return v.strip() if v else v
    
    @validator('descripcion')
    def validate_descripcion(cls, v):
        """Validate description if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('contenido_alcohol')
    def validate_contenido_alcohol(cls, v):
        """Validate alcohol content is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Alcohol content must be between 0 and 100 percent")
        return v
    
    @validator('temperatura_servicio')
    def validate_temperatura_servicio(cls, v):
        """Validate service temperature."""
        if v is not None and v not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Service temperature must be 'fria', 'caliente', or 'ambiente'")
        return v
    
    @validator('tipo_bebida')
    def validate_tipo_bebida(cls, v):
        """Validate beverage type if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('marca')
    def validate_marca(cls, v):
        """Validate brand name if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('origen')
    def validate_origen(cls, v):
        """Validate origin if provided."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        use_enum_values = True


class BebidaResponseDTO(BaseModel):
    """DTO for beverage responses."""
    
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
    volumen: float
    contenido_alcohol: float
    temperatura_servicio: Optional[str]
    tipo_bebida: Optional[str]
    marca: Optional[str]
    origen: Optional[str]
    
    class Config:
        use_enum_values = True
        from_attributes = True