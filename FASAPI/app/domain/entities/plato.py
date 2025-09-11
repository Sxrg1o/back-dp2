"""Plato domain entity for menu management."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set
from uuid import UUID

from app.domain.entities.item import Item
from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato


@dataclass
class Plato(Item):
    """Domain entity for dishes."""
    
    tipo_plato: EtiquetaPlato
    receta: Dict[UUID, float] = field(default_factory=dict)  # ingrediente_id -> cantidad_necesaria
    instrucciones: Optional[str] = None
    porciones: int = 1
    dificultad: Optional[str] = None  # "facil", "medio", "dificil"
    chef_recomendado: Optional[str] = None
    
    def __post_init__(self):
        """Validate dish data after initialization."""
        super().__post_init__()
        
        if self.porciones <= 0:
            raise ValueError("Portions must be positive")
        
        if self.dificultad and self.dificultad not in ["facil", "medio", "dificil"]:
            raise ValueError("Difficulty must be 'facil', 'medio', or 'dificil'")
        
        # Validate recipe quantities
        for ingrediente_id, cantidad in self.receta.items():
            if cantidad <= 0:
                raise ValueError("Recipe quantities must be positive")
    
    def agregar_ingrediente(self, ingrediente_id: UUID, cantidad: float) -> None:
        """Add ingredient to recipe."""
        if cantidad <= 0:
            raise ValueError("Ingredient quantity must be positive")
        
        self.receta[ingrediente_id] = cantidad
        self.updated_at = datetime.utcnow()
    
    def remover_ingrediente(self, ingrediente_id: UUID) -> None:
        """Remove ingredient from recipe."""
        if ingrediente_id in self.receta:
            del self.receta[ingrediente_id]
            self.updated_at = datetime.utcnow()
    
    def actualizar_cantidad_ingrediente(self, ingrediente_id: UUID, nueva_cantidad: float) -> None:
        """Update ingredient quantity in recipe."""
        if ingrediente_id not in self.receta:
            raise ValueError("Ingredient not found in recipe")
        
        if nueva_cantidad <= 0:
            raise ValueError("Ingredient quantity must be positive")
        
        self.receta[ingrediente_id] = nueva_cantidad
        self.updated_at = datetime.utcnow()
    
    def obtener_ingredientes_necesarios(self) -> Dict[UUID, float]:
        """Get required ingredients for the dish."""
        return self.receta.copy()
    
    def verificar_disponibilidad_ingredientes(self, ingredientes_disponibles: Dict[UUID, Ingrediente]) -> bool:
        """Check if all required ingredients are available."""
        for ingrediente_id, cantidad_necesaria in self.receta.items():
            if ingrediente_id not in ingredientes_disponibles:
                return False
            
            ingrediente = ingredientes_disponibles[ingrediente_id]
            if not ingrediente.is_disponible():
                return False
            
            # Check if there's enough stock
            if ingrediente.stock_actual < cantidad_necesaria:
                return False
        
        return True
    
    def calcular_costo_ingredientes(self, ingredientes_disponibles: Dict[UUID, Ingrediente]) -> Precio:
        """Calculate total cost of ingredients."""
        from decimal import Decimal
        
        costo_total = Decimal("0")
        
        for ingrediente_id, cantidad_necesaria in self.receta.items():
            if ingrediente_id not in ingredientes_disponibles:
                raise ValueError(f"Ingredient {ingrediente_id} not available")
            
            ingrediente = ingredientes_disponibles[ingrediente_id]
            # Calculate cost per unit based on unit weight
            costo_por_gramo = ingrediente.precio.value / Decimal(str(ingrediente.peso_unitario))
            costo_ingrediente = costo_por_gramo * Decimal(str(cantidad_necesaria))
            costo_total += costo_ingrediente
        
        return Precio(costo_total)
    
    def es_entrada(self) -> bool:
        """Check if dish is an appetizer."""
        return self.tipo_plato == EtiquetaPlato.ENTRADA
    
    def es_fondo(self) -> bool:
        """Check if dish is a main course."""
        return self.tipo_plato == EtiquetaPlato.FONDO
    
    def es_postre(self) -> bool:
        """Check if dish is a dessert."""
        return self.tipo_plato == EtiquetaPlato.POSTRE
    
    def es_facil_preparar(self) -> bool:
        """Check if dish is easy to prepare."""
        return self.dificultad == "facil"
    
    def requiere_chef_especializado(self) -> bool:
        """Check if dish requires specialized chef."""
        return self.dificultad == "dificil" or self.chef_recomendado is not None
    
    def is_disponible(self) -> bool:
        """Override availability check to include ingredient availability."""
        base_disponible = super().is_disponible()
        if not base_disponible:
            return False
        
        # For now, we assume ingredients are available
        # In a real implementation, this would check ingredient availability
        return True
    
    def calcular_tiempo_preparacion_total(self) -> int:
        """Calculate total preparation time including ingredient prep."""
        # Base preparation time plus estimated ingredient prep time
        tiempo_ingredientes = len(self.receta) * 2  # 2 minutes per ingredient
        return self.tiempo_preparacion + tiempo_ingredientes
    
    def actualizar_instrucciones(self, nuevas_instrucciones: str) -> None:
        """Update cooking instructions."""
        self.instrucciones = nuevas_instrucciones.strip() if nuevas_instrucciones else None
        self.updated_at = datetime.utcnow()
    
    def asignar_chef(self, chef: str) -> None:
        """Assign recommended chef."""
        if not chef or not chef.strip():
            raise ValueError("Chef name cannot be empty")
        
        self.chef_recomendado = chef.strip()
        self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tipo_plato.value}) - {self.porciones} porción(es) - {self.precio}"