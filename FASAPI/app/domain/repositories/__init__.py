"""Repository interfaces for menu domain."""

from .item_repository import ItemRepositoryPort
from .ingrediente_repository import IngredienteRepositoryPort
from .plato_repository import PlatoRepositoryPort
from .bebida_repository import BebidaRepositoryPort

__all__ = [
    "ItemRepositoryPort",
    "IngredienteRepositoryPort", 
    "PlatoRepositoryPort",
    "BebidaRepositoryPort",
]