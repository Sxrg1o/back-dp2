"""
Excepciones específicas para la gestión de opciones de productos por tipo.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class ProductoTipoOpcionValidationError(ValidationError):
    """Excepción lanzada cuando la validación de una opción de producto por tipo falla."""

    def __init__(self, message: str, error_code: str = "PRODUCTO_TIPO_OPCION_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de opción de producto por tipo.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoTipoOpcionNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra una opción de producto por tipo."""

    def __init__(self, message: str = "Opción de producto por tipo no encontrada", error_code: str = "PRODUCTO_TIPO_OPCION_NOT_FOUND"):
        """
        Inicializa la excepción de opción de producto por tipo no encontrada.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoTipoOpcionConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con una opción de producto por tipo (por ejemplo, nombre duplicado)."""

    def __init__(self, message: str, error_code: str = "PRODUCTO_TIPO_OPCION_CONFLICT"):
        """
        Inicializa la excepción de conflicto de opción de producto por tipo.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
