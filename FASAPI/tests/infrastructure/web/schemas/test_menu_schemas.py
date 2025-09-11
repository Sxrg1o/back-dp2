"""
Tests for menu API schemas.
"""
import pytest
from decimal import Decimal
from uuid import uuid4

from app.infrastructure.web.schemas.menu_schemas import (
    InformacionNutricionalSchema,
    ItemCreateSchema,
    ItemUpdateSchema,
    ItemResponseSchema,
    ItemListResponseSchema
)
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestInformacionNutricionalSchema:
    """Test nutritional information schema."""
    
    def test_valid_nutritional_info(self):
        """Test valid nutritional information."""
        schema = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2,
            grasas=8.0,
            carbohidratos=30.0,
            fibra=5.0,
            sodio=200.0
        )
        
        assert schema.calorias == 250
        assert schema.proteinas == 15.5
        assert schema.azucares == 10.2
        assert schema.grasas == 8.0
        assert schema.carbohidratos == 30.0
        assert schema.fibra == 5.0
        assert schema.sodio == 200.0
    
    def test_negative_values_rejected(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValueError):
            InformacionNutricionalSchema(
                calorias=-100,
                proteinas=15.5,
                azucares=10.2
            )
    
    def test_optional_fields(self):
        """Test that optional fields work correctly."""
        schema = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2
        )
        
        assert schema.calorias == 250
        assert schema.proteinas == 15.5
        assert schema.azucares == 10.2
        assert schema.grasas is None
        assert schema.carbohidratos is None
        assert schema.fibra is None
        assert schema.sodio is None


class TestItemCreateSchema:
    """Test item create schema."""
    
    def test_valid_item_create(self):
        """Test valid item creation."""
        nutritional_info = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2
        )
        
        schema = ItemCreateSchema(
            nombre="Test Item",
            descripcion="Test description",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5,
            etiquetas={EtiquetaItem.SIN_GLUTEN, EtiquetaItem.VEGANO},
            activo=True
        )
        
        assert schema.nombre == "Test Item"
        assert schema.descripcion == "Test description"
        assert schema.precio == Decimal("15.99")
        assert schema.tiempo_preparacion == 10
        assert schema.stock_actual == 50
        assert schema.stock_minimo == 5
        assert EtiquetaItem.SIN_GLUTEN in schema.etiquetas
        assert EtiquetaItem.VEGANO in schema.etiquetas
        assert schema.activo is True
    
    def test_empty_etiquetas_default(self):
        """Test that etiquetas defaults to empty set."""
        nutritional_info = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2
        )
        
        schema = ItemCreateSchema(
            nombre="Test Item",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5,
            activo=True
        )
        
        assert schema.etiquetas == set()


class TestItemUpdateSchema:
    """Test item update schema."""
    
    def test_all_fields_optional(self):
        """Test that all fields are optional in update schema."""
        schema = ItemUpdateSchema()
        
        assert schema.nombre is None
        assert schema.descripcion is None
        assert schema.precio is None
        assert schema.informacion_nutricional is None
        assert schema.tiempo_preparacion is None
        assert schema.stock_actual is None
        assert schema.stock_minimo is None
        assert schema.etiquetas is None
        assert schema.activo is None
    
    def test_partial_update(self):
        """Test partial update with some fields."""
        schema = ItemUpdateSchema(
            nombre="Updated Name",
            precio=Decimal("20.99"),
            activo=False
        )
        
        assert schema.nombre == "Updated Name"
        assert schema.precio == Decimal("20.99")
        assert schema.activo is False
        assert schema.descripcion is None


class TestItemResponseSchema:
    """Test item response schema."""
    
    def test_response_includes_audit_fields(self):
        """Test that response schema includes audit fields."""
        from datetime import datetime
        
        nutritional_info = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2
        )
        
        now = datetime.utcnow()
        item_id = uuid4()
        
        schema = ItemResponseSchema(
            id=item_id,
            nombre="Test Item",
            descripcion="Test description",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5,
            etiquetas={EtiquetaItem.SIN_GLUTEN},
            activo=True,
            created_at=now,
            updated_at=now,
            version=1
        )
        
        assert schema.id == item_id
        assert schema.created_at == now
        assert schema.updated_at == now
        assert schema.version == 1


class TestItemListResponseSchema:
    """Test item list response schema."""
    
    def test_list_response_minimal_fields(self):
        """Test that list response contains only essential fields."""
        item_id = uuid4()
        
        schema = ItemListResponseSchema(
            id=item_id,
            nombre="Test Item",
            precio=Decimal("15.99"),
            stock_actual=50,
            activo=True,
            etiquetas={EtiquetaItem.SIN_GLUTEN}
        )
        
        assert schema.id == item_id
        assert schema.nombre == "Test Item"
        assert schema.precio == Decimal("15.99")
        assert schema.stock_actual == 50
        assert schema.activo is True
        assert EtiquetaItem.SIN_GLUTEN in schema.etiquetas