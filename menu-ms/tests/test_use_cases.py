"""
Tests unitarios para los casos de uso.
"""

import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from domain.entities import Plato, Bebida, Ingrediente
from domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato
from domain.use_cases import (
    CreateItemUseCase, GetItemUseCase, GetAllItemsUseCase,
    CreateIngredienteUseCase, GetIngredienteUseCase
)


class TestCreateItemUseCase:
    """Tests para el caso de uso CreateItemUseCase."""
    
    def test_crear_plato_exitoso(self):
        """Test para crear un plato exitosamente."""
        # Arrange
        mock_repository = Mock()
        mock_repository.create.return_value = Plato(
            id=1,
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        use_case = CreateItemUseCase(mock_repository)
        plato = Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        # Act
        result = use_case.execute(plato)
        
        # Assert
        assert result.id == 1
        assert result.descripcion == "Pasta Carbonara"
        mock_repository.create.assert_called_once_with(plato)
    
    def test_crear_plato_descripcion_vacia(self):
        """Test para crear plato con descripción vacía (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = CreateItemUseCase(mock_repository)
        plato = Plato(
            descripcion="",  # Descripción vacía
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="La descripción del ítem es obligatoria"):
            use_case.execute(plato)
    
    def test_crear_plato_precio_negativo(self):
        """Test para crear plato con precio negativo (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = CreateItemUseCase(mock_repository)
        plato = Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('-10.0'),  # Precio negativo
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            use_case.execute(plato)
    
    def test_crear_bebida_litros_negativos(self):
        """Test para crear bebida con litros negativos (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = CreateItemUseCase(mock_repository)
        bebida = Bebida(
            descripcion="Coca Cola",
            precio=Decimal('3.50'),
            litros=Decimal('-0.5'),  # Litros negativos
            alcoholico=False
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Los litros de la bebida deben ser mayores a 0"):
            use_case.execute(bebida)


class TestGetItemUseCase:
    """Tests para el caso de uso GetItemUseCase."""
    
    def test_obtener_item_exitoso(self):
        """Test para obtener un ítem exitosamente."""
        # Arrange
        mock_repository = Mock()
        expected_item = Plato(
            id=1,
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        mock_repository.get_by_id.return_value = expected_item
        
        use_case = GetItemUseCase(mock_repository)
        
        # Act
        result = use_case.execute(1)
        
        # Assert
        assert result == expected_item
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_obtener_item_no_existe(self):
        """Test para obtener un ítem que no existe."""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.return_value = None
        
        use_case = GetItemUseCase(mock_repository)
        
        # Act
        result = use_case.execute(1)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_obtener_item_id_invalido(self):
        """Test para obtener ítem con ID inválido (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = GetItemUseCase(mock_repository)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El ID del ítem debe ser mayor a 0"):
            use_case.execute(0)
        
        with pytest.raises(ValueError, match="El ID del ítem debe ser mayor a 0"):
            use_case.execute(-1)


class TestGetAllItemsUseCase:
    """Tests para el caso de uso GetAllItemsUseCase."""
    
    def test_obtener_todos_items(self):
        """Test para obtener todos los ítems."""
        # Arrange
        mock_repository = Mock()
        expected_items = [
            Plato(id=1, descripcion="Pasta", precio=Decimal('10.0'), peso=Decimal('300.0')),
            Bebida(id=2, descripcion="Coca Cola", precio=Decimal('3.0'), litros=Decimal('0.5'))
        ]
        mock_repository.get_all.return_value = expected_items
        
        use_case = GetAllItemsUseCase(mock_repository)
        
        # Act
        result = use_case.execute()
        
        # Assert
        assert result == expected_items
        mock_repository.get_all.assert_called_once()
    
    def test_obtener_items_disponibles(self):
        """Test para obtener solo ítems disponibles."""
        # Arrange
        mock_repository = Mock()
        expected_items = [
            Plato(id=1, descripcion="Pasta", precio=Decimal('10.0'), peso=Decimal('300.0'), disponible=True)
        ]
        mock_repository.get_available.return_value = expected_items
        
        use_case = GetAllItemsUseCase(mock_repository)
        
        # Act
        result = use_case.execute(only_available=True)
        
        # Assert
        assert result == expected_items
        mock_repository.get_available.assert_called_once()
    
    def test_obtener_items_por_rango_precio(self):
        """Test para obtener ítems por rango de precios."""
        # Arrange
        mock_repository = Mock()
        expected_items = [
            Plato(id=1, descripcion="Pasta", precio=Decimal('10.0'), peso=Decimal('300.0'))
        ]
        mock_repository.get_by_price_range.return_value = expected_items
        
        use_case = GetAllItemsUseCase(mock_repository)
        
        # Act
        result = use_case.execute_by_price_range(Decimal('5.0'), Decimal('15.0'))
        
        # Assert
        assert result == expected_items
        mock_repository.get_by_price_range.assert_called_once_with(Decimal('5.0'), Decimal('15.0'))
    
    def test_obtener_items_por_rango_precio_invalido(self):
        """Test para obtener ítems por rango de precios inválido (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = GetAllItemsUseCase(mock_repository)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El precio mínimo no puede ser negativo"):
            use_case.execute_by_price_range(Decimal('-5.0'), Decimal('15.0'))
        
        with pytest.raises(ValueError, match="El precio mínimo no puede ser mayor al precio máximo"):
            use_case.execute_by_price_range(Decimal('20.0'), Decimal('15.0'))


class TestCreateIngredienteUseCase:
    """Tests para el caso de uso CreateIngredienteUseCase."""
    
    def test_crear_ingrediente_exitoso(self):
        """Test para crear un ingrediente exitosamente."""
        # Arrange
        mock_repository = Mock()
        expected_ingrediente = Ingrediente(
            id=1,
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        mock_repository.create.return_value = expected_ingrediente
        
        use_case = CreateIngredienteUseCase(mock_repository)
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        # Act
        result = use_case.execute(ingrediente)
        
        # Assert
        assert result.id == 1
        assert result.nombre == "Tomate"
        mock_repository.create.assert_called_once_with(ingrediente)
    
    def test_crear_ingrediente_nombre_vacio(self):
        """Test para crear ingrediente con nombre vacío (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = CreateIngredienteUseCase(mock_repository)
        ingrediente = Ingrediente(
            nombre="",  # Nombre vacío
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="El nombre del ingrediente es obligatorio"):
            use_case.execute(ingrediente)
    
    def test_crear_ingrediente_stock_negativo(self):
        """Test para crear ingrediente con stock negativo (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = CreateIngredienteUseCase(mock_repository)
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('-5.0'),  # Stock negativo
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            use_case.execute(ingrediente)


class TestGetIngredienteUseCase:
    """Tests para el caso de uso GetIngredienteUseCase."""
    
    def test_obtener_ingrediente_exitoso(self):
        """Test para obtener un ingrediente exitosamente."""
        # Arrange
        mock_repository = Mock()
        expected_ingrediente = Ingrediente(
            id=1,
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        mock_repository.get_by_id.return_value = expected_ingrediente
        
        use_case = GetIngredienteUseCase(mock_repository)
        
        # Act
        result = use_case.execute(1)
        
        # Assert
        assert result == expected_ingrediente
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_obtener_ingrediente_no_existe(self):
        """Test para obtener un ingrediente que no existe."""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.return_value = None
        
        use_case = GetIngredienteUseCase(mock_repository)
        
        # Act
        result = use_case.execute(1)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_obtener_ingrediente_id_invalido(self):
        """Test para obtener ingrediente con ID inválido (debe fallar)."""
        # Arrange
        mock_repository = Mock()
        use_case = GetIngredienteUseCase(mock_repository)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El ID del ingrediente debe ser mayor a 0"):
            use_case.execute(0)
        
        with pytest.raises(ValueError, match="El ID del ingrediente debe ser mayor a 0"):
            use_case.execute(-1)
