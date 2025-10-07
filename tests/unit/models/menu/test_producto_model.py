"""
Pruebas unitarias para el modelo de productos.

Este módulo contiene las pruebas unitarias para verificar el correcto funcionamiento
del modelo ProductoModel, incluyendo la creación, validación y métodos de utilidad.

PRECONDICIONES:
    - El módulo ProductoModel debe estar correctamente implementado.
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

from decimal import Decimal
from uuid import UUID, uuid4
from src.models.menu.producto_model import ProductoModel


def test_producto_creation():
    """
    Verifica que un objeto ProductoModel se crea correctamente.

    PRECONDICIONES:
        - Dado un id, id_categoria, nombre, precio_base y otros campos.

    PROCESO:
        - Crear un registro de ProductoModel con valores predefinidos.

    POSTCONDICIONES:
        - La instancia debe tener los valores exactos proporcionados.
    """
    producto_id: UUID = uuid4()
    categoria_id: UUID = uuid4()
    producto_nombre = "Hamburguesa Clásica"
    producto_descripcion = "Hamburguesa con carne, lechuga y tomate"
    producto_precio = Decimal("12.50")
    producto_imagen = "/images/hamburguesa.jpg"

    producto = ProductoModel(
        id=producto_id,
        id_categoria=categoria_id,
        nombre=producto_nombre,
        descripcion=producto_descripcion,
        precio_base=producto_precio,
        imagen_path=producto_imagen,
        disponible=True,
        destacado=False,
    )

    assert producto.id == producto_id
    assert producto.id_categoria == categoria_id
    assert producto.nombre == producto_nombre
    assert producto.descripcion == producto_descripcion
    assert producto.precio_base == producto_precio
    assert producto.imagen_path == producto_imagen
    assert producto.disponible is True
    assert producto.destacado is False


def test_producto_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.

    PRECONDICIONES:
        - La clase ProductoModel debe tener implementado el método to_dict().
        - Los atributos deben existir en el modelo.

    PROCESO:
        - Crear una instancia de ProductoModel con valores específicos.
        - Llamar al método to_dict() para obtener un diccionario.

    POSTCONDICIONES:
        - El diccionario debe contener todas las claves esperadas.
        - Los valores deben coincidir con los de la instancia original.
    """
    producto_id: UUID = uuid4()
    categoria_id: UUID = uuid4()
    producto_nombre = "Pizza Margarita"
    producto_precio = Decimal("15.00")
    
    producto = ProductoModel(
        id=producto_id,
        id_categoria=categoria_id,
        nombre=producto_nombre,
        precio_base=producto_precio,
    )

    dict_result = producto.to_dict()

    assert "id" in dict_result
    assert "id_categoria" in dict_result
    assert "nombre" in dict_result
    assert "precio_base" in dict_result

    assert dict_result["id"] == producto_id
    assert dict_result["id_categoria"] == categoria_id
    assert dict_result["nombre"] == producto_nombre
    assert dict_result["precio_base"] == producto_precio
    assert dict_result["disponible"] is None
    assert dict_result["destacado"] is None


def test_producto_disponible_default():
    """
    Verifica el comportamiento del valor predeterminado para el atributo disponible.

    PRECONDICIONES:
        - La clase ProductoModel debe tener un atributo disponible con valor predeterminado.
        - La clase ProductoModel debe aceptar la creación de instancias sin valor para disponible.

    PROCESO:
        - Crear una instancia de ProductoModel proporcionando solo los campos obligatorios.

    POSTCONDICIONES:
        - Los atributos con nullable=True deben ser None si no se proporcionan.
    """
    categoria_id: UUID = uuid4()
    producto = ProductoModel(
        nombre="test_producto",
        id_categoria=categoria_id,
        precio_base=Decimal("10.00"),
    )

    assert producto.descripcion is None
    assert producto.imagen_path is None
    assert producto.imagen_alt_text is None
    assert producto.disponible is None
    assert producto.destacado is None


def test_producto_decimal_precision():
    """
    Verifica que el precio_base mantiene la precisión decimal correcta.

    PRECONDICIONES:
        - El campo precio_base debe ser de tipo DECIMAL(10, 2).

    PROCESO:
        - Crear un producto con un precio que tenga decimales.
        - Verificar que se mantiene la precisión.

    POSTCONDICIONES:
        - El precio debe mantener exactamente 2 decimales.
    """
    categoria_id: UUID = uuid4()
    producto = ProductoModel(
        nombre="Producto Test",
        id_categoria=categoria_id,
        precio_base=Decimal("99.99"),
    )

    assert producto.precio_base == Decimal("99.99")
    assert isinstance(producto.precio_base, Decimal)
