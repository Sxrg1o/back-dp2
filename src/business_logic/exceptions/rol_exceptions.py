"""
Excepciones específicas para la gestión de roles.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class RolValidationError(ValidationError):
    """Excepción lanzada cuando la validación de un rol falla."""

    def __init__(self, message: str, error_code: str = "ROL_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de rol.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class RolNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra un rol."""

    def __init__(self, message: str = "Rol no encontrado", error_code: str = "ROL_NOT_FOUND"):
        """
        Inicializa la excepción de rol no encontrado.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class RolConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con un rol (por ejemplo, nombre duplicado)."""

    def __init__(self, message: str, error_code: str = "ROL_CONFLICT"):
        """
        Inicializa la excepción de conflicto de rol.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)