"""
Módulo de repositorios del dominio para el menú y carta.
Exporta todas las interfaces de repositorios del dominio.
"""

from .item_repository import ItemRepository, PlatoRepository, BebidaRepository
from .ingrediente_repository import IngredienteRepository

__all__ = [
    'ItemRepository',
    'PlatoRepository', 
    'BebidaRepository',
    'IngredienteRepository'
]
