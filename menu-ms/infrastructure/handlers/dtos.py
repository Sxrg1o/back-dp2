"""
DTOs (Data Transfer Objects) para los endpoints del menú.
"""

from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from ...domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato


# DTOs para ítems
class ItemBaseDTO(BaseModel):
    """DTO base para ítems."""
    valor_nutricional: str = Field(default="", description="Información nutricional completa")
    precio: Decimal = Field(..., gt=0, description="Precio del ítem en el menú")
    tiempo_preparacion: Decimal = Field(default=0, ge=0, description="Tiempo promedio de preparación en minutos")
    comentarios: str = Field(default="", description="Notas adicionales sobre el ítem")
    receta: str = Field(default="", description="Receta asociada para preparación")
    disponible: bool = Field(default=True, description="Disponibilidad actual en carta")
    unidades_disponibles: int = Field(default=0, ge=0, description="Stock disponible del ítem")
    num_ingredientes: int = Field(default=0, ge=0, description="Número total de ingredientes")
    kcal: int = Field(default=0, ge=0, description="Calorías por porción")
    calorias: Decimal = Field(default=0, ge=0, description="Energía total en calorías")
    proteinas: Decimal = Field(default=0, ge=0, description="Contenido de proteínas en gramos")
    azucares: Decimal = Field(default=0, ge=0, description="Contenido de azúcares en gramos")
    descripcion: str = Field(..., min_length=1, description="Descripción detallada del ítem")
    etiquetas: List[EtiquetaItem] = Field(default=[], description="Lista de etiquetas del ítem")


class PlatoCreateDTO(ItemBaseDTO):
    """DTO para crear un plato."""
    peso: Decimal = Field(..., gt=0, description="Peso total del plato en gramos")
    tipo: EtiquetaPlato = Field(..., description="Clasificación del plato")


class PlatoUpdateDTO(ItemBaseDTO):
    """DTO para actualizar un plato."""
    peso: Decimal = Field(..., gt=0, description="Peso total del plato en gramos")
    tipo: EtiquetaPlato = Field(..., description="Clasificación del plato")


class PlatoResponseDTO(ItemBaseDTO):
    """DTO de respuesta para un plato."""
    id: int = Field(..., description="Identificador único del plato")
    peso: Decimal = Field(..., description="Peso total del plato en gramos")
    tipo: EtiquetaPlato = Field(..., description="Clasificación del plato")
    
    class Config:
        from_attributes = True


class BebidaCreateDTO(ItemBaseDTO):
    """DTO para crear una bebida."""
    litros: Decimal = Field(..., gt=0, description="Cantidad en litros del contenido")
    alcoholico: bool = Field(default=False, description="Indica si la bebida contiene alcohol")


class BebidaUpdateDTO(ItemBaseDTO):
    """DTO para actualizar una bebida."""
    litros: Decimal = Field(..., gt=0, description="Cantidad en litros del contenido")
    alcoholico: bool = Field(..., description="Indica si la bebida contiene alcohol")


class BebidaResponseDTO(ItemBaseDTO):
    """DTO de respuesta para una bebida."""
    id: int = Field(..., description="Identificador único de la bebida")
    litros: Decimal = Field(..., description="Cantidad en litros del contenido")
    alcoholico: bool = Field(..., description="Indica si la bebida contiene alcohol")
    
    class Config:
        from_attributes = True


class ItemResponseDTO(ItemBaseDTO):
    """DTO de respuesta genérico para un ítem."""
    id: int = Field(..., description="Identificador único del ítem")
    tipo: str = Field(..., description="Tipo del ítem (PLATO o BEBIDA)")
    
    class Config:
        from_attributes = True


class StockUpdateDTO(BaseModel):
    """DTO para actualizar el stock de un ítem."""
    unidades_disponibles: int = Field(..., ge=0, description="Nuevo stock disponible")


# DTOs para ingredientes
class IngredienteBaseDTO(BaseModel):
    """DTO base para ingredientes."""
    nombre: str = Field(..., min_length=1, description="Nombre del ingrediente")
    stock: Decimal = Field(default=0, ge=0, description="Cantidad disponible en inventario")
    peso: Decimal = Field(..., gt=0, description="Peso por unidad del ingrediente")
    tipo: EtiquetaIngrediente = Field(..., description="Clasificación del ingrediente")


class IngredienteCreateDTO(IngredienteBaseDTO):
    """DTO para crear un ingrediente."""
    pass


class IngredienteUpdateDTO(IngredienteBaseDTO):
    """DTO para actualizar un ingrediente."""
    pass


class IngredienteResponseDTO(IngredienteBaseDTO):
    """DTO de respuesta para un ingrediente."""
    id: int = Field(..., description="Identificador único del ingrediente")
    
    class Config:
        from_attributes = True


class IngredienteStockUpdateDTO(BaseModel):
    """DTO para actualizar el stock de un ingrediente."""
    stock: Decimal = Field(..., ge=0, description="Nuevo stock disponible")


# DTOs para búsquedas y filtros
class ItemSearchDTO(BaseModel):
    """DTO para búsqueda de ítems."""
    search_term: str = Field(..., min_length=1, description="Término de búsqueda")


class PriceRangeDTO(BaseModel):
    """DTO para filtro por rango de precios."""
    min_price: Decimal = Field(..., ge=0, description="Precio mínimo")
    max_price: Decimal = Field(..., ge=0, description="Precio máximo")


class VolumeRangeDTO(BaseModel):
    """DTO para filtro por rango de volumen."""
    min_volume: Decimal = Field(..., ge=0, description="Volumen mínimo en litros")
    max_volume: Decimal = Field(..., ge=0, description="Volumen máximo en litros")


class LowStockDTO(BaseModel):
    """DTO para filtro de stock bajo."""
    threshold: Decimal = Field(default=10.0, ge=0, description="Umbral de stock bajo")


# DTOs de respuesta genéricos
class MessageResponseDTO(BaseModel):
    """DTO de respuesta genérico con mensaje."""
    message: str = Field(..., description="Mensaje de respuesta")
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")


class ErrorResponseDTO(BaseModel):
    """DTO de respuesta de error."""
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalle adicional del error")
    success: bool = Field(default=False, description="Indica que la operación falló")
