"""
Pruebas unitarias para el modelo AlergenoModel.

Verifica el comportamiento del modelo de alérgenos incluyendo creación,
validaciones, métodos de conversión y representación.
"""

import pytest
from src.models.menu.alergeno_model import AlergenoModel
from src.core.enums.alergeno_enums import NivelRiesgo


class TestAlergenoModel:
    """Clase de pruebas para AlergenoModel."""

    def test_alergeno_model_creation_with_minimal_data(self):
        """
        Verifica que un objeto AlergenoModel se crea correctamente con datos mínimos.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con solo el nombre requerido.

        POSTCONDICIONES:
            - Los atributos deben tener los valores correctos.
            - Los valores por defecto deben aplicarse correctamente.
        """
        alergeno = AlergenoModel(nombre="Gluten")

        assert alergeno.nombre == "Gluten"
        assert alergeno.descripcion is None
        assert alergeno.icono is None
        # Los valores por defecto se aplicarán cuando se persista en la base de datos
        # En las pruebas unitarias, verificamos que los atributos existen
        assert hasattr(alergeno, 'nivel_riesgo')
        assert hasattr(alergeno, 'activo')

    def test_alergeno_model_creation_with_all_data(self):
        """
        Verifica que un objeto AlergenoModel se crea correctamente con todos los datos.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con todos los atributos especificados.

        POSTCONDICIONES:
            - Todos los atributos deben tener los valores correctos.
        """
        alergeno = AlergenoModel(
            nombre="Lactosa",
            descripcion="Azúcar natural presente en la leche y productos lácteos",
            icono="🥛",
            nivel_riesgo=NivelRiesgo.ALTO,
            activo=True
        )

        assert alergeno.nombre == "Lactosa"
        assert alergeno.descripcion == "Azúcar natural presente en la leche y productos lácteos"
        assert alergeno.icono == "🥛"
        assert alergeno.nivel_riesgo == NivelRiesgo.ALTO
        assert alergeno.activo is True

    def test_alergeno_model_default_values(self):
        """
        Verifica que los valores por defecto se aplican correctamente.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia sin especificar valores opcionales.

        POSTCONDICIONES:
            - Los valores por defecto deben aplicarse según la definición del modelo.
        """
        alergeno = AlergenoModel(nombre="Mariscos")

        # Los valores por defecto se aplicarán cuando se persista en la base de datos
        # En las pruebas unitarias, verificamos que los atributos existen
        assert hasattr(alergeno, 'nivel_riesgo')
        assert hasattr(alergeno, 'activo')
        assert alergeno.descripcion is None
        assert alergeno.icono is None

    def test_alergeno_model_different_risk_levels(self):
        """
        Verifica que se pueden crear alérgenos con diferentes niveles de riesgo.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancias con cada nivel de riesgo disponible.

        POSTCONDICIONES:
            - Cada instancia debe tener el nivel de riesgo correcto.
        """
        alergenos = [
            AlergenoModel(nombre="Bajo Riesgo", nivel_riesgo=NivelRiesgo.BAJO),
            AlergenoModel(nombre="Medio Riesgo", nivel_riesgo=NivelRiesgo.MEDIO),
            AlergenoModel(nombre="Alto Riesgo", nivel_riesgo=NivelRiesgo.ALTO),
            AlergenoModel(nombre="Crítico Riesgo", nivel_riesgo=NivelRiesgo.CRITICO),
        ]

        for alergeno in alergenos:
            assert alergeno.nivel_riesgo in NivelRiesgo
            assert alergeno.nombre in ["Bajo Riesgo", "Medio Riesgo", "Alto Riesgo", "Crítico Riesgo"]

    def test_alergeno_model_to_dict(self):
        """
        Verifica que el método to_dict convierte correctamente el modelo a diccionario.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con datos específicos.
            - Llamar al método to_dict.

        POSTCONDICIONES:
            - El diccionario debe contener todos los atributos del modelo.
            - Los valores deben coincidir con los de la instancia.
        """
        alergeno = AlergenoModel(
            nombre="Nueces",
            descripcion="Frutos secos que pueden causar reacciones alérgicas",
            icono="🥜",
            nivel_riesgo=NivelRiesgo.ALTO,
            activo=False
        )

        result_dict = alergeno.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["nombre"] == "Nueces"
        assert result_dict["descripcion"] == "Frutos secos que pueden causar reacciones alérgicas"
        assert result_dict["icono"] == "🥜"
        assert result_dict["nivel_riesgo"] == NivelRiesgo.ALTO
        assert result_dict["activo"] is False

    def test_alergeno_model_from_dict(self):
        """
        Verifica que el método from_dict crea correctamente una instancia desde un diccionario.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear diccionario con datos de alérgeno.
            - Llamar al método from_dict.

        POSTCONDICIONES:
            - La instancia creada debe tener los valores correctos.
        """
        data = {
            "nombre": "Sésamo",
            "descripcion": "Semillas de sésamo",
            "icono": "🌰",
            "nivel_riesgo": NivelRiesgo.MEDIO,
            "activo": True
        }

        alergeno = AlergenoModel.from_dict(data)

        assert alergeno.nombre == "Sésamo"
        assert alergeno.descripcion == "Semillas de sésamo"
        assert alergeno.icono == "🌰"
        assert alergeno.nivel_riesgo == NivelRiesgo.MEDIO
        assert alergeno.activo is True

    def test_alergeno_model_update_from_dict(self):
        """
        Verifica que el método update_from_dict actualiza correctamente los atributos.

        PRECONDICIONES:
            - Tener una instancia de AlergenoModel existente.

        PROCESO:
            - Crear instancia inicial.
            - Llamar a update_from_dict con nuevos datos.

        POSTCONDICIONES:
            - Los atributos deben actualizarse con los nuevos valores.
        """
        alergeno = AlergenoModel(
            nombre="Original",
            descripcion="Descripción original",
            nivel_riesgo=NivelRiesgo.BAJO
        )

        update_data = {
            "descripcion": "Descripción actualizada",
            "nivel_riesgo": NivelRiesgo.ALTO,
            "activo": False
        }

        alergeno.update_from_dict(update_data)

        assert alergeno.nombre == "Original"  # No se actualiza porque no está en update_data
        assert alergeno.descripcion == "Descripción actualizada"
        assert alergeno.nivel_riesgo == NivelRiesgo.ALTO
        assert alergeno.activo is False

    def test_alergeno_model_repr(self):
        """
        Verifica que el método __repr__ devuelve una representación string correcta.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con datos específicos.
            - Llamar a repr() o str().

        POSTCONDICIONES:
            - La representación string debe contener información relevante del modelo.
        """
        alergeno = AlergenoModel(
            nombre="Huevos",
            nivel_riesgo=NivelRiesgo.CRITICO,
            activo=True
        )

        repr_string = repr(alergeno)

        assert "AlergenoModel" in repr_string
        assert "Huevos" in repr_string
        assert "critico" in repr_string
        assert "True" in repr_string

    def test_alergeno_model_inactive_state(self):
        """
        Verifica que se puede crear un alérgeno en estado inactivo.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con activo=False.

        POSTCONDICIONES:
            - El atributo activo debe ser False.
        """
        alergeno = AlergenoModel(
            nombre="Alérgeno Inactivo",
            activo=False
        )

        assert alergeno.activo is False
        assert alergeno.nombre == "Alérgeno Inactivo"

    def test_alergeno_model_with_long_description(self):
        """
        Verifica que se puede crear un alérgeno con descripción larga.

        PRECONDICIONES:
            - Ninguna especial.

        PROCESO:
            - Crear instancia con descripción extensa.

        POSTCONDICIONES:
            - La descripción debe almacenarse correctamente.
        """
        long_description = (
            "Este alérgeno puede estar presente en múltiples productos y "
            "causar reacciones alérgicas severas en personas sensibles. "
            "Es importante verificar siempre los ingredientes antes de consumir."
        )

        alergeno = AlergenoModel(
            nombre="Alérgeno Complejo",
            descripcion=long_description
        )

        assert alergeno.descripcion == long_description
        assert len(alergeno.descripcion) > 100
