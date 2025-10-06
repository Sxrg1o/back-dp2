"""
Order model for managing customer orders.
Adapted to match existing MySQL schema restaurant_dp2.pedido
"""

from sqlalchemy import Column, String, Integer, Numeric, Text, Enum, ForeignKey, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class PedidoModel(Base):
    """Order model matching restaurant_dp2.pedido table."""

    __tablename__ = "pedido"
    __table_args__ = (
        CheckConstraint("subtotal >= 0 AND total >= 0", name="chk_totales_positivos"),
        Index("idx_mesa", "id_mesa"),
        Index("idx_numero", "numero_pedido"),
        Index("idx_estado", "estado"),
        Index("idx_created_at", "fecha_creacion"),
        Index("created_by", "creado_por"),
        Index("updated_by", "modificado_por"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Pedidos/órdenes del restaurante'
        }
    )

    # Primary key
    id_pedido = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_mesa = Column(
        Integer,
        ForeignKey("restaurant_dp2.mesa.id_mesa"),
        nullable=False,
        comment="Foreign key to mesa table"
    )

    numero_pedido = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Unique order number"
    )

    estado = Column(
        Enum('pendiente', 'confirmado', 'en_preparacion', 'listo', 'entregado', 'cancelado', name='estado_pedido_enum'),
        default='pendiente',
        nullable=True,
        comment="Order status"
    )

    prioridad = Column(
        Enum('normal', 'alta', 'urgente', name='prioridad_pedido_enum'),
        default='normal',
        nullable=True,
        comment="Order priority"
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Order subtotal"
    )

    impuestos = Column(
        Numeric(10, 2),
        nullable=True,
        default=0.00,
        comment="Tax amount"
    )

    descuentos = Column(
        Numeric(10, 2),
        nullable=True,
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
        TIMESTAMP,
        nullable=True,
        comment="Order confirmation timestamp"
    )

    fecha_en_preparacion = Column(
        TIMESTAMP,
        nullable=True,
        comment="Order preparation start timestamp"
    )

    fecha_listo = Column(
        TIMESTAMP,
        nullable=True,
        comment="Order ready timestamp"
    )

    fecha_entregado = Column(
        TIMESTAMP,
        nullable=True,
        comment="Order delivered timestamp"
    )

    fecha_cancelado = Column(
        TIMESTAMP,
        nullable=True,
        comment="Order cancellation timestamp"
    )

    fecha_creacion = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
    )

    fecha_modificacion = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Last modification timestamp"
    )

    creado_por = Column(
        Integer,
        ForeignKey("restaurant_dp2.usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
        comment="User who created the order"
    )

    modificado_por = Column(
        Integer,
        ForeignKey("restaurant_dp2.usuario.id_usuario", ondelete="SET NULL"),
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
        lazy="select"
    )

    usuario_modificador = relationship(
        "UsuarioModel",
        foreign_keys=[modificado_por],
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

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_pedido': self.id_pedido,
            'id_mesa': self.id_mesa,
            'numero_pedido': self.numero_pedido,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'subtotal': self.subtotal,
            'impuestos': self.impuestos,
            'descuentos': self.descuentos,
            'total': self.total,
            'notas_cliente': self.notas_cliente,
            'notas_cocina': self.notas_cocina,
            'fecha_confirmado': self.fecha_confirmado,
            'fecha_en_preparacion': self.fecha_en_preparacion,
            'fecha_listo': self.fecha_listo,
            'fecha_entregado': self.fecha_entregado,
            'fecha_cancelado': self.fecha_cancelado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion,
            'creado_por': self.creado_por,
            'modificado_por': self.modificado_por
        }
