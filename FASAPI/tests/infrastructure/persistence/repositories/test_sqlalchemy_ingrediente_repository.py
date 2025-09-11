"""
Tests for SqlAlchemyIngredienteRepository.
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.infrastructure.persistence.repositories.sqlalchemy_ingrediente_repository import SqlAlchemyIngredienteRepository
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.mappers.ingrediente_mapper import IngredienteMapper


class TestSqlAlchemyIngredienteRepository:
    """Test cases for SqlAlchemyIngredienteRepository."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def mapper(self):
        """Create ingrediente mapper."""
        return IngredienteMapper()

    @pytest.fixture
    def repository(self, mock_session, mapper):
        """Create repository instance."""
        return SqlAlchemyIngredienteRepository(mock_session, mapper)

    @pytest.fixture
    def sample_ingrediente(self):
        """Create sample ingrediente entity."""
        precio = Precio(Decimal("2.50"))
        info_nutricional = InformacionNutricional(
            calorias=25,
            proteinas=Decimal("2.0"),
            azucares=Decimal("3.0"),
            grasas=Decimal("0.1"),
            carbohidratos=Decimal("5.0"),
            fibra=Decimal("2.5"),
            sodio=Decimal("5.0")
        )
        
        return Ingrediente(
            id=uuid4(),
            nombre="Tomate",
            descripcion="Fresh tomato",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=10,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN, EtiquetaItem.VEGANO],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            peso_unitario=Decimal("150.0"),
            unidad_medida="gramos",
            fecha_vencimiento=datetime.utcnow() + timedelta(days=7),
            proveedor="Fresh Farms",
            tipo=EtiquetaIngrediente.VERDURA
        )

    async def test_save_and_get_by_id(self, repository, mock_session, mapper, sample_ingrediente):
        """Test saving and retrieving ingrediente by ID."""
        # Mock the database operations
        mock_result = MagicMock()
        mock_model = IngredienteModel()
        mock_model.id = sample_ingrediente.id
        mock_model.nombre = sample_ingrediente.nombre
        mock_model.descripcion = sample_ingrediente.descripcion
        mock_model.precio = float(sample_ingrediente.precio.value)
        mock_model.calorias = sample_ingrediente.informacion_nutricional.calorias
        mock_model.proteinas = float(sample_ingrediente.informacion_nutricional.proteinas)
        mock_model.azucares = float(sample_ingrediente.informacion_nutricional.azucares)
        mock_model.grasas = float(sample_ingrediente.informacion_nutricional.grasas)
        mock_model.carbohidratos = float(sample_ingrediente.informacion_nutricional.carbohidratos)
        mock_model.fibra = float(sample_ingrediente.informacion_nutricional.fibra)
        mock_model.sodio = float(sample_ingrediente.informacion_nutricional.sodio)
        mock_model.tiempo_preparacion = sample_ingrediente.tiempo_preparacion
        mock_model.stock_actual = sample_ingrediente.stock_actual
        mock_model.stock_minimo = sample_ingrediente.stock_minimo
        mock_model.activo = sample_ingrediente.activo
        mock_model.etiquetas = [tag.value for tag in sample_ingrediente.etiquetas]
        mock_model.created_at = sample_ingrediente.created_at
        mock_model.updated_at = sample_ingrediente.updated_at
        mock_model.version = sample_ingrediente.version
        mock_model.peso_unitario = float(sample_ingrediente.peso_unitario)
        mock_model.unidad_medida = sample_ingrediente.unidad_medida
        mock_model.fecha_vencimiento = sample_ingrediente.fecha_vencimiento
        mock_model.proveedor = sample_ingrediente.proveedor
        mock_model.tipo = sample_ingrediente.tipo.value

        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result
        mock_session.refresh = AsyncMock()

        # Test save
        saved_ingrediente = await repository.save(sample_ingrediente)
        assert saved_ingrediente.id == sample_ingrediente.id
        assert saved_ingrediente.nombre == sample_ingrediente.nombre

        # Test get by ID
        retrieved_ingrediente = await repository.get_by_id(sample_ingrediente.id)
        assert retrieved_ingrediente is not None
        assert retrieved_ingrediente.id == sample_ingrediente.id
        assert retrieved_ingrediente.nombre == sample_ingrediente.nombre

    async def test_get_by_type(self, repository, mock_session):
        """Test getting ingredientes by type."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        ingredientes = await repository.get_by_type(EtiquetaIngrediente.VERDURA)
        assert isinstance(ingredientes, list)
        mock_session.execute.assert_called_once()

    async def test_check_stock(self, repository, mock_session, sample_ingrediente):
        """Test checking stock availability."""
        mock_result = MagicMock()
        mock_model = IngredienteModel()
        mock_model.stock_actual = 50
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        has_stock = await repository.check_stock(sample_ingrediente.id, Decimal("30.0"))
        assert has_stock is True

        has_stock = await repository.check_stock(sample_ingrediente.id, Decimal("60.0"))
        assert has_stock is False

    async def test_update_stock(self, repository, mock_session, sample_ingrediente):
        """Test updating stock."""
        mock_result = MagicMock()
        mock_model = IngredienteModel()
        mock_model.id = sample_ingrediente.id
        mock_model.stock_actual = 100
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        success = await repository.update_stock(sample_ingrediente.id, Decimal("20.0"))
        assert success is True
        assert mock_model.stock_actual == 120

    async def test_get_expiring_soon(self, repository, mock_session):
        """Test getting ingredientes expiring soon."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        ingredientes = await repository.get_expiring_soon(days=7)
        assert isinstance(ingredientes, list)
        mock_session.execute.assert_called_once()

    async def test_get_by_supplier(self, repository, mock_session):
        """Test getting ingredientes by supplier."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        ingredientes = await repository.get_by_supplier("Fresh Farms")
        assert isinstance(ingredientes, list)
        mock_session.execute.assert_called_once()

    async def test_exists_by_name(self, repository, mock_session):
        """Test checking if ingrediente exists by name."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = IngredienteModel()
        mock_session.execute.return_value = mock_result

        exists = await repository.exists_by_name("Tomate")
        assert exists is True

        mock_result.scalar_one_or_none.return_value = None
        exists = await repository.exists_by_name("NonExistent")
        assert exists is False

    async def test_delete(self, repository, mock_session, sample_ingrediente):
        """Test deleting ingrediente."""
        mock_result = MagicMock()
        mock_model = IngredienteModel()
        mock_result.scalar_one_or_none.return_value = mock_model
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_ingrediente.id)
        assert success is True
        mock_session.delete.assert_called_once_with(mock_model)
        mock_session.commit.assert_called_once()

    async def test_delete_not_found(self, repository, mock_session, sample_ingrediente):
        """Test deleting non-existent ingrediente."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        success = await repository.delete(sample_ingrediente.id)
        assert success is False
        mock_session.delete.assert_not_called()