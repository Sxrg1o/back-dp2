"""
Pruebas de integración para el repositorio de roles.
"""

import pytest
from ulid import ULID

from src.models.auth.rol_model import RolModel
from src.repositories.auth.rol_repository import RolRepository


@pytest.fixture(scope="function")
def rol_repository(db_session) -> RolRepository:
    """
    Crea una instancia del repositorio de roles con una sesión de base de datos.

    PRECONDICIONES:
        - La sesión de base de datos debe estar inicializada en conftest.py.

    PROCESO:
        - Crea y retorna una instancia del repositorio con la sesión proporcionada.

    POSTCONDICIONES:
        - El repositorio está listo para ser utilizado en las pruebas.
    """
    return RolRepository(db_session)


@pytest.mark.asyncio
async def test_integration_create_rol(rol_repository: RolRepository):
    """
    Prueba de integración para verificar la creación de un rol en la base de datos.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - La base de datos debe estar vacía.

    PROCESO:
        - Crear un modelo de rol con datos de prueba.
        - Persistir el modelo en la base de datos usando el repositorio.
        - Verificar que el rol se ha creado correctamente con un ID válido.

    POSTCONDICIONES:
        - El rol debe existir en la base de datos con todos sus atributos correctos.
        - El método create debe retornar el modelo con su ID asignado.
    """
    # Arrange
    rol = RolModel(nombre="rol_test", descripcion="Rol de prueba para integración")

    # Act
    resultado = await rol_repository.create(rol)

    # Assert
    assert resultado is not None
    assert resultado.id is not None
    assert resultado.nombre == "rol_test"
    assert resultado.descripcion == "Rol de prueba para integración"
    assert resultado.activo is True  # Debe tener el valor por defecto


@pytest.mark.asyncio
async def test_integration_get_rol_by_id(rol_repository: RolRepository):
    """
    Prueba de integración para verificar la recuperación de un rol por su ID.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Debe existir un rol en la base de datos.

    PROCESO:
        - Crear un rol en la base de datos.
        - Recuperar el rol usando get_by_id con su ID.
        - Verificar que el rol recuperado coincide con el creado.
        - Intentar recuperar un rol con un ID inexistente.

    POSTCONDICIONES:
        - El método get_by_id debe retornar el rol correcto cuando existe.
        - Debe retornar None cuando el ID no existe en la base de datos.
    """
    # Arrange - Crear un rol para la prueba
    rol = RolModel(nombre="rol_recuperable", descripcion="Rol para probar get_by_id")
    rol_creado = await rol_repository.create(rol)
    rol_id = rol_creado.id

    # Act - Recuperar el rol por su ID
    rol_recuperado = await rol_repository.get_by_id(rol_id)

    # Assert - Verificar que se recuperó correctamente
    assert rol_recuperado is not None
    assert rol_recuperado.id == rol_id
    assert rol_recuperado.nombre == "rol_recuperable"
    assert rol_recuperado.descripcion == "Rol para probar get_by_id"

    # Probar con ID inexistente
    rol_inexistente = await rol_repository.get_by_id(str(ULID()))
    assert rol_inexistente is None


@pytest.mark.asyncio
async def test_integration_delete_rol(rol_repository: RolRepository):
    """
    Prueba de integración para verificar la eliminación de un rol.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Debe existir un rol en la base de datos para ser eliminado.

    PROCESO:
        - Crear un rol en la base de datos.
        - Eliminar el rol usando su ID.
        - Verificar que el rol ya no existe en la base de datos.
        - Intentar eliminar un rol con un ID inexistente.

    POSTCONDICIONES:
        - El método delete debe retornar True cuando el rol se elimina correctamente.
        - Debe retornar False cuando el ID no existe en la base de datos.
        - El rol eliminado no debe ser recuperable después de la eliminación.
    """
    # Arrange - Crear un rol para eliminarlo
    rol = RolModel(nombre="rol_eliminar", descripcion="Rol para probar delete")
    rol_creado = await rol_repository.create(rol)
    rol_id = rol_creado.id

    # Act - Eliminar el rol
    resultado_eliminacion = await rol_repository.delete(rol_id)

    # Assert - Verificar que se eliminó correctamente
    assert resultado_eliminacion is True

    # Verificar que el rol ya no existe
    rol_eliminado = await rol_repository.get_by_id(rol_id)
    assert rol_eliminado is None

    # Probar eliminar un rol inexistente
    resultado_no_existe = await rol_repository.delete(str(ULID()))
    assert resultado_no_existe is False
