"""
Order-related enumerations.
"""

from enum import Enum


class EstadoPedido(str, Enum):
    """Order status enum."""
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class PrioridadPedido(str, Enum):
    """Order priority enum."""
    NORMAL = "normal"
    ALTA = "alta"
    URGENTE = "urgente"


class TipoDivision(str, Enum):
    """Bill division type enum."""
    EQUITATIVA = "equitativa"
    POR_ITEMS = "por_items"
    MANUAL = "manual"