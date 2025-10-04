"""
Payment-related enumerations.
"""

from enum import Enum


class MetodoPago(str, Enum):
    """Payment method enum."""
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    YAPE = "yape"
    PLIN = "plin"
    TRANSFERENCIA = "transferencia"


class EstadoPago(str, Enum):
    """Payment status enum."""
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADO = "completado"
    FALLIDO = "fallido"
    CANCELADO = "cancelado"