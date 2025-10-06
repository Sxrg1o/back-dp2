"""
Payment model for order payments.
Adapted to match existing MySQL schema restaurant_dp2.pago
"""

from sqlalchemy import Column, String, Integer, Numeric, Text, Enum, ForeignKey, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class PagoModel(Base):
    """Payment model matching restaurant_dp2.pago table."""

    __tablename__ = "pago"
    __table_args__ = (
        CheckConstraint("monto >= 0 AND total >= 0", name="chk_montos_positivos"),
        Index("idx_pedido", "id_pedido"),
        Index("id_usuario", "id_usuario"),
        Index("idx_estado", "estado"),
        Index("idx_persona", "persona_numero"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Pagos realizados para pedidos'
        }
    )

    # Primary key
    id_pago = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_pedido = Column(
        Integer,
        ForeignKey("restaurant_dp2.pedido.id_pedido"),
        nullable=False,
        comment="Foreign key to pedido table"
    )

    id_usuario = Column(
        Integer,
        ForeignKey("restaurant_dp2.usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
        comment="Foreign key to usuario table (nullable for anonymous payments)"
    )

    persona_numero = Column(
        Integer,
        nullable=True,
        comment="Person number for bill division (1, 2, 3, etc.)"
    )

    metodo_pago = Column(
        Enum('efectivo', 'tarjeta', 'yape', 'plin', 'transferencia', name='metodo_pago_enum'),
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
        nullable=True,
        default=0.00,
        comment="Tip amount"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Total payment amount (monto + propina)"
    )

    estado = Column(
        Enum('pendiente', 'procesando', 'completado', 'fallido', 'cancelado', name='estado_pago_enum'),
        nullable=True,
        default='pendiente',
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
        TIMESTAMP,
        nullable=True,
        comment="Payment processing timestamp"
    )

    completado_at = Column(
        TIMESTAMP,
        nullable=True,
        comment="Payment completion timestamp"
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
        back_populates="pagos",
        lazy="select"
    )

    usuario = relationship(
        "UsuarioModel",
        back_populates="pagos",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_pago': self.id_pago,
            'id_pedido': self.id_pedido,
            'id_usuario': self.id_usuario,
            'persona_numero': self.persona_numero,
            'metodo_pago': self.metodo_pago,
            'monto': self.monto,
            'propina': self.propina,
            'total': self.total,
            'estado': self.estado,
            'referencia_externa': self.referencia_externa,
            'notas': self.notas,
            'procesado_at': self.procesado_at,
            'completado_at': self.completado_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
