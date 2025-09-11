"""Value objects for the menu domain."""

from .etiqueta_item import EtiquetaItem
from .etiqueta_ingrediente import EtiquetaIngrediente
from .etiqueta_plato import EtiquetaPlato
from .precio import Precio
from .informacion_nutricional import InformacionNutricional

__all__ = [
    "EtiquetaItem",
    "EtiquetaIngrediente", 
    "EtiquetaPlato",
    "Precio",
    "InformacionNutricional"
]