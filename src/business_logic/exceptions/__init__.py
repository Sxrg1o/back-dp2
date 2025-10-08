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
from src.business_logic.exceptions.producto_tipo_opcion_exceptions import (
    ProductoTipoOpcionValidationError,
    ProductoTipoOpcionNotFoundError,
    ProductoTipoOpcionConflictError,
)

__all__ = [
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "RolValidationError",
    "RolNotFoundError",
    "RolConflictError",
    "ProductoTipoOpcionValidationError",
    "ProductoTipoOpcionNotFoundError",
    "ProductoTipoOpcionConflictError",
]
