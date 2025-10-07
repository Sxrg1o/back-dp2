"""
Excepciones específicas para la gestión de alérgenos.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class AlergenoValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un alérgeno falla."""

    def __init__(self, message: str, error_code: str = "ALERGENO_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de alérgeno.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class AlergenoNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un alérgeno."""

    def __init__(self, message: str = "Alérgeno no encontrado", error_code: str = "ALERGENO_NOT_FOUND"):
        """
        Inicializa la excepción de alérgeno no encontrado.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class AlergenoConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un alérgeno (por ejemplo, nombre duplicado)."""

    def __init__(self, message: str, error_code: str = "ALERGENO_CONFLICT"):
        """
        Inicializa la excepción de conflicto de alérgeno.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
