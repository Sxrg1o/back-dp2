"""Tests for ItemApplicationService."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

from app.application.services.item_service import ItemApplicationService
from app.application.dto.item_dto import CreateItemDTO, UpdateItemDTO, InformacionNutricionalDTO
from app.domain.entities.item import Item
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.exceptions.menu_exceptions import ItemNotFoundError, ItemAlreadyExistsError


@pytest.fixture
def mock_item_repository():
    """Create mock item repository."""
    return AsyncMock()


@pytest.fixture
def item_service(mock_item_repository):
    """Create ItemApplicationService with mocked repository."""
    return ItemApplicationService(mock_item_repository)


@pytest.fixture
def sample_nutritional_dto():
    """Create sample nutritional DTO."""
    return InformacionNutricionalDTO(
        calorias=250,
        proteinas=15.0,
        azucares=5.0,
        grasas=10.0,
        carbohidratos=30.0
    )


@pytest.fixture
def sample_create_dto(sample_nutritional_dto):
    """Create sample CreateItemDTO."""
    return CreateItemDTO(
        nombre="Test Item",
        descripcion="Test description",
        precio=Decimal("15.99"),
        informacion_nutricional=sample_nutritional_dto,
        tiempo_preparacion=10,
        stock_actual=50,
        stock_minimo=5,
        etiquetas={EtiquetaItem.VEGANO},
        activo=True
    )


@pytest.fixture
def sample_item():
    """Create sample Item domain entity."""
    return Item(
        id=uuid4(),
        nombre="Test Item",
        descripcion="Test description",
        precio=Precio.from_float(15.99),
        informacion_nutricional=InformacionNutricional(
            calorias=250,
            proteinas=15.0,
            azucares=5.0,
            grasas=10.0,
            carbohidratos=30.0
        ),
        tiempo_preparacion=10,
        stock_actual=50,
        stock_minimo=5,
        etiquetas={EtiquetaItem.VEGANO},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1
    )


class TestItemApplicationService:
    """Test ItemApplicationService methods."""
    
    @pytest.mark.asyncio
    async def test_create_item_success(self, item_service, mock_item_repository, sample_create_dto, sample_item):
        """Test successful item creation."""
        # Arrange
        mock_item_repository.exists_by_name.return_value = False
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.create_item(sample_create_dto)
        
        # Assert
        assert result.nombre == "Test Item"
        assert result.precio == Decimal("15.99")
        assert result.activo is True
        mock_item_repository.exists_by_name.assert_called_once_with("Test Item")
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_item_name_already_exists(self, item_service, mock_item_repository, sample_create_dto):
        """Test item creation with existing name raises error."""
        # Arrange
        mock_item_repository.exists_by_name.return_value = True
        
        # Act & Assert
        with pytest.raises(ItemAlreadyExistsError) as exc_info:
            await item_service.create_item(sample_create_dto)
        
        assert "Test Item" in str(exc_info.value)
        mock_item_repository.exists_by_name.assert_called_once_with("Test Item")
        mock_item_repository.save.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_item_by_id_success(self, item_service, mock_item_repository, sample_item):
        """Test successful item retrieval by ID."""
        # Arrange
        item_id = sample_item.id
        mock_item_repository.get_by_id.return_value = sample_item
        
        # Act
        result = await item_service.get_item_by_id(item_id)
        
        # Assert
        assert result.id == item_id
        assert result.nombre == "Test Item"
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
    
    @pytest.mark.asyncio
    async def test_get_item_by_id_not_found(self, item_service, mock_item_repository):
        """Test item retrieval with non-existent ID raises error."""
        # Arrange
        item_id = uuid4()
        mock_item_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ItemNotFoundError) as exc_info:
            await item_service.get_item_by_id(item_id)
        
        assert str(item_id) in str(exc_info.value)
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
    
    @pytest.mark.asyncio
    async def test_update_item_success(self, item_service, mock_item_repository, sample_item, sample_nutritional_dto):
        """Test successful item update."""
        # Arrange
        item_id = sample_item.id
        update_dto = UpdateItemDTO(
            nombre="Updated Item",
            precio=Decimal("20.99"),
            informacion_nutricional=sample_nutritional_dto
        )
        
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.exists_by_name.return_value = False
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.update_item(item_id, update_dto)
        
        # Assert
        assert result.id == item_id
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_item_not_found(self, item_service, mock_item_repository):
        """Test item update with non-existent ID raises error."""
        # Arrange
        item_id = uuid4()
        update_dto = UpdateItemDTO(nombre="Updated Item")
        mock_item_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(ItemNotFoundError) as exc_info:
            await item_service.update_item(item_id, update_dto)
        
        assert str(item_id) in str(exc_info.value)
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_item_name_already_exists(self, item_service, mock_item_repository, sample_item):
        """Test item update with existing name raises error."""
        # Arrange
        item_id = sample_item.id
        update_dto = UpdateItemDTO(nombre="Existing Item")
        
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.exists_by_name.return_value = True
        
        # Act & Assert
        with pytest.raises(ItemAlreadyExistsError) as exc_info:
            await item_service.update_item(item_id, update_dto)
        
        assert "Existing Item" in str(exc_info.value)
        mock_item_repository.exists_by_name.assert_called_once_with("Existing Item")
        mock_item_repository.save.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_available_items(self, item_service, mock_item_repository, sample_item):
        """Test getting available items."""
        # Arrange
        mock_item_repository.get_available_items.return_value = [sample_item]
        
        # Act
        result = await item_service.get_available_items()
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Test Item"
        mock_item_repository.get_available_items.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_check_stock(self, item_service, mock_item_repository, sample_item):
        """Test checking item stock."""
        # Arrange
        item_id = sample_item.id
        mock_item_repository.get_by_id.return_value = sample_item
        
        # Act
        result = await item_service.check_stock(item_id)
        
        # Assert
        assert result == 50
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
    
    @pytest.mark.asyncio
    async def test_update_stock_increase(self, item_service, mock_item_repository, sample_item):
        """Test increasing item stock."""
        # Arrange
        item_id = sample_item.id
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.update_stock(item_id, 25, "aumentar")
        
        # Assert
        assert result.id == item_id
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_stock_decrease(self, item_service, mock_item_repository, sample_item):
        """Test decreasing item stock."""
        # Arrange
        item_id = sample_item.id
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.update_stock(item_id, 10, "reducir")
        
        # Assert
        assert result.id == item_id
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_activate_item(self, item_service, mock_item_repository, sample_item):
        """Test activating an item."""
        # Arrange
        item_id = sample_item.id
        sample_item.activo = False
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.activate_item(item_id)
        
        # Assert
        assert result.id == item_id
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_deactivate_item(self, item_service, mock_item_repository, sample_item):
        """Test deactivating an item."""
        # Arrange
        item_id = sample_item.id
        mock_item_repository.get_by_id.return_value = sample_item
        mock_item_repository.save.return_value = sample_item
        
        # Act
        result = await item_service.deactivate_item(item_id)
        
        # Assert
        assert result.id == item_id
        mock_item_repository.get_by_id.assert_called_once_with(item_id)
        mock_item_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_item(self, item_service, mock_item_repository):
        """Test deleting an item."""
        # Arrange
        item_id = uuid4()
        mock_item_repository.delete.return_value = True
        
        # Act
        result = await item_service.delete_item(item_id)
        
        # Assert
        assert result is True
        mock_item_repository.delete.assert_called_once_with(item_id)
    
    @pytest.mark.asyncio
    async def test_get_items_by_category(self, item_service, mock_item_repository, sample_item):
        """Test getting items by category."""
        # Arrange
        etiqueta = EtiquetaItem.VEGANO
        mock_item_repository.get_by_category.return_value = [sample_item]
        
        # Act
        result = await item_service.get_items_by_category(etiqueta)
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Test Item"
        mock_item_repository.get_by_category.assert_called_once_with(etiqueta)
    
    @pytest.mark.asyncio
    async def test_get_low_stock_items(self, item_service, mock_item_repository, sample_item):
        """Test getting low stock items."""
        # Arrange
        mock_item_repository.get_low_stock_items.return_value = [sample_item]
        
        # Act
        result = await item_service.get_low_stock_items()
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Test Item"
        mock_item_repository.get_low_stock_items.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_items_by_price_range(self, item_service, mock_item_repository, sample_item):
        """Test getting items by price range."""
        # Arrange
        min_price = 10.0
        max_price = 20.0
        mock_item_repository.get_by_price_range.return_value = [sample_item]
        
        # Act
        result = await item_service.get_items_by_price_range(min_price, max_price)
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Test Item"
        mock_item_repository.get_by_price_range.assert_called_once_with(min_price, max_price)