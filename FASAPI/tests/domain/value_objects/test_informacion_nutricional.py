"""Tests for InformacionNutricional value object."""

import pytest
from app.domain.value_objects.informacion_nutricional import InformacionNutricional


class TestInformacionNutricional:
    """Test cases for InformacionNutricional value object."""
    
    def test_valid_informacion_nutricional_creation(self):
        """Test creating valid InformacionNutricional instances."""
        # Test with required fields only
        info1 = InformacionNutricional(calorias=250, proteinas=15.0, azucares=5.0)
        assert info1.calorias == 250
        assert info1.proteinas == 15.0
        assert info1.azucares == 5.0
        
        # Test with all fields
        info2 = InformacionNutricional(
            calorias=300,
            proteinas=20.0,
            azucares=8.0,
            grasas=12.0,
            carbohidratos=35.0,
            fibra=6.0,
            sodio=450.0
        )
        assert info2.calorias == 300
        assert info2.grasas == 12.0
        assert info2.fibra == 6.0
    
    def test_invalid_negative_calorias(self):
        """Test that negative calories raise ValueError."""
        with pytest.raises(ValueError, match="Calories cannot be negative"):
            InformacionNutricional(calorias=-100, proteinas=10.0, azucares=5.0)
    
    def test_invalid_negative_proteinas(self):
        """Test that negative proteins raise ValueError."""
        with pytest.raises(ValueError, match="Proteins cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=-5.0, azucares=5.0)
    
    def test_invalid_negative_azucares(self):
        """Test that negative sugars raise ValueError."""
        with pytest.raises(ValueError, match="Sugars cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=10.0, azucares=-2.0)
    
    def test_invalid_negative_optional_fields(self):
        """Test that negative optional fields raise ValueError."""
        # Test negative fats
        with pytest.raises(ValueError, match="Fats cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, grasas=-3.0)
        
        # Test negative carbohydrates
        with pytest.raises(ValueError, match="Carbohydrates cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, carbohidratos=-10.0)
        
        # Test negative fiber
        with pytest.raises(ValueError, match="Fiber cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, fibra=-2.0)
        
        # Test negative sodium
        with pytest.raises(ValueError, match="Sodium cannot be negative"):
            InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, sodio=-100.0)
    
    def test_calorie_validation_with_macronutrients(self):
        """Test calorie validation against macronutrient breakdown."""
        # Valid case: 20g protein (80 cal) + 30g carbs (120 cal) + 10g fat (90 cal) = 290 cal
        # Allow 20% variance, so 290 ± 58 calories is acceptable
        info = InformacionNutricional(
            calorias=300,  # Within acceptable range
            proteinas=20.0,
            azucares=5.0,
            grasas=10.0,
            carbohidratos=30.0
        )
        assert info.calorias == 300
    
    def test_invalid_calorie_validation(self):
        """Test that invalid calorie counts raise ValueError."""
        # Invalid case: macronutrients suggest ~290 calories, but claiming 500
        with pytest.raises(ValueError, match="Calorie count doesn't match macronutrient breakdown"):
            InformacionNutricional(
                calorias=500,  # Too high compared to macronutrients
                proteinas=20.0,
                azucares=5.0,
                grasas=10.0,
                carbohidratos=30.0
            )
    
    def test_es_alto_en_proteinas(self):
        """Test high protein detection."""
        # High protein: 25g protein (100 cal) out of 400 total = 25% > 20%
        info_high = InformacionNutricional(calorias=400, proteinas=25.0, azucares=5.0)
        assert info_high.es_alto_en_proteinas() is True
        
        # Low protein: 10g protein (40 cal) out of 400 total = 10% < 20%
        info_low = InformacionNutricional(calorias=400, proteinas=10.0, azucares=5.0)
        assert info_low.es_alto_en_proteinas() is False
        
        # Edge case: zero calories
        info_zero = InformacionNutricional(calorias=0, proteinas=0.0, azucares=0.0)
        assert info_zero.es_alto_en_proteinas() is False
    
    def test_es_bajo_en_azucar(self):
        """Test low sugar detection."""
        # Low sugar: <5g
        info_low = InformacionNutricional(calorias=200, proteinas=10.0, azucares=3.0)
        assert info_low.es_bajo_en_azucar() is True
        
        # High sugar: >=5g
        info_high = InformacionNutricional(calorias=200, proteinas=10.0, azucares=8.0)
        assert info_high.es_bajo_en_azucar() is False
        
        # Edge case: exactly 5g
        info_edge = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0)
        assert info_edge.es_bajo_en_azucar() is False
    
    def test_es_alto_en_fibra(self):
        """Test high fiber detection."""
        # High fiber: >=5g
        info_high = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, fibra=6.0)
        assert info_high.es_alto_en_fibra() is True
        
        # Low fiber: <5g
        info_low = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, fibra=3.0)
        assert info_low.es_alto_en_fibra() is False
        
        # No fiber data
        info_none = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0)
        assert info_none.es_alto_en_fibra() is False
        
        # Edge case: exactly 5g
        info_edge = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0, fibra=5.0)
        assert info_edge.es_alto_en_fibra() is True
    
    def test_informacion_nutricional_immutability(self):
        """Test that InformacionNutricional is immutable."""
        info = InformacionNutricional(calorias=200, proteinas=10.0, azucares=5.0)
        with pytest.raises(AttributeError):
            info.calorias = 300
    
    def test_string_representation(self):
        """Test string representation of InformacionNutricional."""
        info = InformacionNutricional(calorias=250, proteinas=15.0, azucares=8.0)
        expected = "Calories: 250, Protein: 15.0g, Sugar: 8.0g"
        assert str(info) == expected