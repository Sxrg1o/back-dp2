"""Mapper for Ingrediente entity and IngredienteModel."""

from decimal import Decimal
from typing import Set

from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.infrastructure.persistence.models.ingrediente_model import IngredienteModel
from app.infrastructure.persistence.mappers.base_mapper import BaseMapper


class IngredienteMapper(BaseMapper[Ingrediente, IngredienteModel]):
    """Mapper for converting between Ingrediente entity and IngredienteModel."""
    
    def to_entity(self, model: IngredienteModel) -> Ingrediente:
        """Convert IngredienteModel to Ingrediente entity."""
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
        
        # Convert tipo_ingrediente string to EtiquetaIngrediente enum
        tipo = EtiquetaIngrediente(model.tipo_ingrediente)
        
        return Ingrediente(
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
            tipo=tipo,
            peso_unitario=model.peso_unitario,
            unidad_medida=model.unidad_medida,
            fecha_vencimiento=model.fecha_vencimiento,
            proveedor=model.proveedor
        )
    
    def to_model(self, entity: Ingrediente) -> IngredienteModel:
        """Convert Ingrediente entity to IngredienteModel."""
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
        
        return IngredienteModel(
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
            tipo_ingrediente=entity.tipo.value,
            peso_unitario=entity.peso_unitario,
            unidad_medida=entity.unidad_medida,
            fecha_vencimiento=entity.fecha_vencimiento,
            proveedor=entity.proveedor
        )