"""
Unit tests for ProductoModel
"""

from src.models.menu.producto_model import ProductoModel


def test_producto_model_creation():
    """
    Verifica que un objeto ProductoModel se crea con los atributos correctos.
    """
    producto = ProductoModel(
        id_producto=1,
        id_categoria=1,
        nombre="Pizza Margherita",
        descripcion="Clásica pizza con tomate y mozzarella",
        precio_base=12.50,
        disponible=True
    )

    assert producto.id_producto == 1
    assert producto.nombre == "Pizza Margherita"
    assert producto.precio_base == 12.50
    assert producto.disponible is True


def test_producto_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.
    """
    producto = ProductoModel(
        id_producto=1,
        id_categoria=1,
        nombre="Test Pizza",
        precio_base=15.00
    )

    dict_result = producto.to_dict()

    assert "id_producto" in dict_result
    assert "nombre" in dict_result
    assert dict_result["nombre"] == "Test Pizza"
    assert dict_result["precio_base"] == 15.00


def test_producto_default_values():
    """
    Verifica que los valores por defecto se asignan correctamente.
    """
    producto = ProductoModel(
        id_categoria=1,
        nombre="Producto Test",
        precio_base=10.00
    )

    # Los valores por defecto deberían ser aplicados por SQLAlchemy
    assert producto.disponible is None or producto.disponible is True
    assert producto.destacado is None or producto.destacado is False
