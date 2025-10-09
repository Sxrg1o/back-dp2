"""
Excepciones específicas para la gestión de relaciones producto-alérgeno.
"""

from src.business_logic.exceptions.base_exceptions import (
    ValidationError, NotFoundError, ConflictError
)


class ProductoAlergenoValidationError(ValidationError):
    """Excepción lanzada cuando la validación de una relación producto-alérgeno falla."""

    def __init__(self, message: str, error_code: str = "PRODUCTO_ALERGENO_VALIDATION_ERROR"):
        """
        Inicializa la excepción de validación de producto-alérgeno.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de validación.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoAlergenoNotFoundError(NotFoundError):
    """Excepción lanzada cuando no se encuentra una relación producto-alérgeno."""

    def __init__(
        self, 
        message: str = "Relación producto-alérgeno no encontrada", 
        error_code: str = "PRODUCTO_ALERGENO_NOT_FOUND"
    ):
        """
        Inicializa la excepción de relación producto-alérgeno no encontrada.

        Parameters
        ----------
        message : str, optional
            Mensaje descriptivo del error.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)


class ProductoAlergenoConflictError(ConflictError):
    """Excepción lanzada cuando hay un conflicto con una relación producto-alérgeno.
    
    Por ejemplo, cuando se intenta crear una relación duplicada entre el mismo
    producto y alérgeno.
    """

    def __init__(self, message: str, error_code: str = "PRODUCTO_ALERGENO_CONFLICT"):
        """
        Inicializa la excepción de conflicto de producto-alérgeno.

        Parameters
        ----------
        message : str
            Mensaje descriptivo del error de conflicto.
        error_code : str, optional
            Código de error para identificar el tipo específico de error.
        """
        super().__init__(message, error_code)
