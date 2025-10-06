"""
Pruebas unitarias para el repositorio de roles.

Este módulo contiene las pruebas unitarias para verificar el correcto funcionamiento
del repositorio encargado de las operaciones CRUD relacionadas con los roles del sistema.
Se utilizan mocks para simular la capa de base de datos.

PRECONDICIONES:
    - Los módulos RolRepository y RolModel deben estar correctamente implementados.
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
from uuid import UUID, uuid4
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.repositories.auth.rol_repository import RolRepository
from src.models.auth.rol_model import RolModel


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Verifica que el método get_by_id recupera correctamente un rol por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para buscar.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_by_id con un ID específico.
        - Verificar que se ejecute la consulta correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar un objeto RolModel cuando existe el rol.
        - El método debe retornar None cuando no existe el rol.
        - La consulta SQL debe formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = RolModel(
        id=uuid4(), nombre="admin", descripcion="Administrador del sistema"
    )
    mock_session.execute.return_value = mock_result

    rol_id = uuid4()
    repository = RolRepository(mock_session)

    # Act
    result = await repository.get_by_id(rol_id)

    # Assert
    assert result is not None
    assert isinstance(result, RolModel)
    mock_session.execute.assert_called_once()

    # Prueba de caso negativo
    mock_result.scalars.return_value.first.return_value = None
    result = await repository.get_by_id(rol_id)
    assert result is None


@pytest.mark.asyncio
async def test_create_rol():
    """
    Verifica que el método create persiste correctamente un rol en la base de datos.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un objeto RolModel válido para crear.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método create con una instancia de RolModel.
        - Verificar que se realicen todas las operaciones necesarias para persistir el objeto.

    POSTCONDICIONES:
        - El método debe añadir el rol a la sesión.
        - El método debe hacer flush, commit y refresh.
        - El método debe retornar el rol creado.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    rol = RolModel(nombre="nuevo_rol", descripcion="Nuevo rol de prueba")
    repository = RolRepository(mock_session)

    # Act
    result = await repository.create(rol)

    # Assert - Caso exitoso
    assert result is not None
    assert result == rol
    mock_session.add.assert_called_once_with(rol)
    mock_session.flush.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(rol)

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.flush.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.create(rol)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_rol():
    """
    Verifica que el método delete elimina correctamente un rol por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para eliminar.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método delete con un ID específico.
        - Verificar que se ejecute la sentencia correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar True cuando se elimina un rol existente.
        - El método debe retornar False cuando no existe el rol a eliminar.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange - Caso exitoso (se elimina el rol)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.rowcount = 1  # Simula que se eliminó una fila
    mock_session.execute.return_value = mock_result

    rol_id = uuid4()
    repository = RolRepository(mock_session)

    # Act
    result = await repository.delete(rol_id)

    # Assert
    assert result is True
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso rol no existe
    mock_session.reset_mock()
    mock_result.rowcount = 0  # Simula que no se eliminó ninguna fila

    # Act
    result = await repository.delete(rol_id)

    # Assert
    assert result is False
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.execute.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.delete(rol_id)

    mock_session.rollback.assert_called_once()
