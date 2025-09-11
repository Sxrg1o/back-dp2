"""
Tests for schema mappers.
"""
import pytest
from decimal import Decimal
from uuid import uuid4

from app.application.dto.item_dto import CreateItemDTO, InformacionNutricionalDTO
from app.infrastructure.web.schemas.menu_schemas import ItemCreateSchema, InformacionNutricionalSchema
from app.infrastructure.web.schemas.mappers.menu_schema_mapper import MenuSchemaMapper
from app.domain.value_objects.etiqueta_item import EtiquetaItem


class TestMenuSchemaMapper:
    """Test menu schema mapper."""
    
    def test_informacion_nutricional_schema_to_dto(self):
        """Test nutritional information schema to DTO conversion."""
        schema = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2,
            grasas=8.0,
            carbohidratos=30.0,
            fibra=5.0,
            sodio=200.0
        )
        
        dto = MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema)
        
        assert isinstance(dto, InformacionNutricionalDTO)
        assert dto.calorias == 250
        assert dto.proteinas == 15.5
        assert dto.azucares == 10.2
        assert dto.grasas == 8.0
        assert dto.carbohidratos == 30.0
        assert dto.fibra == 5.0
        assert dto.sodio == 200.0
    
    def test_informacion_nutricional_dto_to_schema(self):
        """Test nutritional information DTO to schema conversion."""
        dto = InformacionNutricionalDTO(
            calorias=250,
            proteinas=15.5,
            azucares=10.2,
            grasas=8.0,
            carbohidratos=30.0,
            fibra=5.0,
            sodio=200.0
        )
        
        schema = MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto)
        
        assert isinstance(schema, InformacionNutricionalSchema)
        assert schema.calorias == 250
        assert schema.proteinas == 15.5
        assert schema.azucares == 10.2
        assert schema.grasas == 8.0
        assert schema.carbohidratos == 30.0
        assert schema.fibra == 5.0
        assert schema.sodio == 200.0
    
    def test_item_create_schema_to_dto(self):
        """Test item create schema to DTO conversion."""
        nutritional_schema = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2
        )
        
        schema = ItemCreateSchema(
            nombre="Test Item",
            descripcion="Test description",
            precio=Decimal("15.99"),
            informacion_nutricional=nutritional_schema,
            tiempo_preparacion=10,
            stock_actual=50,
            stock_minimo=5,
            etiquetas={EtiquetaItem.SIN_GLUTEN, EtiquetaItem.VEGANO},
            activo=True
        )
        
        dto = MenuSchemaMapper.item_create_schema_to_dto(schema)
        
        assert isinstance(dto, CreateItemDTO)
        assert dto.nombre == "Test Item"
        assert dto.descripcion == "Test description"
        assert dto.precio == Decimal("15.99")
        assert isinstance(dto.informacion_nutricional, InformacionNutricionalDTO)
        assert dto.tiempo_preparacion == 10
        assert dto.stock_actual == 50
        assert dto.stock_minimo == 5
        assert EtiquetaItem.SIN_GLUTEN in dto.etiquetas
        assert EtiquetaItem.VEGANO in dto.etiquetas
        assert dto.activo is True
    
    def test_bidirectional_conversion_consistency(self):
        """Test that converting schema->dto->schema maintains data integrity."""
        original_schema = InformacionNutricionalSchema(
            calorias=250,
            proteinas=15.5,
            azucares=10.2,
            grasas=8.0
        )
        
        # Convert to DTO and back to schema
        dto = MenuSchemaMapper.informacion_nutricional_schema_to_dto(original_schema)
        converted_schema = MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto)
        
        # Verify all fields match
        assert converted_schema.calorias == original_schema.calorias
        assert converted_schema.proteinas == original_schema.proteinas
        assert converted_schema.azucares == original_schema.azucares
        assert converted_schema.grasas == original_schema.grasas
        assert converted_schema.carbohidratos == original_schema.carbohidratos
        assert converted_schema.fibra == original_schema.fibra
        assert converted_schema.sodio == original_schema.sodio