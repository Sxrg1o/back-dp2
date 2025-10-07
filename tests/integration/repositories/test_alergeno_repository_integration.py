"""
Pruebas de integración para el repositorio de alérgenos.
"""

import pytest
from uuid import uuid4

from src.models.menu.alergeno_model import AlergenoModel
from src.repositories.menu.alergeno_repository import AlergenoRepository
from src.core.enums.alergeno_enums import NivelRiesgo


@pytest.fixture(scope="function")
def alergeno_repository(db_session) -> AlergenoRepository:
    """
    Crea una instancia del repositorio de alérgenos con una sesión de base de datos.

    PRECONDICIONES:
        - La sesión de base de datos debe estar inicializada en conftest.py.

    PROCESO:
        - Crea y retorna una instancia del repositorio con la sesión proporcionada.

    POSTCONDICIONES:
        - El repositorio está listo para ser utilizado en las pruebas.
    """
    return AlergenoRepository(db_session)


@pytest.mark.asyncio
async def test_integration_create_alergeno(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la creación de un alérgeno en la base de datos.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - La base de datos debe estar vacía.

    PROCESO:
        - Crear un modelo de alérgeno con datos de prueba.
        - Persistir el modelo en la base de datos usando el repositorio.
        - Verificar que el alérgeno se ha creado correctamente con un ID válido.

    POSTCONDICIONES:
        - El alérgeno debe existir en la base de datos con todos sus atributos correctos.
        - El método create debe retornar el modelo con su ID asignado.
    """
    # Arrange
    alergeno = AlergenoModel(
        nombre="alergeno_test", 
        descripcion="Alérgeno de prueba para integración",
        icono="🧪",
        nivel_riesgo=NivelRiesgo.MEDIO
    )

    # Act
    resultado = await alergeno_repository.create(alergeno)

    # Assert
    assert resultado is not None
    assert resultado.id is not None
    assert resultado.nombre == "alergeno_test"
    assert resultado.descripcion == "Alérgeno de prueba para integración"
    assert resultado.icono == "🧪"
    assert resultado.nivel_riesgo == NivelRiesgo.MEDIO
    assert resultado.activo is True  # Debe tener el valor por defecto


@pytest.mark.asyncio
async def test_integration_get_alergeno_by_id(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la recuperación de un alérgeno por su ID.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Recuperar el alérgeno usando get_by_id con su ID.
        - Verificar que el alérgeno recuperado coincide con el creado.
        - Intentar recuperar un alérgeno con un ID inexistente.

    POSTCONDICIONES:
        - El método get_by_id debe retornar el alérgeno correcto cuando existe.
        - Debe retornar None cuando el ID no existe en la base de datos.
    """
    # Arrange - Crear un alérgeno para la prueba
    alergeno = AlergenoModel(
        nombre="alergeno_recuperable", 
        descripcion="Alérgeno para probar get_by_id",
        nivel_riesgo=NivelRiesgo.ALTO
    )
    alergeno_creado = await alergeno_repository.create(alergeno)
    alergeno_id = alergeno_creado.id

    # Act - Recuperar el alérgeno por su ID
    alergeno_recuperado = await alergeno_repository.get_by_id(alergeno_id)

    # Assert - Verificar que se recuperó correctamente
    assert alergeno_recuperado is not None
    assert alergeno_recuperado.id == alergeno_id
    assert alergeno_recuperado.nombre == "alergeno_recuperable"
    assert alergeno_recuperado.descripcion == "Alérgeno para probar get_by_id"
    assert alergeno_recuperado.nivel_riesgo == NivelRiesgo.ALTO

    # Probar con ID inexistente
    alergeno_inexistente = await alergeno_repository.get_by_id(uuid4())
    assert alergeno_inexistente is None


@pytest.mark.asyncio
async def test_integration_delete_alergeno(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la eliminación de un alérgeno.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos para ser eliminado.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Eliminar el alérgeno usando su ID.
        - Verificar que el alérgeno ya no existe en la base de datos.
        - Intentar eliminar un alérgeno con un ID inexistente.

    POSTCONDICIONES:
        - El método delete debe retornar True cuando el alérgeno se elimina correctamente.
        - Debe retornar False cuando el ID no existe en la base de datos.
        - El alérgeno eliminado no debe ser recuperable después de la eliminación.
    """
    # Arrange - Crear un alérgeno para eliminarlo
    alergeno = AlergenoModel(
        nombre="alergeno_eliminar", 
        descripcion="Alérgeno para probar delete",
        nivel_riesgo=NivelRiesgo.BAJO
    )
    alergeno_creado = await alergeno_repository.create(alergeno)
    alergeno_id = alergeno_creado.id

    # Act - Eliminar el alérgeno
    resultado_eliminacion = await alergeno_repository.delete(alergeno_id)

    # Assert - Verificar que se eliminó correctamente
    assert resultado_eliminacion is True

    # Verificar que el alérgeno ya no existe
    alergeno_eliminado = await alergeno_repository.get_by_id(alergeno_id)
    assert alergeno_eliminado is None

    # Probar eliminar un alérgeno inexistente
    resultado_no_existe = await alergeno_repository.delete(uuid4())
    assert resultado_no_existe is False


@pytest.mark.asyncio
async def test_integration_get_by_nombre(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la recuperación de un alérgeno por su nombre.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Debe existir un alérgeno en la base de datos.

    PROCESO:
        - Crear un alérgeno en la base de datos.
        - Recuperar el alérgeno usando get_by_nombre con su nombre.
        - Verificar que el alérgeno recuperado coincide con el creado.
        - Intentar recuperar un alérgeno con un nombre inexistente.

    POSTCONDICIONES:
        - El método get_by_nombre debe retornar el alérgeno correcto cuando existe.
        - Debe retornar None cuando el nombre no existe en la base de datos.
    """
    # Arrange - Crear un alérgeno para la prueba
    alergeno = AlergenoModel(
        nombre="alergeno_por_nombre", 
        descripcion="Alérgeno para probar get_by_nombre",
        icono="🔍",
        nivel_riesgo=NivelRiesgo.CRITICO
    )
    await alergeno_repository.create(alergeno)

    # Act - Recuperar el alérgeno por su nombre
    alergeno_recuperado = await alergeno_repository.get_by_nombre("alergeno_por_nombre")

    # Assert - Verificar que se recuperó correctamente
    assert alergeno_recuperado is not None
    assert alergeno_recuperado.nombre == "alergeno_por_nombre"
    assert alergeno_recuperado.descripcion == "Alérgeno para probar get_by_nombre"
    assert alergeno_recuperado.icono == "🔍"
    assert alergeno_recuperado.nivel_riesgo == NivelRiesgo.CRITICO

    # Probar con nombre inexistente
    alergeno_inexistente = await alergeno_repository.get_by_nombre("nombre_inexistente")
    assert alergeno_inexistente is None


@pytest.mark.asyncio
async def test_integration_get_activos(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la recuperación de alérgenos activos.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Deben existir alérgenos activos e inactivos en la base de datos.

    PROCESO:
        - Crear alérgenos activos e inactivos en la base de datos.
        - Recuperar solo los alérgenos activos usando get_activos.
        - Verificar que solo se retornan los alérgenos activos.

    POSTCONDICIONES:
        - El método get_activos debe retornar solo los alérgenos con activo=True.
        - No debe retornar alérgenos con activo=False.
    """
    # Arrange - Crear alérgenos activos e inactivos
    alergeno_activo1 = AlergenoModel(
        nombre="alergeno_activo_1", 
        descripcion="Alérgeno activo 1",
        activo=True
    )
    alergeno_activo2 = AlergenoModel(
        nombre="alergeno_activo_2", 
        descripcion="Alérgeno activo 2",
        activo=True
    )
    alergeno_inactivo = AlergenoModel(
        nombre="alergeno_inactivo", 
        descripcion="Alérgeno inactivo",
        activo=False
    )

    await alergeno_repository.create(alergeno_activo1)
    await alergeno_repository.create(alergeno_activo2)
    await alergeno_repository.create(alergeno_inactivo)

    # Act - Recuperar solo los alérgenos activos
    alergenos_activos = await alergeno_repository.get_activos()

    # Assert - Verificar que solo se retornan los activos
    assert alergenos_activos is not None
    assert isinstance(alergenos_activos, list)
    assert len(alergenos_activos) == 2
    
    nombres_activos = [alergeno.nombre for alergeno in alergenos_activos]
    assert "alergeno_activo_1" in nombres_activos
    assert "alergeno_activo_2" in nombres_activos
    assert "alergeno_inactivo" not in nombres_activos
    
    # Verificar que todos los alérgenos retornados están activos
    assert all(alergeno.activo is True for alergeno in alergenos_activos)


@pytest.mark.asyncio
async def test_integration_get_all(alergeno_repository: AlergenoRepository):
    """
    Prueba de integración para verificar la recuperación paginada de alérgenos.

    PRECONDICIONES:
        - El repositorio debe estar correctamente inicializado.
        - Deben existir múltiples alérgenos en la base de datos.

    PROCESO:
        - Crear múltiples alérgenos en la base de datos.
        - Recuperar los alérgenos usando get_all con paginación.
        - Verificar que se retorna la lista correcta y el total de registros.

    POSTCONDICIONES:
        - El método get_all debe retornar una tupla con lista de alérgenos y total.
        - La paginación debe funcionar correctamente.
    """
    # Arrange - Crear múltiples alérgenos
    alergenos_creados = []
    for i in range(5):
        alergeno = AlergenoModel(
            nombre=f"alergeno_paginacion_{i}", 
            descripcion=f"Alérgeno para probar paginación {i}",
            nivel_riesgo=NivelRiesgo.MEDIO
        )
        alergeno_creado = await alergeno_repository.create(alergeno)
        alergenos_creados.append(alergeno_creado)

    # Act - Recuperar con paginación
    alergenos, total = await alergeno_repository.get_all(skip=0, limit=3)

    # Assert - Verificar la paginación
    assert alergenos is not None
    assert isinstance(alergenos, list)
    assert len(alergenos) == 3  # Limitamos a 3
    assert total == 5  # Total de alérgenos creados
    
    # Verificar que todos son instancias de AlergenoModel
    assert all(isinstance(alergeno, AlergenoModel) for alergeno in alergenos)

    # Probar con offset
    alergenos_offset, total_offset = await alergeno_repository.get_all(skip=2, limit=2)
    assert len(alergenos_offset) == 2
    assert total_offset == 5
