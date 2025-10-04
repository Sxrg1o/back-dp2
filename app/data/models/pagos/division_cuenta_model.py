"""
Bill division model for splitting order costs.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Enum, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel
from app.shared.enums.pedido_enums import TipoDivision


class DivisionCuentaModel(BaseModel):
    """Bill division model for splitting order costs."""

    __tablename__ = "division_cuenta"

    id_pedido = Column(
        Integer,
        ForeignKey("pedido.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to order"
    )

    tipo_division = Column(
        Enum(TipoDivision),
        nullable=False,
        default=TipoDivision.EQUITATIVA,
        comment="Type of bill division"
    )

    cantidad_personas = Column(
        Integer,
        nullable=False,
        comment="Number of people to split the bill"
    )

    notas = Column(
        Text,
        nullable=True,
        comment="Notes about the division"
    )

    # Relationships
    pedido = relationship(
        "PedidoModel",
        back_populates="divisiones_cuenta",
        lazy="select"
    )

    detalles = relationship(
        "DivisionCuentaDetalleModel",
        back_populates="division_cuenta",
        lazy="select",
        cascade="all, delete-orphan"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("cantidad_personas > 0", name="ck_division_cuenta_personas_positivo"),
        Index("idx_division_cuenta_pedido", "id_pedido"),
    )