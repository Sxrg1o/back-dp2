"""
Pedido (Order) model.
"""
from enum import Enum
from sqlalchemy import Column, String, ForeignKey, Numeric, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class EstadoPedido(str, Enum):
    """Order status enumeration."""
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class Pedido(BaseModel):
    """Pedido/Order model."""
    
    __tablename__ = "pedidos"
    
    numero = Column(String(50), unique=True, nullable=False, index=True)
    mesa_id = Column(UUID(as_uuid=True), ForeignKey("mesas.id"), nullable=False)
    cliente_nombre = Column(String(200))
    total = Column(Numeric(10, 2), nullable=False, default=0)
    estado = Column(SQLEnum(EstadoPedido), default=EstadoPedido.PENDIENTE, nullable=False)
    observaciones = Column(Text)
    
    # Relationships
    # mesa = relationship("Mesa", back_populates="pedidos")
    # items = relationship("ItemPedido", back_populates="pedido")
    
    def __repr__(self) -> str:
        return f"<Pedido(numero='{self.numero}', estado='{self.estado}')>"