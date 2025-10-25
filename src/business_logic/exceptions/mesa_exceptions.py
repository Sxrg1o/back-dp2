"""
Excepciones específicas para la gestión de mesas.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class MesaValidationError(ValidationError):
    """Excepción lanzada cuando la validación de una mesa falla."""

    def __init__(self, message: str, error_code: str = "MESA_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de mesa.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class MesaNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra una mesa."""

    def __init__(self, message: str = "Mesa no encontrada", error_code: str = "MESA_NOT_FOUND"):
        """
        Inicializa la excepción de mesa no encontrado.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class MesaConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con una mesa (por ejemplo, numero duplicado)."""

    def __init__(self, message: str, error_code: str = "MESA_CONFLICT"):
        """
        Inicializa la excepción de conflicto de mesa.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
