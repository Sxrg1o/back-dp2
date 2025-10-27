"""
Excepciones específicas para la gestión de pedidos.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class PedidoValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un pedido falla."""

    def __init__(self, message: str, error_code: str = "PEDIDO_VALIDATION_ERROR"):
        super().__init__(message, error_code)


class PedidoNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un pedido."""

    def __init__(self, message: str = "Pedido no encontrado", error_code: str = "PEDIDO_NOT_FOUND"):
        super().__init__(message, error_code)


class PedidoConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un pedido."""

    def __init__(self, message: str, error_code: str = "PEDIDO_CONFLICT"):
        super().__init__(message, error_code)

