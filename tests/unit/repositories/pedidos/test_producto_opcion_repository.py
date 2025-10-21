"""
Pruebas unitarias para el repositorio de opciones de productos.

Este módulo contiene las pruebas unitarias para verificar el correcto funcionamiento
del repositorio encargado de las operaciones CRUD relacionadas con las opciones de productos.
Se utilizan mocks para simular la capa de base de datos.

PRECONDICIONES:
    - Los módulos ProductoOpcionRepository y ProductoOpcionModel deben estar correctamente implementados.
    - SQLAlchemy y sus dependencias deben estar instaladas.
    - pytest y pytest-asyncio deben estar disponibles para ejecutar pruebas asíncronas.

PROCESO:
    - Configurar mocks para simular la sesión de base de datos.
    - Ejecutar los métodos del repositorio con parámetros controlados.
    - Verificar que el comportamiento de los métodos sea el esperado.

POSTCONDICIONES:
    - Todas las pruebas deben pasar satisfactoriamente.
    - Los métodos del repositorio deben funcionar según las especificaciones.
"""

import pytest
from ulid import ULID
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.repositories.pedidos.producto_opcion_repository import ProductoOpcionRepository
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Verifica que el método get_by_id recupera correctamente una opción de producto por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para buscar.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_by_id con un ID específico.
        - Verificar que se ejecute la consulta correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar un objeto ProductoOpcionModel cuando existe la opción.
        - El método debe retornar None cuando no existe la opción.
        - La consulta SQL debe formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = ProductoOpcionModel(
        id=str(ULID()),
        id_producto=str(ULID()),
        id_tipo_opcion=str(ULID()),
        nombre="Ají suave",
        precio_adicional=Decimal("0.00"),
        activo=True,
        orden=1
    )
    mock_session.execute.return_value = mock_result

    opcion_id = str(ULID())
    repository = ProductoOpcionRepository(mock_session)

    # Act
    result = await repository.get_by_id(opcion_id)

    # Assert
    assert result is not None
    assert isinstance(result, ProductoOpcionModel)
    mock_session.execute.assert_called_once()

    # Prueba de caso negativo
    mock_result.scalars.return_value.first.return_value = None
    result = await repository.get_by_id(opcion_id)
    assert result is None


@pytest.mark.asyncio
async def test_create_producto_opcion():
    """
    Verifica que el método create persiste correctamente una opción de producto en la base de datos.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un objeto ProductoOpcionModel válido para crear.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método create con una instancia de ProductoOpcionModel.
        - Verificar que se realicen todas las operaciones necesarias para persistir el objeto.

    POSTCONDICIONES:
        - El método debe añadir la opción de producto a la sesión.
        - El método debe hacer flush, commit y refresh.
        - El método debe retornar la opción de producto creada.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    producto_opcion = ProductoOpcionModel(
        id_producto=str(ULID()),
        id_tipo_opcion=str(ULID()),
        nombre="Sin ají",
        precio_adicional=Decimal("0.00"),
        activo=True,
        orden=0
    )
    repository = ProductoOpcionRepository(mock_session)

    # Act
    result = await repository.create(producto_opcion)

    # Assert - Caso exitoso
    assert result is not None
    assert result == producto_opcion
    mock_session.add.assert_called_once_with(producto_opcion)
    mock_session.flush.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(producto_opcion)

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.flush.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.create(producto_opcion)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_producto_opcion():
    """
    Verifica que el método delete elimina correctamente una opción de producto por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para eliminar.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método delete con un ID específico.
        - Verificar que se ejecute la sentencia correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar True cuando se elimina una opción de producto existente.
        - El método debe retornar False cuando no existe la opción de producto a eliminar.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange - Caso exitoso (se elimina la opción)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.rowcount = 1  # Simula que se eliminó una fila
    mock_session.execute.return_value = mock_result

    opcion_id = str(ULID())
    repository = ProductoOpcionRepository(mock_session)

    # Act
    result = await repository.delete(opcion_id)

    # Assert
    assert result is True
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso opción no existe
    mock_session.reset_mock()
    mock_result.rowcount = 0  # Simula que no se eliminó ninguna fila

    # Act
    result = await repository.delete(opcion_id)

    # Assert
    assert result is False
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.execute.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.delete(opcion_id)

    mock_session.rollback.assert_called_once()
