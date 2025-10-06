"""
Product model for menu items.
Adapted to match existing MySQL schema restaurant_dp2.producto
"""

from sqlalchemy import Column, String, Text, Integer, Numeric, Boolean, ForeignKey, Index, CheckConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductoModel(Base):
    """Product model matching restaurant_dp2.producto table."""

    __tablename__ = "producto"
    __table_args__ = (
        CheckConstraint("precio_base > 0", name="chk_precio_positivo"),
        Index("idx_categoria", "id_categoria"),
        Index("idx_destacado", "destacado"),
        Index("idx_disponible", "disponible"),
        Index("idx_precio", "precio_base"),
        Index("idx_busqueda", "nombre", "descripcion", mysql_prefix="FULLTEXT"),
        {
            'schema': 'restaurant_dp2',
            'comment': 'Platos disponibles en el menú'
        }
    )

    # Primary key matching your schema
    id_producto = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_categoria = Column(
        Integer,
        ForeignKey("restaurant_dp2.categoria.id_categoria", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to category table"
    )

    nombre = Column(
        String(255),
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
        nullable=True,
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
        nullable=True,
        comment="Product availability status"
    )

    destacado = Column(
        Boolean,
        default=False,
        nullable=True,
        comment="Featured product flag"
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

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_producto': self.id_producto,
            'id_categoria': self.id_categoria,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_base': self.precio_base,
            'imagen_path': self.imagen_path,
            'imagen_alt_text': self.imagen_alt_text,
            'disponible': self.disponible,
            'destacado': self.destacado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }