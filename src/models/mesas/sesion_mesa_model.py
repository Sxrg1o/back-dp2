"""
Table session model for tracking customer sessions at tables.
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class SesionMesaModel(BaseModel):
    """Table session model for tracking customer sessions."""

    __tablename__ = "sesiones_mesa"

    mesa_id = Column(
        Integer,
        ForeignKey("mesa.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to table"
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuario.id", ondelete="SET NULL"),
        nullable=True,
        comment="Foreign key to user (nullable for anonymous sessions)"
    )

    token_sesion = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="Unique session token"
    )

    alias_comensal = Column(
        String(100),
        nullable=True,
        comment="Customer alias for the session"
    )

    fecha_inicio = Column(
        DateTime,
        nullable=False,
        comment="Session start timestamp"
    )

    fecha_fin = Column(
        DateTime,
        nullable=True,
        comment="Session end timestamp"
    )

    activa = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Session active status"
    )

    ip_address = Column(
        String(45),
        nullable=True,
        comment="Client IP address (supports IPv6)"
    )

    user_agent = Column(
        String(500),
        nullable=True,
        comment="Client user agent string"
    )

    # Relationships
    mesa = relationship(
        "MesaModel",
        back_populates="sesiones",
        lazy="select"
    )

    usuario = relationship(
        "UsuarioModel",
        back_populates="sesiones_mesa",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint("token_sesion", name="uq_sesion_mesa_token"),
        Index("idx_sesion_mesa_mesa", "mesa_id"),
        Index("idx_sesion_mesa_token", "token_sesion"),
        Index("idx_sesion_mesa_activa", "activa"),
        Index("idx_sesion_mesa_usuario", "usuario_id"),
    )