"""Menu domain-specific exceptions."""

from typing import Optional, Any
from uuid import UUID


class MenuDomainException(Exception):
    """Base exception for menu domain operations."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class ItemNotFoundError(MenuDomainException):
    """Raised when a menu item is not found."""
    
    def __init__(self, item_id: Optional[UUID] = None, item_name: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            if item_id:
                message = f"Item with ID {item_id} not found"
            elif item_name:
                message = f"Item '{item_name}' not found"
            else:
                message = "Item not found"
        
        details = {}
        if item_id:
            details["item_id"] = str(item_id)
        if item_name:
            details["item_name"] = item_name
        
        super().__init__(message, details)
        self.item_id = item_id
        self.item_name = item_name


class ItemNotAvailableError(MenuDomainException):
    """Raised when a menu item is not available for ordering."""
    
    def __init__(self, item_id: Optional[UUID] = None, item_name: Optional[str] = None, 
                 reason: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            base_msg = f"Item '{item_name}' is not available" if item_name else "Item is not available"
            if reason:
                message = f"{base_msg}: {reason}"
            else:
                message = base_msg
        
        details = {}
        if item_id:
            details["item_id"] = str(item_id)
        if item_name:
            details["item_name"] = item_name
        if reason:
            details["reason"] = reason
        
        super().__init__(message, details)
        self.item_id = item_id
        self.item_name = item_name
        self.reason = reason


class InsufficientStockError(MenuDomainException):
    """Raised when there is insufficient stock for an operation."""
    
    def __init__(self, item_id: Optional[UUID] = None, item_name: Optional[str] = None,
                 requested_quantity: Optional[int] = None, available_quantity: Optional[int] = None,
                 message: Optional[str] = None):
        if message is None:
            item_ref = item_name if item_name else f"item {item_id}" if item_id else "item"
            if requested_quantity is not None and available_quantity is not None:
                message = f"Insufficient stock for {item_ref}: requested {requested_quantity}, available {available_quantity}"
            else:
                message = f"Insufficient stock for {item_ref}"
        
        details = {}
        if item_id:
            details["item_id"] = str(item_id)
        if item_name:
            details["item_name"] = item_name
        if requested_quantity is not None:
            details["requested_quantity"] = requested_quantity
        if available_quantity is not None:
            details["available_quantity"] = available_quantity
        
        super().__init__(message, details)
        self.item_id = item_id
        self.item_name = item_name
        self.requested_quantity = requested_quantity
        self.available_quantity = available_quantity


class InvalidNutritionalDataError(MenuDomainException):
    """Raised when nutritional data is invalid or inconsistent."""
    
    def __init__(self, field_name: Optional[str] = None, field_value: Optional[Any] = None,
                 validation_rule: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            if field_name and validation_rule:
                message = f"Invalid nutritional data for {field_name}: {validation_rule}"
            elif field_name:
                message = f"Invalid nutritional data for {field_name}"
            else:
                message = "Invalid nutritional data"
        
        details = {}
        if field_name:
            details["field_name"] = field_name
        if field_value is not None:
            details["field_value"] = field_value
        if validation_rule:
            details["validation_rule"] = validation_rule
        
        super().__init__(message, details)
        self.field_name = field_name
        self.field_value = field_value
        self.validation_rule = validation_rule


class InvalidPriceError(MenuDomainException):
    """Raised when price data is invalid."""
    
    def __init__(self, price_value: Optional[Any] = None, validation_rule: Optional[str] = None,
                 message: Optional[str] = None):
        if message is None:
            if validation_rule:
                message = f"Invalid price: {validation_rule}"
            else:
                message = "Invalid price"
        
        details = {}
        if price_value is not None:
            details["price_value"] = price_value
        if validation_rule:
            details["validation_rule"] = validation_rule
        
        super().__init__(message, details)
        self.price_value = price_value
        self.validation_rule = validation_rule


class IngredientExpiredError(MenuDomainException):
    """Raised when trying to use an expired ingredient."""
    
    def __init__(self, ingredient_id: Optional[UUID] = None, ingredient_name: Optional[str] = None,
                 expiration_date: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            ingredient_ref = ingredient_name if ingredient_name else f"ingredient {ingredient_id}" if ingredient_id else "ingredient"
            if expiration_date:
                message = f"Ingredient {ingredient_ref} expired on {expiration_date}"
            else:
                message = f"Ingredient {ingredient_ref} is expired"
        
        details = {}
        if ingredient_id:
            details["ingredient_id"] = str(ingredient_id)
        if ingredient_name:
            details["ingredient_name"] = ingredient_name
        if expiration_date:
            details["expiration_date"] = expiration_date
        
        super().__init__(message, details)
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name
        self.expiration_date = expiration_date


class RecipeValidationError(MenuDomainException):
    """Raised when recipe data is invalid."""
    
    def __init__(self, dish_id: Optional[UUID] = None, dish_name: Optional[str] = None,
                 validation_issue: Optional[str] = None, message: Optional[str] = None):
        if message is None:
            dish_ref = dish_name if dish_name else f"dish {dish_id}" if dish_id else "dish"
            if validation_issue:
                message = f"Recipe validation error for {dish_ref}: {validation_issue}"
            else:
                message = f"Recipe validation error for {dish_ref}"
        
        details = {}
        if dish_id:
            details["dish_id"] = str(dish_id)
        if dish_name:
            details["dish_name"] = dish_name
        if validation_issue:
            details["validation_issue"] = validation_issue
        
        super().__init__(message, details)
        self.dish_id = dish_id
        self.dish_name = dish_name
        self.validation_issue = validation_issue


class InvalidVolumeError(MenuDomainException):
    """Raised when beverage volume is invalid."""
    
    def __init__(self, volume_value: Optional[float] = None, validation_rule: Optional[str] = None,
                 message: Optional[str] = None):
        if message is None:
            if validation_rule:
                message = f"Invalid volume: {validation_rule}"
            else:
                message = "Invalid volume"
        
        details = {}
        if volume_value is not None:
            details["volume_value"] = volume_value
        if validation_rule:
            details["validation_rule"] = validation_rule
        
        super().__init__(message, details)
        self.volume_value = volume_value
        self.validation_rule = validation_rule


class InvalidAlcoholContentError(MenuDomainException):
    """Raised when alcohol content is invalid."""
    
    def __init__(self, alcohol_content: Optional[float] = None, validation_rule: Optional[str] = None,
                 message: Optional[str] = None):
        if message is None:
            if validation_rule:
                message = f"Invalid alcohol content: {validation_rule}"
            else:
                message = "Invalid alcohol content"
        
        details = {}
        if alcohol_content is not None:
            details["alcohol_content"] = alcohol_content
        if validation_rule:
            details["validation_rule"] = validation_rule
        
        super().__init__(message, details)
        self.alcohol_content = alcohol_content
        self.validation_rule = validation_rule