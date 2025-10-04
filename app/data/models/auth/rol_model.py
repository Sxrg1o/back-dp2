"""
Role model for user authentication and authorization.
Adapted to match existing MySQL schema restaurant_dp2.rol
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.config.database import Base


class RolModel(Base):
    """Role model matching restaurant_dp2.rol table."""

    __tablename__ = "rol"
    __table_args__ = {
        'schema': 'restaurant_dp2',
        'comment': 'Roles del sistema (cliente, mesero, cocina, admin)'
    }

    # Primary key matching your schema
    id_rol = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    nombre = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Role name"
    )

    descripcion = Column(
        String(255),
        nullable=True,
        comment="Role description"
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
    # usuarios = relationship("UsuarioModel", back_populates="rol")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_rol': self.id_rol,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }