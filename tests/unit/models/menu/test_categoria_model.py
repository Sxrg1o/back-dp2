"""
Unit tests for CategoriaModel
"""

from src.models.menu.categoria_model import CategoriaModel


def test_categoria_model_creation():
    """
    Verifica que un objeto CategoriaModel se crea correctamente.
    """
    categoria = CategoriaModel(
        id_categoria=1,
        nombre="Pizzas",
        descripcion="Pizzas artesanales",
        activo=True
    )

    assert categoria.id_categoria == 1
    assert categoria.nombre == "Pizzas"
    assert categoria.descripcion == "Pizzas artesanales"
    assert categoria.activo is True


def test_categoria_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.
    """
    categoria = CategoriaModel(
        id_categoria=2,
        nombre="Bebidas",
        activo=True
    )

    dict_result = categoria.to_dict()

    assert "id_categoria" in dict_result
    assert "nombre" in dict_result
    assert dict_result["nombre"] == "Bebidas"
    assert dict_result["activo"] is True


def test_categoria_default_orden():
    """
    Verifica que el orden por defecto es 0.
    """
    categoria = CategoriaModel(
        nombre="Nueva Categoría"
    )

    assert categoria.orden is None or categoria.orden == 0
