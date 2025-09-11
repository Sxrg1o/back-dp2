"""Tests for Bebida DTOs."""

import pytest
from decimal import Decimal
from pydantic import ValidationError

from app.application.dto.bebida_dto import (
    CreateBebidaDTO,
    UpdateBebidaDTO
)
from app.application.dto.item_dto import InformacionNutricionalDTO
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestCreateBebidaDTO:
    """Test CreateBebidaDTO validation."""
    
    def test_valid_create_bebida_dto(self):
        """Test valid beverage creation DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        dto = CreateBebidaDTO(
            nombre="Coca Cola",
            descripcion="Bebida gaseosa refrescante",
            precio=Decimal("3.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=2,
            stock_actual=100,
            stock_minimo=20,
            etiquetas={EtiquetaItem.FRIO},
            activo=True,
            volumen=350.0,
            contenido_alcohol=0.0,
            temperatura_servicio="fria",
            tipo_bebida="Gaseosa",
            marca="Coca Cola",
            origen="Estados Unidos"
        )
        
        assert dto.nombre == "Coca Cola"
        assert dto.volumen == 350.0
        assert dto.contenido_alcohol == 0.0
        assert dto.temperatura_servicio == "fria"
        assert dto.tipo_bebida == "Gaseosa"
        assert dto.marca == "Coca Cola"
        assert dto.origen == "Estados Unidos"
    
    def test_alcoholic_beverage_dto(self):
        """Test valid alcoholic beverage creation DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=200,
            proteinas=0.5,
            azucares=5.0
        )
        
        dto = CreateBebidaDTO(
            nombre="Vino Tinto",
            descripcion="Vino tinto reserva",
            precio=Decimal("25.00"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=1,
            stock_actual=50,
            stock_minimo=10,
            etiquetas={EtiquetaItem.ACIDO},
            activo=True,
            volumen=750.0,
            contenido_alcohol=13.5,
            temperatura_servicio="ambiente",
            tipo_bebida="Vino",
            marca="Bodega Premium",
            origen="Argentina"
        )
        
        assert dto.nombre == "Vino Tinto"
        assert dto.volumen == 750.0
        assert dto.contenido_alcohol == 13.5
        assert dto.temperatura_servicio == "ambiente"
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateBebidaDTO(
                nombre="",
                precio=Decimal("3.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=2,
                stock_actual=100,
                stock_minimo=20,
                volumen=350.0,
                contenido_alcohol=0.0
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_negative_volumen_raises_error(self):
        """Test that negative volume raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateBebidaDTO(
                nombre="Coca Cola",
                precio=Decimal("3.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=2,
                stock_actual=100,
                stock_minimo=20,
                volumen=-350.0,
                contenido_alcohol=0.0
            )
        
        assert "Input should be greater than 0" in str(exc_info.value)
    
    def test_negative_alcohol_content_raises_error(self):
        """Test that negative alcohol content raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateBebidaDTO(
                nombre="Coca Cola",
                precio=Decimal("3.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=2,
                stock_actual=100,
                stock_minimo=20,
                volumen=350.0,
                contenido_alcohol=-5.0
            )
        
        assert "Alcohol content must be between 0 and 100 percent" in str(exc_info.value) or "Input should be greater than or equal to 0" in str(exc_info.value)
    
    def test_excessive_alcohol_content_raises_error(self):
        """Test that alcohol content over 100% raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateBebidaDTO(
                nombre="Alcohol Puro",
                precio=Decimal("50.00"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=1,
                stock_actual=10,
                stock_minimo=2,
                volumen=500.0,
                contenido_alcohol=150.0
            )
        
        assert "Alcohol content must be between 0 and 100 percent" in str(exc_info.value) or "Input should be less than or equal to 100" in str(exc_info.value)
    
    def test_invalid_temperatura_servicio_raises_error(self):
        """Test that invalid service temperature raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateBebidaDTO(
                nombre="Coca Cola",
                precio=Decimal("3.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=2,
                stock_actual=100,
                stock_minimo=20,
                volumen=350.0,
                contenido_alcohol=0.0,
                temperatura_servicio="hirviendo"
            )
        
        assert "Service temperature must be 'fria', 'caliente', or 'ambiente'" in str(exc_info.value) or "string does not match regex" in str(exc_info.value)
    
    def test_whitespace_fields_are_trimmed(self):
        """Test that whitespace in fields is trimmed."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=150,
            proteinas=0.0,
            azucares=35.0
        )
        
        dto = CreateBebidaDTO(
            nombre="  Coca Cola  ",
            descripcion="  Bebida gaseosa  ",
            precio=Decimal("3.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=2,
            stock_actual=100,
            stock_minimo=20,
            volumen=350.0,
            contenido_alcohol=0.0,
            tipo_bebida="  Gaseosa  ",
            marca="  Coca Cola  ",
            origen="  Estados Unidos  "
        )
        
        assert dto.nombre == "Coca Cola"
        assert dto.descripcion == "Bebida gaseosa"
        assert dto.tipo_bebida == "Gaseosa"
        assert dto.marca == "Coca Cola"
        assert dto.origen == "Estados Unidos"


class TestUpdateBebidaDTO:
    """Test UpdateBebidaDTO validation."""
    
    def test_valid_update_bebida_dto(self):
        """Test valid beverage update DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=160,
            proteinas=0.0,
            azucares=40.0
        )
        
        dto = UpdateBebidaDTO(
            nombre="Coca Cola Zero",
            precio=Decimal("3.75"),
            informacion_nutricional=nutritional_info,
            volumen=500.0,
            contenido_alcohol=0.0,
            temperatura_servicio="fria",
            marca="Coca Cola Company"
        )
        
        assert dto.nombre == "Coca Cola Zero"
        assert dto.precio == Decimal("3.75")
        assert dto.volumen == 500.0
        assert dto.contenido_alcohol == 0.0
        assert dto.temperatura_servicio == "fria"
        assert dto.marca == "Coca Cola Company"
    
    def test_partial_update_dto(self):
        """Test partial update with only some fields."""
        dto = UpdateBebidaDTO(
            nombre="Bebida Actualizada",
            activo=False
        )
        
        assert dto.nombre == "Bebida Actualizada"
        assert dto.precio is None
        assert dto.activo is False
    
    def test_empty_name_in_update_raises_error(self):
        """Test that empty name in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateBebidaDTO(nombre="")
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_negative_volumen_in_update_raises_error(self):
        """Test that negative volume in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateBebidaDTO(volumen=-250.0)
        
        assert "Input should be greater than 0" in str(exc_info.value)
    
    def test_invalid_alcohol_content_in_update_raises_error(self):
        """Test that invalid alcohol content in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateBebidaDTO(contenido_alcohol=120.0)
        
        assert "Alcohol content must be between 0 and 100 percent" in str(exc_info.value) or "Input should be less than or equal to 100" in str(exc_info.value)
    
    def test_invalid_temperatura_servicio_in_update_raises_error(self):
        """Test that invalid service temperature in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdateBebidaDTO(temperatura_servicio="congelada")
        
        assert "Service temperature must be 'fria', 'caliente', or 'ambiente'" in str(exc_info.value) or "string does not match regex" in str(exc_info.value)
    
    def test_none_values_are_allowed(self):
        """Test that None values are allowed in update DTO."""
        dto = UpdateBebidaDTO()
        
        assert dto.nombre is None
        assert dto.precio is None
        assert dto.volumen is None
        assert dto.contenido_alcohol is None
        assert dto.activo is None