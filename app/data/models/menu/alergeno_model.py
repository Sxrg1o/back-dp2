"""
Allergen model for menu item allergen management.
Adapted to match existing MySQL schema restaurant_dp2.alergeno
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, TIMESTAMP, func, Index
from sqlalchemy.orm import relationship

from app.config.database import Base


class AlergenoModel(Base):
    """Allergen model matching restaurant_dp2.alergeno table."""

    __tablename__ = "alergeno"
    __table_args__ = (
        Index('idx_activo', 'activo'),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Catálogo de alérgenos alimentarios'
        }
    )

    # Primary key matching your schema
    id_alergeno = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    nombre = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Gluten, Lactosa, Mariscos, etc"
    )

    descripcion = Column(
        Text,
        nullable=True,
        comment="Allergen description"
    )

    icono = Column(
        String(50),
        nullable=True,
        comment="Nombre del icono o emoji para UI"
    )

    nivel_riesgo = Column(
        Enum('bajo', 'medio', 'alto', 'critico', name='nivel_riesgo_enum'),
        default='medio',
        nullable=True,
        comment="Risk level"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Active status"
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

    # Relationships (will be added when other models are adapted)
    # productos = relationship("ProductoModel", secondary="producto_alergeno", back_populates="alergenos")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_alergeno': self.id_alergeno,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'icono': self.icono,
            'nivel_riesgo': self.nivel_riesgo,
            'activo': self.activo,
            'orden': self.orden,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }