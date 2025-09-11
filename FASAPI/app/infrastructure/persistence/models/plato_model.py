"""SQLAlchemy model for Plato entity."""

from sqlalchemy import Column, String, Text, Integer, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.models.item_model import ItemModel


class PlatoModel(ItemModel):
    """SQLAlchemy model for Plato persistence."""
    
    __tablename__ = "platos"
    
    # Foreign key to parent table for joined table inheritance
    id = Column(UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True)
    
    # Dish-specific fields
    tipo_plato = Column(String(50), nullable=False)  # EtiquetaPlato enum value
    receta = Column(JSON, nullable=False, default=dict)  # ingrediente_id -> cantidad_necesaria mapping
    instrucciones = Column(Text)
    porciones = Column(Integer, nullable=False, default=1)
    dificultad = Column(String(20))  # "facil", "medio", "dificil"
    chef_recomendado = Column(String(255))
    
    __mapper_args__ = {
        "polymorphic_identity": "plato",
    }