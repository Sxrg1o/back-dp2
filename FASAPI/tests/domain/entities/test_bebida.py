"""
Tests for Bebida domain entity.
"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.bebida import Bebida
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestBebida:
    """Test cases for Bebida domain entity."""

    def test_valid_bebida_creation(self):
        """Test creating a valid bebida."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        bebida = Bebida(
            id=uuid4(),
            nombre="Coca Cola",
            descripcion="Refreshing cola drink",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=2,
            stock_actual=50,
            stock_minimo=10,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("330.0"),
            contenido_alcohol=Decimal("0.0"),
            temperatura_servicio="fria",
            tipo_bebida="gaseosa",
            marca="Coca Cola",
            origen="USA"
        )
        
        assert bebida.nombre == "Coca Cola"
        assert bebida.volumen == Decimal("330.0")
        assert bebida.contenido_alcohol == Decimal("0.0")
        assert bebida.temperatura_servicio == "fria"
        assert bebida.tipo_bebida == "gaseosa"
        assert bebida.marca == "Coca Cola"
        assert bebida.origen == "USA"

    def test_invalid_negative_volume(self):
        """Test that negative volume raises error."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        with pytest.raises(ValueError, match="Volume must be positive"):
            Bebida(
                id=uuid4(),
                nombre="Coca Cola",
                descripcion="Refreshing cola drink",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=2,
                stock_actual=50,
                stock_minimo=10,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("-330.0"),  # Negative volume
                contenido_alcohol=Decimal("0.0"),
                temperatura_servicio="fria",
                tipo_bebida="gaseosa",
                marca="Coca Cola",
                origen="USA"
            )

    def test_invalid_alcohol_content_over_100(self):
        """Test that alcohol content over 100% raises error."""
        precio = Precio(Decimal("25.99"))
        info_nutricional = InformacionNutricional(
            calorias=200,
            proteinas=Decimal("0.0"),
            azucares=Decimal("0.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("0.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("0.0")
        )
        
        with pytest.raises(ValueError, match="Alcohol content cannot exceed 100%"):
            Bebida(
                id=uuid4(),
                nombre="Super Vodka",
                descripcion="Impossible vodka",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=1,
                stock_actual=10,
                stock_minimo=2,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("750.0"),
                contenido_alcohol=Decimal("150.0"),  # Over 100%
                temperatura_servicio="ambiente",
                tipo_bebida="licor",
                marca="Super Brand",
                origen="Unknown"
            )

    def test_invalid_negative_alcohol_content(self):
        """Test that negative alcohol content raises error."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        with pytest.raises(ValueError, match="Alcohol content cannot be negative"):
            Bebida(
                id=uuid4(),
                nombre="Coca Cola",
                descripcion="Refreshing cola drink",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=2,
                stock_actual=50,
                stock_minimo=10,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("330.0"),
                contenido_alcohol=Decimal("-5.0"),  # Negative alcohol
                temperatura_servicio="fria",
                tipo_bebida="gaseosa",
                marca="Coca Cola",
                origen="USA"
            )

    def test_invalid_temperature_service(self):
        """Test that invalid temperature service raises error."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        with pytest.raises(ValueError, match="Service temperature must be 'fria', 'caliente', or 'ambiente'"):
            Bebida(
                id=uuid4(),
                nombre="Coca Cola",
                descripcion="Refreshing cola drink",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=2,
                stock_actual=50,
                stock_minimo=10,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("330.0"),
                contenido_alcohol=Decimal("0.0"),
                temperatura_servicio="frozen",  # Invalid temperature
                tipo_bebida="gaseosa",
                marca="Coca Cola",
                origen="USA"
            )

    def test_invalid_empty_brand(self):
        """Test that empty brand raises error."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        with pytest.raises(ValueError, match="Brand cannot be empty"):
            Bebida(
                id=uuid4(),
                nombre="Coca Cola",
                descripcion="Refreshing cola drink",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=2,
                stock_actual=50,
                stock_minimo=10,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("330.0"),
                contenido_alcohol=Decimal("0.0"),
                temperatura_servicio="fria",
                tipo_bebida="gaseosa",
                marca="",  # Empty brand
                origen="USA"
            )

    def test_invalid_empty_origin(self):
        """Test that empty origin raises error."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        with pytest.raises(ValueError, match="Origin cannot be empty"):
            Bebida(
                id=uuid4(),
                nombre="Coca Cola",
                descripcion="Refreshing cola drink",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=2,
                stock_actual=50,
                stock_minimo=10,
                activo=True,
                etiquetas=[EtiquetaItem.SIN_GLUTEN],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                volumen=Decimal("330.0"),
                contenido_alcohol=Decimal("0.0"),
                temperatura_servicio="fria",
                tipo_bebida="gaseosa",
                marca="Coca Cola",
                origen=""  # Empty origin
            )

    def test_is_alcoholic(self):
        """Test checking if bebida is alcoholic."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=200,
            proteinas=Decimal("0.0"),
            azucares=Decimal("0.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("0.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("0.0")
        )
        
        # Alcoholic bebida
        alcoholic_bebida = Bebida(
            id=uuid4(),
            nombre="Beer",
            descripcion="Cold beer",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=1,
            stock_actual=30,
            stock_minimo=5,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("500.0"),
            contenido_alcohol=Decimal("5.0"),
            temperatura_servicio="fria",
            tipo_bebida="cerveza",
            marca="Beer Brand",
            origen="Germany"
        )
        
        # Non-alcoholic bebida
        non_alcoholic_bebida = Bebida(
            id=uuid4(),
            nombre="Water",
            descripcion="Pure water",
            precio=Precio(Decimal("1.99")),
            informacion_nutricional=InformacionNutricional(
                calorias=0,
                proteinas=Decimal("0.0"),
                azucares=Decimal("0.0"),
                grasas=Decimal("0.0"),
                carbohidratos=Decimal("0.0"),
                fibra=Decimal("0.0"),
                sodio=Decimal("0.0")
            ),
            tiempo_preparacion=0,
            stock_actual=100,
            stock_minimo=20,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("500.0"),
            contenido_alcohol=Decimal("0.0"),
            temperatura_servicio="fria",
            tipo_bebida="agua",
            marca="Pure Brand",
            origen="Local"
        )
        
        assert alcoholic_bebida.is_alcoholic() is True
        assert non_alcoholic_bebida.is_alcoholic() is False

    def test_requires_age_verification(self):
        """Test age verification requirement."""
        precio = Precio(Decimal("25.99"))
        info_nutricional = InformacionNutricional(
            calorias=200,
            proteinas=Decimal("0.0"),
            azucares=Decimal("0.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("0.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("0.0")
        )
        
        # High alcohol content bebida
        strong_bebida = Bebida(
            id=uuid4(),
            nombre="Vodka",
            descripcion="Strong vodka",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=1,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("750.0"),
            contenido_alcohol=Decimal("40.0"),
            temperatura_servicio="ambiente",
            tipo_bebida="licor",
            marca="Vodka Brand",
            origen="Russia"
        )
        
        # Low alcohol content bebida
        light_bebida = Bebida(
            id=uuid4(),
            nombre="Light Beer",
            descripcion="Light beer",
            precio=Precio(Decimal("3.99")),
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=1,
            stock_actual=50,
            stock_minimo=10,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("330.0"),
            contenido_alcohol=Decimal("2.5"),
            temperatura_servicio="fria",
            tipo_bebida="cerveza",
            marca="Light Brand",
            origen="Local"
        )
        
        assert strong_bebida.requires_age_verification() is True
        assert light_bebida.requires_age_verification() is False

    def test_get_serving_temperature_recommendation(self):
        """Test getting serving temperature recommendation."""
        precio = Precio(Decimal("5.99"))
        info_nutricional = InformacionNutricional(
            calorias=150,
            proteinas=Decimal("0.0"),
            azucares=Decimal("35.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("35.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("10.0")
        )
        
        bebida = Bebida(
            id=uuid4(),
            nombre="Coca Cola",
            descripcion="Refreshing cola drink",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=2,
            stock_actual=50,
            stock_minimo=10,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("330.0"),
            contenido_alcohol=Decimal("0.0"),
            temperatura_servicio="fria",
            tipo_bebida="gaseosa",
            marca="Coca Cola",
            origen="USA"
        )
        
        recommendation = bebida.get_serving_temperature_recommendation()
        assert "fria" in recommendation.lower()

    def test_calculate_alcohol_units(self):
        """Test calculating alcohol units."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=200,
            proteinas=Decimal("0.0"),
            azucares=Decimal("0.0"),
            grasas=Decimal("0.0"),
            carbohidratos=Decimal("0.0"),
            fibra=Decimal("0.0"),
            sodio=Decimal("0.0")
        )
        
        bebida = Bebida(
            id=uuid4(),
            nombre="Beer",
            descripcion="Cold beer",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=1,
            stock_actual=30,
            stock_minimo=5,
            activo=True,
            etiquetas=[EtiquetaItem.SIN_GLUTEN],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            volumen=Decimal("500.0"),  # 500ml
            contenido_alcohol=Decimal("5.0"),  # 5%
            temperatura_servicio="fria",
            tipo_bebida="cerveza",
            marca="Beer Brand",
            origen="Germany"
        )
        
        # Alcohol units = (volume_ml * alcohol_percentage) / 1000
        # = (500 * 5) / 1000 = 2.5 units
        units = bebida.calculate_alcohol_units()
        assert units == Decimal("2.5")