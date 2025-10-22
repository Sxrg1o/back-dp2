"""
Pruebas unitarias para el modelo de categorías.

Este módulo contiene las pruebas unitarias para verificar el correcto funcionamiento
del modelo CategoriaModel, incluyendo la creación, validación y métodos de utilidad.

PRECONDICIONES:
    - El módulo CategoriaModel debe estar correctamente implementado.
    - SQLAlchemy y sus dependencias deben estar instaladas.
    - pytest debe estar disponible para ejecutar las pruebas.

PROCESO:
    - Crear instancias del modelo con diferentes configuraciones.
    - Verificar que los atributos se asignen correctamente.
    - Probar los métodos de utilidad (to_dict, from_dict, update_from_dict).

POSTCONDICIONES:
    - Todas las pruebas deben pasar satisfactoriamente.
    - El modelo debe funcionar según las especificaciones.
"""

from ulid import ULID
from src.models.menu.categoria_model import CategoriaModel


def test_categoria_creation():
    """
    Verifica que un objeto CategoriaModel se crea correctamente.

    PRECONDICIONES:
        - Dado un id, nombre, descripcion e imagen_path.

    PROCESO:
        - Crear un registro de CategoriaModel con valores predefinidos.

    POSTCONDICIONES:
        - La instancia debe tener los valores exactos proporcionados.
    """
    categoria_id: str = str(ULID())
    categoria_nombre = "Entradas"
    categoria_descripcion = "Platos de entrada y aperitivos"
    categoria_imagen = "/images/entradas.jpg"

    categoria = CategoriaModel(
        id=categoria_id,
        nombre=categoria_nombre,
        descripcion=categoria_descripcion,
        imagen_path=categoria_imagen,
    )

    assert categoria.id == categoria_id
    assert categoria.nombre == categoria_nombre
    assert categoria.descripcion == categoria_descripcion
    assert categoria.imagen_path == categoria_imagen


def test_categoria_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.

    PRECONDICIONES:
        - La clase CategoriaModel debe tener implementado el método to_dict().
        - Los atributos id, nombre, descripcion, imagen_path y activo deben existir en el modelo.

    PROCESO:
        - Crear una instancia de CategoriaModel con valores específicos.
        - Llamar al método to_dict() para obtener un diccionario.

    POSTCONDICIONES:
        - El diccionario debe contener todas las claves esperadas.
        - Los valores deben coincidir con los de la instancia original.
    """
    categoria_id: str = str(ULID())
    categoria_nombre = "Postres"
    categoria_descripcion = "Dulces y postres"
    categoria = CategoriaModel(
        id=categoria_id, 
        nombre=categoria_nombre, 
        descripcion=categoria_descripcion
    )

    dict_result = categoria.to_dict()

    assert "id" in dict_result
    assert "nombre" in dict_result
    assert "descripcion" in dict_result

    assert dict_result["id"] == categoria_id
    assert dict_result["nombre"] == categoria_nombre
    assert dict_result["descripcion"] == categoria_descripcion
    assert dict_result["activo"] is None


def test_categoria_activo_default():
    """
    Verifica el comportamiento del valor predeterminado para el atributo activo.

    PRECONDICIONES:
        - La clase CategoriaModel debe tener un atributo activo con valor predeterminado.
        - La clase CategoriaModel debe aceptar la creación de instancias sin valor para activo.

    PROCESO:
        - Crear una instancia de CategoriaModel proporcionando solo el nombre obligatorio.

    POSTCONDICIONES:
        - Los atributos con nullable=True deben ser None si no se proporcionan.
    """
    categoria = CategoriaModel(nombre="test_categoria")

    assert categoria.descripcion is None
    assert categoria.imagen_path is None
    assert categoria.activo is None
