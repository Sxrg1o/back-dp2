"""
Modelo de relación entre pedidos y productos.

Implementa la tabla intermedia que vincula pedidos con productos,
incluyendo información de cantidad, precios y personalización.
"""

from typing import Any, Dict, Optional, Type, TypeVar, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, DECIMAL, ForeignKey, VARCHAR
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

if TYPE_CHECKING:
    from src.models.pedidos.pedido_model import PedidoModel
    from src.models.menu.producto_model import ProductoModel

T = TypeVar("T", bound="PedidoProductoModel")


class PedidoProductoModel(BaseModel, AuditMixin):
    """Modelo para representar items de productos en un pedido.

    Define los productos individuales que forman parte de un pedido,
    incluyendo cantidad, precios y personalizaciones.

    Attributes
    ----------
    id_pedido : str
        Identificador del pedido al que pertenece este item.
    id_producto : str
        Identificador del producto.
    cantidad : int
        Cantidad del producto solicitada.
    precio_unitario : Decimal
        Precio unitario del producto al momento del pedido.
    precio_opciones : Decimal
        Suma de precios adicionales por opciones seleccionadas.
    subtotal : Decimal
        Subtotal del item (cantidad × precio_unitario + precio_opciones).
    notas_personalizacion : str, optional
        Notas o personalizaciones específicas del item.
    """

    __tablename__ = "pedido_producto"

    # Foreign Keys
    id_pedido: Mapped[str] = mapped_column(
        ForeignKey("pedido.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    id_producto: Mapped[str] = mapped_column(
        ForeignKey("producto.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Columnas específicas del modelo
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    precio_unitario: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    precio_opciones: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    subtotal: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    notas_personalizacion: Mapped[Optional[str]] = mapped_column(VARCHAR(200), nullable=True)

    # Relaciones
    pedido: Mapped["PedidoModel"] = relationship(
        "PedidoModel",
        back_populates="pedido_productos",
        lazy="selectin"
    )
    producto: Mapped["ProductoModel"] = relationship(
        "ProductoModel",
        lazy="selectin"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la instancia del modelo a un diccionario."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Crea una instancia del modelo a partir de un diccionario."""
        valid_columns = [c.name for c in cls.__table__.columns]
        filtered_data = {
            k: v for k, v in data.items() 
            if k in valid_columns
        }
        return cls(**filtered_data)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Actualiza la instancia con datos de un diccionario."""
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def __repr__(self) -> str:
        """Representación en string del modelo PedidoProducto."""
        return (
            f"<PedidoProductoModel(id={self.id}, cantidad={self.cantidad}, "
            f"subtotal={self.subtotal})>"
        )

