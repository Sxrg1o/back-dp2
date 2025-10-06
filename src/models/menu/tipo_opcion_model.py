"""
Option type model for product customization categories.
Adapted to match existing MySQL schema restaurant_dp2.tipo_opcion
"""

from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class TipoOpcionModel(Base):
    """Option type model matching restaurant_dp2.tipo_opcion table."""

    __tablename__ = "tipo_opcion"
    __table_args__ = {
        'schema': 'restaurant_dp2'
    }

    # Primary key matching your schema
    id_tipo_opcion = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    codigo = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="nivel_aji, acompanamiento, temperatura"
    )

    nombre = Column(
        String(100),
        nullable=False,
        comment="Nivel de Ají, Acompañamiento, Temperatura"
    )

    descripcion = Column(
        String(255),
        nullable=True,
        comment="Option type description"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Option type active status"
    )

    orden = Column(
        Integer,
        default=0,
        nullable=True,
        comment="Display order"
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
    producto_opciones = relationship(
        "ProductoOpcionModel",
        back_populates="tipo_opcion",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_tipo_opcion': self.id_tipo_opcion,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'orden': self.orden,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }