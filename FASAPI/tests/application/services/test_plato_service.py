"""Unit tests for PlatoApplicationService."""

import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.application.services.plato_service import PlatoApplicationService
from app.application.dto.plato_dto import (
    CreatePlatoDTO,
    UpdatePlatoDTO,
    AgregarIngredienteRecetaDTO,
    ActualizarIngredienteRecetaDTO
)
from app.application.dto.item_dto import InformacionNutricionalDTO
from app.domain.entities.plato import Plato
from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.exceptions.menu_exceptions import (
    PlatoNotFoundError,
    PlatoAlreadyExistsError,
    IngredienteNotFoundError
)


@pytest.fixture
def mock_plato_repository():
    """Create mock plato repository."""
    return AsyncMock()


@pytest.fixture
def mock_ingrediente_repository():
    """Create mock ingrediente repository."""
    return AsyncMock()


@pytest.fixture
def plato_service(mock_plato_repository, mock_ingrediente_repository):
    """Create PlatoApplicationService with mocked dependencies."""
    return PlatoApplicationService(mock_plato_repository, mock_ingrediente_repository)


@pytest.fixture
def sample_plato():
    """Create sample plato entity."""
    return Plato(
        id=uuid4(),
        nombre="Pasta Carbonara",
        descripcion="Delicious pasta with bacon and eggs",
        precio=Precio(Decimal("15.99")),
        informacion_nutricional=InformacionNutricional(
            calorias=450,
            proteinas=20.0,
            azucares=5.0,
            grasas=15.0,
            carbohidratos=60.0,
            fibra=3.0,
            sodio=800.0
        ),
        tiempo_preparacion=25,
        stock_actual=10,
        stock_minimo=2,
        etiquetas={EtiquetaItem.CALIENTE},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1,
        tipo_plato=EtiquetaPlato.FONDO,
        receta={},
        instrucciones="Cook pasta, mix with sauce",
        porciones=2,
        dificultad="medio",
        chef_recomendado="Chef Mario"
    )


@pytest.fixture
def sample_ingrediente():
    """Create sample ingrediente entity."""
    return Ingrediente(
        id=uuid4(),
        nombre="Bacon",
        descripcion="Premium bacon strips",
        precio=Precio(Decimal("8.50")),
        informacion_nutricional=InformacionNutricional(
            calorias=150,
            proteinas=12.0,
            azucares=0.0,
            grasas=12.0,
            carbohidratos=0.0,
            fibra=0.0,
            sodio=600.0
        ),
        tiempo_preparacion=5,
        stock_actual=50,
        stock_minimo=10,
        etiquetas={EtiquetaItem.SALADO},
        activo=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        version=1,
        tipo=EtiquetaIngrediente.CARNE,
        peso_unitario=100.0,
        unidad_medida="gramos",
        fecha_vencimiento=None,
        proveedor="Meat Co."
    )


@pytest.fixture
def create_plato_dto():
    """Create sample CreatePlatoDTO."""
    return CreatePlatoDTO(
        nombre="Pasta Carbonara",
        descripcion="Delicious pasta with bacon and eggs",
        precio=Decimal("15.99"),
        informacion_nutricional=InformacionNutricionalDTO(
            calorias=450,
            proteinas=20.0,
            azucares=5.0,
            grasas=15.0,
            carbohidratos=60.0,
            fibra=3.0,
            sodio=800.0
        ),
        tiempo_preparacion=25,
        stock_actual=10,
        stock_minimo=2,
        etiquetas={EtiquetaItem.CALIENTE},
        activo=True,
        tipo_plato=EtiquetaPlato.FONDO,
        receta={},
        instrucciones="Cook pasta, mix with sauce",
        porciones=2,
        dificultad="medio",
        chef_recomendado="Chef Mario"
    )


