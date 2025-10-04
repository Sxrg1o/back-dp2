"""
Menu-related business exceptions.
"""

from app.business.exceptions.base_exceptions import BusinessError


class MenuError(BusinessError):
    """Base exception for menu-related errors."""
    pass


class ProductoNotFoundError(MenuError):
    """Exception raised when a product is not found."""
    pass


class ProductoNotAvailableError(MenuError):
    """Exception raised when a product is not available."""
    pass


class CategoriaNotFoundError(MenuError):
    """Exception raised when a category is not found."""
    pass


class CategoriaNotActiveError(MenuError):
    """Exception raised when a category is not active."""
    pass


class AlergenoNotFoundError(MenuError):
    """Exception raised when an allergen is not found."""
    pass


class InvalidProductDataError(MenuError):
    """Exception raised when product data is invalid."""
    pass


class InvalidPriceError(MenuError):
    """Exception raised when price is invalid."""
    pass


class ProductoOpcionNotFoundError(MenuError):
    """Exception raised when a product option is not found."""
    pass


class InvalidOpcionSelectionError(MenuError):
    """Exception raised when option selection is invalid."""
    pass