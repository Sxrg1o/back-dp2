"""
Pruebas unitarias para el servicio de roles.
"""

import pytest
from unittest.mock import AsyncMock
import uuid
from datetime import datetime


from src.business_logic.auth.rol_service import RolService
from src.models.auth.rol_model import RolModel
from src.api.schemas.rol_schema import RolCreate, RolUpdate
from src.business_logic.exceptions.rol_exceptions import (
    RolValidationError,
    RolNotFoundError,
    RolConflictError,
)
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def mock_repository():
    """
    Fixture que proporciona un mock del repositorio de roles.

    PROCESO:
        - Crea un mock del repositorio con métodos asíncronos.

    POSTCONDICIONES:
        - El mock puede ser utilizado para simular cualquier comportamiento del repositorio.
    """
    repository = AsyncMock()
    return repository


@pytest.fixture
def rol_service(mock_repository):
    """
    Fixture que proporciona una instancia del servicio de roles con un repositorio mockeado.

    PROCESO:
        - Crea una instancia del servicio con un mock del repositorio.

    POSTCONDICIONES:
        - El servicio está listo para ser utilizado en las pruebas.
    """
    service = RolService(AsyncMock())
    service.repository = mock_repository
    return service


@pytest.fixture
def sample_rol_data():
    """
    Fixture que proporciona datos de muestra para un rol.

    PROCESO:
        - Crea datos de muestra para las pruebas.

    POSTCONDICIONES:
        - Los datos de muestra están disponibles para las pruebas.
    """
    return {
        "id": uuid.uuid4(),
        "nombre": "Test Rol",
        "descripcion": "Rol para pruebas",
        "activo": True,
        "fecha_creacion": datetime.now(),
        "fecha_modificacion": datetime.now(),
    }


@pytest.mark.asyncio
async def test_create_rol_success(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la creación exitosa de un rol.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una creación exitosa.
        - Llama al método create_rol con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe crear el rol correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    rol_create = RolCreate(
        nombre=sample_rol_data["nombre"], descripcion=sample_rol_data["descripcion"]
    )
    mock_repository.create.return_value = RolModel(**sample_rol_data)

    # Act
    result = await rol_service.create_rol(rol_create)

    # Assert
    assert result.id == sample_rol_data["id"]
    assert result.nombre == sample_rol_data["nombre"]
    assert result.descripcion == sample_rol_data["descripcion"]
    mock_repository.create.assert_called_once()

    # Verificar que se pasó un objeto RolModel al repositorio
    args, _ = mock_repository.create.call_args
    assert isinstance(args[0], RolModel)
    assert args[0].nombre == sample_rol_data["nombre"]
    assert args[0].descripcion == sample_rol_data["descripcion"]


@pytest.mark.asyncio
async def test_create_rol_duplicate_name(rol_service, mock_repository, sample_rol_data):
    """
    Prueba el manejo de errores al intentar crear un rol con nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método create_rol con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolConflictError.
    """
    # Arrange
    rol_create = RolCreate(
        nombre=sample_rol_data["nombre"], descripcion=sample_rol_data["descripcion"]
    )
    mock_repository.create.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(RolConflictError) as excinfo:
        await rol_service.create_rol(rol_create)

    assert "Ya existe un rol con el nombre" in str(excinfo.value)
    mock_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_rol_by_id_success(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la obtención exitosa de un rol por su ID.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del rol.
        - Llama al método get_rol_by_id con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar el rol correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    rol_id = sample_rol_data["id"]
    mock_repository.get_by_id.return_value = RolModel(**sample_rol_data)

    # Act
    result = await rol_service.get_rol_by_id(rol_id)

    # Assert
    assert result.id == rol_id
    assert result.nombre == sample_rol_data["nombre"]
    assert result.descripcion == sample_rol_data["descripcion"]
    mock_repository.get_by_id.assert_called_once_with(rol_id)


@pytest.mark.asyncio
async def test_get_rol_by_id_not_found(rol_service, mock_repository):
    """
    Prueba el manejo de errores al intentar obtener un rol que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Llama al método get_rol_by_id con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolNotFoundError.
    """
    # Arrange
    rol_id = uuid.uuid4()
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(RolNotFoundError) as excinfo:
        await rol_service.get_rol_by_id(rol_id)

    assert f"No se encontró el rol con ID {rol_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(rol_id)


@pytest.mark.asyncio
async def test_delete_rol_success(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la eliminación exitosa de un rol.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia y eliminación exitosa del rol.
        - Llama al método delete_rol con un ID válido.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe eliminar el rol correctamente.
        - El repositorio debe ser llamado con el ID correcto.
    """
    # Arrange
    rol_id = sample_rol_data["id"]
    mock_repository.get_by_id.return_value = RolModel(**sample_rol_data)
    mock_repository.delete.return_value = True

    # Act
    result = await rol_service.delete_rol(rol_id)

    # Assert
    assert result is True
    mock_repository.get_by_id.assert_called_once_with(rol_id)
    mock_repository.delete.assert_called_once_with(rol_id)


@pytest.mark.asyncio
async def test_delete_rol_not_found(rol_service, mock_repository):
    """
    Prueba el manejo de errores al intentar eliminar un rol que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Llama al método delete_rol con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolNotFoundError.
    """
    # Arrange
    rol_id = uuid.uuid4()
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(RolNotFoundError) as excinfo:
        await rol_service.delete_rol(rol_id)

    assert f"No se encontró el rol con ID {rol_id}" in str(excinfo.value)
    mock_repository.get_by_id.assert_called_once_with(rol_id)
    mock_repository.delete.assert_not_called()


@pytest.mark.asyncio
async def test_get_roles_success(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la obtención exitosa de una lista paginada de roles.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular una lista de roles.
        - Llama al método get_roles con parámetros válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe retornar la lista de roles correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    roles = [
        RolModel(**sample_rol_data),
        RolModel(
            id=uuid.uuid4(),
            nombre="Otro Rol",
            descripcion="Otro rol para pruebas",
            activo=True,
        ),
    ]
    mock_repository.get_all.return_value = (roles, len(roles))

    # Act
    result = await rol_service.get_roles(skip=0, limit=10)

    # Assert
    assert result.total == 2
    assert len(result.items) == 2
    assert result.items[0].nombre == sample_rol_data["nombre"]
    assert result.items[1].nombre == "Otro Rol"
    mock_repository.get_all.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_roles_validation_error(rol_service):
    """
    Prueba el manejo de errores al proporcionar parámetros inválidos para obtener roles.

    PRECONDICIONES:
        - El servicio debe estar configurado.

    PROCESO:
        - Llama al método get_roles con parámetros inválidos.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolValidationError.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(RolValidationError) as excinfo:
        await rol_service.get_roles(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(RolValidationError) as excinfo:
        await rol_service.get_roles(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)


@pytest.mark.asyncio
async def test_update_rol_success(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la actualización exitosa de un rol.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la actualización exitosa de un rol.
        - Llama al método update_rol con datos válidos.
        - Verifica el resultado y las llamadas al mock.

    POSTCONDICIONES:
        - El servicio debe actualizar el rol correctamente.
        - El repositorio debe ser llamado con los parámetros correctos.
    """
    # Arrange
    rol_id = sample_rol_data["id"]
    update_data = RolUpdate(
        nombre="Rol Actualizado", descripcion="Descripción actualizada"
    )

    updated_rol = RolModel(
        **{
            **sample_rol_data,
            "nombre": "Rol Actualizado",
            "descripcion": "Descripción actualizada",
        }
    )
    mock_repository.update.return_value = updated_rol

    # Act
    result = await rol_service.update_rol(rol_id, update_data)

    # Assert
    assert result.id == rol_id
    assert result.nombre == "Rol Actualizado"
    assert result.descripcion == "Descripción actualizada"
    mock_repository.update.assert_called_once_with(
        rol_id, nombre="Rol Actualizado", descripcion="Descripción actualizada"
    )


@pytest.mark.asyncio
async def test_update_rol_not_found(rol_service, mock_repository):
    """
    Prueba el manejo de errores al intentar actualizar un rol que no existe.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular que el rol no existe.
        - Llama al método update_rol con un ID inexistente.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolNotFoundError.
    """
    # Arrange
    rol_id = uuid.uuid4()
    update_data = RolUpdate(nombre="Rol Actualizado")
    mock_repository.update.return_value = None

    # Act & Assert
    with pytest.raises(RolNotFoundError) as excinfo:
        await rol_service.update_rol(rol_id, update_data)

    assert f"No se encontró el rol con ID {rol_id}" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(rol_id, nombre="Rol Actualizado")


@pytest.mark.asyncio
async def test_update_rol_duplicate_name(rol_service, mock_repository, sample_rol_data):
    """
    Prueba el manejo de errores al intentar actualizar un rol con un nombre duplicado.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular un error de integridad.
        - Llama al método update_rol con un nombre duplicado.
        - Verifica que se lance la excepción adecuada.

    POSTCONDICIONES:
        - El servicio debe lanzar RolConflictError.
    """
    # Arrange
    rol_id = sample_rol_data["id"]
    update_data = RolUpdate(nombre="Rol Duplicado")
    mock_repository.update.side_effect = IntegrityError(
        statement="Duplicate entry", params={}, orig=Exception("Duplicate entry")
    )

    # Act & Assert
    with pytest.raises(RolConflictError) as excinfo:
        await rol_service.update_rol(rol_id, update_data)

    assert "Ya existe un rol con el nombre" in str(excinfo.value)
    mock_repository.update.assert_called_once_with(rol_id, nombre="Rol Duplicado")


@pytest.mark.asyncio
async def test_update_rol_no_changes(rol_service, mock_repository, sample_rol_data):
    """
    Prueba la actualización de un rol cuando no se proporcionan cambios.

    PRECONDICIONES:
        - El servicio y repositorio mock deben estar configurados.

    PROCESO:
        - Configura el mock para simular la existencia del rol.
        - Llama al método update_rol sin proporcionar campos para actualizar.
        - Verifica que se recupere el rol existente sin cambios.

    POSTCONDICIONES:
        - El servicio debe retornar el rol existente sin modificaciones.
        - El método update del repositorio no debe ser llamado.
    """
    # Arrange
    rol_id = sample_rol_data["id"]
    update_data = RolUpdate()  # Sin datos para actualizar
    mock_repository.get_by_id.return_value = RolModel(**sample_rol_data)

    # Act
    result = await rol_service.update_rol(rol_id, update_data)

    # Assert
    assert result.id == rol_id
    assert result.nombre == sample_rol_data["nombre"]
    mock_repository.get_by_id.assert_called_once_with(rol_id)
    mock_repository.update.assert_not_called()
