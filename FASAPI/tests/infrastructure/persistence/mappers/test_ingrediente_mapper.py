"""Tests for IngredienteMapper."""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.mappers.ingrediente_mapper import IngredienteMapper


class TestIngredienteMapper:
    """Test cases for IngredienteMapper."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mapper = IngredienteMapper()
        self.ingrediente_id = uuid4()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.fecha_vencimiento = datetime.utcnow()
    
    def test_to_entity_converts_model_to_entity(self):
        """Test conversion from IngredienteModel to Ingrediente entity."""
        # Arrange
        model = IngredienteModel(
            id=self.ingrediente_id,
            nombre="Tomate",
            descripcion="Tomate fresco",
            precio=2.50,
            informacion_nutricional={
                'calorias': 18,
                'proteinas': 0.9,
                'azucares': 2.6
            },
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=20,
            etiquetas=['vegano', 'sin_gluten'],
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1,
            tipo_ingrediente='verdura',
            peso_unitario=150.0,
            unidad_medida='gramos',
            fecha_vencimiento=self.fecha_vencimiento,
            proveedor='Proveedor Test'
        )
        
        # Act
        entity = self.mapper.to_entity(model)
        
        # Assert
        assert isinstance(entity, Ingrediente)
        assert entity.id == self.ingrediente_id
        assert entity.nombre == "Tomate"
        assert entity.tipo == EtiquetaIngrediente.VERDURA
        assert entity.peso_unitario == 150.0
        assert entity.unidad_medida == 'gramos'
        assert entity.fecha_vencimiento == self.fecha_vencimiento
        assert entity.proveedor == 'Proveedor Test'
        assert EtiquetaItem.VEGANO in entity.etiquetas
    
    def test_to_model_converts_entity_to_model(self):
        """Test conversion from Ingrediente entity to IngredienteModel."""
        # Arrange
        entity = Ingrediente(
            id=self.ingrediente_id,
            nombre="Tomate",
            descripcion="Tomate fresco",
            precio=Precio(Decimal("2.50")),
            informacion_nutricional=InformacionNutricional(
                calorias=18,
                proteinas=0.9,
                azucares=2.6
            ),
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=20,
            etiquetas={EtiquetaItem.VEGANO, EtiquetaItem.SIN_GLUTEN},
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1,
            tipo=EtiquetaIngrediente.VERDURA,
            peso_unitario=150.0,
            unidad_medida='gramos',
            fecha_vencimiento=self.fecha_vencimiento,
            proveedor='Proveedor Test'
        )
        
        # Act
        model = self.mapper.to_model(entity)
        
        # Assert
        assert isinstance(model, IngredienteModel)
        assert model.id == self.ingrediente_id
        assert model.nombre == "Tomate"
        assert model.tipo_ingrediente == 'verdura'
        assert model.peso_unitario == 150.0
        assert model.unidad_medida == 'gramos'
        assert model.fecha_vencimiento == self.fecha_vencimiento
        assert model.proveedor == 'Proveedor Test'
        assert 'vegano' in model.etiquetas
    
    def test_bidirectional_mapping_preserves_data(self):
        """Test that converting entity->model->entity preserves data."""
        # Arrange
        original_entity = Ingrediente(
            id=self.ingrediente_id,
            nombre="Tomate",
            descripcion="Tomate fresco",
            precio=Precio(Decimal("2.50")),
            informacion_nutricional=InformacionNutricional(
                calorias=18,
                proteinas=0.9,
                azucares=2.6
            ),
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=20,
            etiquetas={EtiquetaItem.VEGANO},
            activo=True,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=1,
            tipo=EtiquetaIngrediente.VERDURA,
            peso_unitario=150.0,
            unidad_medida='gramos'
        )
        
        # Act
        model = self.mapper.to_model(original_entity)
        converted_entity = self.mapper.to_entity(model)
        
        # Assert
        assert converted_entity.id == original_entity.id
        assert converted_entity.tipo == original_entity.tipo
        assert converted_entity.peso_unitario == original_entity.peso_unitario
        assert converted_entity.unidad_medida == original_entity.unidad_medida