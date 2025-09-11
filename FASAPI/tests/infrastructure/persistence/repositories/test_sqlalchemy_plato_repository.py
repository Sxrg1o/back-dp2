"""
Tests for SqlAlchemyPlatoRepository.
"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.plato import Plato
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.infrastructure.persistence.repositories.sqlalchemy_plato_repository import SqlAlchemyPlatoRepository
from app.infrastructure.persistence.models.plato_model import PlatoModel
from app.infrastructure.persistence.mappers.plato_mapper import PlatoMapper


class TestSqlAlchemyPlatoRepository:
    """Test cases for SqlAlchemyPlatoRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def mapper(self):
        """Create plato mapper."""
        return PlatoMapper()

    @pytest.fixture
    def repository(self, mock_session, mapper):
        """Create repository instance."""
        return SqlAlchemyPlatoRepository(mock_session, mapper)

    @pytest.fixture
    def sample_plato(self):
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

    async def test_save_and_get_by_id(self, repository, mock_session, mapper, sample_plato):
        """Test saving and retrieving plato by ID."""
        # Mock the database operations
        mock_result = MagicMock()
        mock_model = PlatoModel()
        mock_model.id = sample_plato.id
        mock_model.nombre = sample_plato.nombre
        mock_model.descripcion = sample_plato.descripcion
        mock_model.precio = float(sample_plato.precio.value)
        mock_model.calorias = sample_plato.informacion_nutricional.calorias
        mock_model.proteinas = float(sample_plato.informacion_nutricional.proteinas)
        mock_model.azucares = float(sample_plato.informacion_nutricional.azucares)
        mock_model.grasas = float(sample_plato.informacion_nutricional.grasas)
        mock_model.carbohidratos = float(sample_plato.informacion_nutricional.carbohidratos)
        mock_model.fibra = float(sample_plato.informacion_nutricional.fibra)
        mock_model.sodio = float(sample_plato.informacion_nutricional.sodio)
        mock_model.tiempo_preparacion = sample_plato.tiempo_preparacion
        mock_model.stock_actual = sample_plato.stock_actual
        mock_model.stock_minimo = sample_plato.stock_minimo
        mock_model.activo = sample_plato.activo
        mock_model.etiquetas = [tag.value for tag in sample_plato.etiquetas]
        mock_model.created_at = sample_plato.created_at
        mock_model.updated_at = sample_plato.updated_at
        mock_model.version = sample_plato.version
        mock_model.receta = {str(k): float(v) for k, v in sample_plato.receta.items()}
        mock_model.tipo_plato = sample_plato.tipo_plato.value
        mock_model.instrucciones = sample_plato.instrucciones
        mock_model.dificultad = sample_plato.dificultad
        mock_model.chef_recomendado = sample_plato.chef_recomendado

        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result
        mock_session.refresh = AsyncMock()

        # Test save
        saved_plato = await repository.save(sample_plato)
        assert saved_plato.id == sample_plato.id
        assert saved_plato.nombre == sample_plato.nombre

        # Test get by ID
        retrieved_plato = await repository.get_by_id(sample_plato.id)
        assert retrieved_plato is not None
        assert retrieved_plato.id == sample_plato.id
        assert retrieved_plato.nombre == sample_plato.nombre

    async def test_get_by_dish_type(self, repository, mock_session):
        """Test getting platos by dish type."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        platos = await repository.get_by_dish_type(EtiquetaPlato.FONDO)
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_get_with_ingredients(self, repository, mock_session, sample_plato):
        """Test getting platos with their ingredients."""
        mock_result = MagicMock()
        mock_model = PlatoModel()
        mock_model.id = sample_plato.id
        mock_model.receta = {str(k): float(v) for k, v in sample_plato.receta.items()}
        mock_result.scalars.return_value.all.return_value = [mock_model]
        mock_session.execute.return_value = mock_result

        platos = await repository.get_with_ingredients()
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_difficulty(self, repository, mock_session):
        """Test getting platos by difficulty."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        platos = await repository.get_by_difficulty("medio")
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_chef(self, repository, mock_session):
        """Test getting platos by chef."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        platos = await repository.get_by_chef("Chef Mario")
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_get_available_platos(self, repository, mock_session):
        """Test getting available platos."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        platos = await repository.get_available_platos()
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_exists_by_name(self, repository, mock_session):
        """Test checking if plato exists by name."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = PlatoModel()
        mock_session.execute.return_value = mock_result

        exists = await repository.exists_by_name("Pasta Carbonara")
        assert exists is True

        mock_result.scalar_one_or_none.return_value = None
        exists = await repository.exists_by_name("NonExistent")
        assert exists is False

    async def test_delete(self, repository, mock_session, sample_plato):
        """Test deleting plato."""
        mock_result = MagicMock()
        mock_model = PlatoModel()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_plato.id)
        assert success is True
        mock_session.delete.assert_called_once_with(mock_model)
        mock_session.commit.assert_called_once()

    async def test_delete_not_found(self, repository, mock_session, sample_plato):
        """Test deleting non-existent plato."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_plato.id)
        assert success is False
        mock_session.delete.assert_not_called()

    async def test_search_by_ingredients(self, repository, mock_session):
        """Test searching platos by ingredients."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        ingredient_ids = [uuid4(), uuid4()]
        platos = await repository.search_by_ingredients(ingredient_ids)
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()

    async def test_get_popular_platos(self, repository, mock_session):
        """Test getting popular platos (by stock turnover)."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        platos = await repository.get_popular_platos(limit=10)
        assert isinstance(platos, list)
        mock_session.execute.assert_called_once()