"""
Order item model for products within an order.
"""

from sqlalchemy import Column, String, Integer, Numeric, Text, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class PedidoProductoModel(BaseModel):
    """Order item model for products in orders."""

    __tablename__ = "pedido_producto"

    id_pedido = Column(
        Integer,
        ForeignKey("pedido.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to order"
    )

    id_producto = Column(
        Integer,
        ForeignKey("producto.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to product"
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
        nullable=False,
        default=0.00,
        comment="Total price of selected options"
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Item subtotal (quantity * (unit_price + options_price))"
    )

    notas_personalizacion = Column(
        Text,
        nullable=True,
        comment="Customization notes for this item"
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
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_pedido_producto_cantidad_positiva"),
        CheckConstraint("precio_unitario >= 0", name="ck_pedido_producto_precio_no_negativo"),
        CheckConstraint("precio_opciones >= 0", name="ck_pedido_producto_opciones_no_negativo"),
        CheckConstraint("subtotal >= 0", name="ck_pedido_producto_subtotal_no_negativo"),
        Index("idx_pedido_producto_pedido", "id_pedido"),
        Index("idx_pedido_producto_producto", "id_producto"),
    )