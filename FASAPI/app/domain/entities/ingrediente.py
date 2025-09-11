"""Ingrediente domain entity for menu management."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Set
from uuid import UUID

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente


@dataclass
class Ingrediente(Item):
    """Domain entity for ingredients."""
    
    tipo: EtiquetaIngrediente
    peso_unitario: float  # in grams
    unidad_medida: str    # e.g., "gramos", "litros", "unidades"
    fecha_vencimiento: Optional[datetime] = None
    proveedor: Optional[str] = None
    
    def __post_init__(self):
        """Validate ingredient data after initialization."""
        super().__post_init__()
        
        if self.peso_unitario <= 0:
            raise ValueError("Unit weight must be positive")
        
        if not self.unidad_medida or not self.unidad_medida.strip():
            raise ValueError("Unit of measure cannot be empty")
        
        if self.fecha_vencimiento and self.fecha_vencimiento <= datetime.utcnow():
            raise ValueError("Expiration date must be in the future")
    
    def esta_vencido(self) -> bool:
        """Check if ingredient is expired."""
        if not self.fecha_vencimiento:
            return False
        return datetime.utcnow() > self.fecha_vencimiento
    
    def dias_hasta_vencimiento(self) -> Optional[int]:
        """Calculate days until expiration."""
        if not self.fecha_vencimiento:
            return None
        
        delta = self.fecha_vencimiento - datetime.utcnow()
        return max(0, delta.days)
    
    def esta_proximo_a_vencer(self, dias_limite: int = 3) -> bool:
        """Check if ingredient is close to expiration."""
        dias = self.dias_hasta_vencimiento()
        return dias is not None and dias <= dias_limite
    
    def calcular_peso_total(self) -> float:
        """Calculate total weight based on stock and unit weight."""
        return self.stock_actual * self.peso_unitario
    
    def es_verdura(self) -> bool:
        """Check if ingredient is a vegetable."""
        return self.tipo == EtiquetaIngrediente.VERDURA
    
    def es_carne(self) -> bool:
        """Check if ingredient is meat."""
        return self.tipo == EtiquetaIngrediente.CARNE
    
    def es_fruta(self) -> bool:
        """Check if ingredient is fruit."""
        return self.tipo == EtiquetaIngrediente.FRUTA
    
    def is_disponible(self) -> bool:
        """Override availability check to include expiration."""
        base_disponible = super().is_disponible()
        return base_disponible and not self.esta_vencido()
    
    def actualizar_fecha_vencimiento(self, nueva_fecha: datetime) -> None:
        """Update expiration date."""
        if nueva_fecha <= datetime.utcnow():
            raise ValueError("New expiration date must be in the future")
        
        self.fecha_vencimiento = nueva_fecha
        self.updated_at = datetime.utcnow()
    
    def cambiar_proveedor(self, nuevo_proveedor: str) -> None:
        """Change ingredient supplier."""
        if not nuevo_proveedor or not nuevo_proveedor.strip():
            raise ValueError("Supplier name cannot be empty")
        
        self.proveedor = nuevo_proveedor.strip()
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tipo.value}) - {self.peso_unitario}g - {self.precio}"