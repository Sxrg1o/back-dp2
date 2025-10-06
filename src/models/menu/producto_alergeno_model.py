"""
Product-Allergen association model for many-to-many relationship.
Adapted to match existing MySQL schema restaurant_dp2.producto_alergeno
"""

from sqlalchemy import Column, Integer, ForeignKey, Enum, String, Boolean, Index, PrimaryKeyConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductoAlergenoModel(Base):
    """Product-Allergen association model matching restaurant_dp2.producto_alergeno table."""

    __tablename__ = "producto_alergeno"
    __table_args__ = (
        PrimaryKeyConstraint("id_producto", "id_alergeno"),
        Index("idx_producto", "id_producto"),
        Index("idx_alergeno", "id_alergeno"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Alérgenos presentes en cada producto'
        }
    )

    id_producto = Column(
        Integer,
        ForeignKey("restaurant_dp2.producto.id_producto", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to product table"
    )

    id_alergeno = Column(
        Integer,
        ForeignKey("restaurant_dp2.alergeno.id_alergeno", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to allergen table"
    )

    nivel_presencia = Column(
        Enum('contiene', 'trazas', 'puede_contener', name='nivel_presencia_enum'),
        default='contiene',
        nullable=True,
        comment="Allergen presence level in product"
    )

    notas = Column(
        String(255),
        nullable=True,
        comment="Información adicional sobre el alérgeno en este producto"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Association active status"
    )

    fecha_creacon = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Creation timestamp"
    )

    fecha_modificacion = Column(
        TIMESTAMP,
        nullable=True,
        default=func.current_timestamp(),
        comment="Last modification timestamp"
    )

    # Relationships
    producto = relationship(
        "ProductoModel",
        back_populates="alergenos",
        lazy="select"
    )

    alergeno = relationship(
        "AlergenoModel",
        back_populates="productos_alergenos",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_producto': self.id_producto,
            'id_alergeno': self.id_alergeno,
            'nivel_presencia': self.nivel_presencia,
            'notas': self.notas,
            'activo': self.activo,
            'fecha_creacon': self.fecha_creacon,
            'fecha_modificacion': self.fecha_modificacion
        }