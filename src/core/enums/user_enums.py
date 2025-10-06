"""
User-related enumerations.
"""

from enum import Enum


class RoleName(str, Enum):
    """User role names."""
    CLIENTE = "cliente"
    MESERO = "mesero"
    COCINA = "cocina"
    ADMIN = "admin"