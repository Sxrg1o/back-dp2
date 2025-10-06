"""
Unit tests for ProductoRepository
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.repositories.menu.producto_repository import ProductoRepository
from src.models.menu.producto_model import ProductoModel


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Verifica que get_by_id ejecuta la consulta correcta.
    """
    # Mock de AsyncSession
    mock_db = AsyncMock()

    # Producto esperado
    producto_esperado = ProductoModel(
        id_producto=1,
        nombre="Pizza Test",
        precio_base=15.0
    )

    # Configurar el mock para que devuelva el producto
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = producto_esperado
    mock_db.execute.return_value = mock_result

    # Ejecutar
    repo = ProductoRepository()
    resultado = await repo.get_by_id(mock_db, 1)

    # Verificar
    assert resultado is not None
    assert resultado.id_producto == 1
    assert resultado.nombre == "Pizza Test"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_category():
    """
    Verifica que get_by_category filtra correctamente por categoría.
    """
    mock_db = AsyncMock()

    # Lista de productos esperados
    productos_esperados = [
        ProductoModel(id_producto=1, nombre="Pizza 1", id_categoria=1),
        ProductoModel(id_producto=2, nombre="Pizza 2", id_categoria=1)
    ]

    # Configurar mock
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = productos_esperados
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Ejecutar
    repo = ProductoRepository()
    resultado = await repo.get_by_category(mock_db, category_id=1, available_only=True)

    # Verificar
    assert len(resultado) == 2
    assert resultado[0].nombre == "Pizza 1"
    assert resultado[1].nombre == "Pizza 2"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create():
    """
    Verifica que create agrega y confirma el producto.
    """
    mock_db = AsyncMock()

    producto = ProductoModel(
        nombre="Nuevo Producto",
        precio_base=20.0,
        id_categoria=1
    )

    # Ejecutar
    repo = ProductoRepository()
    await repo.create(mock_db, producto)

    # Verificar que se llamaron los métodos correctos
    mock_db.add.assert_called_once_with(producto)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(producto)


@pytest.mark.asyncio
async def test_delete():
    """
    Verifica que delete elimina correctamente un producto.
    """
    mock_db = AsyncMock()

    producto = ProductoModel(id_producto=1, nombre="A eliminar")

    # Ejecutar
    repo = ProductoRepository()
    await repo.delete(mock_db, producto)

    # Verificar
    mock_db.delete.assert_called_once_with(producto)
    mock_db.commit.assert_called_once()
