"""
Excepciones específicas para la gestión de categorías.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class CategoriaValidationError(ValidationError):
    """Excepción lanzada cuando la validación de una categoría falla."""

    def __init__(self, message: str, error_code: str = "CATEGORIA_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de categoría.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class CategoriaNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra una categoría."""

    def __init__(self, message: str = "Categoría no encontrada", error_code: str = "CATEGORIA_NOT_FOUND"):
        """
        Inicializa la excepción de categoría no encontrada.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class CategoriaConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con una categoría (por ejemplo, nombre duplicado)."""

    def __init__(self, message: str, error_code: str = "CATEGORIA_CONFLICT"):
        """
        Inicializa la excepción de conflicto de categoría.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
