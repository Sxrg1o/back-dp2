"""
Bill division model for splitting order costs.
Adapted to match existing MySQL schema restaurant_dp2.division_cuenta
"""

from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class DivisionCuentaModel(Base):
    """Bill division model matching restaurant_dp2.division_cuenta table."""

    __tablename__ = "division_cuenta"
    __table_args__ = (
        CheckConstraint("cantidad_personas > 0", name="chk_cantidad_personas"),
        Index("idx_pedido", "id_pedido"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'División de cuentas para pedidos compartidos'
        }
    )

    # Primary key
    id_division_cuenta = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_pedido = Column(
        Integer,
        ForeignKey("restaurant_dp2.pedido.id_pedido", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to pedido table"
    )

    tipo_division = Column(
        Enum('equitativa', 'por_items', 'manual', name='tipo_division_enum'),
        nullable=False,
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
        back_populates="divisiones_cuenta",
        lazy="select"
    )

    detalles = relationship(
        "DivisionCuentaDetalleModel",
        back_populates="division_cuenta",
        lazy="select",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_division_cuenta': self.id_division_cuenta,
            'id_pedido': self.id_pedido,
            'tipo_division': self.tipo_division,
            'cantidad_personas': self.cantidad_personas,
            'notas': self.notas,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
