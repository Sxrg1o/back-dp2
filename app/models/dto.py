from pydantic import BaseModel, Field
from typing import List, Optional, Union

class ItemListDTO(BaseModel):
    """DTO para listar items del menú con información básica"""
    valor_nutricional: str = ""
    precio: Union[float, str] = 0
    tiempo_preparacion: Union[int, str] = 0
    comentarios: str = ""
    receta: str = ""
    disponible: bool = True
    unidades_disponibles: int = 0
    num_ingredientes: int = 0
    kcal: int = 0
    calorias: Union[str, int] = "0"
    proteinas: Union[str, int] = "0"
    azucares: Union[str, int] = "0"
    descripcion: str = ""
    etiquetas: List[str] = []
    ingredientes_ids: List[int] = []
    id: int
    tipo: str

class AcompanamientoDTO(BaseModel):
    """DTO para acompañamientos de platos"""
    id: str
    nombre: str
    precio_adicional: float
    obligatorio: bool = False

class OpcionAdicionalDTO(BaseModel):
    """DTO para opciones adicionales de platos"""
    id: str
    nombre: str
    precio: float
    max_selecciones: int = 1

class ItemDetailDTO(BaseModel):
    """DTO para detalles completos de un item del menú"""
    id: str
    nombre: str
    descripcion: str
    precio: float
    imagen_url: str
    categoria: str
    tiempo_preparacion: int
    ingredientes: List[str]
    acompañamientos: List[AcompanamientoDTO]
    opciones_adicionales: List[OpcionAdicionalDTO]

class ValidarItemReq(BaseModel):
    """Request para validar disponibilidad de un item"""
    producto_id: str
    cantidad: int

class ValidarDisponReq(BaseModel):
    """Request para validar disponibilidad de múltiples items"""
    items: List[ValidarItemReq]

class NoDisponible(BaseModel):
    """Item no disponible con razón"""
    producto_id: str
    razon: str

class ValidarDisponResp(BaseModel):
    """Response de validación de disponibilidad"""
    disponibles: List[str]
    no_disponibles: List[NoDisponible]

class OrdenItemReq(BaseModel):
    """Item de una orden con opciones"""
    producto_id: str
    cantidad: int
    acompañamientos_ids: List[str] = []
    opciones_adicionales_ids: List[str] = []
    comentarios: str = ""

class CrearOrdenReq(BaseModel):
    """Request para crear una nueva orden"""
    cliente_nombre: str
    cliente_telefono: str
    items: List[OrdenItemReq]
    comentarios_generales: str = ""
    tipo_entrega: str = "local"

class CrearOrdenResp(BaseModel):
    """Response de creación de orden"""
    order_id: str
    total: float
    tiempo_estimado: int
    estado: str
