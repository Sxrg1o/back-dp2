"""Tests for ItemMapper."""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.models.item_model import ItemModel
from app.infrastructure.persistence.mappers.item_mapper import ItemMapper


class TestItemMapper:
    """Test cases for ItemMapper."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mapper = ItemMapper()
        self.item_id = uuid4()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def test_to_entity_converts_model_to_entity(self):
        """Test conversion from ItemModel to Item entity."""
        # Arrange
        model = ItemModel(
            id=self.item_id,
            nombre="Test Item",
            descripcion="Test description",
            precio=15.99,
            informacion_nutricional={
                'calorias': 250,
                'proteinas': 12.5,
                'azucares': 5.0,
                'grasas': 8.0,
                'carbohidratos': 30.0,
                'fibra': 3.0,
                'sodio': 500.0
            },
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=10,
            etiquetas=['sin_gluten', 'vegano'],
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1
        )
        
        # Act
        entity = self.mapper.to_entity(model)
        
        # Assert
        assert isinstance(entity, Item)
        assert entity.id == self.item_id
        assert entity.nombre == "Test Item"
        assert entity.descripcion == "Test description"
        assert entity.precio == Precio(Decimal("15.99"))
        assert entity.informacion_nutricional.calorias == 250
        assert entity.informacion_nutricional.proteinas == 12.5
        assert entity.tiempo_preparacion == 10
        assert entity.stock_actual == 50
        assert entity.stock_minimo == 10
        assert EtiquetaItem.SIN_GLUTEN in entity.etiquetas
        assert EtiquetaItem.VEGANO in entity.etiquetas
        assert entity.activo is True
        assert entity.version == 1
    
    def test_to_model_converts_entity_to_model(self):
        """Test conversion from Item entity to ItemModel."""
        # Arrange
        informacion_nutricional = InformacionNutricional(
            calorias=250,
            proteinas=12.5,
            azucares=5.0,
            grasas=8.0,
            carbohidratos=30.0,
            fibra=3.0,
            sodio=500.0
        )
        
        entity = Item(
            id=self.item_id,
            nombre="Test Item",
            descripcion="Test description",
            precio=Precio(Decimal("15.99")),
            informacion_nutricional=informacion_nutricional,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=10,
            etiquetas={EtiquetaItem.SIN_GLUTEN, EtiquetaItem.VEGANO},
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1
        )
        
        # Act
        model = self.mapper.to_model(entity)
        
        # Assert
        assert isinstance(model, ItemModel)
        assert model.id == self.item_id
        assert model.nombre == "Test Item"
        assert model.descripcion == "Test description"
        assert model.precio == 15.99
        assert model.informacion_nutricional['calorias'] == 250
        assert model.informacion_nutricional['proteinas'] == 12.5
        assert model.tiempo_preparacion == 10
        assert model.stock_actual == 50
        assert model.stock_minimo == 10
        assert 'sin_gluten' in model.etiquetas
        assert 'vegano' in model.etiquetas
        assert model.activo is True
        assert model.version == 1
    
    def test_bidirectional_mapping_preserves_data(self):
        """Test that converting entity->model->entity preserves data."""
        # Arrange
        original_entity = Item(
            id=self.item_id,
            nombre="Test Item",
            descripcion="Test description",
            precio=Precio(Decimal("15.99")),
            informacion_nutricional=InformacionNutricional(
                calorias=250,
                proteinas=12.5,
                azucares=5.0
            ),
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=10,
            etiquetas={EtiquetaItem.SIN_GLUTEN},
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1
        )
        
        # Act
        model = self.mapper.to_model(original_entity)
        converted_entity = self.mapper.to_entity(model)
        
        # Assert
        assert converted_entity.id == original_entity.id
        assert converted_entity.nombre == original_entity.nombre
        assert converted_entity.precio == original_entity.precio
        assert converted_entity.etiquetas == original_entity.etiquetas
        assert converted_entity.activo == original_entity.activo