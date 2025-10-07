from uuid import UUID, uuid4
from src.models.pedidos.tipo_opciones_model import OpcionModel


def test_opcion_model_creation():
    """
    Verifica que un objeto OpcionModel se crea correctamente.

    PRECONDICIONES:
        - Dado un id, etiqueta, precio adicional y es_default.

    PROCESO:
        - Crear un registro de OpcionModel con valores predefinidos.

    POSTCONDICIONES:
        - La instancia debe tener los valores exactos proporcionados durante la creación.
    """
    opcion_id: UUID = uuid4()
    etiqueta = "Tamaño grande"
    precio_adicional = 5.50
    es_default = False

    opcion = OpcionModel(
        id=opcion_id,
        etiqueta=etiqueta,
        precio_adicional=precio_adicional,
        es_default=es_default,
    )

    assert opcion.id == opcion_id
    assert opcion.etiqueta == etiqueta
    assert float(opcion.precio_adicional) == precio_adicional
    assert opcion.es_default == es_default


def test_opcion_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.

    PRECONDICIONES:
        - La clase OpcionModel debe tener implementado el método to_dict().
        - Los atributos id, etiqueta, precio_adicional, es_default y activo deben existir en el modelo.

    PROCESO:
        - Crear una instancia de OpcionModel con valores específicos.
        - Llamar al método to_dict() para obtener un diccionario.

    POSTCONDICIONES:
        - El diccionario debe contener todas las claves esperadas.
        - Los valores deben coincidir con los de la instancia original.
    """
    opcion_id: UUID = uuid4()
    etiqueta = "Extra queso"
    precio_adicional = 2.75
    es_default = True

    opcion = OpcionModel(
        id=opcion_id,
        etiqueta=etiqueta,
        precio_adicional=precio_adicional,
        es_default=es_default,
    )

    dict_result = opcion.to_dict()

    assert "id" in dict_result
    assert "etiqueta" in dict_result
    assert "precio_adicional" in dict_result
    assert "es_default" in dict_result
    assert "activo" in dict_result

    assert dict_result["id"] == opcion_id
    assert dict_result["etiqueta"] == etiqueta
    assert float(dict_result["precio_adicional"]) == precio_adicional
    assert dict_result["es_default"] == es_default
    assert dict_result["activo"] is None


def test_opcion_activo_default():
    """
    Verifica el comportamiento del valor predeterminado para el atributo activo.

    PRECONDICIONES:
        - La clase OpcionModel debe tener un atributo activo con valor predeterminado.
        - La clase OpcionModel debe aceptar la creación de instancias sin valor para activo.

    PROCESO:
        - Crear una instancia de OpcionModel proporcionando solo la etiqueta y precio.

    POSTCONDICIONES:
        - Los atributos con nullable=True deben ser None si no se proporcionan.
        - El atributo activo debe tener su valor por defecto definido.
    """
    opcion = OpcionModel(etiqueta="Sin aderezos", precio_adicional=0.0)

    assert opcion.precio_adicional == 0.0
    assert opcion.es_default in (None, False)
    assert opcion.activo is None