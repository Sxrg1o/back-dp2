"""
Tests for PlatoMapper.
"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.plato import Plato
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.infrastructure.persistence.models.plato_model import PlatoModel
from app.infrastructure.persistence.mappers.plato_mapper import PlatoMapper


class TestPlatoMapper:
    """Test cases for PlatoMapper."""

    @pytest.fixture
    def mapper(self):
        """Create mapper instance."""
        return PlatoMapper()

    @pytest.fixture
    def sample_entity(self):
        """Create sample plato entity."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        return Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta with bacon and cream",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas=[EtiquetaItem.CON_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={uuid4(): Decimal("200.0"), uuid4(): Decimal("100.0")},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta, add sauce",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )

    @pytest.fixture
    def sample_model(self, sample_entity):
        """Create sample plato model."""
        model = PlatoModel()
        model.id = sample_entity.id
        model.nombre = sample_entity.nombre
        model.descripcion = sample_entity.descripcion
        model.precio = float(sample_entity.precio.value)
        model.calorias = sample_entity.informacion_nutricional.calorias
        model.proteinas = float(sample_entity.informacion_nutricional.proteinas)
        model.azucares = float(sample_entity.informacion_nutricional.azucares)
        model.grasas = float(sample_entity.informacion_nutricional.grasas)
        model.carbohidratos = float(sample_entity.informacion_nutricional.carbohidratos)
        model.fibra = float(sample_entity.informacion_nutricional.fibra)
        model.sodio = float(sample_entity.informacion_nutricional.sodio)
        model.tiempo_preparacion = sample_entity.tiempo_preparacion
        model.stock_actual = sample_entity.stock_actual
        model.stock_minimo = sample_entity.stock_minimo
        model.activo = sample_entity.activo
        model.etiquetas = [tag.value for tag in sample_entity.etiquetas]
        model.created_at = sample_entity.created_at
        model.updated_at = sample_entity.updated_at
        model.version = sample_entity.version
        model.receta = {str(k): float(v) for k, v in sample_entity.receta.items()}
        model.tipo_plato = sample_entity.tipo_plato.value
        model.instrucciones = sample_entity.instrucciones
        model.dificultad = sample_entity.dificultad
        model.chef_recomendado = sample_entity.chef_recomendado
        return model

    def test_to_entity_converts_model_to_entity(self, mapper, sample_model):
        """Test converting model to entity."""
        entity = mapper.to_entity(sample_model)
        
        assert isinstance(entity, Plato)
        assert entity.id == sample_model.id
        assert entity.nombre == sample_model.nombre
        assert entity.descripcion == sample_model.descripcion
        assert entity.precio.value == Decimal(str(sample_model.precio))
        assert entity.informacion_nutricional.calorias == sample_model.calorias
        assert entity.informacion_nutricional.proteinas == Decimal(str(sample_model.proteinas))
        assert entity.tiempo_preparacion == sample_model.tiempo_preparacion
        assert entity.stock_actual == sample_model.stock_actual
        assert entity.stock_minimo == sample_model.stock_minimo
        assert entity.activo == sample_model.activo
        assert entity.created_at == sample_model.created_at
        assert entity.updated_at == sample_model.updated_at
        assert entity.version == sample_model.version
        assert entity.tipo_plato.value == sample_model.tipo_plato
        assert entity.instrucciones == sample_model.instrucciones
        assert entity.dificultad == sample_model.dificultad
        assert entity.chef_recomendado == sample_model.chef_recomendado

    def test_to_model_converts_entity_to_model(self, mapper, sample_entity):
        """Test converting entity to model."""
        model = mapper.to_model(sample_entity)
        
        assert isinstance(model, PlatoModel)
        assert model.id == sample_entity.id
        assert model.nombre == sample_entity.nombre
        assert model.descripcion == sample_entity.descripcion
        assert Decimal(str(model.precio)) == sample_entity.precio.value
        assert model.calorias == sample_entity.informacion_nutricional.calorias
        assert Decimal(str(model.proteinas)) == sample_entity.informacion_nutricional.proteinas
        assert model.tiempo_preparacion == sample_entity.tiempo_preparacion
        assert model.stock_actual == sample_entity.stock_actual
        assert model.stock_minimo == sample_entity.stock_minimo
        assert model.activo == sample_entity.activo
        assert model.created_at == sample_entity.created_at
        assert model.updated_at == sample_entity.updated_at
        assert model.version == sample_entity.version
        assert model.tipo_plato == sample_entity.tipo_plato.value
        assert model.instrucciones == sample_entity.instrucciones
        assert model.dificultad == sample_entity.dificultad
        assert model.chef_recomendado == sample_entity.chef_recomendado

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
        assert converted_entity.tipo_plato == sample_entity.tipo_plato
        assert converted_entity.instrucciones == sample_entity.instrucciones
        assert converted_entity.dificultad == sample_entity.dificultad
        assert converted_entity.chef_recomendado == sample_entity.chef_recomendado

    def test_etiquetas_mapping(self, mapper, sample_entity):
        """Test that etiquetas are properly mapped."""
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        assert len(converted_entity.etiquetas) == len(sample_entity.etiquetas)
        for original_tag, converted_tag in zip(sample_entity.etiquetas, converted_entity.etiquetas):
            assert original_tag == converted_tag

    def test_receta_mapping(self, mapper, sample_entity):
        """Test that receta is properly mapped."""
        model = mapper.to_model(sample_entity)
        converted_entity = mapper.to_entity(model)
        
        assert len(converted_entity.receta) == len(sample_entity.receta)
        # Note: UUID keys are converted to strings in the model, so we can't do direct comparison
        # but we can verify the values are preserved
        assert sum(converted_entity.receta.values()) == sum(sample_entity.receta.values())

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