"""
Tests for BebidaMapper.
"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.bebida import Bebida
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.models.bebida_model import BebidaModel
from app.infrastructure.persistence.mappers.bebida_mapper import BebidaMapper


class TestBebidaMapper:
    """Test cases for BebidaMapper."""

    @pytest.fixture
    def mapper(self):
        """Create mapper instance."""
        return BebidaMapper()

    @pytest.fixture
    def sample_entity(self):
        """Create sample bebida entity."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        return Bebida(
            id=uuid4(),
            nombre="Coca Cola",
            descripcion="Refreshing cola drink",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=2,
            stock_actual=50,
            stock_minimo=10,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("330.0"),
            contenido_alcohol=Decimal("0.0"),
            temperatura_servicio="fria",
            tipo_bebida="gaseosa",
            marca="Coca Cola",
            origen="USA"
        )

    @pytest.fixture
    def sample_model(self, sample_entity):
        """Create sample bebida model."""
        model = BebidaModel()
        model.id = sample_entity.id
        model.nombre = sample_entity.nombre
        model.descripcion = sample_entity.descripcion
        model.precio = float(sample_entity.precio.value)
        model.informacion_nutricional = {
            'calorias': sample_entity.informacion_nutricional.calorias,
            'proteinas': float(sample_entity.informacion_nutricional.proteinas),
            'azucares': float(sample_entity.informacion_nutricional.azucares),
            'grasas': float(sample_entity.informacion_nutricional.grasas),
            'carbohidratos': float(sample_entity.informacion_nutricional.carbohidratos),
            'fibra': float(sample_entity.informacion_nutricional.fibra),
            'sodio': float(sample_entity.informacion_nutricional.sodio)
        }
        model.tiempo_preparacion = sample_entity.tiempo_preparacion
        model.stock_actual = sample_entity.stock_actual
        model.stock_minimo = sample_entity.stock_minimo
        model.activo = sample_entity.activo
        model.etiquetas = [tag.value for tag in sample_entity.etiquetas]
        model.created_at = sample_entity.created_at
        model.updated_at = sample_entity.updated_at
        model.version = sample_entity.version
        model.volumen = float(sample_entity.volumen)
        model.contenido_alcohol = float(sample_entity.contenido_alcohol)
        model.temperatura_servicio = sample_entity.temperatura_servicio
        model.tipo_bebida = sample_entity.tipo_bebida
        model.marca = sample_entity.marca
        model.origen = sample_entity.origen
        return model

    def test_to_entity_converts_model_to_entity(self, mapper, sample_model):
        """Test converting model to entity."""
        entity = mapper.to_entity(sample_model)
        
        assert isinstance(entity, Bebida)
        assert entity.id == sample_model.id
        assert entity.nombre == sample_model.nombre
        assert entity.descripcion == sample_model.descripcion
        assert entity.precio.value == Decimal(str(sample_model.precio))
        assert entity.informacion_nutricional.calorias == sample_model.informacion_nutricional['calorias']
        assert entity.informacion_nutricional.proteinas == Decimal(str(sample_model.informacion_nutricional['proteinas']))
        assert entity.tiempo_preparacion == sample_model.tiempo_preparacion
        assert entity.stock_actual == sample_model.stock_actual
        assert entity.stock_minimo == sample_model.stock_minimo
        assert entity.activo == sample_model.activo
        assert entity.created_at == sample_model.created_at
        assert entity.updated_at == sample_model.updated_at
        assert entity.version == sample_model.version
        assert entity.volumen == Decimal(str(sample_model.volumen))
        assert entity.contenido_alcohol == Decimal(str(sample_model.contenido_alcohol))
        assert entity.temperatura_servicio == sample_model.temperatura_servicio
        assert entity.tipo_bebida == sample_model.tipo_bebida
        assert entity.marca == sample_model.marca
        assert entity.origen == sample_model.origen

    def test_to_model_converts_entity_to_model(self, mapper, sample_entity):
        """Test converting entity to model."""
        model = mapper.to_model(sample_entity)
        
        assert isinstance(model, BebidaModel)
        assert model.id == sample_entity.id
        assert model.nombre == sample_entity.nombre
        assert model.descripcion == sample_entity.descripcion
        assert Decimal(str(model.precio)) == sample_entity.precio.value
        assert model.informacion_nutricional['calorias'] == sample_entity.informacion_nutricional.calorias
        assert Decimal(str(model.informacion_nutricional['proteinas'])) == sample_entity.informacion_nutricional.proteinas
        assert model.tiempo_preparacion == sample_entity.tiempo_preparacion
        assert model.stock_actual == sample_entity.stock_actual
        assert model.stock_minimo == sample_entity.stock_minimo
        assert model.activo == sample_entity.activo
        assert model.created_at == sample_entity.created_at
        assert model.updated_at == sample_entity.updated_at
        assert model.version == sample_entity.version
        assert Decimal(str(model.volumen)) == sample_entity.volumen
        assert Decimal(str(model.contenido_alcohol)) == sample_entity.contenido_alcohol
        assert model.temperatura_servicio == sample_entity.temperatura_servicio
        assert model.tipo_bebida == sample_entity.tipo_bebida
        assert model.marca == sample_entity.marca
        assert model.origen == sample_entity.origen

    def test_bidirectional_mapping_preserves_data(self, mapper, sample_entity):
        """Test that converting entity->model->entity preserves data."""
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        assert converted_entity.id == sample_entity.id
        assert converted_entity.nombre == sample_entity.nombre
        assert converted_entity.descripcion == sample_entity.descripcion
        assert converted_entity.precio.value == sample_entity.precio.value
        assert converted_entity.informacion_nutricional.calorias == sample_entity.informacion_nutricional.calorias
        assert converted_entity.tiempo_preparacion == sample_entity.tiempo_preparacion
        assert converted_entity.stock_actual == sample_entity.stock_actual
        assert converted_entity.stock_minimo == sample_entity.stock_minimo
        assert converted_entity.activo == sample_entity.activo
        assert converted_entity.version == sample_entity.version
        assert converted_entity.volumen == sample_entity.volumen
        assert converted_entity.contenido_alcohol == sample_entity.contenido_alcohol
        assert converted_entity.temperatura_servicio == sample_entity.temperatura_servicio
        assert converted_entity.tipo_bebida == sample_entity.tipo_bebida
        assert converted_entity.marca == sample_entity.marca
        assert converted_entity.origen == sample_entity.origen

    def test_etiquetas_mapping(self, mapper, sample_entity):
        """Test that etiquetas are properly mapped."""
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        assert len(converted_entity.etiquetas) == len(sample_entity.etiquetas)
        for original_tag, converted_tag in zip(sample_entity.etiquetas, converted_entity.etiquetas):
            assert original_tag == converted_tag

    def test_informacion_nutricional_mapping(self, mapper, sample_entity):
        """Test that nutritional information is properly mapped."""
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        original_info = sample_entity.informacion_nutricional
        converted_info = converted_entity.informacion_nutricional
        
        assert converted_info.calorias == original_info.calorias
        assert converted_info.proteinas == original_info.proteinas
        assert converted_info.azucares == original_info.azucares
        assert converted_info.grasas == original_info.grasas
        assert converted_info.carbohidratos == original_info.carbohidratos
        assert converted_info.fibra == original_info.fibra
        assert converted_info.sodio == original_info.sodio

    def test_alcoholic_bebida_mapping(self, mapper):
        """Test mapping of alcoholic bebida."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=0,
            proteinas=Decimal("0.0"),
            azucares=Decimal("0.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("0.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("0.0")
        )
        
        alcoholic_bebida = Bebida(
            id=uuid4(),
            nombre="Beer",
            descripcion="Cold beer",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=1,
            stock_actual=30,
            stock_minimo=5,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("500.0"),
            contenido_alcohol=Decimal("5.0"),
            temperatura_servicio="fria",
            tipo_bebida="cerveza",
            marca="Beer Brand",
            origen="Germany"
        )
        
        model = mapper.to_model(alcoholic_bebida)
        converted_entity = mapper.to_entity(model)
        
        assert converted_entity.contenido_alcohol == Decimal("5.0")
        assert converted_entity.is_alcoholic() is True

    def test_volume_precision_mapping(self, mapper, sample_entity):
        """Test that volume precision is preserved in mapping."""
        # Test with precise decimal volume
        sample_entity.volumen = Decimal("330.50")
        
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        # Note: Due to float conversion, we might lose some precision
        # but it should be close enough for practical purposes
        assert abs(converted_entity.volumen - sample_entity.volumen) < Decimal("0.01")