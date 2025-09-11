"""Mapper for Bebida entity and BebidaModel."""

from decimal import Decimal
from typing import Set

from app.domain.entities.bebida import Bebida
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.infrastructure.persistence.models.bebida_model import BebidaModel
from app.infrastructure.persistence.mappers.base_mapper import BaseMapper


class BebidaMapper(BaseMapper[Bebida, BebidaModel]):
    """Mapper for converting between Bebida entity and BebidaModel."""
    
    def to_entity(self, model: BebidaModel) -> Bebida:
        """Convert BebidaModel to Bebida entity."""
        # Convert etiquetas from list of strings to set of EtiquetaItem enums
        etiquetas = set()
        if model.etiquetas:
            for etiqueta_str in model.etiquetas:
                try:
                    etiquetas.add(EtiquetaItem(etiqueta_str))
                except ValueError:
                    # Skip invalid enum values
                    continue
        
        # Convert nutritional information from JSON to value object
        nutricional_data = model.informacion_nutricional or {}
        informacion_nutricional = InformacionNutricional(
            calorias=nutricional_data.get('calorias', 0),
            proteinas=nutricional_data.get('proteinas', 0.0),
            azucares=nutricional_data.get('azucares', 0.0),
            grasas=nutricional_data.get('grasas'),
            carbohidratos=nutricional_data.get('carbohidratos'),
            fibra=nutricional_data.get('fibra'),
            sodio=nutricional_data.get('sodio')
        )
        
        return Bebida(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            precio=Precio(Decimal(str(model.precio))),
            informacion_nutricional=informacion_nutricional,
            tiempo_preparacion=model.tiempo_preparacion,
            stock_actual=model.stock_actual,
            stock_minimo=model.stock_minimo,
            etiquetas=etiquetas,
            activo=model.activo,
            created_at=model.created_at,
            updated_at=model.updated_at,
            version=model.version,
            volumen=model.volumen,
            contenido_alcohol=model.contenido_alcohol,
            temperatura_servicio=model.temperatura_servicio,
            tipo_bebida=model.tipo_bebida,
            marca=model.marca,
            origen=model.origen
        )
    
    def to_model(self, entity: Bebida) -> BebidaModel:
        """Convert Bebida entity to BebidaModel."""
        # Convert etiquetas from set of EtiquetaItem enums to list of strings
        etiquetas_list = [etiqueta.value for etiqueta in entity.etiquetas]
        
        # Convert nutritional information to JSON
        nutricional_dict = {
            'calorias': entity.informacion_nutricional.calorias,
            'proteinas': entity.informacion_nutricional.proteinas,
            'azucares': entity.informacion_nutricional.azucares,
            'grasas': entity.informacion_nutricional.grasas,
            'carbohidratos': entity.informacion_nutricional.carbohidratos,
            'fibra': entity.informacion_nutricional.fibra,
            'sodio': entity.informacion_nutricional.sodio
        }
        
        return BebidaModel(
            id=entity.id,
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            precio=float(entity.precio.value),
            informacion_nutricional=nutricional_dict,
            tiempo_preparacion=entity.tiempo_preparacion,
            stock_actual=entity.stock_actual,
            stock_minimo=entity.stock_minimo,
            etiquetas=etiquetas_list,
            activo=entity.activo,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            version=entity.version,
            volumen=entity.volumen,
            contenido_alcohol=entity.contenido_alcohol,
            temperatura_servicio=entity.temperatura_servicio,
            tipo_bebida=entity.tipo_bebida,
            marca=entity.marca,
            origen=entity.origen
        )