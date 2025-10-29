"""
Pruebas unitarias para el repositorio de alérgenos.

Este módulo contiene las pruebas unitarias para verificar el correcto funcionamiento
del repositorio encargado de las operaciones CRUD relacionadas con los alérgenos del sistema.
Se utilizan mocks para simular la capa de base de datos.

PRECONDICIONES:
    - Los módulos AlergenoRepository y AlergenoModel deben estar correctamente implementados.
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
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.repositories.menu.alergeno_repository import AlergenoRepository
from src.models.menu.alergeno_model import AlergenoModel
from src.core.enums.alergeno_enums import NivelRiesgo


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Verifica que el método get_by_id recupera correctamente un alérgeno por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para buscar.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_by_id con un ID específico.
        - Verificar que se ejecute la consulta correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar un objeto AlergenoModel cuando existe el alérgeno.
        - El método debe retornar None cuando no existe el alérgeno.
        - La consulta SQL debe formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = AlergenoModel(
        id=str(ULID()), 
        nombre="Gluten", 
        descripcion="Proteína presente en cereales",
        nivel_riesgo=NivelRiesgo.ALTO
    )
    mock_session.execute.return_value = mock_result

    alergeno_id = str(ULID())
    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.get_by_id(alergeno_id)

    # Assert
    assert result is not None
    assert isinstance(result, AlergenoModel)
    mock_session.execute.assert_called_once()

    # Prueba de caso negativo
    mock_result.scalars.return_value.first.return_value = None
    result = await repository.get_by_id(alergeno_id)
    assert result is None


@pytest.mark.asyncio
async def test_create_alergeno():
    """
    Verifica que el método create persiste correctamente un alérgeno en la base de datos.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un objeto AlergenoModel válido para crear.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método create con una instancia de AlergenoModel.
        - Verificar que se realicen todas las operaciones necesarias para persistir el objeto.

    POSTCONDICIONES:
        - El método debe añadir el alérgeno a la sesión.
        - El método debe hacer flush, commit y refresh.
        - El método debe retornar el alérgeno creado.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    alergeno = AlergenoModel(
        nombre="Lactosa", 
        descripcion="Azúcar natural presente en la leche",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.create(alergeno)

    # Assert - Caso exitoso
    assert result is not None
    assert result == alergeno
    mock_session.add.assert_called_once_with(alergeno)
    mock_session.flush.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(alergeno)

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.flush.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.create(alergeno)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_alergeno():
    """
    Verifica que el método delete elimina correctamente un alérgeno por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para eliminar.

    PROCESO:
        - Configurar los mocks para simular el comportamiento de la base de datos.
        - Llamar al método delete con un ID específico.
        - Verificar que se ejecute la sentencia correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar True cuando se elimina un alérgeno existente.
        - El método debe retornar False cuando no existe el alérgeno a eliminar.
        - En caso de error, debe hacer rollback y propagar la excepción.
    """
    # Arrange - Caso exitoso (se elimina el alérgeno)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.rowcount = 1  # Simula que se eliminó una fila
    mock_session.execute.return_value = mock_result

    alergeno_id = str(ULID())
    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.delete(alergeno_id)

    # Assert
    assert result is True
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso alérgeno no existe
    mock_session.reset_mock()
    mock_result.rowcount = 0  # Simula que no se eliminó ninguna fila

    # Act
    result = await repository.delete(alergeno_id)

    # Assert
    assert result is False
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

    # Arrange - Caso de error
    mock_session.reset_mock()
    mock_session.execute.side_effect = SQLAlchemyError("Error de prueba")

    # Act & Assert - Caso de error
    with pytest.raises(SQLAlchemyError):
        await repository.delete(alergeno_id)

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_nombre():
    """
    Verifica que el método get_by_nombre recupera correctamente un alérgeno por su nombre.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un nombre válido para buscar.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_by_nombre con un nombre específico.
        - Verificar que se ejecute la consulta correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar un objeto AlergenoModel cuando existe el alérgeno.
        - El método debe retornar None cuando no existe el alérgeno.
        - La consulta SQL debe formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = AlergenoModel(
        id=str(ULID()), 
        nombre="Mariscos", 
        descripcion="Crustáceos y moluscos",
        nivel_riesgo=NivelRiesgo.CRITICO
    )
    mock_session.execute.return_value = mock_result

    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.get_by_nombre("Mariscos")

    # Assert
    assert result is not None
    assert isinstance(result, AlergenoModel)
    assert result.nombre == "Mariscos"
    mock_session.execute.assert_called_once()

    # Prueba de caso negativo
    mock_result.scalars.return_value.first.return_value = None
    result = await repository.get_by_nombre("Alérgeno Inexistente")
    assert result is None


@pytest.mark.asyncio
async def test_get_activos():
    """
    Verifica que el método get_activos recupera correctamente todos los alérgenos activos.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_activos.
        - Verificar que se ejecute la consulta correcta y se retorne la lista esperada.

    POSTCONDICIONES:
        - El método debe retornar una lista de objetos AlergenoModel activos.
        - La consulta SQL debe formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_alergenos = [
        AlergenoModel(id=str(ULID()), nombre="Gluten", activo=True),
        AlergenoModel(id=str(ULID()), nombre="Lactosa", activo=True),
    ]
    mock_result.scalars.return_value.all.return_value = mock_alergenos
    mock_session.execute.return_value = mock_result

    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.get_activos()

    # Assert
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(alergeno, AlergenoModel) for alergeno in result)
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all():
    """
    Verifica que el método get_all recupera correctamente una lista paginada de alérgenos.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.

    PROCESO:
        - Configurar los mocks para simular las respuestas de la base de datos.
        - Llamar al método get_all con parámetros de paginación.
        - Verificar que se ejecuten las consultas correctas y se retorne la tupla esperada.

    POSTCONDICIONES:
        - El método debe retornar una tupla con lista de alérgenos y total de registros.
        - Las consultas SQL deben formarse correctamente.
    """
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    
    # Mock para la consulta de alérgenos
    mock_result = MagicMock()
    mock_alergenos = [
        AlergenoModel(id=str(ULID()), nombre="Gluten"),
        AlergenoModel(id=str(ULID()), nombre="Lactosa"),
    ]
    mock_result.scalars.return_value.all.return_value = mock_alergenos
    
    # Mock para la consulta de conteo
    mock_count_result = MagicMock()
    mock_count_result.scalar.return_value = 2
    
    # Configurar el mock para devolver diferentes resultados según la consulta
    def mock_execute_side_effect(query):
        if "count" in str(query):
            return mock_count_result
        return mock_result
    
    mock_session.execute.side_effect = mock_execute_side_effect

    repository = AlergenoRepository(mock_session)

    # Act
    result = await repository.get_all(skip=0, limit=10)

    # Assert
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    
    alergenos, total = result
    assert isinstance(alergenos, list)
    assert len(alergenos) == 2
    assert total == 2
    assert all(isinstance(alergeno, AlergenoModel) for alergeno in alergenos)
    
    # Verificar que se llamó execute dos veces (una para datos, otra para conteo)
    assert mock_session.execute.call_count == 2
