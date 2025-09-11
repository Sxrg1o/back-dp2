"""SQLAlchemy repository adapters for domain entities."""

from .base_repository import BaseSQLAlchemyRepository
from .sqlalchemy_item_repository import SqlAlchemyItemRepository
from .sqlalchemy_ingrediente_repository import SqlAlchemyIngredienteRepository
from .sqlalchemy_plato_repository import SqlAlchemyPlatoRepository
from .sqlalchemy_bebida_repository import SqlAlchemyBebidaRepository

__all__ = [
    "BaseSQLAlchemyRepository",
    "SqlAlchemyItemRepository",
    "SqlAlchemyIngredienteRepository",
    "SqlAlchemyPlatoRepository",
    "SqlAlchemyBebidaRepository",
]