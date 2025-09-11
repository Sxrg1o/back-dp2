"""Tests for menu domain exceptions."""

import pytest
from uuid import uuid4

from app.domain.exceptions.menu_exceptions import (
    MenuDomainException,
    ItemNotFoundError,
    ItemNotAvailableError,
    InsufficientStockError,
    InvalidNutritionalDataError,
    InvalidPriceError,
    IngredientExpiredError,
    RecipeValidationError,
    InvalidVolumeError,
    InvalidAlcoholContentError
)


class TestMenuDomainException:
    """Test cases for MenuDomainException base class."""
    
    def test_basic_exception_creation(self):
        """Test creating basic exception."""
        exception = MenuDomainException("Test error message")
        assert str(exception) == "Test error message"
        assert exception.message == "Test error message"
        assert exception.details == {}
    
    def test_exception_with_details(self):
        """Test creating exception with details."""
        details = {"field": "value", "code": 123}
        exception = MenuDomainException("Test error", details)
        assert exception.message == "Test error"
        assert exception.details == details
        assert "Details:" in str(exception)


class TestItemNotFoundError:
    """Test cases for ItemNotFoundError."""
    
    def test_item_not_found_with_id(self):
        """Test ItemNotFoundError with item ID."""
        item_id = uuid4()
        exception = ItemNotFoundError(item_id=item_id)
        assert f"Item with ID {item_id} not found" in str(exception)
        assert exception.item_id == item_id
        assert str(item_id) in exception.details["item_id"]
    
    def test_item_not_found_with_name(self):
        """Test ItemNotFoundError with item name."""
        item_name = "Pizza Margherita"
        exception = ItemNotFoundError(item_name=item_name)
        assert f"Item '{item_name}' not found" in str(exception)
        assert exception.item_name == item_name
        assert exception.details["item_name"] == item_name
    
    def test_item_not_found_with_custom_message(self):
        """Test ItemNotFoundError with custom message."""
        custom_message = "Custom not found message"
        exception = ItemNotFoundError(message=custom_message)
        assert str(exception) == custom_message
    
    def test_item_not_found_default(self):
        """Test ItemNotFoundError with default message."""
        exception = ItemNotFoundError()
        assert str(exception) == "Item not found"


class TestItemNotAvailableError:
    """Test cases for ItemNotAvailableError."""
    
    def test_item_not_available_with_reason(self):
        """Test ItemNotAvailableError with reason."""
        item_name = "Pasta Carbonara"
        reason = "Out of stock"
        exception = ItemNotAvailableError(item_name=item_name, reason=reason)
        assert item_name in str(exception)
        assert reason in str(exception)
        assert exception.reason == reason
    
    def test_item_not_available_without_reason(self):
        """Test ItemNotAvailableError without reason."""
        item_name = "Caesar Salad"
        exception = ItemNotAvailableError(item_name=item_name)
        assert f"Item '{item_name}' is not available" in str(exception)
        assert exception.reason is None


class TestInsufficientStockError:
    """Test cases for InsufficientStockError."""
    
    def test_insufficient_stock_with_quantities(self):
        """Test InsufficientStockError with quantities."""
        item_name = "Chicken Breast"
        requested = 10
        available = 5
        exception = InsufficientStockError(
            item_name=item_name,
            requested_quantity=requested,
            available_quantity=available
        )
        assert item_name in str(exception)
        assert f"requested {requested}" in str(exception)
        assert f"available {available}" in str(exception)
        assert exception.requested_quantity == requested
        assert exception.available_quantity == available
    
    def test_insufficient_stock_basic(self):
        """Test InsufficientStockError basic case."""
        item_id = uuid4()
        exception = InsufficientStockError(item_id=item_id)
        assert f"item {item_id}" in str(exception)
        assert "Insufficient stock" in str(exception)


class TestInvalidNutritionalDataError:
    """Test cases for InvalidNutritionalDataError."""
    
    def test_invalid_nutritional_data_with_field(self):
        """Test InvalidNutritionalDataError with field details."""
        field_name = "calories"
        field_value = -100
        validation_rule = "must be non-negative"
        exception = InvalidNutritionalDataError(
            field_name=field_name,
            field_value=field_value,
            validation_rule=validation_rule
        )
        assert field_name in str(exception)
        assert validation_rule in str(exception)
        assert exception.field_name == field_name
        assert exception.field_value == field_value
    
    def test_invalid_nutritional_data_basic(self):
        """Test InvalidNutritionalDataError basic case."""
        exception = InvalidNutritionalDataError()
        assert str(exception) == "Invalid nutritional data"


