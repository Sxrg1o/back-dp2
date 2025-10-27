"""
Excepciones específicas para la gestión de pedido_producto.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class PedidoProductoValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un pedido_producto falla."""

    def __init__(self, message: str, error_code: str = "PEDIDO_PRODUCTO_VALIDATION_ERROR"):
        super().__init__(message, error_code)


class PedidoProductoNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un pedido_producto."""

    def __init__(self, message: str = "Item de pedido no encontrado", error_code: str = "PEDIDO_PRODUCTO_NOT_FOUND"):
        super().__init__(message, error_code)


class PedidoProductoConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un pedido_producto."""

    def __init__(self, message: str, error_code: str = "PEDIDO_PRODUCTO_CONFLICT"):
        super().__init__(message, error_code)

