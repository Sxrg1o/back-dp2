"""SQLAlchemy model for Item entity."""

from sqlalchemy import Column, String, Text, Integer, Boolean, Numeric, JSON

from app.infrastructure.persistence.models.base import BaseModel


class ItemModel(BaseModel):
    """SQLAlchemy model for Item persistence."""
    
    __tablename__ = "items"
    
    # Basic item information
    nombre = Column(String(255), nullable=False, index=True)
    descripcion = Column(Text)
    
    # Price information (stored as decimal for precision)
    precio = Column(Numeric(10, 2), nullable=False)
    
    # Nutritional information (stored as JSON for flexibility)
    informacion_nutricional = Column(JSON, nullable=False)
    
    # Stock and preparation
    tiempo_preparacion = Column(Integer, nullable=False)  # in minutes
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    
    # Labels/tags (stored as JSON array for SQLite compatibility)
    etiquetas = Column(JSON, nullable=False, default=list)
    
    # Status
    activo = Column(Boolean, nullable=False, default=True)
    
    # Discriminator for inheritance
    tipo = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": tipo,
    }