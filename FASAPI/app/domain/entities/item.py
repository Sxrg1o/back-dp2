"""Item base domain entity for menu management."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Set
from uuid import UUID

from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem


@dataclass
class Item:
    """Base domain entity for menu items."""
    
    id: UUID
    nombre: str
    descripcion: Optional[str]
    precio: Precio
    informacion_nutricional: InformacionNutricional
    tiempo_preparacion: int  # in minutes
    stock_actual: int
    stock_minimo: int
    etiquetas: Set[EtiquetaItem]
    activo: bool
    created_at: datetime
    updated_at: datetime
    version: int
    
    def __post_init__(self):
        """Validate item data after initialization."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("Item name cannot be empty")
        
        if self.tiempo_preparacion < 0:
            raise ValueError("Preparation time cannot be negative")
        
        if self.stock_actual < 0:
            raise ValueError("Current stock cannot be negative")
        
        if self.stock_minimo < 0:
            raise ValueError("Minimum stock cannot be negative")
        
        if not isinstance(self.etiquetas, set):
            raise ValueError("Etiquetas must be a set")
    
    def verificar_stock(self) -> bool:
        """Check if item has sufficient stock."""
        return self.stock_actual > 0 and self.activo
    
    def calcular_calorias(self) -> int:
        """Calculate calories from nutritional information."""
        return self.informacion_nutricional.calorias
    
    def is_disponible(self) -> bool:
        """Check if item is available for ordering."""
        return (
            self.activo and 
            self.stock_actual > 0 and 
            self.stock_actual > self.stock_minimo
        )
    
    def reducir_stock(self, cantidad: int) -> None:
        """Reduce stock by specified amount."""
        if cantidad <= 0:
            raise ValueError("Quantity must be positive")
        
        if cantidad > self.stock_actual:
            raise ValueError("Insufficient stock available")
        
        self.stock_actual -= cantidad
        self.updated_at = datetime.utcnow()
    
    def aumentar_stock(self, cantidad: int) -> None:
        """Increase stock by specified amount."""
        if cantidad <= 0:
            raise ValueError("Quantity must be positive")
        
        self.stock_actual += cantidad
        self.updated_at = datetime.utcnow()
    
    def actualizar_precio(self, nuevo_precio: Precio) -> None:
        """Update item price."""
        self.precio = nuevo_precio
        self.updated_at = datetime.utcnow()
    
    def agregar_etiqueta(self, etiqueta: EtiquetaItem) -> None:
        """Add a label to the item."""
        self.etiquetas.add(etiqueta)
        self.updated_at = datetime.utcnow()
    
    def remover_etiqueta(self, etiqueta: EtiquetaItem) -> None:
        """Remove a label from the item."""
        self.etiquetas.discard(etiqueta)
        self.updated_at = datetime.utcnow()
    
    def tiene_etiqueta(self, etiqueta: EtiquetaItem) -> bool:
        """Check if item has specific label."""
        return etiqueta in self.etiquetas
    
    def activar(self) -> None:
        """Activate the item."""
        self.activo = True
        self.updated_at = datetime.utcnow()
    
    def desactivar(self) -> None:
        """Deactivate the item."""
        self.activo = False
        self.updated_at = datetime.utcnow()
    
    def necesita_restock(self) -> bool:
        """Check if item needs restocking."""
        return self.stock_actual <= self.stock_minimo
    
    def es_vegano(self) -> bool:
        """Check if item is vegan."""
        return EtiquetaItem.VEGANO in self.etiquetas
    
    def es_sin_gluten(self) -> bool:
        """Check if item is gluten-free."""
        return EtiquetaItem.SIN_GLUTEN in self.etiquetas
    
    def __str__(self) -> str:
        return f"{self.nombre} - {self.precio}"