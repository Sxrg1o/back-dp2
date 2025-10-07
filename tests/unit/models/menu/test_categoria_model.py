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

import pytest
from uuid import uuid4
from datetime import datetime

from src.models.menu.categoria_model import CategoriaModel


def test_categoria_model_creation():
    """
    Verifica que se puede crear una instancia de CategoriaModel correctamente.

    PRECONDICIONES:
        - Se debe tener acceso al modelo CategoriaModel.

    PROCESO:
        - Crear una instancia con datos válidos.
        - Verificar que todos los atributos se asignen correctamente.

    POSTCONDICIONES:
        - La instancia debe crearse sin errores.
        - Todos los atributos deben tener los valores esperados.
    """
    # Arrange
    categoria_id = uuid4()
    nombre = "Entradas"
    descripcion = "Platos de entrada y aperitivos"
    activo = True

    # Act
    categoria = CategoriaModel(
        id=categoria_id,
        nombre=nombre,
        descripcion=descripcion,
        activo=activo
    )

    # Assert
    assert categoria.id == categoria_id
    assert categoria.nombre == nombre
    assert categoria.descripcion == descripcion
    assert categoria.activo == activo


def test_categoria_model_default_values():
    """
    Verifica que los valores por defecto se asignen correctamente.

    PRECONDICIONES:
        - Se debe tener acceso al modelo CategoriaModel.

    PROCESO:
        - Crear una instancia con solo los campos requeridos.
        - Verificar que los valores por defecto se apliquen.

    POSTCONDICIONES:
        - Los valores por defecto deben ser los esperados.
    """
    # Arrange & Act
    categoria = CategoriaModel(nombre="Bebidas")

    # Assert
    assert categoria.nombre == "Bebidas"
    assert categoria.descripcion is None
    assert categoria.activo is None  # El default se aplica a nivel de BD, no de Python


def test_categoria_model_to_dict():
    """
    Verifica que el método to_dict convierte correctamente la instancia a diccionario.

    PRECONDICIONES:
        - Se debe tener una instancia válida de CategoriaModel.

    PROCESO:
        - Crear una instancia con datos conocidos.
        - Llamar al método to_dict.
        - Verificar que el diccionario contenga todos los campos esperados.

    POSTCONDICIONES:
        - El diccionario debe contener todos los atributos del modelo.
        - Los valores deben coincidir con los de la instancia.
    """
    # Arrange
    categoria_id = uuid4()
    categoria = CategoriaModel(
        id=categoria_id,
        nombre="Postres",
        descripcion="Dulces y postres",
        activo=True
    )

    # Act
    result = categoria.to_dict()

    # Assert
    assert isinstance(result, dict)
    assert result["id"] == categoria_id
    assert result["nombre"] == "Postres"
    assert result["descripcion"] == "Dulces y postres"
    assert result["activo"] is True


def test_categoria_model_from_dict():
    """
    Verifica que el método from_dict crea correctamente una instancia desde un diccionario.

    PRECONDICIONES:
        - Se debe tener acceso al método from_dict de CategoriaModel.

    PROCESO:
        - Crear un diccionario con datos válidos.
        - Llamar al método from_dict.
        - Verificar que la instancia creada tenga los valores correctos.

    POSTCONDICIONES:
        - La instancia debe crearse correctamente.
        - Todos los valores deben coincidir con el diccionario original.
    """
    # Arrange
    categoria_id = uuid4()
    data = {
        "id": categoria_id,
        "nombre": "Platos Principales",
        "descripcion": "Platos principales del menú",
        "activo": False
    }

    # Act
    categoria = CategoriaModel.from_dict(data)

    # Assert
    assert isinstance(categoria, CategoriaModel)
    assert categoria.id == categoria_id
    assert categoria.nombre == "Platos Principales"
    assert categoria.descripcion == "Platos principales del menú"
    assert categoria.activo is False


def test_categoria_model_update_from_dict():
    """
    Verifica que el método update_from_dict actualiza correctamente la instancia.

    PRECONDICIONES:
        - Se debe tener una instancia válida de CategoriaModel.

    PROCESO:
        - Crear una instancia inicial.
        - Crear un diccionario con datos de actualización.
        - Llamar al método update_from_dict.
        - Verificar que los campos se actualicen correctamente.

    POSTCONDICIONES:
        - Los campos especificados deben actualizarse.
        - Los campos no especificados deben mantener sus valores originales.
    """
    # Arrange
    categoria = CategoriaModel(
        nombre="Original",
        descripcion="Descripción original",
        activo=True
    )

    update_data = {
        "nombre": "Actualizado",
        "descripcion": "Nueva descripción",
        "activo": False
    }

    # Act
    categoria.update_from_dict(update_data)

    # Assert
    assert categoria.nombre == "Actualizado"
    assert categoria.descripcion == "Nueva descripción"
    assert categoria.activo is False


def test_categoria_model_update_from_dict_partial():
    """
    Verifica que el método update_from_dict actualiza solo los campos especificados.

    PRECONDICIONES:
        - Se debe tener una instancia válida de CategoriaModel.

    PROCESO:
        - Crear una instancia inicial con todos los campos.
        - Crear un diccionario con solo algunos campos para actualizar.
        - Llamar al método update_from_dict.
        - Verificar que solo se actualicen los campos especificados.

    POSTCONDICIONES:
        - Solo los campos especificados deben actualizarse.
        - Los demás campos deben mantener sus valores originales.
    """
    # Arrange
    categoria = CategoriaModel(
        nombre="Original",
        descripcion="Descripción original",
        activo=True
    )

    update_data = {
        "nombre": "Solo nombre actualizado"
    }

    # Act
    categoria.update_from_dict(update_data)

    # Assert
    assert categoria.nombre == "Solo nombre actualizado"
    assert categoria.descripcion == "Descripción original"  # No cambió
    assert categoria.activo is True  # No cambió


def test_categoria_model_table_name():
    """
    Verifica que el nombre de la tabla esté correctamente definido.

    PRECONDICIONES:
        - Se debe tener acceso al modelo CategoriaModel.

    PROCESO:
        - Verificar el atributo __tablename__ del modelo.

    POSTCONDICIONES:
        - El nombre de la tabla debe ser "categoria".
    """
    # Assert
    assert CategoriaModel.__tablename__ == "categoria"


def test_categoria_model_required_fields():
    """
    Verifica que los campos requeridos estén correctamente definidos.

    PRECONDICIONES:
        - Se debe tener acceso al modelo CategoriaModel.

    PROCESO:
        - Crear una instancia sin el campo nombre (requerido).
        - Verificar que el campo nombre sea None.

    POSTCONDICIONES:
        - El campo nombre debe ser None cuando no se proporciona.
    """
    # Arrange & Act
    categoria = CategoriaModel()  # Sin el campo requerido 'nombre'
    
    # Assert
    assert categoria.nombre is None
