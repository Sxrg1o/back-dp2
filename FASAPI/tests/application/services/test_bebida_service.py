"""Unit tests for BebidaApplicationService."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.application.services.bebida_service import BebidaApplicationService
from app.application.dto.bebida_dto import CreateBebidaDTO, UpdateBebidaDTO
from app.application.dto.item_dto import InformacionNutricionalDTO
from app.domain.entities.bebida import Bebida
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.exceptions.menu_exceptions import (
    BebidaNotFoundError,
    BebidaAlreadyExistsError,
    InsufficientStockError
)


@pytest.fixture
def mock_bebida_repository():
    """Create mock bebida repository."""
    return AsyncMock()


@pytest.fixture
def bebida_service(mock_bebida_repository):
    """Create BebidaApplicationService with mocked dependencies."""
    return BebidaApplicationService(mock_bebida_repository)


@pytest.fixture
def sample_bebida():
    """Create sample bebida entity."""
    return Bebida(
        id=uuid4(),
        nombre="Coca Cola",
        descripcion="Refreshing cola drink",
        precio=Precio(Decimal("2.50")),
        informacion_nutricional=InformacionNutricional(
            calorias=140,
            proteinas=0.0,
            azucares=39.0,
            grasas=0.0,
            carbohidratos=39.0,
            fibra=0.0,
            sodio=45.0
        ),
        tiempo_preparacion=1,
        stock_actual=100,
        stock_minimo=20,
        etiquetas={EtiquetaItem.FRIO},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1,
        volumen=330.0,
        contenido_alcohol=0.0,
        temperatura_servicio="fria",
        tipo_bebida="gaseosa",
        marca="Coca Cola",
        origen="USA"
    )


@pytest.fixture
def sample_alcoholic_bebida():
    """Create sample alcoholic bebida entity."""
    return Bebida(
        id=uuid4(),
        nombre="Corona Beer",
        descripcion="Mexican lager beer",
        precio=Precio(Decimal("4.50")),
        informacion_nutricional=InformacionNutricional(
            calorias=148,
            proteinas=1.2,
            azucares=0.0,
            grasas=0.0,
            carbohidratos=13.9,
            fibra=0.0,
            sodio=10.0
        ),
        tiempo_preparacion=1,
        stock_actual=50,
        stock_minimo=10,
        etiquetas={EtiquetaItem.FRIO},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1,
        volumen=355.0,
        contenido_alcohol=4.5,
        temperatura_servicio="fria",
        tipo_bebida="cerveza",
        marca="Corona",
        origen="Mexico"
    )


@pytest.fixture
def create_bebida_dto():
    """Create sample CreateBebidaDTO."""
    return CreateBebidaDTO(
        nombre="Coca Cola",
        descripcion="Refreshing cola drink",
        precio=Decimal("2.50"),
        informacion_nutricional=InformacionNutricionalDTO(
            calorias=140,
            proteinas=0.0,
            azucares=39.0,
            grasas=0.0,
            carbohidratos=39.0,
            fibra=0.0,
            sodio=45.0
        ),
        tiempo_preparacion=1,
        stock_actual=100,
        stock_minimo=20,
        etiquetas={EtiquetaItem.FRIO},
        activo=True,
        volumen=330.0,
        contenido_alcohol=0.0,
        temperatura_servicio="fria",
        tipo_bebida="gaseosa",
        marca="Coca Cola",
        origen="USA"
    )


class TestBebidaApplicationService:
    """Test cases for BebidaApplicationService."""
    
    @pytest.mark.asyncio
    async def test_create_bebida_success(
        self, 
        bebida_service, 
        mock_bebida_repository, 
        create_bebida_dto, 
        sample_bebida
    ):
        """Test successful bebida creation."""
        # Arrange
        mock_bebida_repository.exists_by_name.return_value = False
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.create_bebida(create_bebida_dto)
        
        # Assert
        assert result.nombre == "Coca Cola"
        assert result.volumen == 330.0
        assert result.contenido_alcohol == 0.0
        mock_bebida_repository.exists_by_name.assert_called_once_with("Coca Cola")
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_bebida_already_exists(
        self, 
        bebida_service, 
        mock_bebida_repository,
        create_bebida_dto
    ):
        """Test bebida creation when name already exists."""
        # Arrange
        mock_bebida_repository.exists_by_name.return_value = True
        
        # Act & Assert
        with pytest.raises(BebidaAlreadyExistsError):
            await bebida_service.create_bebida(create_bebida_dto)
    
    @pytest.mark.asyncio
    async def test_get_bebida_by_id_success(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test successful bebida retrieval by ID."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act
        result = await bebida_service.get_bebida_by_id(bebida_id)
        
        # Assert
        assert result.id == bebida_id
        assert result.nombre == "Coca Cola"
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_get_bebida_by_id_not_found(
        self, 
        bebida_service, 
        mock_bebida_repository
    ):
        """Test bebida retrieval when not found."""
        # Arrange
        bebida_id = uuid4()
        mock_bebida_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(BebidaNotFoundError):
            await bebida_service.get_bebida_by_id(bebida_id)
    
    @pytest.mark.asyncio
    async def test_update_bebida_success(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test successful bebida update."""
        # Arrange
        bebida_id = sample_bebida.id
        update_dto = UpdateBebidaDTO(
            nombre="Updated Cola",
            precio=Decimal("3.00"),
            volumen=500.0
        )
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        mock_bebida_repository.exists_by_name.return_value = False
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.update_bebida(bebida_id, update_dto)
        
        # Assert
        assert result.id == bebida_id
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_available_bebidas(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting available bebidas."""
        # Arrange
        mock_bebida_repository.get_available.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_available_bebidas()
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Coca Cola"
        mock_bebida_repository.get_available.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_alcoholic_bebidas(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_alcoholic_bebida
    ):
        """Test getting alcoholic bebidas."""
        # Arrange
        mock_bebida_repository.get_alcoholic.return_value = [sample_alcoholic_bebida]
        
        # Act
        result = await bebida_service.get_alcoholic_bebidas()
        
        # Assert
        assert len(result) == 1
        assert result[0].contenido_alcohol > 0
        mock_bebida_repository.get_alcoholic.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_non_alcoholic_bebidas(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting non-alcoholic bebidas."""
        # Arrange
        mock_bebida_repository.get_non_alcoholic.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_non_alcoholic_bebidas()
        
        # Assert
        assert len(result) == 1
        assert result[0].contenido_alcohol == 0
        mock_bebida_repository.get_non_alcoholic.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_bebidas_by_volume_range(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting bebidas by volume range."""
        # Arrange
        mock_bebida_repository.get_by_volume_range.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_bebidas_by_volume_range(300.0, 400.0)
        
        # Assert
        assert len(result) == 1
        assert 300.0 <= result[0].volumen <= 400.0
        mock_bebida_repository.get_by_volume_range.assert_called_once_with(300.0, 400.0)
    
    @pytest.mark.asyncio
    async def test_get_bebidas_by_temperature(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting bebidas by temperature."""
        # Arrange
        mock_bebida_repository.get_by_temperature.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_bebidas_by_temperature("fria")
        
        # Assert
        assert len(result) == 1
        assert result[0].temperatura_servicio == "fria"
        mock_bebida_repository.get_by_temperature.assert_called_once_with("fria")
    
    @pytest.mark.asyncio
    async def test_get_bebidas_by_temperature_invalid(
        self, 
        bebida_service
    ):
        """Test getting bebidas by invalid temperature."""
        # Act & Assert
        with pytest.raises(ValueError):
            await bebida_service.get_bebidas_by_temperature("invalid")
    
    @pytest.mark.asyncio
    async def test_get_bebidas_by_brand(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting bebidas by brand."""
        # Arrange
        mock_bebida_repository.get_by_brand.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_bebidas_by_brand("Coca Cola")
        
        # Assert
        assert len(result) == 1
        assert result[0].marca == "Coca Cola"
        mock_bebida_repository.get_by_brand.assert_called_once_with("Coca Cola")
    
    @pytest.mark.asyncio
    async def test_check_stock_success(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test checking bebida stock."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act
        result = await bebida_service.check_stock(bebida_id)
        
        # Assert
        assert result == 100
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_check_stock_not_found(
        self, 
        bebida_service, 
        mock_bebida_repository
    ):
        """Test checking stock for non-existent bebida."""
        # Arrange
        bebida_id = uuid4()
        mock_bebida_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(BebidaNotFoundError):
            await bebida_service.check_stock(bebida_id)
    
    @pytest.mark.asyncio
    async def test_update_stock_increase(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test increasing bebida stock."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.update_stock(bebida_id, 50, "aumentar")
        
        # Assert
        assert result.id == bebida_id
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_stock_reduce_success(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test reducing bebida stock successfully."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.update_stock(bebida_id, 30, "reducir")
        
        # Assert
        assert result.id == bebida_id
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_stock_insufficient(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test reducing more stock than available."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act & Assert
        with pytest.raises(InsufficientStockError):
            await bebida_service.update_stock(bebida_id, 150, "reducir")  # More than 100 available
    
    @pytest.mark.asyncio
    async def test_update_stock_invalid_operation(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test stock update with invalid operation."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act & Assert
        with pytest.raises(ValueError):
            await bebida_service.update_stock(bebida_id, 50, "invalid")
    
    @pytest.mark.asyncio
    async def test_verify_age_restriction_alcoholic(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_alcoholic_bebida
    ):
        """Test age restriction verification for alcoholic beverage."""
        # Arrange
        bebida_id = sample_alcoholic_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_alcoholic_bebida
        
        # Act
        result = await bebida_service.verify_age_restriction(bebida_id)
        
        # Assert
        assert result is True
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_verify_age_restriction_non_alcoholic(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test age restriction verification for non-alcoholic beverage."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act
        result = await bebida_service.verify_age_restriction(bebida_id)
        
        # Assert
        assert result is False
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_calculate_alcohol_content(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_alcoholic_bebida
    ):
        """Test calculating alcohol content."""
        # Arrange
        bebida_id = sample_alcoholic_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_alcoholic_bebida
        
        # Act
        result = await bebida_service.calculate_alcohol_content(bebida_id)
        
        # Assert
        expected_alcohol = (355.0 * 4.5) / 100  # volume * percentage / 100
        assert result == expected_alcohol
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_calculate_price_per_ml(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test calculating price per milliliter."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        
        # Act
        result = await bebida_service.calculate_price_per_ml(bebida_id)
        
        # Assert
        expected_price_per_ml = float(sample_bebida.precio.value) / sample_bebida.volumen
        assert result == expected_price_per_ml
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_get_bebidas_suitable_for_minors(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting beverages suitable for minors."""
        # Arrange
        mock_bebida_repository.get_non_alcoholic.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_bebidas_suitable_for_minors()
        
        # Assert
        assert len(result) == 1
        assert result[0].contenido_alcohol == 0
        mock_bebida_repository.get_non_alcoholic.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_activate_bebida(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test activating a bebida."""
        # Arrange
        bebida_id = sample_bebida.id
        sample_bebida.activo = False
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.activate_bebida(bebida_id)
        
        # Assert
        assert result.id == bebida_id
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_deactivate_bebida(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test deactivating a bebida."""
        # Arrange
        bebida_id = sample_bebida.id
        mock_bebida_repository.get_by_id.return_value = sample_bebida
        mock_bebida_repository.save.return_value = sample_bebida
        
        # Act
        result = await bebida_service.deactivate_bebida(bebida_id)
        
        # Assert
        assert result.id == bebida_id
        mock_bebida_repository.get_by_id.assert_called_once_with(bebida_id)
        mock_bebida_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_bebida_success(
        self, 
        bebida_service, 
        mock_bebida_repository
    ):
        """Test successful bebida deletion."""
        # Arrange
        bebida_id = uuid4()
        mock_bebida_repository.delete.return_value = True
        
        # Act
        result = await bebida_service.delete_bebida(bebida_id)
        
        # Assert
        assert result is True
        mock_bebida_repository.delete.assert_called_once_with(bebida_id)
    
    @pytest.mark.asyncio
    async def test_get_all_bebidas(
        self, 
        bebida_service, 
        mock_bebida_repository,
        sample_bebida
    ):
        """Test getting all bebidas."""
        # Arrange
        mock_bebida_repository.get_all.return_value = [sample_bebida]
        
        # Act
        result = await bebida_service.get_all_bebidas()
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Coca Cola"
        mock_bebida_repository.get_all.assert_called_once()