class TestPlatoApplicationService:
    """Test cases for PlatoApplicationService."""
    
    @pytest.mark.asyncio
    async def test_create_plato_success(
        self, 
        plato_service, 
        mock_plato_repository, 
        mock_ingrediente_repository,
        create_plato_dto, 
        sample_plato
    ):
        """Test successful plato creation."""
        # Arrange
        mock_plato_repository.exists_by_name.return_value = False
        mock_plato_repository.save.return_value = sample_plato
        
        # Act
        result = await plato_service.create_plato(create_plato_dto)
        
        # Assert
        assert result.nombre == "Pasta Carbonara"
        assert result.tipo_plato == EtiquetaPlato.FONDO
        assert result.porciones == 2
        mock_plato_repository.exists_by_name.assert_called_once_with("Pasta Carbonara")
        mock_plato_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_plato_already_exists(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        create_plato_dto
    ):
        """Test plato creation when name already exists."""
        # Arrange
        mock_plato_repository.exists_by_name.return_value = True
        
        # Act & Assert
        with pytest.raises(PlatoAlreadyExistsError):
            await plato_service.create_plato(create_plato_dto)
    
    @pytest.mark.asyncio
    async def test_create_plato_with_recipe_ingredient_not_found(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        create_plato_dto
    ):
        """Test plato creation with non-existent ingredient in recipe."""
        # Arrange
        ingrediente_id = uuid4()
        create_plato_dto.receta = {ingrediente_id: 100.0}
        mock_plato_repository.exists_by_name.return_value = False
        mock_ingrediente_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(IngredienteNotFoundError):
            await plato_service.create_plato(create_plato_dto)
    
    @pytest.mark.asyncio
    async def test_get_plato_by_id_success(
        self, 
        plato_service, 
        mock_plato_repository,
        sample_plato
    ):
        """Test successful plato retrieval by ID."""
        # Arrange
        plato_id = sample_plato.id
        mock_plato_repository.get_by_id.return_value = sample_plato
        
        # Act
        result = await plato_service.get_plato_by_id(plato_id)
        
        # Assert
        assert result.id == plato_id
        assert result.nombre == "Pasta Carbonara"
        mock_plato_repository.get_by_id.assert_called_once_with(plato_id)
    
    @pytest.mark.asyncio
    async def test_get_plato_by_id_not_found(
        self, 
        plato_service, 
        mock_plato_repository
    ):
        """Test plato retrieval when not found."""
        # Arrange
        plato_id = uuid4()
        mock_plato_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(PlatoNotFoundError):
            await plato_service.get_plato_by_id(plato_id)
    
    @pytest.mark.asyncio
    async def test_update_plato_success(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        sample_plato
    ):
        """Test successful plato update."""
        # Arrange
        plato_id = sample_plato.id
        update_dto = UpdatePlatoDTO(
            nombre="Updated Pasta",
            precio=Decimal("18.99"),
            porciones=3
        )
        mock_plato_repository.get_by_id.return_value = sample_plato
        mock_plato_repository.exists_by_name.return_value = False
        mock_plato_repository.save.return_value = sample_plato
        
        # Act
        result = await plato_service.update_plato(plato_id, update_dto)
        
        # Assert
        assert result.id == plato_id
        mock_plato_repository.get_by_id.assert_called_once_with(plato_id)
        mock_plato_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_available_platos(
        self, 
        plato_service, 
        mock_plato_repository,
        sample_plato
    ):
        """Test getting available platos."""
        # Arrange
        mock_plato_repository.get_available.return_value = [sample_plato]
        
        # Act
        result = await plato_service.get_available_platos()
        
        # Assert
        assert len(result) == 1
        assert result[0].nombre == "Pasta Carbonara"
        mock_plato_repository.get_available.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_platos_by_dish_type(
        self, 
        plato_service, 
        mock_plato_repository,
        sample_plato
    ):
        """Test getting platos by dish type."""
        # Arrange
        mock_plato_repository.get_by_dish_type.return_value = [sample_plato]
        
        # Act
        result = await plato_service.get_platos_by_dish_type(EtiquetaPlato.FONDO)
        
        # Assert
        assert len(result) == 1
        assert result[0].tipo_plato == EtiquetaPlato.FONDO
        mock_plato_repository.get_by_dish_type.assert_called_once_with(EtiquetaPlato.FONDO)
    
    @pytest.mark.asyncio
    async def test_agregar_ingrediente_receta_success(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        sample_plato,
        sample_ingrediente
    ):
        """Test adding ingredient to recipe."""
        # Arrange
        plato_id = sample_plato.id
        ingrediente_id = sample_ingrediente.id
        agregar_dto = AgregarIngredienteRecetaDTO(
            ingrediente_id=ingrediente_id,
            cantidad=150.0
        )
        mock_plato_repository.get_by_id.return_value = sample_plato
        mock_ingrediente_repository.get_by_id.return_value = sample_ingrediente
        mock_plato_repository.save.return_value = sample_plato
        
        # Act
        result = await plato_service.agregar_ingrediente_receta(plato_id, agregar_dto)
        
        # Assert
        assert result.id == plato_id
        mock_plato_repository.get_by_id.assert_called_once_with(plato_id)
        mock_ingrediente_repository.get_by_id.assert_called_once_with(ingrediente_id)
        mock_plato_repository.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_agregar_ingrediente_receta_plato_not_found(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository
    ):
        """Test adding ingredient to non-existent plato."""
        # Arrange
        plato_id = uuid4()
        ingrediente_id = uuid4()
        agregar_dto = AgregarIngredienteRecetaDTO(
            ingrediente_id=ingrediente_id,
            cantidad=150.0
        )
        mock_plato_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(PlatoNotFoundError):
            await plato_service.agregar_ingrediente_receta(plato_id, agregar_dto)
    
    @pytest.mark.asyncio
    async def test_agregar_ingrediente_receta_ingrediente_not_found(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        sample_plato
    ):
        """Test adding non-existent ingredient to recipe."""
        # Arrange
        plato_id = sample_plato.id
        ingrediente_id = uuid4()
        agregar_dto = AgregarIngredienteRecetaDTO(
            ingrediente_id=ingrediente_id,
            cantidad=150.0
        )
        mock_plato_repository.get_by_id.return_value = sample_plato
        mock_ingrediente_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(IngredienteNotFoundError):
            await plato_service.agregar_ingrediente_receta(plato_id, agregar_dto)
    
    @pytest.mark.asyncio
    async def test_verificar_disponibilidad_ingredientes_success(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        sample_plato,
        sample_ingrediente
    ):
        """Test verifying ingredient availability."""
        # Arrange
        plato_id = sample_plato.id
        ingrediente_id = sample_ingrediente.id
        sample_plato.receta = {ingrediente_id: 50.0}  # Need 50g, have 50 in stock
        mock_plato_repository.get_by_id.return_value = sample_plato
        mock_ingrediente_repository.get_by_id.return_value = sample_ingrediente
        
        # Act
        result = await plato_service.verificar_disponibilidad_ingredientes(plato_id)
        
        # Assert
        assert result is True
        mock_plato_repository.get_by_id.assert_called_once_with(plato_id)
        mock_ingrediente_repository.get_by_id.assert_called_once_with(ingrediente_id)
    
    @pytest.mark.asyncio
    async def test_calcular_costo_ingredientes_success(
        self, 
        plato_service, 
        mock_plato_repository,
        mock_ingrediente_repository,
        sample_plato,
        sample_ingrediente
    ):
        """Test calculating ingredient costs."""
        # Arrange
        plato_id = sample_plato.id
        ingrediente_id = sample_ingrediente.id
        sample_plato.receta = {ingrediente_id: 100.0}  # Need 100g
        mock_plato_repository.get_by_id.return_value = sample_plato
        mock_ingrediente_repository.get_by_id.return_value = sample_ingrediente
        
        # Act
        result = await plato_service.calcular_costo_ingredientes(plato_id)
        
        # Assert
        assert isinstance(result, float)
        assert result > 0
        mock_plato_repository.get_by_id.assert_called_once_with(plato_id)
        mock_ingrediente_repository.get_by_id.assert_called_once_with(ingrediente_id)
    
    @pytest.mark.asyncio
    async def test_get_platos_by_difficulty(
        self, 
        plato_service, 
        mock_plato_repository,
        sample_plato
    ):
        """Test getting platos by difficulty."""
        # Arrange
        mock_plato_repository.get_by_difficulty.return_value = [sample_plato]
        
        # Act
        result = await plato_service.get_platos_by_difficulty("medio")
        
        # Assert
        assert len(result) == 1
        assert result[0].dificultad == "medio"
        mock_plato_repository.get_by_difficulty.assert_called_once_with("medio")
    
    @pytest.mark.asyncio
    async def test_get_platos_by_difficulty_invalid(
        self, 
        plato_service
    ):
        """Test getting platos by invalid difficulty."""
        # Act & Assert
        with pytest.raises(ValueError):
            await plato_service.get_platos_by_difficulty("invalid")
    
    @pytest.mark.asyncio
    async def test_delete_plato_success(
        self, 
        plato_service, 
        mock_plato_repository
    ):
        """Test successful plato deletion."""
        # Arrange
        plato_id = uuid4()
        mock_plato_repository.delete.return_value = True
        
        # Act
        result = await plato_service.delete_plato(plato_id)
        
        # Assert
        assert result is True
        mock_plato_repository.delete.assert_called_once_with(plato_id)