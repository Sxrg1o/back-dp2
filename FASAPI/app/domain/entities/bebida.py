"""Bebida domain entity for menu management."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Set
from uuid import UUID

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem


@dataclass
class Bebida(Item):
    """Domain entity for beverages."""
    
    volumen: float  # in milliliters
    contenido_alcohol: float  # percentage (0-100)
    temperatura_servicio: Optional[str] = None  # "fria", "caliente", "ambiente"
    tipo_bebida: Optional[str] = None  # "gaseosa", "jugo", "cafe", "te", "cerveza", "vino", etc.
    marca: Optional[str] = None
    origen: Optional[str] = None
    
    def __post_init__(self):
        """Validate beverage data after initialization."""
        super().__post_init__()
        
        if self.volumen <= 0:
            raise ValueError("Volume must be positive")
        
        if self.contenido_alcohol < 0 or self.contenido_alcohol > 100:
            raise ValueError("Alcohol content must be between 0 and 100 percent")
        
        if self.temperatura_servicio and self.temperatura_servicio not in ["fria", "caliente", "ambiente"]:
            raise ValueError("Service temperature must be 'fria', 'caliente', or 'ambiente'")
    
    def es_alcoholica(self) -> bool:
        """Check if beverage contains alcohol."""
        return self.contenido_alcohol > 0
    
    def es_sin_alcohol(self) -> bool:
        """Check if beverage is non-alcoholic."""
        return self.contenido_alcohol == 0
    
    def es_bebida_fria(self) -> bool:
        """Check if beverage is served cold."""
        return self.temperatura_servicio == "fria"
    
    def es_bebida_caliente(self) -> bool:
        """Check if beverage is served hot."""
        return self.temperatura_servicio == "caliente"
    
    def calcular_alcohol_total(self) -> float:
        """Calculate total alcohol content in milliliters."""
        return (self.volumen * self.contenido_alcohol) / 100
    
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
    
    def calcular_precio_por_ml(self) -> float:
        """Calculate price per milliliter."""
        return float(self.precio.value) / self.volumen
    
    def es_volumen_estandar(self) -> bool:
        """Check if beverage has standard volume (250ml, 330ml, 500ml, etc.)."""
        volumenes_estandar = [200, 250, 330, 355, 500, 750, 1000]
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
            raise ValueError("Brand name cannot be empty")
        
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
        if self.volumen <= 250:
            return "pequeño"
        elif self.volumen <= 500:
            return "mediano"
        elif self.volumen <= 750:
            return "grande"
        else:
            return "extra_grande"
    
    def __str__(self) -> str:
        alcohol_info = f" ({self.contenido_alcohol}% alcohol)" if self.es_alcoholica() else ""
        return f"{self.nombre} - {self.volumen}ml{alcohol_info} - {self.precio}"