class TestInvalidPriceError:
    """Test cases for InvalidPriceError."""
    
    def test_invalid_price_with_rule(self):
        """Test InvalidPriceError with validation rule."""
        price_value = -10.50
        validation_rule = "must be positive"
        exception = InvalidPriceError(
            price_value=price_value,
            validation_rule=validation_rule
        )
        assert validation_rule in str(exception)
        assert exception.price_value == price_value
        assert exception.validation_rule == validation_rule
    
    def test_invalid_price_basic(self):
        """Test InvalidPriceError basic case."""
        exception = InvalidPriceError()
        assert str(exception) == "Invalid price"


class TestIngredientExpiredError:
    """Test cases for IngredientExpiredError."""
    
    def test_ingredient_expired_with_date(self):
        """Test IngredientExpiredError with expiration date."""
        ingredient_name = "Milk"
        expiration_date = "2024-01-15"
        exception = IngredientExpiredError(
            ingredient_name=ingredient_name,
            expiration_date=expiration_date
        )
        assert ingredient_name in str(exception)
        assert expiration_date in str(exception)
        assert "expired on" in str(exception)
    
    def test_ingredient_expired_basic(self):
        """Test IngredientExpiredError basic case."""
        ingredient_id = uuid4()
        exception = IngredientExpiredError(ingredient_id=ingredient_id)
        assert f"ingredient {ingredient_id}" in str(exception)
        assert "is expired" in str(exception)


class TestRecipeValidationError:
    """Test cases for RecipeValidationError."""
    
    def test_recipe_validation_with_issue(self):
        """Test RecipeValidationError with validation issue."""
        dish_name = "Beef Stew"
        validation_issue = "missing required ingredient"
        exception = RecipeValidationError(
            dish_name=dish_name,
            validation_issue=validation_issue
        )
        assert dish_name in str(exception)
        assert validation_issue in str(exception)
        assert exception.validation_issue == validation_issue
    
    def test_recipe_validation_basic(self):
        """Test RecipeValidationError basic case."""
        dish_id = uuid4()
        exception = RecipeValidationError(dish_id=dish_id)
        assert f"dish {dish_id}" in str(exception)


class TestInvalidVolumeError:
    """Test cases for InvalidVolumeError."""
    
    def test_invalid_volume_with_rule(self):
        """Test InvalidVolumeError with validation rule."""
        volume_value = -250.0
        validation_rule = "must be positive"
        exception = InvalidVolumeError(
            volume_value=volume_value,
            validation_rule=validation_rule
        )
        assert validation_rule in str(exception)
        assert exception.volume_value == volume_value
    
    def test_invalid_volume_basic(self):
        """Test InvalidVolumeError basic case."""
        exception = InvalidVolumeError()
        assert str(exception) == "Invalid volume"


class TestInvalidAlcoholContentError:
    """Test cases for InvalidAlcoholContentError."""
    
    def test_invalid_alcohol_content_with_rule(self):
        """Test InvalidAlcoholContentError with validation rule."""
        alcohol_content = 150.0
        validation_rule = "must be between 0 and 100"
        exception = InvalidAlcoholContentError(
            alcohol_content=alcohol_content,
            validation_rule=validation_rule
        )
        assert validation_rule in str(exception)
        assert exception.alcohol_content == alcohol_content
    
    def test_invalid_alcohol_content_basic(self):
        """Test InvalidAlcoholContentError basic case."""
        exception = InvalidAlcoholContentError()
        assert str(exception) == "Invalid alcohol content"


class TestExceptionInheritance:
    """Test exception inheritance and behavior."""
    
    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from MenuDomainException."""
        exceptions = [
            ItemNotFoundError(),
            ItemNotAvailableError(),
            InsufficientStockError(),
            InvalidNutritionalDataError(),
            InvalidPriceError(),
            IngredientExpiredError(),
            RecipeValidationError(),
            InvalidVolumeError(),
            InvalidAlcoholContentError()
        ]
        
        for exception in exceptions:
            assert isinstance(exception, MenuDomainException)
            assert isinstance(exception, Exception)
    
    def test_exceptions_can_be_raised_and_caught(self):
        """Test that exceptions can be properly raised and caught."""
        with pytest.raises(ItemNotFoundError):
            raise ItemNotFoundError("Test item not found")
        
        with pytest.raises(MenuDomainException):
            raise ItemNotAvailableError("Test item not available")
        
        # Test catching base exception
        try:
            raise InsufficientStockError("Test insufficient stock")
        except MenuDomainException as e:
            assert isinstance(e, InsufficientStockError)
            assert "Test insufficient stock" in str(e)