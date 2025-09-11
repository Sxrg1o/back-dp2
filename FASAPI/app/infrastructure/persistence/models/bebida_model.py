"""SQLAlchemy model for Bebida entity."""

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.infrastructure.persistence.models.item_model import ItemModel


class BebidaModel(ItemModel):
    """SQLAlchemy model for Bebida persistence."""
    
    __tablename__ = "bebidas"
    
    # Foreign key to parent table for joined table inheritance
    id = Column(UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True)
    
    # Beverage-specific fields
    volumen = Column(Float, nullable=False)  # in milliliters
    contenido_alcohol = Column(Float, nullable=False, default=0.0)  # percentage (0-100)
    temperatura_servicio = Column(String(20))  # "fria", "caliente", "ambiente"
    tipo_bebida = Column(String(50))  # "gaseosa", "jugo", "cafe", "te", "cerveza", "vino", etc.
    marca = Column(String(255))
    origen = Column(String(255))
    
    __mapper_args__ = {
        "polymorphic_identity": "bebida",
    }