"""
Bill division detail model for individual item assignments.
"""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class DivisionCuentaDetalleModel(BaseModel):
    """Bill division detail model for individual item assignments."""

    __tablename__ = "division_cuenta_detalle"

    id_division_cuenta = Column(
        Integer,
        ForeignKey("division_cuenta.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to bill division"
    )

    id_pedido_producto = Column(
        Integer,
        ForeignKey("pedido_producto.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to order item"
    )

    persona_numero = Column(
        Integer,
        nullable=False,
        comment="Person number (1, 2, 3, etc.)"
    )

    monto_asignado = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Amount assigned to this person for this item"
    )

    # Relationships
    division_cuenta = relationship(
        "DivisionCuentaModel",
        back_populates="detalles",
        lazy="select"
    )

    pedido_producto = relationship(
        "PedidoProductoModel",
        back_populates="divisiones_detalle",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("monto_asignado >= 0", name="ck_division_detalle_monto_no_negativo"),
        CheckConstraint("persona_numero > 0", name="ck_division_detalle_persona_positivo"),
        Index("idx_division_detalle_division", "id_division_cuenta"),
        Index("idx_division_detalle_persona", "persona_numero"),
        Index("idx_division_detalle_pedido_producto", "id_pedido_producto"),
    )