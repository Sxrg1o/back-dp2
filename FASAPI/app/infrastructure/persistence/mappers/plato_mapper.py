"""Mapper for Plato entity and PlatoModel."""

from decimal import Decimal
from typing import Set, Dict
from uuid import UUID

from app.domain.entities.plato import Plato
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.infrastructure.persistence.models.plato_model import PlatoModel
from app.infrastructure.persistence.mappers.base_mapper import BaseMapper


class PlatoMapper(BaseMapper[Plato, PlatoModel]):
    """Mapper for converting between Plato entity and PlatoModel."""
    
    def to_entity(self, model: PlatoModel) -> Plato:
        """Convert PlatoModel to Plato entity."""
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
        
        # Convert tipo_plato string to EtiquetaPlato enum
        tipo_plato = EtiquetaPlato(model.tipo_plato)
        
        # Convert receta from JSON dict with string keys to Dict[UUID, float]
        receta = {}
        if model.receta:
            for ingrediente_id_str, cantidad in model.receta.items():
                try:
                    ingrediente_id = UUID(ingrediente_id_str)
                    receta[ingrediente_id] = float(cantidad)
                except (ValueError, TypeError):
                    # Skip invalid UUID or cantidad values
                    continue
        
        return Plato(
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
            tipo_plato=tipo_plato,
            receta=receta,
            instrucciones=model.instrucciones,
            porciones=model.porciones,
            dificultad=model.dificultad,
            chef_recomendado=model.chef_recomendado
        )
    
    def to_model(self, entity: Plato) -> PlatoModel:
        """Convert Plato entity to PlatoModel."""
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
        
        # Convert receta from Dict[UUID, float] to JSON dict with string keys
        receta_dict = {}
        for ingrediente_id, cantidad in entity.receta.items():
            receta_dict[str(ingrediente_id)] = cantidad
        
        return PlatoModel(
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
            tipo_plato=entity.tipo_plato.value,
            receta=receta_dict,
            instrucciones=entity.instrucciones,
            porciones=entity.porciones,
            dificultad=entity.dificultad,
            chef_recomendado=entity.chef_recomendado
        )