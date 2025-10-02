from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

class Categoria(BaseModel):
    """Modelo para categorías de items"""
    nombre: str
    descripcion: str

class Opcion(BaseModel):
    """Modelo para opciones de personalización"""
    etiqueta: str
    precio_adicional: float = 0.0
    es_default: bool = False
    seleccionado: bool = False

class GrupoPersonalizacion(BaseModel):
    """Modelo para grupos de personalización de items"""
    etiqueta: str
    tipo: str
    opciones: List[Opcion] = []
    max_selecciones: int = 1

class Item(BaseModel, ABC):
    """Clase base abstracta para items del menú"""
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

    def verificar_stock(self) -> bool:
        """Verifica si el item tiene stock disponible"""
        return self.disponible and self.stock > 0

    @abstractmethod
    def get_tipo_item(self) -> str:
        """Método abstracto para obtener el tipo de item"""
        pass

class Plato(Item):
    """Modelo para platos que hereda de Item"""
    peso: float  # en gramos
    tipo: str  # String en lugar de enum (ej: "ENTRADA", "FONDO", "POSTRE")

    def get_tipo_item(self) -> str:
        return "PLATO"

class Bebida(Item):
    """Modelo para bebidas que hereda de Item"""
    litros: float
    con_alcohol: bool

    def get_tipo_item(self) -> str:
        return "BEBIDA"