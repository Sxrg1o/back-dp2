"""Tests for Ingrediente DTOs."""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from pydantic import ValidationError

from app.application.dto.ingrediente_dto import (
    CreateIngredienteDTO,
    UpdateIngredienteDTO,
    StockUpdateDTO
)
from app.application.dto.item_dto import InformacionNutricionalDTO
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente


class TestCreateIngredienteDTO:
    """Test CreateIngredienteDTO validation."""
    
    def test_valid_create_ingrediente_dto(self):
        """Test valid ingredient creation DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=100,
            proteinas=5.0,
            azucares=2.0
        )
        
        future_date = datetime.utcnow() + timedelta(days=30)
        
        dto = CreateIngredienteDTO(
            nombre="Tomate",
            descripcion="Tomate fresco",
            precio=Decimal("2.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=10,
            etiquetas={EtiquetaItem.VEGANO},
            activo=True,
            tipo=EtiquetaIngrediente.VERDURA,
            peso_unitario=150.0,
            unidad_medida="gramos",
            fecha_vencimiento=future_date,
            proveedor="Proveedor Local"
        )
        
        assert dto.nombre == "Tomate"
        assert dto.tipo == EtiquetaIngrediente.VERDURA
        assert dto.peso_unitario == 150.0
        assert dto.unidad_medida == "gramos"
        assert dto.proveedor == "Proveedor Local"
    
    def test_negative_peso_unitario_raises_error(self):
        """Test that negative unit weight raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=100,
            proteinas=5.0,
            azucares=2.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateIngredienteDTO(
                nombre="Tomate",
                precio=Decimal("2.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=5,
                stock_actual=100,
                stock_minimo=10,
                tipo=EtiquetaIngrediente.VERDURA,
                peso_unitario=-150.0,
                unidad_medida="gramos"
            )
        
        assert "ensure this value is greater than 0" in str(exc_info.value)
    
    def test_empty_unidad_medida_raises_error(self):
        """Test that empty unit of measure raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=100,
            proteinas=5.0,
            azucares=2.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreateIngredienteDTO(
                nombre="Tomate",
                precio=Decimal("2.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=5,
                stock_actual=100,
                stock_minimo=10,
                tipo=EtiquetaIngrediente.VERDURA,
                peso_unitario=150.0,
                unidad_medida=""
            )
        
        assert "Unit of measure cannot be empty" in str(exc_info.value)
    
    def test_past_expiration_date_raises_error(self):
        """Test that past expiration date raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=100,
            proteinas=5.0,
            azucares=2.0
        )
        
        past_date = datetime.utcnow() - timedelta(days=1)
        
        with pytest.raises(ValidationError) as exc_info:
            CreateIngredienteDTO(
                nombre="Tomate",
                precio=Decimal("2.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=5,
                stock_actual=100,
                stock_minimo=10,
                tipo=EtiquetaIngrediente.VERDURA,
                peso_unitario=150.0,
                unidad_medida="gramos",
                fecha_vencimiento=past_date
            )
        
        assert "Expiration date must be in the future" in str(exc_info.value)
    
    def test_whitespace_fields_are_trimmed(self):
        """Test that whitespace in fields is trimmed."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=100,
            proteinas=5.0,
            azucares=2.0
        )
        
        dto = CreateIngredienteDTO(
            nombre="  Tomate  ",
            descripcion="  Tomate fresco  ",
            precio=Decimal("2.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=5,
            stock_actual=100,
            stock_minimo=10,
            tipo=EtiquetaIngrediente.VERDURA,
            peso_unitario=150.0,
            unidad_medida="  gramos  ",
            proveedor="  Proveedor Local  "
        )
        
        assert dto.nombre == "Tomate"
        assert dto.descripcion == "Tomate fresco"
        assert dto.unidad_medida == "gramos"
        assert dto.proveedor == "Proveedor Local"


class TestUpdateIngredienteDTO:
    """Test UpdateIngredienteDTO validation."""
    
    def test_valid_update_ingrediente_dto(self):
        """Test valid ingredient update DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=120,
            proteinas=6.0,
            azucares=3.0
        )
        
        future_date = datetime.utcnow() + timedelta(days=45)
        
        dto = UpdateIngredienteDTO(
            nombre="Tomate Cherry",
            precio=Decimal("3.00"),
            informacion_nutricional=nutritional_info,
            peso_unitario=80.0,
            fecha_vencimiento=future_date,
            proveedor="Nuevo Proveedor"
        )
        
        assert dto.nombre == "Tomate Cherry"
        assert dto.precio == Decimal("3.00")
        assert dto.peso_unitario == 80.0
        assert dto.proveedor == "Nuevo Proveedor"
    
    def test_partial_update_dto(self):
        """Test partial update with only some fields."""
        dto = UpdateIngredienteDTO(
            nombre="Tomate Actualizado",
            activo=False
        )
        
        assert dto.nombre == "Tomate Actualizado"
        assert dto.precio is None
        assert dto.activo is False
    
    def test_past_expiration_date_in_update_raises_error(self):
        """Test that past expiration date in update raises validation error."""
        past_date = datetime.utcnow() - timedelta(days=1)
        
        with pytest.raises(ValidationError) as exc_info:
            UpdateIngredienteDTO(fecha_vencimiento=past_date)
        
        assert "Expiration date must be in the future" in str(exc_info.value)


class TestStockUpdateDTO:
    """Test StockUpdateDTO validation."""
    
    def test_valid_stock_increase(self):
        """Test valid stock increase DTO."""
        dto = StockUpdateDTO(
            cantidad=50,
            operacion="aumentar"
        )
        
        assert dto.cantidad == 50
        assert dto.operacion == "aumentar"
    
    def test_valid_stock_decrease(self):
        """Test valid stock decrease DTO."""
        dto = StockUpdateDTO(
            cantidad=25,
            operacion="reducir"
        )
        
        assert dto.cantidad == 25
        assert dto.operacion == "reducir"
    
    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            StockUpdateDTO(
                cantidad=-10,
                operacion="aumentar"
            )
        
        assert "ensure this value is greater than 0" in str(exc_info.value)
    
    def test_invalid_operation_raises_error(self):
        """Test that invalid operation raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            StockUpdateDTO(
                cantidad=10,
                operacion="invalid"
            )
        
        assert "Operation must be 'aumentar' or 'reducir'" in str(exc_info.value) or "string does not match regex" in str(exc_info.value)