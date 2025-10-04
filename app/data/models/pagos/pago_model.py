"""
Payment model for order payments.
"""

from sqlalchemy import (
    Column, String, Integer, Numeric, Text, DateTime, ForeignKey,
    Enum, Index, CheckConstraint
)
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel
from app.shared.enums.pago_enums import MetodoPago, EstadoPago


class PagoModel(BaseModel):
    """Payment model for order payments."""

    __tablename__ = "pago"

    id_pedido = Column(
        Integer,
        ForeignKey("pedido.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to order"
    )

    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,
        comment="Foreign key to user (nullable for anonymous payments)"
    )

    persona_numero = Column(
        Integer,
        nullable=True,
        comment="Person number for bill division (1, 2, 3, etc.)"
    )

    metodo_pago = Column(
        Enum(MetodoPago),
        nullable=False,
        comment="Payment method"
    )

    monto = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Payment amount (without tip)"
    )

    propina = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Tip amount"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Total payment amount (monto + propina)"
    )

    estado = Column(
        Enum(EstadoPago),
        nullable=False,
        default=EstadoPago.PENDIENTE,
        comment="Payment status"
    )

    referencia_externa = Column(
        String(255),
        nullable=True,
        comment="External payment reference (transaction ID, etc.)"
    )

    notas = Column(
        Text,
        nullable=True,
        comment="Payment notes"
    )

    procesado_at = Column(
        DateTime,
        nullable=True,
        comment="Payment processing timestamp"
    )

    completado_at = Column(
        DateTime,
        nullable=True,
        comment="Payment completion timestamp"
    )

    # Relationships
    pedido = relationship(
        "PedidoModel",
        back_populates="pagos",
        lazy="select"
    )

    usuario = relationship(
        "UsuarioModel",
        back_populates="pagos",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("monto >= 0", name="ck_pago_monto_no_negativo"),
        CheckConstraint("total >= 0", name="ck_pago_total_no_negativo"),
        CheckConstraint("propina >= 0", name="ck_pago_propina_no_negativo"),
        CheckConstraint("persona_numero > 0", name="ck_pago_persona_positivo"),
        Index("idx_pago_pedido", "id_pedido"),
        Index("idx_pago_estado", "estado"),
        Index("idx_pago_persona", "persona_numero"),
        Index("idx_pago_usuario", "id_usuario"),
        Index("idx_pago_metodo", "metodo_pago"),
    )