"""
Option type model for product customization categories.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class TipoOpcionModel(BaseModel):
    """Option type model for categorizing product options."""

    __tablename__ = "tipo_opcion"

    codigo = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Option type code (e.g., nivel_aji, acompanamiento)"
    )

    nombre = Column(
        String(100),
        nullable=False,
        comment="Option type name"
    )

    descripcion = Column(
        Text,
        nullable=True,
        comment="Option type description"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Option type active status"
    )

    orden = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Display order"
    )

    # Relationships
    producto_opciones = relationship(
        "ProductoOpcionModel",
        back_populates="tipo_opcion",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        UniqueConstraint("codigo", name="uq_tipo_opcion_codigo"),
        Index("idx_tipo_opcion_activo", "activo"),
        Index("idx_tipo_opcion_orden", "orden"),
    )