"""
Excepciones del módulo de business logic.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
)
from src.business_logic.exceptions.rol_exceptions import (
    RolValidationError,
    RolNotFoundError,
    RolConflictError,
)
from src.business_logic.exceptions.producto_opcion_exceptions import (
    ProductoOpcionValidationError,
    ProductoOpcionNotFoundError,
    ProductoOpcionConflictError,
)

__all__ = [
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "RolValidationError",
    "RolNotFoundError",
    "RolConflictError",
    "ProductoOpcionValidationError",
    "ProductoOpcionNotFoundError",
    "ProductoOpcionConflictError",
]
