"""Tests for Precio value object."""

import pytest
from decimal import Decimal
from app.domain.value_objects.precio import Precio


class TestPrecio:
    """Test cases for Precio value object."""
    
    def test_valid_precio_creation(self):
        """Test creating valid Precio instances."""
        # Test with Decimal
        precio1 = Precio(Decimal("10.50"))
        assert precio1.value == Decimal("10.50")
        
        # Test with integer
        precio2 = Precio(Decimal("15"))
        assert precio2.value == Decimal("15")
        
        # Test with string
        precio3 = Precio(Decimal("25.99"))
        assert precio3.value == Decimal("25.99")
    
    def test_precio_from_float(self):
        """Test creating Precio from float."""
        precio = Precio.from_float(12.50)
        assert precio.value == Decimal("12.50")
    
    def test_precio_from_int(self):
        """Test creating Precio from integer."""
        precio = Precio.from_int(20)
        assert precio.value == Decimal("20")
    
    def test_invalid_precio_negative(self):
        """Test that negative prices raise ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Precio(Decimal("-10.50"))
    
    def test_invalid_precio_zero(self):
        """Test that zero price raises ValueError."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Precio(Decimal("0"))
    
    def test_invalid_precio_too_many_decimals(self):
        """Test that prices with more than 2 decimal places raise ValueError."""
        with pytest.raises(ValueError, match="Price cannot have more than 2 decimal places"):
            Precio(Decimal("10.123"))
    
    def test_precio_immutability(self):
        """Test that Precio is immutable."""
        precio = Precio(Decimal("10.50"))
        with pytest.raises(AttributeError):
            precio.value = Decimal("20.00")
    
    def test_precio_string_representation(self):
        """Test string representation of Precio."""
        precio = Precio(Decimal("15.75"))
        assert str(precio) == "$15.75"
    
    def test_precio_addition(self):
        """Test adding two Precio instances."""
        precio1 = Precio(Decimal("10.50"))
        precio2 = Precio(Decimal("5.25"))
        result = precio1 + precio2
        assert result.value == Decimal("15.75")
    
    def test_precio_addition_invalid_type(self):
        """Test that adding non-Precio raises TypeError."""
        precio = Precio(Decimal("10.50"))
        with pytest.raises(TypeError, match="Can only add Precio to Precio"):
            precio + 5
    
    def test_precio_multiplication(self):
        """Test multiplying Precio by numeric factors."""
        precio = Precio(Decimal("10.00"))
        
        # Test with integer
        result1 = precio * 2
        assert result1.value == Decimal("20.00")
        
        # Test with float
        result2 = precio * 1.5
        assert result2.value == Decimal("15.00")
        
        # Test with Decimal
        result3 = precio * Decimal("0.5")
        assert result3.value == Decimal("5.00")
    
    def test_precio_multiplication_negative_factor(self):
        """Test that multiplying by negative factor raises ValueError."""
        precio = Precio(Decimal("10.00"))
        with pytest.raises(ValueError, match="Factor must be non-negative"):
            precio * -1
    
    def test_precio_multiplication_invalid_type(self):
        """Test that multiplying by invalid type raises TypeError."""
        precio = Precio(Decimal("10.00"))
        with pytest.raises(TypeError, match="Factor must be numeric"):
            precio * "invalid"
    
    def test_precio_equality(self):
        """Test Precio equality comparison."""
        precio1 = Precio(Decimal("10.50"))
        precio2 = Precio(Decimal("10.50"))
        precio3 = Precio(Decimal("15.00"))
        
        assert precio1 == precio2
        assert precio1 != precio3