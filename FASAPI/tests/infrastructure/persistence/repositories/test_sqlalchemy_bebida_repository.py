"""
Tests for SqlAlchemyBebidaRepository.
"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.bebida import Bebida
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.repositories.sqlalchemy_bebida_repository import SqlAlchemyBebidaRepository
from app.infrastructure.persistence.models.bebida_model import BebidaModel
from app.infrastructure.persistence.mappers.bebida_mapper import BebidaMapper


class TestSqlAlchemyBebidaRepository:
    """Test cases for SqlAlchemyBebidaRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def mapper(self):
        """Create bebida mapper."""
        return BebidaMapper()

    @pytest.fixture
    def repository(self, mock_session):
        """Create repository instance."""
        return SqlAlchemyBebidaRepository(mock_session)

    @pytest.fixture
    def sample_bebida(self):
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

    async def test_save_and_get_by_id(self, repository, mock_session, mapper, sample_bebida):
        """Test saving and retrieving bebida by ID."""
        # Mock the database operations
        mock_result = MagicMock()
        mock_model = BebidaModel()
        mock_model.id = sample_bebida.id
        mock_model.nombre = sample_bebida.nombre
        mock_model.descripcion = sample_bebida.descripcion
        mock_model.precio = float(sample_bebida.precio.value)
        mock_model.calorias = sample_bebida.informacion_nutricional.calorias
        mock_model.proteinas = float(sample_bebida.informacion_nutricional.proteinas)
        mock_model.azucares = float(sample_bebida.informacion_nutricional.azucares)
        mock_model.grasas = float(sample_bebida.informacion_nutricional.grasas)
        mock_model.carbohidratos = float(sample_bebida.informacion_nutricional.carbohidratos)
        mock_model.fibra = float(sample_bebida.informacion_nutricional.fibra)
        mock_model.sodio = float(sample_bebida.informacion_nutricional.sodio)
        mock_model.tiempo_preparacion = sample_bebida.tiempo_preparacion
        mock_model.stock_actual = sample_bebida.stock_actual
        mock_model.stock_minimo = sample_bebida.stock_minimo
        mock_model.activo = sample_bebida.activo
        mock_model.etiquetas = [tag.value for tag in sample_bebida.etiquetas]
        mock_model.created_at = sample_bebida.created_at
        mock_model.updated_at = sample_bebida.updated_at
        mock_model.version = sample_bebida.version
        mock_model.volumen = float(sample_bebida.volumen)
        mock_model.contenido_alcohol = float(sample_bebida.contenido_alcohol)
        mock_model.temperatura_servicio = sample_bebida.temperatura_servicio
        mock_model.tipo_bebida = sample_bebida.tipo_bebida
        mock_model.marca = sample_bebida.marca
        mock_model.origen = sample_bebida.origen

        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result
        mock_session.refresh = AsyncMock()

        # Test save
        saved_bebida = await repository.save(sample_bebida)
        assert saved_bebida.id == sample_bebida.id
        assert saved_bebida.nombre == sample_bebida.nombre

        # Test get by ID
        retrieved_bebida = await repository.get_by_id(sample_bebida.id)
        assert retrieved_bebida is not None
        assert retrieved_bebida.id == sample_bebida.id
        assert retrieved_bebida.nombre == sample_bebida.nombre

    async def test_get_alcoholic(self, repository, mock_session):
        """Test getting alcoholic bebidas."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_alcoholic()
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_non_alcoholic(self, repository, mock_session):
        """Test getting non-alcoholic bebidas."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_non_alcoholic()
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_brand(self, repository, mock_session):
        """Test getting bebidas by brand."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_brand("Coca Cola")
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_type(self, repository, mock_session):
        """Test getting bebidas by type."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_type("gaseosa")
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_temperature(self, repository, mock_session):
        """Test getting bebidas by serving temperature."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_temperature("fria")
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_origin(self, repository, mock_session):
        """Test getting bebidas by origin."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_origin("USA")
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_available_bebidas(self, repository, mock_session):
        """Test getting available bebidas."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_available_bebidas()
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_exists_by_name(self, repository, mock_session):
        """Test checking if bebida exists by name."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = BebidaModel()
        mock_session.execute.return_value = mock_result

        exists = await repository.exists_by_name("Coca Cola")
        assert exists is True

        mock_result.scalar_one_or_none.return_value = None
        exists = await repository.exists_by_name("NonExistent")
        assert exists is False

    async def test_delete(self, repository, mock_session, sample_bebida):
        """Test deleting bebida."""
        mock_result = MagicMock()
        mock_model = BebidaModel()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_bebida.id)
        assert success is True
        mock_session.delete.assert_called_once_with(mock_model)
        mock_session.commit.assert_called_once()

    async def test_delete_not_found(self, repository, mock_session, sample_bebida):
        """Test deleting non-existent bebida."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_bebida.id)
        assert success is False
        mock_session.delete.assert_not_called()

    async def test_get_by_alcohol_range(self, repository, mock_session):
        """Test getting bebidas by alcohol content range."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_alcohol_range(Decimal("0.0"), Decimal("5.0"))
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_volume_range(self, repository, mock_session):
        """Test getting bebidas by volume range."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_by_volume_range(Decimal("200.0"), Decimal("500.0"))
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()

    async def test_get_premium_bebidas(self, repository, mock_session):
        """Test getting premium bebidas (by price threshold)."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        bebidas = await repository.get_premium_bebidas(Decimal("10.00"))
        assert isinstance(bebidas, list)
        mock_session.execute.assert_called_once()