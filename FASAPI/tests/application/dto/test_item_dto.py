"""Tests for Item DTOs."""

import pytest
from decimal import Decimal
from pydantic import ValidationError

from app.application.dto.item_dto import (
    CreateItemDTO,
    UpdateItemDTO,
    InformacionNutricionalDTO
)
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestInformacionNutricionalDTO:
    """Test InformacionNutricionalDTO validation."""
    
    def test_valid_nutritional_info(self):
        """Test valid nutritional information."""
        dto = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0,
            grasas=10.0,
            carbohidratos=30.0,
            fibra=3.0,
            sodio=500.0
        )
        
        assert dto.calorias == 250
        assert dto.proteinas == 15.5
        assert dto.azucares == 5.0
    
    def test_negative_calories_raises_error(self):
        """Test that negative calories raise validation error."""
        with pytest.raises(ValidationError) as exc_info:
            InformacionNutricionalDTO(
                calorias=-100,
                proteinas=15.5,
                azucares=5.0
            )
        
        assert "Input should be greater than or equal to 0" in str(exc_info.value)
    
    def test_negative_proteins_raises_error(self):
        """Test that negative proteins raise validation error."""
        with pytest.raises(ValidationError) as exc_info:
            InformacionNutricionalDTO(
                calorias=250,
                proteinas=-5.0,
                azucares=5.0
            )
        
        assert "Input should be greater than or equal to 0" in str(exc_info.value)
    
    def test_calorie_consistency_validation(self):
        """Test calorie consistency with macronutrients."""
        # This should pass (rough calculation: 10*4 + 20*4 + 5*9 = 165, 200 is within 20% variance)
        dto = InformacionNutricionalDTO(
            calorias=200,
            proteinas=10.0,
            azucares=5.0,
            grasas=5.0,
            carbohidratos=20.0
        )
        assert dto.calorias == 200


class TestCreateItemDTO:
    """Test CreateItemDTO validation."""
    
    def test_valid_create_item_dto(self):
        """Test valid item creation DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        dto = CreateItemDTO(
            nombre="Test Item",
            descripcion="Test description",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5,
            etiquetas={EtiquetaItem.VEGANO, EtiquetaItem.SIN_GLUTEN},
            activo=True
        )
        
        assert dto.nombre == "Test Item"
        assert dto.precio == Decimal("15.99")
        assert dto.stock_actual == 50
        assert "vegano" in dto.etiquetas
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateItemDTO(
                nombre="",
                precio=Decimal("15.99"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=10,
                stock_actual=50,
                stock_minimo=5
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_negative_price_raises_error(self):
        """Test that negative price raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateItemDTO(
                nombre="Test Item",
                precio=Decimal("-5.99"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=10,
                stock_actual=50,
                stock_minimo=5
            )
        
        assert "Input should be greater than 0" in str(exc_info.value)
    
    def test_negative_stock_raises_error(self):
        """Test that negative stock raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateItemDTO(
                nombre="Test Item",
                precio=Decimal("15.99"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=10,
                stock_actual=-10,
                stock_minimo=5
            )
        
        assert "Input should be greater than or equal to 0" in str(exc_info.value)
    
    def test_minimum_stock_greater_than_current_raises_error(self):
        """Test that minimum stock greater than current stock raises error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateItemDTO(
                nombre="Test Item",
                precio=Decimal("15.99"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=10,
                stock_actual=5,
                stock_minimo=10
            )
        
        assert "Minimum stock cannot be greater than current stock" in str(exc_info.value)
    
    def test_whitespace_name_is_trimmed(self):
        """Test that whitespace in name is trimmed."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=5.0
        )
        
        dto = CreateItemDTO(
            nombre="  Test Item  ",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5
        )
        
        assert dto.nombre == "Test Item"


class TestUpdateItemDTO:
    """Test UpdateItemDTO validation."""
    
    def test_valid_update_item_dto(self):
        """Test valid item update DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=300,
            proteinas=20.0,
            azucares=8.0
        )
        
        dto = UpdateItemDTO(
            nombre="Updated Item",
            precio=Decimal("18.99"),
            informacion_nutricional=nutritional_info,
            activo=False
        )
        
        assert dto.nombre == "Updated Item"
        assert dto.precio == Decimal("18.99")
        assert dto.activo is False
    
    def test_partial_update_dto(self):
        """Test partial update with only some fields."""
        dto = UpdateItemDTO(
            nombre="Updated Name",
            activo=False
        )
        
        assert dto.nombre == "Updated Name"
        assert dto.precio is None
        assert dto.activo is False
    
    def test_empty_name_in_update_raises_error(self):
        """Test that empty name in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateItemDTO(nombre="")
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_none_values_are_allowed(self):
        """Test that None values are allowed in update DTO."""
        dto = UpdateItemDTO()
        
        assert dto.nombre is None
        assert dto.precio is None
        assert dto.activo is None