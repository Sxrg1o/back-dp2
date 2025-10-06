"""
Bill division detail model for individual item assignments.
Adapted to match existing MySQL schema restaurant_dp2.division_cuenta_detalle
"""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class DivisionCuentaDetalleModel(Base):
    """Bill division detail model matching restaurant_dp2.division_cuenta_detalle table."""

    __tablename__ = "division_cuenta_detalle"
    __table_args__ = (
        CheckConstraint("monto_asignado >= 0", name="chk_monto_asignado"),
        Index("idx_division", "id_division_cuenta"),
        Index("idx_persona", "persona_numero"),
        Index("id_pedido_producto", "id_pedido_producto"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Detalle de división de cuenta por producto y persona'
        }
    )

    # Primary key
    id_division_detalle = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_division_cuenta = Column(
        Integer,
        ForeignKey("restaurant_dp2.division_cuenta.id_division_cuenta", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to division_cuenta table"
    )

    id_pedido_producto = Column(
        Integer,
        ForeignKey("restaurant_dp2.pedido_producto.id_pedido_producto", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to pedido_producto table"
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

    created_at = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
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

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_division_detalle': self.id_division_detalle,
            'id_division_cuenta': self.id_division_cuenta,
            'id_pedido_producto': self.id_pedido_producto,
            'persona_numero': self.persona_numero,
            'monto_asignado': self.monto_asignado,
            'created_at': self.created_at
        }
