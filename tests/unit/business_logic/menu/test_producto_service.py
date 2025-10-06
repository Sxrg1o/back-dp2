"""
Unit tests for ProductoService
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.business_logic.menu.producto_service import ProductoService
from src.business_logic.exceptions.menu_exceptions import (
    ProductoNotFoundError,
    CategoriaNotFoundError
)
from src.models.menu.producto_model import ProductoModel
from src.models.menu.categoria_model import CategoriaModel


@pytest.mark.asyncio
async def test_get_product_by_id_success():
    """
    Verifica que get_product_by_id devuelve un producto correctamente.
    """
    mock_db = AsyncMock()

    # Producto esperado
    producto_esperado = ProductoModel(
        id_producto=1,
        nombre="Pizza Margherita",
        precio_base=15.0
    )

    # Mock del repositorio
    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.producto_repo = MagicMock()
        service.producto_repo.get_by_id = AsyncMock(return_value=producto_esperado)

        # Ejecutar
        resultado = await service.get_product_by_id(mock_db, 1)

        # Verificar
        assert resultado is not None
        assert resultado.id_producto == 1
        assert resultado.nombre == "Pizza Margherita"
        service.producto_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_by_id_not_found():
    """
    Verifica que get_product_by_id lanza excepción cuando no encuentra el producto.
    """
    mock_db = AsyncMock()

    # Mock del repositorio que devuelve None
    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.producto_repo = MagicMock()
        service.producto_repo.get_by_id = AsyncMock(return_value=None)

        # Verificar que lanza ProductoNotFoundError
        with pytest.raises(ProductoNotFoundError):
            await service.get_product_by_id(mock_db, 999)


@pytest.mark.asyncio
async def test_create_product_success():
    """
    Verifica que create_product crea un producto correctamente.
    """
    mock_db = AsyncMock()

    product_data = {
        "id_categoria": 1,
        "nombre": "Nueva Pizza",
        "precio_base": 20.0,
        "descripcion": "Deliciosa pizza"
    }

    # Categoría existente y activa
    categoria_mock = CategoriaModel(id_categoria=1, nombre="Pizzas", activo=True)

    # Producto creado
    producto_creado = ProductoModel(
        id_producto=1,
        id_categoria=1,
        nombre="Nueva Pizza",
        precio_base=20.0
    )

    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.validator = MagicMock()
        service.validator.validate_product_data = MagicMock()
        service.categoria_repo = MagicMock()
        service.categoria_repo.get_by_id = AsyncMock(return_value=categoria_mock)
        service.producto_repo = MagicMock()
        service.producto_repo.create = AsyncMock(return_value=producto_creado)

        # Ejecutar
        resultado = await service.create_product(mock_db, product_data)

        # Verificar
        assert resultado is not None
        assert resultado.nombre == "Nueva Pizza"
        service.validator.validate_product_data.assert_called_once_with(product_data)
        service.categoria_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_create_product_categoria_not_found():
    """
    Verifica que create_product lanza excepción si la categoría no existe.
    """
    mock_db = AsyncMock()

    product_data = {
        "id_categoria": 999,
        "nombre": "Pizza Inexistente",
        "precio_base": 20.0
    }

    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.validator = MagicMock()
        service.validator.validate_product_data = MagicMock()
        service.categoria_repo = MagicMock()
        service.categoria_repo.get_by_id = AsyncMock(return_value=None)

        # Verificar que lanza CategoriaNotFoundError
        with pytest.raises(CategoriaNotFoundError):
            await service.create_product(mock_db, product_data)


@pytest.mark.asyncio
async def test_create_product_categoria_inactiva():
    """
    Verifica que no se puede crear producto en categoría inactiva.
    """
    mock_db = AsyncMock()

    product_data = {
        "id_categoria": 1,
        "nombre": "Pizza en categoría inactiva",
        "precio_base": 20.0
    }

    # Categoría inactiva
    categoria_inactiva = CategoriaModel(id_categoria=1, nombre="Pizzas", activo=False)

    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.validator = MagicMock()
        service.validator.validate_product_data = MagicMock()
        service.categoria_repo = MagicMock()
        service.categoria_repo.get_by_id = AsyncMock(return_value=categoria_inactiva)

        # Verificar que lanza CategoriaNotFoundError
        with pytest.raises(CategoriaNotFoundError, match="inactive category"):
            await service.create_product(mock_db, product_data)
