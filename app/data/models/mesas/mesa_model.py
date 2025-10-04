"""
Table model for restaurant table management.
"""

from sqlalchemy import Column, String, Integer, Boolean, Enum, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel
from app.shared.enums.mesa_enums import EstadoMesa


class MesaModel(BaseModel):
    """Table model for restaurant tables."""

    __tablename__ = "mesa"

    numero = Column(
        String(10),
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
        comment="Restaurant zone or section"
    )

    qr_code = Column(
        String(255),
        nullable=True,
        unique=True,
        comment="QR code for table identification"
    )

    estado = Column(
        Enum(EstadoMesa),
        nullable=False,
        default=EstadoMesa.DISPONIBLE,
        comment="Current table status"
    )

    activa = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Table active status"
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

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("capacidad > 0", name="ck_mesa_capacidad_positiva"),
        UniqueConstraint("numero", name="uq_mesa_numero"),
        UniqueConstraint("qr_code", name="uq_mesa_qr_code"),
        Index("idx_mesa_qr", "qr_code"),
        Index("idx_mesa_estado", "estado"),
        Index("idx_mesa_zona", "zona"),
        Index("idx_mesa_activa", "activa"),
    )