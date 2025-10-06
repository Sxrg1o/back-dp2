"""
Product option model for customizable product options.
Adapted to match existing MySQL schema restaurant_dp2.producto_opcion
"""

from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, Index, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductoOpcionModel(Base):
    """Product option model matching restaurant_dp2.producto_opcion table."""

    __tablename__ = "producto_opcion"
    __table_args__ = (
        Index("id_tipo_opcion", "id_tipo_opcion"),
        Index("idx_producto_tipo", "id_producto", "id_tipo_opcion"),
        {
            'schema': 'restaurant_dp2'
        }
    )

    # Primary key matching your schema
    id_producto_opcion = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Primary key"
    )

    id_producto = Column(
        Integer,
        ForeignKey("restaurant_dp2.producto.id_producto", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to product table"
    )

    id_tipo_opcion = Column(
        Integer,
        ForeignKey("restaurant_dp2.tipo_opcion.id_tipo_opcion"),
        nullable=False,
        comment="Foreign key to option type table"
    )

    nombre = Column(
        String(100),
        nullable=False,
        comment="Sin ají, en salsa, etc."
    )

    precio_adicional = Column(
        Numeric(10, 2),
        nullable=True,
        default=0.00,
        comment="Additional price for this option"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=True,
        comment="Option active status"
    )

    orden = Column(
        Integer,
        default=0,
        nullable=True,
        comment="Display order within option type"
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
    producto = relationship(
        "ProductoModel",
        back_populates="opciones",
        lazy="select"
    )

    tipo_opcion = relationship(
        "TipoOpcionModel",
        back_populates="producto_opciones",
        lazy="select"
    )

    pedido_opciones = relationship(
        "PedidoOpcionModel",
        back_populates="producto_opcion",
        lazy="select"
    )

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id_producto_opcion': self.id_producto_opcion,
            'id_producto': self.id_producto,
            'id_tipo_opcion': self.id_tipo_opcion,
            'nombre': self.nombre,
            'precio_adicional': self.precio_adicional,
            'activo': self.activo,
            'orden': self.orden,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }