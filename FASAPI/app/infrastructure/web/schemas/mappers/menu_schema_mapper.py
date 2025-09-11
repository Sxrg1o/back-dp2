"""
Mappers between menu DTOs and API schemas.
"""
from typing import Dict, List, Optional, Set
from uuid import UUID

from app.application.dto.item_dto import (
    CreateItemDTO, 
    UpdateItemDTO, 
    ItemResponseDTO,
    InformacionNutricionalDTO
)
from app.application.dto.ingrediente_dto import (
    CreateIngredienteDTO,
    UpdateIngredienteDTO,
    IngredienteResponseDTO,
    StockUpdateDTO
)
from app.application.dto.plato_dto import (
    CreatePlatoDTO,
    UpdatePlatoDTO,
    PlatoResponseDTO,
    AgregarIngredienteRecetaDTO,
    ActualizarIngredienteRecetaDTO
)
from app.application.dto.bebida_dto import (
    CreateBebidaDTO,
    UpdateBebidaDTO,
    BebidaResponseDTO
)
from app.infrastructure.web.schemas.menu_schemas import (
    ItemCreateSchema,
    ItemUpdateSchema,
    ItemResponseSchema,
    ItemListResponseSchema,
    InformacionNutricionalSchema
)
from app.infrastructure.web.schemas.ingrediente_schemas import (
    IngredienteCreateSchema,
    IngredienteUpdateSchema,
    IngredienteResponseSchema,
    IngredienteListResponseSchema,
    StockUpdateSchema
)
from app.infrastructure.web.schemas.plato_schemas import (
    PlatoCreateSchema,
    PlatoUpdateSchema,
    PlatoResponseSchema,
    PlatoListResponseSchema,
    AgregarIngredienteRecetaSchema,
    ActualizarIngredienteRecetaSchema
)
from app.infrastructure.web.schemas.bebida_schemas import (
    BebidaCreateSchema,
    BebidaUpdateSchema,
    BebidaResponseSchema,
    BebidaListResponseSchema
)


class MenuSchemaMapper:
    """Mapper for menu item schemas and DTOs."""
    
    @staticmethod
    def informacion_nutricional_schema_to_dto(schema: InformacionNutricionalSchema) -> InformacionNutricionalDTO:
        """Convert nutritional information schema to DTO."""
        return InformacionNutricionalDTO(
            calorias=schema.calorias,
            proteinas=schema.proteinas,
            azucares=schema.azucares,
            grasas=schema.grasas,
            carbohidratos=schema.carbohidratos,
            fibra=schema.fibra,
            sodio=schema.sodio
        )
    
    @staticmethod
    def informacion_nutricional_dto_to_schema(dto: InformacionNutricionalDTO) -> InformacionNutricionalSchema:
        """Convert nutritional information DTO to schema."""
        return InformacionNutricionalSchema(
            calorias=dto.calorias,
            proteinas=dto.proteinas,
            azucares=dto.azucares,
            grasas=dto.grasas,
            carbohidratos=dto.carbohidratos,
            fibra=dto.fibra,
            sodio=dto.sodio
        )
    
    @staticmethod
    def item_create_schema_to_dto(schema: ItemCreateSchema) -> CreateItemDTO:
        """Convert item create schema to DTO."""
        return CreateItemDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional),
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo
        )
    
    @staticmethod
    def item_update_schema_to_dto(schema: ItemUpdateSchema) -> UpdateItemDTO:
        """Convert item update schema to DTO."""
        return UpdateItemDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional) if schema.informacion_nutricional else None,
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo
        )
    
    @staticmethod
    def item_dto_to_response_schema(dto: ItemResponseDTO) -> ItemResponseSchema:
        """Convert item DTO to response schema."""
        return ItemResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio=dto.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto.informacion_nutricional),
            tiempo_preparacion=dto.tiempo_preparacion,
            stock_actual=dto.stock_actual,
            stock_minimo=dto.stock_minimo,
            etiquetas=dto.etiquetas,
            activo=dto.activo,
            created_at=dto.created_at if hasattr(dto, 'created_at') else None,
            updated_at=dto.updated_at if hasattr(dto, 'updated_at') else None,
            version=dto.version if hasattr(dto, 'version') else 1
        )
    
    @staticmethod
    def item_dto_to_list_response_schema(dto: ItemResponseDTO) -> ItemListResponseSchema:
        """Convert item DTO to list response schema."""
        return ItemListResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            precio=dto.precio,
            stock_actual=dto.stock_actual,
            activo=dto.activo,
            etiquetas=dto.etiquetas
        )


class IngredienteSchemaMapper:
    """Mapper for ingredient schemas and DTOs."""
    
    @staticmethod
    def ingrediente_create_schema_to_dto(schema: IngredienteCreateSchema) -> CreateIngredienteDTO:
        """Convert ingredient create schema to DTO."""
        return CreateIngredienteDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional),
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            tipo=schema.tipo,
            peso_unitario=schema.peso_unitario,
            unidad_medida=schema.unidad_medida,
            fecha_vencimiento=schema.fecha_vencimiento,
            proveedor=schema.proveedor
        )
    
    @staticmethod
    def ingrediente_update_schema_to_dto(schema: IngredienteUpdateSchema) -> UpdateIngredienteDTO:
        """Convert ingredient update schema to DTO."""
        return UpdateIngredienteDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional) if schema.informacion_nutricional else None,
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            tipo=schema.tipo,
            peso_unitario=schema.peso_unitario,
            unidad_medida=schema.unidad_medida,
            fecha_vencimiento=schema.fecha_vencimiento,
            proveedor=schema.proveedor
        )
    
    @staticmethod
    def ingrediente_dto_to_response_schema(dto: IngredienteResponseDTO) -> IngredienteResponseSchema:
        """Convert ingredient DTO to response schema."""
        return IngredienteResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio=dto.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto.informacion_nutricional),
            tiempo_preparacion=dto.tiempo_preparacion,
            stock_actual=dto.stock_actual,
            stock_minimo=dto.stock_minimo,
            etiquetas=dto.etiquetas,
            activo=dto.activo,
            tipo=dto.tipo,
            peso_unitario=dto.peso_unitario,
            unidad_medida=dto.unidad_medida,
            fecha_vencimiento=dto.fecha_vencimiento,
            proveedor=dto.proveedor,
            created_at=dto.created_at if hasattr(dto, 'created_at') else None,
            updated_at=dto.updated_at if hasattr(dto, 'updated_at') else None,
            version=dto.version if hasattr(dto, 'version') else 1
        )
    
    @staticmethod
    def ingrediente_dto_to_list_response_schema(dto: IngredienteResponseDTO) -> IngredienteListResponseSchema:
        """Convert ingredient DTO to list response schema."""
        return IngredienteListResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            tipo=dto.tipo,
            precio=dto.precio,
            stock_actual=dto.stock_actual,
            activo=dto.activo,
            fecha_vencimiento=dto.fecha_vencimiento
        )
    
    @staticmethod
    def stock_update_schema_to_dto(schema: StockUpdateSchema) -> StockUpdateDTO:
        """Convert stock update schema to DTO."""
        return StockUpdateDTO(
            cantidad=schema.cantidad,
            operacion=schema.operacion
        )


class PlatoSchemaMapper:
    """Mapper for dish schemas and DTOs."""
    
    @staticmethod
    def plato_create_schema_to_dto(schema: PlatoCreateSchema) -> CreatePlatoDTO:
        """Convert dish create schema to DTO."""
        return CreatePlatoDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional),
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            tipo_plato=schema.tipo_plato,
            receta=schema.receta,
            instrucciones=schema.instrucciones,
            porciones=schema.porciones,
            dificultad=schema.dificultad,
            chef_recomendado=schema.chef_recomendado
        )
    
    @staticmethod
    def plato_update_schema_to_dto(schema: PlatoUpdateSchema) -> UpdatePlatoDTO:
        """Convert dish update schema to DTO."""
        return UpdatePlatoDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional) if schema.informacion_nutricional else None,
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            tipo_plato=schema.tipo_plato,
            receta=schema.receta,
            instrucciones=schema.instrucciones,
            porciones=schema.porciones,
            dificultad=schema.dificultad,
            chef_recomendado=schema.chef_recomendado
        )
    
    @staticmethod
    def plato_dto_to_response_schema(dto: PlatoResponseDTO) -> PlatoResponseSchema:
        """Convert dish DTO to response schema."""
        return PlatoResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio=dto.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto.informacion_nutricional),
            tiempo_preparacion=dto.tiempo_preparacion,
            stock_actual=dto.stock_actual,
            stock_minimo=dto.stock_minimo,
            etiquetas=dto.etiquetas,
            activo=dto.activo,
            tipo_plato=dto.tipo_plato,
            receta=dto.receta,
            instrucciones=dto.instrucciones,
            porciones=dto.porciones,
            dificultad=dto.dificultad,
            chef_recomendado=dto.chef_recomendado,
            created_at=dto.created_at if hasattr(dto, 'created_at') else None,
            updated_at=dto.updated_at if hasattr(dto, 'updated_at') else None,
            version=dto.version if hasattr(dto, 'version') else 1
        )
    
    @staticmethod
    def plato_dto_to_list_response_schema(dto: PlatoResponseDTO) -> PlatoListResponseSchema:
        """Convert dish DTO to list response schema."""
        return PlatoListResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            tipo_plato=dto.tipo_plato,
            precio=dto.precio,
            stock_actual=dto.stock_actual,
            activo=dto.activo,
            porciones=dto.porciones
        )
    
    @staticmethod
    def agregar_ingrediente_schema_to_dto(schema: AgregarIngredienteRecetaSchema) -> AgregarIngredienteRecetaDTO:
        """Convert add ingredient schema to DTO."""
        return AgregarIngredienteRecetaDTO(
            ingrediente_id=schema.ingrediente_id,
            cantidad=schema.cantidad
        )
    
    @staticmethod
    def actualizar_ingrediente_schema_to_dto(schema: ActualizarIngredienteRecetaSchema) -> ActualizarIngredienteRecetaDTO:
        """Convert update ingredient schema to DTO."""
        return ActualizarIngredienteRecetaDTO(
            nueva_cantidad=schema.nueva_cantidad
        )


class BebidaSchemaMapper:
    """Mapper for beverage schemas and DTOs."""
    
    @staticmethod
    def bebida_create_schema_to_dto(schema: BebidaCreateSchema) -> CreateBebidaDTO:
        """Convert beverage create schema to DTO."""
        return CreateBebidaDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional),
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            volumen=schema.volumen,
            contenido_alcohol=schema.contenido_alcohol,
            temperatura_servicio=schema.temperatura_servicio,
            tipo_bebida=schema.tipo_bebida,
            marca=schema.marca,
            origen=schema.origen
        )
    
    @staticmethod
    def bebida_update_schema_to_dto(schema: BebidaUpdateSchema) -> UpdateBebidaDTO:
        """Convert beverage update schema to DTO."""
        return UpdateBebidaDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio=schema.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_schema_to_dto(schema.informacion_nutricional) if schema.informacion_nutricional else None,
            tiempo_preparacion=schema.tiempo_preparacion,
            stock_actual=schema.stock_actual,
            stock_minimo=schema.stock_minimo,
            etiquetas=schema.etiquetas,
            activo=schema.activo,
            volumen=schema.volumen,
            contenido_alcohol=schema.contenido_alcohol,
            temperatura_servicio=schema.temperatura_servicio,
            tipo_bebida=schema.tipo_bebida,
            marca=schema.marca,
            origen=schema.origen
        )
    
    @staticmethod
    def bebida_dto_to_response_schema(dto: BebidaResponseDTO) -> BebidaResponseSchema:
        """Convert beverage DTO to response schema."""
        return BebidaResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio=dto.precio,
            informacion_nutricional=MenuSchemaMapper.informacion_nutricional_dto_to_schema(dto.informacion_nutricional),
            tiempo_preparacion=dto.tiempo_preparacion,
            stock_actual=dto.stock_actual,
            stock_minimo=dto.stock_minimo,
            etiquetas=dto.etiquetas,
            activo=dto.activo,
            volumen=dto.volumen,
            contenido_alcohol=dto.contenido_alcohol,
            temperatura_servicio=dto.temperatura_servicio,
            tipo_bebida=dto.tipo_bebida,
            marca=dto.marca,
            origen=dto.origen,
            created_at=dto.created_at if hasattr(dto, 'created_at') else None,
            updated_at=dto.updated_at if hasattr(dto, 'updated_at') else None,
            version=dto.version if hasattr(dto, 'version') else 1
        )
    
    @staticmethod
    def bebida_dto_to_list_response_schema(dto: BebidaResponseDTO) -> BebidaListResponseSchema:
        """Convert beverage DTO to list response schema."""
        return BebidaListResponseSchema(
            id=dto.id,
            nombre=dto.nombre,
            precio=dto.precio,
            volumen=dto.volumen,
            contenido_alcohol=dto.contenido_alcohol,
            stock_actual=dto.stock_actual,
            activo=dto.activo
        )