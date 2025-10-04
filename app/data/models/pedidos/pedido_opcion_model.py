"""
Order option model for selected options on order items.
"""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class PedidoOpcionModel(BaseModel):
    """Order option model for selected options on order items."""

    __tablename__ = "pedido_opcion"

    id_pedido_producto = Column(
        Integer,
        ForeignKey("pedido_producto.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to order item"
    )

    id_producto_opcion = Column(
        Integer,
        ForeignKey("producto_opcion.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to product option"
    )

    precio_adicional = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Additional price for this option at time of order"
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

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("precio_adicional >= 0", name="ck_pedido_opcion_precio_no_negativo"),
        Index("idx_pedido_opcion_pedido_item", "id_pedido_producto"),
        Index("idx_pedido_opcion_producto_opcion", "id_producto_opcion"),
    )