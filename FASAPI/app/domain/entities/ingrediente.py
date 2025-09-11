"""Ingrediente domain entity for menu management."""

from dataclasses import dataclass
from datetime import datetime, UTC
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
        # Convert etiquetas to set if it's a list (before calling parent validation)
        if isinstance(self.etiquetas, list):
            self.etiquetas = set(self.etiquetas)
        
        super().__post_init__()
        
        if self.peso_unitario <= 0:
            raise ValueError("Unit weight must be positive")
        
        if not self.unidad_medida or not self.unidad_medida.strip():
            raise ValueError("Unit of measure cannot be empty")
        
        if self.fecha_vencimiento:
            # Handle both naive and aware datetimes
            now = datetime.now(UTC)
            if self.fecha_vencimiento.tzinfo is None:
                # If fecha_vencimiento is naive, compare with naive datetime
                if self.fecha_vencimiento <= datetime.now():
                    raise ValueError("Expiration date must be in the future")
            else:
                # If fecha_vencimiento is aware, compare with aware datetime
                if self.fecha_vencimiento <= now:
                    raise ValueError("Expiration date must be in the future")
    
    def esta_vencido(self) -> bool:
        """Check if ingredient is expired."""
        if not self.fecha_vencimiento:
            return False
        # Handle both naive and aware datetimes
        if self.fecha_vencimiento.tzinfo is None:
            return datetime.now() > self.fecha_vencimiento
        else:
            return datetime.now(UTC) > self.fecha_vencimiento
    
    def dias_hasta_vencimiento(self) -> Optional[int]:
        """Calculate days until expiration."""
        if not self.fecha_vencimiento:
            return None
        
        # Handle both naive and aware datetimes
        if self.fecha_vencimiento.tzinfo is None:
            delta = self.fecha_vencimiento - datetime.now()
        else:
            delta = self.fecha_vencimiento - datetime.now(UTC)
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
        # Handle both naive and aware datetimes
        if nueva_fecha.tzinfo is None:
            if nueva_fecha <= datetime.now():
                raise ValueError("New expiration date must be in the future")
        else:
            if nueva_fecha <= datetime.now(UTC):
                raise ValueError("New expiration date must be in the future")
        
        self.fecha_vencimiento = nueva_fecha
        self.updated_at = datetime.now(UTC)
    
    def cambiar_proveedor(self, nuevo_proveedor: str) -> None:
        """Change ingredient supplier."""
        if not nuevo_proveedor or not nuevo_proveedor.strip():
            raise ValueError("Supplier name cannot be empty")
        
        self.proveedor = nuevo_proveedor.strip()
        self.updated_at = datetime.now(UTC)
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tipo.value}) - {self.peso_unitario}g - {self.precio}"