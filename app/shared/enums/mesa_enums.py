"""
Table-related enumerations.
"""

from enum import Enum


class EstadoMesa(str, Enum):
    """Table status enum."""
    DISPONIBLE = "disponible"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"
    MANTENIMIENTO = "mantenimiento"