"""
Table model for restaurant table management.
Adapted to match existing MySQL schema restaurant_dp2.mesa
"""

from sqlalchemy import Column, String, Integer, Boolean, Enum, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class MesaModel(Base):
    """Table model matching restaurant_dp2.mesa table."""

    __tablename__ = "mesa"
    __table_args__ = (
        CheckConstraint("capacidad > 0", name="chk_capacidad"),
        Index("idx_qr", "qr_code"),
        Index("idx_estado", "estado"),
        Index("idx_zona", "zona"),
        Index("idx_activa", "activa"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Mesas físicas del restaurante'
        }
    )

    # Primary key matching your schema
    id_mesa = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    numero = Column(
        String(20),
        nullable=False,
        unique=True,
        comment="Table number (unique identifier)"
    )

    capacidad = Column(
        Integer,
        nullable=False,
        comment="Table seating capacity"
    )

    zona = Column(
        String(50),
        nullable=True,
        comment="interior, terraza, vip, etc."
    )

    qr_code = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="QR code for table identification"
    )

    estado = Column(
        Enum('disponible', 'ocupada', 'reservada', 'mantenimiento', name='estado_mesa_enum'),
        default='disponible',
        nullable=True,
        comment="Current table status"
    )

    activa = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Table active status"
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

    # Relationships
    sesiones = relationship(
        "SesionMesaModel",
        back_populates="mesa",
        lazy="select"
    )

    pedidos = relationship(
        "PedidoModel",
        back_populates="mesa",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_mesa': self.id_mesa,
            'numero': self.numero,
            'capacidad': self.capacidad,
            'zona': self.zona,
            'qr_code': self.qr_code,
            'estado': self.estado,
            'activa': self.activa,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }