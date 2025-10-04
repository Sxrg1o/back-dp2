"""
Product option model for customizable product options.
"""

from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

from app.data.models.base_model import BaseModel


class ProductoOpcionModel(BaseModel):
    """Product option model for customizable options."""

    __tablename__ = "producto_opcion"

    id_producto = Column(
        Integer,
        ForeignKey("producto.id", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key to product table"
    )

    id_tipo_opcion = Column(
        Integer,
        ForeignKey("tipo_opcion.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Foreign key to option type table"
    )

    nombre = Column(
        String(100),
        nullable=False,
        comment="Option name (e.g., 'Sin ají', 'Ají suave')"
    )

    precio_adicional = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Additional price for this option"
    )

    activo = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Option active status"
    )

    orden = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Display order within option type"
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

    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("precio_adicional >= 0", name="ck_producto_opcion_precio_no_negativo"),
        Index("idx_producto_opcion_producto", "id_producto"),
        Index("idx_producto_opcion_tipo", "id_tipo_opcion"),
        Index("idx_producto_opcion_activo", "activo"),
        Index("idx_producto_opcion_orden", "orden"),
    )