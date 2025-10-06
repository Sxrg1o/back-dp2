"""
Category model for menu organization.
Adapted to match existing MySQL schema restaurant_dp2.categoria
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, func, Index
from sqlalchemy.orm import relationship

from src.core.database import Base


class CategoriaModel(Base):
    """Category model matching restaurant_dp2.categoria table."""

    __tablename__ = "categoria"
    __table_args__ = (
        Index('idx_activo', 'activo'),
        Index('idx_orden', 'orden'),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Categorías principales del menú'
        }
    )

    # Primary key matching your schema
    id_categoria = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    nombre = Column(
        String(100),
        nullable=False,
        comment="Category name"
    )

    descripcion = Column(
        Text,
        nullable=True,
        comment="Category description"
    )

    orden = Column(
        Integer,
        default=0,
        nullable=True,
        comment="Display order"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Category active status"
    )

    imagen_path = Column(
        String(255),
        nullable=True,
        comment="Category image path"
    )

    fecha_creacion = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
    )

    fecha_modificacon = Column(  # Note: typo in original schema
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Last modification timestamp"
    )

    # Relationships (will be added when other models are adapted)
    # productos = relationship("ProductoModel", back_populates="categoria")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_categoria': self.id_categoria,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'orden': self.orden,
            'activo': self.activo,
            'imagen_path': self.imagen_path,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacon': self.fecha_modificacon
        }