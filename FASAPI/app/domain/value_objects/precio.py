"""Precio value object with validation for positive values."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass(frozen=True)
class Precio:
    """Value object for price with validation."""
    
    value: Decimal
    
    def __post_init__(self):
        """Validate price value."""
        if not isinstance(self.value, Decimal):
            # Convert to Decimal if it's a valid numeric type
            if isinstance(self.value, (int, float, str)):
                object.__setattr__(self, 'value', Decimal(str(self.value)))
            else:
                raise ValueError("Price must be a numeric value")
        
        if self.value <= 0:
            raise ValueError("Price must be positive")
        
        # Ensure maximum 2 decimal places for currency
        if self.value.as_tuple().exponent < -2:
            raise ValueError("Price cannot have more than 2 decimal places")
    
    @classmethod
    def from_float(cls, value: float) -> 'Precio':
        """Create Precio from float value."""
        return cls(Decimal(str(value)))
    
    @classmethod
    def from_int(cls, value: int) -> 'Precio':
        """Create Precio from integer value."""
        return cls(Decimal(value))
    
    def __str__(self) -> str:
        return f"${self.value}"
    
    def __add__(self, other: 'Precio') -> 'Precio':
        """Add two prices."""
        if not isinstance(other, Precio):
            raise TypeError("Can only add Precio to Precio")
        return Precio(self.value + other.value)
    
    def __mul__(self, factor: Union[int, float, Decimal]) -> 'Precio':
        """Multiply price by a factor."""
        if isinstance(factor, (int, float)):
            factor = Decimal(str(factor))
        elif not isinstance(factor, Decimal):
            raise TypeError("Factor must be numeric")
        
        if factor < 0:
            raise ValueError("Factor must be non-negative")
        
        return Precio(self.value * factor)