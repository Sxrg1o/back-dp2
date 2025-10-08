"""
Excepciones específicas para la gestión de productos.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class ProductoValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un producto falla."""

    def __init__(self, message: str, error_code: str = "PRODUCTO_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de producto.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un producto."""

    def __init__(self, message: str = "Producto no encontrado", error_code: str = "PRODUCTO_NOT_FOUND"):
        """
        Inicializa la excepción de producto no encontrado.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un producto (por ejemplo, nombre duplicado)."""

    def __init__(self, message: str, error_code: str = "PRODUCTO_CONFLICT"):
        """
        Inicializa la excepción de conflicto de producto.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
