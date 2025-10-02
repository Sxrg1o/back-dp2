from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

class Categoria(BaseModel):
    """Modelo para categorías de items"""
    id: int
    nombre: str
    descripcion: str

class Opcion(BaseModel):
    """Modelo para opciones de personalización"""
    id: int
    etiqueta: str
    precio_adicional: float = 0.0
    es_default: bool = False
    seleccionado: bool = False

class GrupoPersonalizacion(BaseModel):
    """Modelo para grupos de personalización de items"""
    id: int
    etiqueta: str
    tipo: str
    opciones: List[Opcion] = []
    max_selecciones: int = 1

class Item(BaseModel):
    """Modelo unificado para items del menú (platos y bebidas)"""
    id: int
    nombre: str
    imagen: str
    precio: float
    stock: int
    disponible: bool
    categoria: Categoria
    alergenos: List[str] = []  # Lista de strings en lugar de enum
    descripcion: str
    ingredientes: List[str] = []  # Lista de strings en lugar de objetos Ingrediente
    grupo_personalizacion: Optional[List[GrupoPersonalizacion]] = None  # Lista de grupos
    
    # Campos específicos para platos
    peso: Optional[float] = None  # en gramos, solo para platos
    tipo: Optional[str] = None  # String para tipo de plato (ej: "ENTRADA", "FONDO", "POSTRE")
    
    # Campos específicos para bebidas
    litros: Optional[float] = None  # solo para bebidas
    con_alcohol: Optional[bool] = None  # solo para bebidas

    def verificar_stock(self) -> bool:
        """Verifica si el item tiene stock disponible"""
        return self.disponible and self.stock > 0

    def get_tipo_item(self) -> str:
        """Determina el tipo de item basado en los campos presentes"""
        if self.litros is not None or self.con_alcohol is not None:
            return "BEBIDA"
        elif self.peso is not None or self.tipo is not None:
            return "PLATO"
        else:
            return "ITEM"

# Clases Plato y Bebida eliminadas - ahora se usa solo Item