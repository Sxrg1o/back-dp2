"""Bebida domain entity for menu management."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Set
from uuid import UUID
from decimal import Decimal

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem


@dataclass
class Bebida(Item):
    """Domain entity for beverages."""
    
    volumen: Decimal  # in milliliters
    contenido_alcohol: Decimal  # percentage (0-100)
    temperatura_servicio: Optional[str] = None  # "fria", "caliente", "ambiente"
    tipo_bebida: Optional[str] = None  # "gaseosa", "jugo", "cafe", "te", "cerveza", "vino", etc.
    marca: Optional[str] = None
    origen: Optional[str] = None
    
    def __post_init__(self):
        """Validate beverage data after initialization."""
        # Convert etiquetas to set if it's a list (before calling parent validation)
        if isinstance(self.etiquetas, list):
            self.etiquetas = set(self.etiquetas)
        
        super().__post_init__()
        
        if self.volumen <= Decimal("0"):
            raise ValueError("Volume must be positive")
        
        if self.contenido_alcohol < Decimal("0"):
            raise ValueError("Alcohol content cannot be negative")
            
        if self.contenido_alcohol > Decimal("100"):
            raise ValueError("Alcohol content cannot exceed 100%")
        
        if self.temperatura_servicio and self.temperatura_servicio not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Service temperature must be 'fria', 'caliente', or 'ambiente'")
            
        if self.marca is not None and (not self.marca or not self.marca.strip()):
            raise ValueError("Brand cannot be empty")
            
        if self.origen is not None and (not self.origen or not self.origen.strip()):
            raise ValueError("Origin cannot be empty")
    
    def es_alcoholica(self) -> bool:
        """Check if beverage contains alcohol."""
        return self.contenido_alcohol > Decimal("0")
        
    def is_alcoholic(self) -> bool:
        """Check if beverage contains alcohol."""
        return self.es_alcoholica()
    
    def es_sin_alcohol(self) -> bool:
        """Check if beverage is non-alcoholic."""
        return self.contenido_alcohol == Decimal("0")
    
    def es_bebida_fria(self) -> bool:
        """Check if beverage is served cold."""
        return self.temperatura_servicio == "fria"
    
    def es_bebida_caliente(self) -> bool:
        """Check if beverage is served hot."""
        return self.temperatura_servicio == "caliente"
    
    def calcular_alcohol_total(self) -> Decimal:
        """Calculate total alcohol content in milliliters."""
        return (Decimal(str(self.volumen)) * Decimal(str(self.contenido_alcohol))) / Decimal("100")
    
    def es_cerveza(self) -> bool:
        """Check if beverage is beer."""
        return self.tipo_bebida == "cerveza"
    
    def es_vino(self) -> bool:
        """Check if beverage is wine."""
        return self.tipo_bebida == "vino"
    
    def es_gaseosa(self) -> bool:
        """Check if beverage is soda."""
        return self.tipo_bebida == "gaseosa"
    
    def es_jugo(self) -> bool:
        """Check if beverage is juice."""
        return self.tipo_bebida == "jugo"
    
    def es_cafe(self) -> bool:
        """Check if beverage is coffee."""
        return self.tipo_bebida == "cafe"
    
    def es_te(self) -> bool:
        """Check if beverage is tea."""
        return self.tipo_bebida == "te"
    
    def requiere_edad_minima(self) -> bool:
        """Check if beverage requires minimum age (alcoholic beverages)."""
        return self.es_alcoholica()
    
    def calcular_precio_por_ml(self) -> Decimal:
        """Calculate price per milliliter."""
        return self.precio.value / Decimal(str(self.volumen))
    
    def es_volumen_estandar(self) -> bool:
        """Check if beverage has standard volume (250ml, 330ml, 500ml, etc.)."""
        volumenes_estandar = [Decimal("200"), Decimal("250"), Decimal("330"), Decimal("355"), Decimal("500"), Decimal("750"), Decimal("1000")]
        return self.volumen in volumenes_estandar
    
    def actualizar_temperatura_servicio(self, nueva_temperatura: str) -> None:
        """Update service temperature."""
        if nueva_temperatura not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Service temperature must be 'fria', 'caliente', or 'ambiente'")
        
        self.temperatura_servicio = nueva_temperatura
        self.updated_at = datetime.utcnow()
    
    def actualizar_marca(self, nueva_marca: str) -> None:
        """Update beverage brand."""
        if not nueva_marca or not nueva_marca.strip():
            raise ValueError("Brand cannot be empty")
        
        self.marca = nueva_marca.strip()
        self.updated_at = datetime.utcnow()
    
    def actualizar_origen(self, nuevo_origen: str) -> None:
        """Update beverage origin."""
        if not nuevo_origen or not nuevo_origen.strip():
            raise ValueError("Origin cannot be empty")
        
        self.origen = nuevo_origen.strip()
        self.updated_at = datetime.utcnow()
    
    def es_apta_para_menores(self) -> bool:
        """Check if beverage is suitable for minors."""
        return not self.es_alcoholica()
    
    def obtener_categoria_volumen(self) -> str:
        """Get volume category."""
        if self.volumen <= Decimal("250"):
            return "pequeño"
        elif self.volumen <= Decimal("500"):
            return "mediano"
        elif self.volumen <= Decimal("750"):
            return "grande"
        else:
            return "extra_grande"
    
    def requires_age_verification(self) -> bool:
        """Check if beverage requires age verification (high alcohol content)."""
        return self.contenido_alcohol >= Decimal("5.0")
        
    def get_serving_temperature_recommendation(self) -> str:
        """Get serving temperature recommendation."""
        if self.temperatura_servicio == "fria":
            return "Servir bien fria entre 4-8°C"
        elif self.temperatura_servicio == "caliente":
            return "Servir caliente entre 60-70°C"
        else:
            return "Servir a temperatura ambiente"
            
    def calculate_alcohol_units(self) -> Decimal:
        """Calculate alcohol units (volume_ml * alcohol_percentage / 1000)."""
        return (self.volumen * self.contenido_alcohol) / Decimal("1000")

    def __str__(self) -> str:
        alcohol_info = f" ({self.contenido_alcohol}% alcohol)" if self.es_alcoholica() else ""
        return f"{self.nombre} - {self.volumen}ml{alcohol_info} - {self.precio}"