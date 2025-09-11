"""InformacionNutricional value object with nutritional data validation."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InformacionNutricional:
    """Value object for nutritional information."""
    
    calorias: int
    proteinas: float  # in grams
    azucares: float   # in grams
    grasas: Optional[float] = None      # in grams
    carbohidratos: Optional[float] = None  # in grams
    fibra: Optional[float] = None       # in grams
    sodio: Optional[float] = None       # in milligrams
    
    def __post_init__(self):
        """Validate nutritional information."""
        if self.calorias < 0:
            raise ValueError("Calories cannot be negative")
        
        if self.proteinas < 0:
            raise ValueError("Proteins cannot be negative")
        
        if self.azucares < 0:
            raise ValueError("Sugars cannot be negative")
        
        # Validate optional fields if provided
        if self.grasas is not None and self.grasas < 0:
            raise ValueError("Fats cannot be negative")
        
        if self.carbohidratos is not None and self.carbohidratos < 0:
            raise ValueError("Carbohydrates cannot be negative")
        
        if self.fibra is not None and self.fibra < 0:
            raise ValueError("Fiber cannot be negative")
        
        if self.sodio is not None and self.sodio < 0:
            raise ValueError("Sodium cannot be negative")
        
        # Business rule: Basic calorie validation
        # Rough estimate: 4 cal/g protein, 4 cal/g carbs, 9 cal/g fat
        if self.grasas is not None and self.carbohidratos is not None:
            estimated_calories = (self.proteinas * 4) + (self.carbohidratos * 4) + (self.grasas * 9)
            # Allow 20% variance for estimation errors
            if abs(self.calorias - estimated_calories) > (estimated_calories * 0.2):
                raise ValueError("Calorie count doesn't match macronutrient breakdown")
    
    def es_alto_en_proteinas(self) -> bool:
        """Check if item is high in protein (>20% of calories from protein)."""
        protein_calories = self.proteinas * 4
        return (protein_calories / self.calorias) > 0.20 if self.calorias > 0 else False
    
    def es_bajo_en_azucar(self) -> bool:
        """Check if item is low in sugar (<5g per serving)."""
        return self.azucares < 5.0
    
    def es_alto_en_fibra(self) -> bool:
        """Check if item is high in fiber (>5g per serving)."""
        return self.fibra is not None and self.fibra >= 5.0
    
    def __str__(self) -> str:
        return f"Calories: {self.calorias}, Protein: {self.proteinas}g, Sugar: {self.azucares}g"