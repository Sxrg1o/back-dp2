"""
Order model for managing customer orders.
"""

from sqlalchemy import (
    Column, String, Integer, Numeric, Text, DateTime, Boolean, ForeignKey,
    Enum, UniqueConstraint, Index, CheckConstraint
)
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel
from app.shared.enums.pedido_enums import EstadoPedido, PrioridadPedido


class PedidoModel(BaseModel):
    """Order model for customer orders."""

    __tablename__ = "pedido"

    id_mesa = Column(
        Integer,
        ForeignKey("mesa.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to table"
    )

    numero_pedido = Column(
        String(20),
        nullable=False,
        unique=True,
        comment="Unique order number"
    )

    estado = Column(
        Enum(EstadoPedido),
        nullable=False,
        default=EstadoPedido.PENDIENTE,
        comment="Order status"
    )

    prioridad = Column(
        Enum(PrioridadPedido),
        nullable=False,
        default=PrioridadPedido.NORMAL,
        comment="Order priority"
    )

    tiempo_estimado = Column(
        Integer,
        nullable=True,
        comment="Estimated preparation time in minutes"
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Order subtotal before taxes and discounts"
    )

    impuestos = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Tax amount"
    )

    descuentos = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Discount amount"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Order total amount"
    )

    notas_cliente = Column(
        Text,
        nullable=True,
        comment="Customer notes for the order"
    )

    notas_cocina = Column(
        Text,
        nullable=True,
        comment="Kitchen notes for the order"
    )

    fecha_confirmado = Column(
        DateTime,
        nullable=True,
        comment="Order confirmation timestamp"
    )

    fecha_en_preparacion = Column(
        DateTime,
        nullable=True,
        comment="Order preparation start timestamp"
    )

    fecha_listo = Column(
        DateTime,
        nullable=True,
        comment="Order ready timestamp"
    )

    fecha_entregado = Column(
        DateTime,
        nullable=True,
        comment="Order delivered timestamp"
    )

    fecha_cancelado = Column(
        DateTime,
        nullable=True,
        comment="Order cancellation timestamp"
    )

    creado_por = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=False,
        comment="User who created the order"
    )

    modificado_por = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="RESTRICT"),
        nullable=True,
        comment="User who last modified the order"
    )

    # Relationships
    mesa = relationship(
        "MesaModel",
        back_populates="pedidos",
        lazy="select"
    )

    usuario_creador = relationship(
        "UsuarioModel",
        foreign_keys=[creado_por],
        back_populates="pedidos_creados",
        lazy="select"
    )

    usuario_modificador = relationship(
        "UsuarioModel",
        foreign_keys=[modificado_por],
        back_populates="pedidos_modificados",
        lazy="select"
    )

    productos = relationship(
        "PedidoProductoModel",
        back_populates="pedido",
        lazy="select",
        cascade="all, delete-orphan"
    )

    divisiones_cuenta = relationship(
        "DivisionCuentaModel",
        back_populates="pedido",
        lazy="select",
        cascade="all, delete-orphan"
    )

    pagos = relationship(
        "PagoModel",
        back_populates="pedido",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("tiempo_estimado > 0", name="ck_pedido_tiempo_positivo"),
        CheckConstraint("subtotal >= 0", name="ck_pedido_subtotal_no_negativo"),
        CheckConstraint("total >= 0", name="ck_pedido_total_no_negativo"),
        UniqueConstraint("numero_pedido", name="uq_pedido_numero"),
        Index("idx_pedido_mesa", "id_mesa"),
        Index("idx_pedido_numero", "numero_pedido"),
        Index("idx_pedido_estado", "estado"),
        Index("idx_pedido_created_at", "created_at"),
        Index("idx_pedido_creado_por", "creado_por"),
    )