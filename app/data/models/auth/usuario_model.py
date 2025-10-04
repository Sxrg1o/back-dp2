"""
User model for authentication and user management.
Adapted to match existing MySQL schema restaurant_dp2.usuario
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Index, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.config.database import Base


class UsuarioModel(Base):
    """User model matching restaurant_dp2.usuario table."""

    __tablename__ = "usuario"
    __table_args__ = {
        'schema': 'restaurant_dp2',
        'comment': 'Usuarios del sistema (staff y clientes registrados)'
    }

    # Primary key matching your schema
    id_usuario = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_rol = Column(
        Integer,
        ForeignKey("restaurant_dp2.rol.id_rol", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to role table"
    )

    email = Column(
        String(255),
        nullable=True,  # Changed to nullable=True as per your schema
        unique=True,
        comment="User email address"
    )

    password_hash = Column(
        String(255),
        nullable=True,  # Changed to nullable=True as per your schema
        comment="Hashed password"
    )

    nombre = Column(
        String(255),
        nullable=True,  # Changed to nullable=True as per your schema
        comment="User full name"
    )

    telefono = Column(
        String(20),
        nullable=True,
        comment="User phone number"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,  # Changed to nullable=True as per your schema
        comment="User active status"
    )

    ultimo_acceso = Column(
        TIMESTAMP,
        nullable=True,
        comment="Last access timestamp"
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
    # rol = relationship("RolModel", back_populates="usuarios")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_usuario': self.id_usuario,
            'id_rol': self.id_rol,
            'email': self.email,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'activo': self.activo,
            'ultimo_acceso': self.ultimo_acceso,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }