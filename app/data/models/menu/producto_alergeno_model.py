"""
Product-Allergen association model for many-to-many relationship.
"""

from sqlalchemy import Column, Integer, ForeignKey, Enum, String, Boolean, Index, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel
from app.shared.enums.alergeno_enums import NivelPresencia


class ProductoAlergenoModel(BaseModel):
    """Product-Allergen association model."""

    __tablename__ = "producto_alergeno"

    id_producto = Column(
        Integer,
        ForeignKey("producto.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to product table"
    )

    id_alergeno = Column(
        Integer,
        ForeignKey("alergeno.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to allergen table"
    )

    nivel_presencia = Column(
        Enum(NivelPresencia),
        nullable=False,
        default=NivelPresencia.CONTIENE,
        comment="Allergen presence level in product"
    )

    notas = Column(
        String(500),
        nullable=True,
        comment="Additional notes about allergen presence"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Association active status"
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

    # Constraints and indexes
    __table_args__ = (
        PrimaryKeyConstraint("id_producto", "id_alergeno", name="pk_producto_alergeno"),
        Index("idx_producto_alergeno_producto", "id_producto"),
        Index("idx_producto_alergeno_alergeno", "id_alergeno"),
    )