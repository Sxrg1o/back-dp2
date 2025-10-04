"""
Product model for menu items.
"""

from sqlalchemy import Column, String, Text, Integer, Numeric, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class ProductoModel(BaseModel):
    """Product model for menu items."""

    __tablename__ = "producto"

    id_categoria = Column(
        Integer,
        ForeignKey("categoria.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to category table"
    )

    nombre = Column(
        String(200),
        nullable=False,
        comment="Product name"
    )

    descripcion = Column(
        Text,
        nullable=True,
        comment="Product description"
    )

    precio_base = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Base price of the product"
    )

    imagen_path = Column(
        String(255),
        nullable=True,
        comment="Product image path"
    )

    imagen_alt_text = Column(
        String(255),
        nullable=True,
        comment="Image alt text for accessibility"
    )

    disponible = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Product availability status"
    )

    destacado = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Featured product flag"
    )

    # Relationships
    categoria = relationship(
        "CategoriaModel",
        back_populates="productos",
        lazy="select"
    )

    alergenos = relationship(
        "ProductoAlergenoModel",
        back_populates="producto",
        lazy="select",
        cascade="all, delete-orphan"
    )

    opciones = relationship(
        "ProductoOpcionModel",
        back_populates="producto",
        lazy="select",
        cascade="all, delete-orphan"
    )

    pedido_productos = relationship(
        "PedidoProductoModel",
        back_populates="producto",
        lazy="select"
    )

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("precio_base > 0", name="ck_producto_precio_positivo"),
        Index("idx_producto_categoria", "id_categoria"),
        Index("idx_producto_destacado", "destacado"),
        Index("idx_producto_disponible", "disponible"),
        Index("idx_producto_precio", "precio_base"),
        Index("idx_producto_fulltext", "nombre", "descripcion", mysql_prefix="FULLTEXT"),
    )