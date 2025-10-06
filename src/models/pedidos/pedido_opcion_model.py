"""
Order option model for selected options on order items.
Adapted to match existing MySQL schema restaurant_dp2.pedido_opcion
"""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Index, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class PedidoOpcionModel(Base):
    """Order option model matching restaurant_dp2.pedido_opcion table."""

    __tablename__ = "pedido_opcion"
    __table_args__ = (
        Index("idx_pedido_item", "id_pedido_producto"),
        Index("id_producto_opcion", "id_producto_opcion"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Opciones seleccionadas en productos de pedidos'
        }
    )

    # Primary key
    id_pedido_opcion = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_pedido_producto = Column(
        Integer,
        ForeignKey("restaurant_dp2.pedido_producto.id_pedido_producto", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to pedido_producto table"
    )

    id_producto_opcion = Column(
        Integer,
        ForeignKey("restaurant_dp2.producto_opcion.id_producto_opcion"),
        nullable=False,
        comment="Foreign key to producto_opcion table"
    )

    precio_adicional = Column(
        Numeric(10, 2),
        nullable=True,
        default=0.00,
        comment="Additional price for this option"
    )

    fecha_creacion = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
    )

    # Relationships
    pedido_producto = relationship(
        "PedidoProductoModel",
        back_populates="opciones",
        lazy="select"
    )

    producto_opcion = relationship(
        "ProductoOpcionModel",
        back_populates="pedido_opciones",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_pedido_opcion': self.id_pedido_opcion,
            'id_pedido_producto': self.id_pedido_producto,
            'id_producto_opcion': self.id_producto_opcion,
            'precio_adicional': self.precio_adicional,
            'fecha_creacion': self.fecha_creacion
        }
