from ulid import ULID
from src.models.auth.rol_model import RolModel


def test_rol_model_creation():
    """
    Verifica que un objeto RolModel se crea correctamente.

    PRECONDICIONES:
        - Dado un id, nombre y descripcion.

    PROCESO:
        - Crear un registro de RolModel con valores predefinidos.

    POSTCONDICIONES:
        - La instancia debe tener los valores exactos proporcionados durante.
    """
    rol_id: str = str(ULID())
    rol_nombre = "admin"
    rol_descripcion = "Administrador del sistema"

    rol = RolModel(
        id=rol_id,
        nombre=rol_nombre,
        descripcion=rol_descripcion,
    )

    assert rol.id == rol_id
    assert rol.nombre == rol_nombre
    assert rol.descripcion == rol_descripcion


def test_rol_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.

    PRECONDICIONES:
        - La clase RolModel debe tener implementado el método to_dict().
        - Los atributos id, nombre, descripcion y activo deben existir en el modelo.

    PROCESO:
        - Crear una instancia de RolModel con valores específicos.
        - Llamar al método to_dict() para obtener un diccionario.

    POSTCONDICIONES:
        - El diccionario debe contener todas las claves esperadas.
        - Los valores deben coincidir con los de la instancia original.
    """
    rol_id: str = str(ULID())
    rol_nombre = "admin"
    rol_descripcion = "Administrador del sistema"
    rol = RolModel(id=rol_id, nombre=rol_nombre, descripcion=rol_descripcion)

    dict_result = rol.to_dict()

    assert "id" in dict_result
    assert "nombre" in dict_result
    assert "descripcion" in dict_result

    assert dict_result["id"] == rol_id
    assert dict_result["nombre"] == rol_nombre
    assert dict_result["descripcion"] == rol_descripcion
    assert dict_result["activo"] is None


def test_rol_activo_default():
    """
    Verifica el comportamiento del valor predeterminado para el atributo activo.

    PRECONDICIONES:
        - La clase RolModel debe tener un atributo activo con valor predeterminado.
        - La clase RolModel debe aceptar la creación de instancias sin valor para activo.

    PROCESO:
        - Crear una instancia de RolModel proporcionando solo el nombre obligatorio.

    POSTCONDICIONES:
        - Los atributos con nullable=True deben ser None si no se proporcionan.
    """
    rol = RolModel(nombre="test_rol")

    # El default debería ser True según el modelo
    assert rol.descripcion is None
    assert rol.activo is None
