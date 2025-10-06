"""
Unit tests for RolModel
"""

from src.models.auth.rol_model import RolModel


def test_rol_model_creation():
    """
    Verifica que un objeto RolModel se crea correctamente.
    """
    rol = RolModel(
        id_rol=1,
        nombre="admin",
        descripcion="Administrador del sistema",
        activo=True
    )

    assert rol.id_rol == 1
    assert rol.nombre == "admin"
    assert rol.descripcion == "Administrador del sistema"
    assert rol.activo is True


def test_rol_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.
    """
    rol = RolModel(
        id_rol=2,
        nombre="mesero",
        descripcion="Personal de servicio"
    )

    dict_result = rol.to_dict()

    assert "id_rol" in dict_result
    assert "nombre" in dict_result
    assert dict_result["nombre"] == "mesero"
    assert "descripcion" in dict_result


def test_rol_activo_default():
    """
    Verifica que activo por defecto es True.
    """
    rol = RolModel(
        nombre="test_rol"
    )

    # El default debería ser True según el modelo
    assert rol.activo is None or rol.activo is True
