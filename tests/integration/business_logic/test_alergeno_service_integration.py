"""
Pruebas de integración para el servicio de alérgenos.
"""

import pytest
from uuid import uuid4

from src.business_logic.menu.alergeno_service import AlergenoService
from src.api.schemas.alergeno_schema import AlergenoCreate, AlergenoUpdate
from src.business_logic.exceptions.alergeno_exceptions import (
    AlergenoNotFoundError,
    AlergenoConflictError,
    AlergenoValidationError,
)
from src.core.enums.alergeno_enums import NivelRiesgo


@pytest.fixture(scope="function")
def alergeno_service(db_session) -> AlergenoService:
    """
    Crea una instancia del servicio de alérgenos con una sesión de base de datos.

    PRECONDICIONES:
        - La sesión de base de datos debe estar inicializada en conftest.py.

    PROCESO:
        - Crea y retorna una instancia del servicio con la sesión proporcionada.

    POSTCONDICIONES:
        - El servicio está listo para ser utilizado en las pruebas.
    """
    return AlergenoService(db_session)


@pytest.mark.asyncio
async def test_integration_create_alergeno(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar la creación de un alérgeno en la base de datos.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - La base de datos debe estar vacía.

    PROCESO:
        - Crear un esquema de alérgeno con datos de prueba.
        - Persistir el alérgeno en la base de datos usando el servicio.
        - Verificar que el alérgeno se ha creado correctamente con un ID válido.

    POSTCONDICIONES:
        - El alérgeno debe existir en la base de datos con todos sus atributos correctos.
        - El método create_alergeno debe retornar un objeto AlergenoResponse con los datos del alérgeno creado.
    """
    # Arrange
    alergeno_data = AlergenoCreate(
        nombre="alergeno_test",
        descripcion="Alérgeno de prueba para integración",
        icono="🧪",
        nivel_riesgo=NivelRiesgo.MEDIO
    )

    # Act
    resultado = await alergeno_service.create_alergeno(alergeno_data)

    # Assert
    assert resultado is not None
    assert resultado.id is not None
    assert resultado.nombre == "alergeno_test"
    assert resultado.descripcion == "Alérgeno de prueba para integración"
    assert resultado.icono == "🧪"
    assert resultado.nivel_riesgo == NivelRiesgo.MEDIO
    assert resultado.activo is True  # Debe tener el valor por defecto


@pytest.mark.asyncio
async def test_integration_get_alergeno_by_id(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar la recuperación de un alérgeno por su ID.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Recuperar el alérgeno usando get_alergeno_by_id con su ID.
        - Verificar que el alérgeno recuperado coincide con el creado.
        - Intentar recuperar un alérgeno con un ID inexistente.

    POSTCONDICIONES:
        - El método get_alergeno_by_id debe retornar el alérgeno correcto cuando existe.
        - Debe lanzar AlergenoNotFoundError cuando el ID no existe en la base de datos.
    """
    # Arrange - Crear un alérgeno para la prueba
    alergeno_data = AlergenoCreate(
        nombre="alergeno_recuperable",
        descripcion="Alérgeno para probar get_by_id",
        nivel_riesgo=NivelRiesgo.ALTO
    )
    alergeno_creado = await alergeno_service.create_alergeno(alergeno_data)
    alergeno_id = alergeno_creado.id

    # Act - Recuperar el alérgeno por su ID
    alergeno_recuperado = await alergeno_service.get_alergeno_by_id(alergeno_id)

    # Assert - Verificar que se recuperó correctamente
    assert alergeno_recuperado is not None
    assert alergeno_recuperado.id == alergeno_id
    assert alergeno_recuperado.nombre == "alergeno_recuperable"
    assert alergeno_recuperado.descripcion == "Alérgeno para probar get_by_id"
    assert alergeno_recuperado.nivel_riesgo == NivelRiesgo.ALTO

    # Probar con ID inexistente
    with pytest.raises(AlergenoNotFoundError):
        await alergeno_service.get_alergeno_by_id(uuid4())


@pytest.mark.asyncio
async def test_integration_delete_alergeno(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar la eliminación de un alérgeno.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos para ser eliminado.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Eliminar el alérgeno usando su ID.
        - Verificar que el alérgeno ya no existe en la base de datos.
        - Intentar eliminar un alérgeno con un ID inexistente.

    POSTCONDICIONES:
        - El método delete_alergeno debe retornar True cuando el alérgeno se elimina correctamente.
        - Debe lanzar AlergenoNotFoundError cuando el ID no existe en la base de datos.
        - El alérgeno eliminado no debe ser recuperable después de la eliminación.
    """
    # Arrange - Crear un alérgeno para eliminarlo
    alergeno_data = AlergenoCreate(
        nombre="alergeno_eliminar",
        descripcion="Alérgeno para probar delete",
        nivel_riesgo=NivelRiesgo.BAJO
    )
    alergeno_creado = await alergeno_service.create_alergeno(alergeno_data)
    alergeno_id = alergeno_creado.id

    # Act - Eliminar el alérgeno
    resultado_eliminacion = await alergeno_service.delete_alergeno(alergeno_id)

    # Assert - Verificar que se eliminó correctamente
    assert resultado_eliminacion is True

    # Verificar que el alérgeno ya no existe
    with pytest.raises(AlergenoNotFoundError):
        await alergeno_service.get_alergeno_by_id(alergeno_id)

    # Probar eliminar un alérgeno inexistente
    with pytest.raises(AlergenoNotFoundError):
        await alergeno_service.delete_alergeno(uuid4())


@pytest.mark.asyncio
async def test_integration_get_alergenos(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar la recuperación paginada de alérgenos.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - Deben existir múltiples alérgenos en la base de datos.

    PROCESO:
        - Crear múltiples alérgenos en la base de datos.
        - Recuperar los alérgenos usando get_alergenos con paginación.
        - Verificar que se retorna la lista correcta y el total de registros.

    POSTCONDICIONES:
        - El método get_alergenos debe retornar un objeto AlergenoList con lista de alérgenos y total.
        - La paginación debe funcionar correctamente.
    """
    # Arrange - Crear múltiples alérgenos
    for i in range(5):
        alergeno_data = AlergenoCreate(
            nombre=f"alergeno_paginacion_{i}",
            descripcion=f"Alérgeno para probar paginación {i}",
            nivel_riesgo=NivelRiesgo.MEDIO
        )
        await alergeno_service.create_alergeno(alergeno_data)

    # Act - Recuperar con paginación
    alergenos = await alergeno_service.get_alergenos(skip=0, limit=3)

    # Assert - Verificar la paginación
    assert alergenos is not None
    assert isinstance(alergenos.items, list)
    assert len(alergenos.items) == 3  # Limitamos a 3
    assert alergenos.total == 5  # Total de alérgenos creados

    # Verificar que todos son instancias de AlergenoSummary
    assert all(hasattr(item, 'id') for item in alergenos.items)
    assert all(hasattr(item, 'nombre') for item in alergenos.items)

    # Probar con offset
    alergenos_offset = await alergeno_service.get_alergenos(skip=2, limit=2)
    assert len(alergenos_offset.items) == 2
    assert alergenos_offset.total == 5


@pytest.mark.asyncio
async def test_integration_update_alergeno(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar la actualización de un alérgeno.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos para ser actualizado.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Actualizar el alérgeno con nuevos datos.
        - Verificar que los cambios se han aplicado correctamente.
        - Intentar actualizar un alérgeno con un ID inexistente.

    POSTCONDICIONES:
        - El método update_alergeno debe retornar el alérgeno actualizado.
        - Los cambios deben persistirse en la base de datos.
        - Debe lanzar AlergenoNotFoundError cuando el ID no existe.
    """
    # Arrange - Crear un alérgeno para actualizarlo
    alergeno_data = AlergenoCreate(
        nombre="alergeno_actualizar",
        descripcion="Alérgeno para probar update",
        icono="🔄",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    alergeno_creado = await alergeno_service.create_alergeno(alergeno_data)
    alergeno_id = alergeno_creado.id

    # Act - Actualizar el alérgeno
    update_data = AlergenoUpdate(
        nombre="alergeno_actualizado",
        descripcion="Descripción actualizada",
        nivel_riesgo=NivelRiesgo.ALTO
    )
    resultado_actualizacion = await alergeno_service.update_alergeno(alergeno_id, update_data)

    # Assert - Verificar que se actualizó correctamente
    assert resultado_actualizacion is not None
    assert resultado_actualizacion.id == alergeno_id
    assert resultado_actualizacion.nombre == "alergeno_actualizado"
    assert resultado_actualizacion.descripcion == "Descripción actualizada"
    assert resultado_actualizacion.nivel_riesgo == NivelRiesgo.ALTO
    assert resultado_actualizacion.icono == "🔄"  # No se actualizó

    # Verificar que los cambios persisten
    alergeno_verificado = await alergeno_service.get_alergeno_by_id(alergeno_id)
    assert alergeno_verificado.nombre == "alergeno_actualizado"
    assert alergeno_verificado.descripcion == "Descripción actualizada"
    assert alergeno_verificado.nivel_riesgo == NivelRiesgo.ALTO

    # Probar actualizar un alérgeno inexistente
    with pytest.raises(AlergenoNotFoundError):
        await alergeno_service.update_alergeno(uuid4(), update_data)


@pytest.mark.asyncio
async def test_integration_create_alergeno_duplicate_name(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar el manejo de nombres duplicados al crear alérgenos.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.
        - Debe existir un alérgeno con un nombre específico.

    PROCESO:
        - Crear un alérgeno con un nombre específico.
        - Intentar crear otro alérgeno con el mismo nombre.
        - Verificar que se lanza la excepción adecuada.

    POSTCONDICIONES:
        - El primer alérgeno debe crearse correctamente.
        - Debe lanzar AlergenoConflictError al intentar crear un alérgeno con nombre duplicado.
    """
    # Arrange - Crear el primer alérgeno
    alergeno_data = AlergenoCreate(
        nombre="alergeno_duplicado",
        descripcion="Primer alérgeno",
        nivel_riesgo=NivelRiesgo.MEDIO
    )
    await alergeno_service.create_alergeno(alergeno_data)

    # Act & Assert - Intentar crear otro alérgeno con el mismo nombre
    alergeno_duplicado = AlergenoCreate(
        nombre="alergeno_duplicado",
        descripcion="Segundo alérgeno",
        nivel_riesgo=NivelRiesgo.ALTO
    )

    with pytest.raises(AlergenoConflictError) as excinfo:
        await alergeno_service.create_alergeno(alergeno_duplicado)

    assert "Ya existe un alérgeno con el nombre 'alergeno_duplicado'" in str(excinfo.value)


@pytest.mark.asyncio
async def test_integration_validation_errors(alergeno_service: AlergenoService):
    """
    Prueba de integración para verificar las validaciones de parámetros.

    PRECONDICIONES:
        - El servicio debe estar correctamente inicializado.

    PROCESO:
        - Llamar a get_alergenos con parámetros inválidos.
        - Verificar que se lanzan las excepciones de validación adecuadas.

    POSTCONDICIONES:
        - Debe lanzar AlergenoValidationError para parámetros inválidos.
    """
    # Act & Assert - Parámetro skip negativo
    with pytest.raises(AlergenoValidationError) as excinfo:
        await alergeno_service.get_alergenos(skip=-1, limit=10)
    assert "El parámetro 'skip' debe ser mayor o igual a cero" in str(excinfo.value)

    # Act & Assert - Parámetro limit no positivo
    with pytest.raises(AlergenoValidationError) as excinfo:
        await alergeno_service.get_alergenos(skip=0, limit=0)
    assert "El parámetro 'limit' debe ser mayor a cero" in str(excinfo.value)
