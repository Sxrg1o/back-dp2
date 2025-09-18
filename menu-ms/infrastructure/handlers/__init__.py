"""
Módulo de handlers para endpoints del menú y carta.
Exporta todos los handlers de endpoints.
"""

from .item_handler import router as item_router
from .ingrediente_handler import router as ingrediente_router

__all__ = [
    'item_router',
    'ingrediente_router'
]
