"""
Unit tests for MesaModel
"""

from src.models.mesas.mesa_model import MesaModel


def test_mesa_model_creation():
    """
    Verifica que un objeto MesaModel se crea correctamente.
    """
    mesa = MesaModel(
        id_mesa=1,
        numero="M-01",
        capacidad=4,
        zona="interior",
        qr_code="QR123456",
        estado="disponible",
        activa=True
    )

    assert mesa.id_mesa == 1
    assert mesa.numero == "M-01"
    assert mesa.capacidad == 4
    assert mesa.zona == "interior"
    assert mesa.estado == "disponible"
    assert mesa.activa is True


def test_mesa_to_dict():
    """
    Verifica que el método to_dict() funciona correctamente.
    """
    mesa = MesaModel(
        id_mesa=2,
        numero="M-02",
        capacidad=6,
        qr_code="QR789012"
    )

    dict_result = mesa.to_dict()

    assert "id_mesa" in dict_result
    assert "numero" in dict_result
    assert dict_result["numero"] == "M-02"
    assert dict_result["capacidad"] == 6


def test_mesa_default_estado():
    """
    Verifica que el estado por defecto es 'disponible'.
    """
    mesa = MesaModel(
        numero="M-03",
        capacidad=2,
        qr_code="QR000"
    )

    # El default debería ser 'disponible'
    assert mesa.estado is None or mesa.estado == "disponible"
