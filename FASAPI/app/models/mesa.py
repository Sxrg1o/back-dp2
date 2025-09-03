"""
Mesa (Table) model.
"""
from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Mesa(BaseModel):
    """Mesa/Table model for restaurant seating."""
    
    __tablename__ = "mesas"
    
    numero = Column(Integer, unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)
    ubicacion = Column(String(100))
    descripcion = Column(Text)
    activa = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    # pedidos = relationship("Pedido", back_populates="mesa")
    
    def __repr__(self) -> str:
        return f"<Mesa(numero={self.numero}, nombre='{self.nombre}')>"