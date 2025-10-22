"""
Table-related enumerations.
"""

from enum import Enum


class EstadoMesa(str, Enum):
    """Table status enum."""
    LIBRE = "libre"
    DISPONIBLE = "disponible"
    OCUPADA = "ocupada"
    RESERVADA = "reservada"
    MANTENIMIENTO = "mantenimiento"
    FUERA_SERVICIO = "fuera_servicio"