"""Tests for Plato DTOs."""

import pytest
from decimal import Decimal
from uuid import uuid4
from pydantic import ValidationError

from app.application.dto.plato_dto import (
    CreatePlatoDTO,
    UpdatePlatoDTO,
    AgregarIngredienteRecetaDTO,
    ActualizarIngredienteRecetaDTO
)
from app.application.dto.item_dto import InformacionNutricionalDTO
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato


class TestCreatePlatoDTO:
    """Test CreatePlatoDTO validation."""
    
    def test_valid_create_plato_dto(self):
        """Test valid dish creation DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        ingrediente_id = uuid4()
        receta = {ingrediente_id: 200.0}
        
        dto = CreatePlatoDTO(
            nombre="Pasta Carbonara",
            descripcion="Pasta italiana con salsa carbonara",
            precio=Decimal("18.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=25,
            stock_actual=20,
            stock_minimo=5,
            etiquetas={EtiquetaItem.CALIENTE},
            activo=True,
            tipo_plato=EtiquetaPlato.FONDO,
            receta=receta,
            instrucciones="Cocinar pasta, preparar salsa carbonara, mezclar",
            porciones=2,
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        assert dto.nombre == "Pasta Carbonara"
        assert dto.tipo_plato == "fondo"
        assert dto.receta == receta
        assert dto.porciones == 2
        assert dto.dificultad == "medio"
        assert dto.chef_recomendado == "Chef Mario"
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreatePlatoDTO(
                nombre="",
                precio=Decimal("18.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=25,
                stock_actual=20,
                stock_minimo=5,
                tipo_plato=EtiquetaPlato.FONDO,
                porciones=2
            )
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_negative_porciones_raises_error(self):
        """Test that negative portions raise validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreatePlatoDTO(
                nombre="Pasta Carbonara",
                precio=Decimal("18.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=25,
                stock_actual=20,
                stock_minimo=5,
                tipo_plato=EtiquetaPlato.FONDO,
                porciones=-1
            )
        
        assert "Input should be greater than 0" in str(exc_info.value)
    
    def test_invalid_dificultad_raises_error(self):
        """Test that invalid difficulty raises validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        with pytest.raises(ValidationError) as exc_info:
            CreatePlatoDTO(
                nombre="Pasta Carbonara",
                precio=Decimal("18.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=25,
                stock_actual=20,
                stock_minimo=5,
                tipo_plato=EtiquetaPlato.FONDO,
                porciones=2,
                dificultad="imposible"
            )
        
        assert "String should match pattern" in str(exc_info.value)
    
    def test_negative_recipe_quantity_raises_error(self):
        """Test that negative recipe quantities raise validation error."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        ingrediente_id = uuid4()
        receta = {ingrediente_id: -100.0}
        
        with pytest.raises(ValidationError) as exc_info:
            CreatePlatoDTO(
                nombre="Pasta Carbonara",
                precio=Decimal("18.50"),
                informacion_nutricional=nutritional_info,
                tiempo_preparacion=25,
                stock_actual=20,
                stock_minimo=5,
                tipo_plato=EtiquetaPlato.FONDO,
                receta=receta,
                porciones=2
            )
        
        assert "Recipe quantities must be positive" in str(exc_info.value)
    
    def test_whitespace_fields_are_trimmed(self):
        """Test that whitespace in fields is trimmed."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=450,
            proteinas=25.0,
            azucares=8.0
        )
        
        dto = CreatePlatoDTO(
            nombre="  Pasta Carbonara  ",
            descripcion="  Pasta italiana  ",
            precio=Decimal("18.50"),
            informacion_nutricional=nutritional_info,
            tiempo_preparacion=25,
            stock_actual=20,
            stock_minimo=5,
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="  Cocinar pasta  ",
            porciones=2,
            chef_recomendado="  Chef Mario  "
        )
        
        assert dto.nombre == "Pasta Carbonara"
        assert dto.descripcion == "Pasta italiana"
        assert dto.instrucciones == "Cocinar pasta"
        assert dto.chef_recomendado == "Chef Mario"


class TestUpdatePlatoDTO:
    """Test UpdatePlatoDTO validation."""
    
    def test_valid_update_plato_dto(self):
        """Test valid dish update DTO."""
        nutritional_info = InformacionNutricionalDTO(
            calorias=500,
            proteinas=30.0,
            azucares=10.0
        )
        
        ingrediente_id = uuid4()
        receta = {ingrediente_id: 250.0}
        
        dto = UpdatePlatoDTO(
            nombre="Pasta Carbonara Deluxe",
            precio=Decimal("22.50"),
            informacion_nutricional=nutritional_info,
            receta=receta,
            porciones=3,
            dificultad="dificil"
        )
        
        assert dto.nombre == "Pasta Carbonara Deluxe"
        assert dto.precio == Decimal("22.50")
        assert dto.receta == receta
        assert dto.porciones == 3
        assert dto.dificultad == "dificil"
    
    def test_partial_update_dto(self):
        """Test partial update with only some fields."""
        dto = UpdatePlatoDTO(
            nombre="Pasta Actualizada",
            activo=False
        )
        
        assert dto.nombre == "Pasta Actualizada"
        assert dto.precio is None
        assert dto.activo is False
    
    def test_empty_name_in_update_raises_error(self):
        """Test that empty name in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdatePlatoDTO(nombre="")
        
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_invalid_dificultad_in_update_raises_error(self):
        """Test that invalid difficulty in update raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            UpdatePlatoDTO(dificultad="extremo")
        
        assert "String should match pattern" in str(exc_info.value)


class TestAgregarIngredienteRecetaDTO:
    """Test AgregarIngredienteRecetaDTO validation."""
    
    def test_valid_agregar_ingrediente_dto(self):
        """Test valid add ingredient to recipe DTO."""
        ingrediente_id = uuid4()
        
        dto = AgregarIngredienteRecetaDTO(
            ingrediente_id=ingrediente_id,
            cantidad=150.0
        )
        
        assert dto.ingrediente_id == ingrediente_id
        assert dto.cantidad == 150.0
    
    def test_negative_cantidad_raises_error(self):
        """Test that negative quantity raises validation error."""
        ingrediente_id = uuid4()
        
        with pytest.raises(ValidationError) as exc_info:
            AgregarIngredienteRecetaDTO(
                ingrediente_id=ingrediente_id,
                cantidad=-50.0
            )
        
        assert "Ingredient quantity must be positive" in str(exc_info.value) or "Input should be greater than 0" in str(exc_info.value)
    
    def test_zero_cantidad_raises_error(self):
        """Test that zero quantity raises validation error."""
        ingrediente_id = uuid4()
        
        with pytest.raises(ValidationError) as exc_info:
            AgregarIngredienteRecetaDTO(
                ingrediente_id=ingrediente_id,
                cantidad=0.0
            )
        
        assert "Ingredient quantity must be positive" in str(exc_info.value) or "Input should be greater than 0" in str(exc_info.value)


class TestActualizarIngredienteRecetaDTO:
    """Test ActualizarIngredienteRecetaDTO validation."""
    
    def test_valid_actualizar_ingrediente_dto(self):
        """Test valid update ingredient quantity DTO."""
        dto = ActualizarIngredienteRecetaDTO(
            nueva_cantidad=200.0
        )
        
        assert dto.nueva_cantidad == 200.0
    
    def test_negative_nueva_cantidad_raises_error(self):
        """Test that negative new quantity raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ActualizarIngredienteRecetaDTO(
                nueva_cantidad=-100.0
            )
        
        assert "New ingredient quantity must be positive" in str(exc_info.value) or "Input should be greater than 0" in str(exc_info.value)
    
    def test_zero_nueva_cantidad_raises_error(self):
        """Test that zero new quantity raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ActualizarIngredienteRecetaDTO(
                nueva_cantidad=0.0
            )
        
        assert "New ingredient quantity must be positive" in str(exc_info.value) or "Input should be greater than 0" in str(exc_info.value)