"""
Excepciones específicas para la gestión de tipos de opciones.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class TipoOpcionValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un tipo de opción falla."""

    def __init__(self, message: str, error_code: str = "TIPO_OPCION_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de tipo de opción.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class TipoOpcionNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un tipo de opción."""

    def __init__(self, message: str = "Tipo de opción no encontrado", error_code: str = "TIPO_OPCION_NOT_FOUND"):
        """
        Inicializa la excepción de tipo de opción no encontrado.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class TipoOpcionConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un tipo de opción (por ejemplo, código duplicado)."""

    def __init__(self, message: str, error_code: str = "TIPO_OPCION_CONFLICT"):
        """
        Inicializa la excepción de conflicto de tipo de opción.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)

