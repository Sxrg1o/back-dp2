"""
Order product model for products within an order.
Adapted to match existing MySQL schema restaurant_dp2.pedido_producto
"""

from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey, Index, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class PedidoProductoModel(Base):
    """Order product model matching restaurant_dp2.pedido_producto table."""

    __tablename__ = "pedido_producto"
    __table_args__ = (
        Index("idx_pedido", "id_pedido"),
        Index("id_producto", "id_producto"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Productos dentro de un pedido'
        }
    )

    # Primary key
    id_pedido_producto = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_pedido = Column(
        Integer,
        ForeignKey("restaurant_dp2.pedido.id_pedido", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to pedido table"
    )

    id_producto = Column(
        Integer,
        ForeignKey("restaurant_dp2.producto.id_producto"),
        nullable=False,
        comment="Foreign key to producto table"
    )

    cantidad = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Product quantity"
    )

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Unit price at time of order"
    )

    precio_opciones = Column(
        Numeric(10, 2),
        nullable=True,
        default=0.00,
        comment="Total price of selected options"
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Item subtotal"
    )

    notas_personalizacion = Column(
        Text,
        nullable=True,
        comment="Customization notes for this item"
    )

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Last update timestamp"
    )

    # Relationships
    pedido = relationship(
        "PedidoModel",
        back_populates="productos",
        lazy="select"
    )

    producto = relationship(
        "ProductoModel",
        back_populates="pedido_productos",
        lazy="select"
    )

    opciones = relationship(
        "PedidoOpcionModel",
        back_populates="pedido_producto",
        lazy="select",
        cascade="all, delete-orphan"
    )

    divisiones_detalle = relationship(
        "DivisionCuentaDetalleModel",
        back_populates="pedido_producto",
        lazy="select",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_pedido_producto': self.id_pedido_producto,
            'id_pedido': self.id_pedido,
            'id_producto': self.id_producto,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'precio_opciones': self.precio_opciones,
            'subtotal': self.subtotal,
            'notas_personalizacion': self.notas_personalizacion,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
