"""
Enumeraciones para el sistema de sesiones de mesa.
"""

from enum import Enum


class EstadoSesionMesa(str, Enum):
    """
    Estados posibles de una sesión de mesa.

    Attributes
    ----------
    ACTIVA : str
        La sesión está activa y se pueden crear pedidos.
    FINALIZADA : str
        La sesión ha sido finalizada, no se pueden crear más pedidos.
    """

    ACTIVA = "activa"
    FINALIZADA = "finalizada"
