"""
Modelo de pedidos.

Implementa la estructura de datos para los pedidos realizados por los clientes
en las mesas del restaurante.
"""

from typing import Any, Dict, Optional, Type, TypeVar, TYPE_CHECKING, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, DECIMAL, ForeignKey, Enum as SQLEnum, VARCHAR, TIMESTAMP
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin
from src.core.enums.pedido_enums import EstadoPedido

if TYPE_CHECKING:
    from src.models.mesas.mesa_model import MesaModel
    from src.models.pedidos.pedido_producto_model import PedidoProductoModel

T = TypeVar("T", bound="PedidoModel")


class PedidoModel(BaseModel, AuditMixin):
    """Modelo para representar pedidos en el sistema.

    Define los pedidos realizados por clientes en las mesas del restaurante,
    incluyendo información de estado, precios, notas y timestamps de seguimiento.

    Attributes
    ----------
    id_mesa : str
        Identificador de la mesa asociada al pedido.
    numero_pedido : str, optional
        Número de pedido único para identificación.
    estado : EstadoPedido
        Estado actual del pedido (pendiente, confirmado, etc.).
    subtotal : Decimal
        Subtotal del pedido antes de impuestos y descuentos.
    impuestos : Decimal
        Monto de impuestos aplicados.
    descuentos : Decimal
        Monto de descuentos aplicados.
    total : Decimal
        Total final del pedido.
    notas_cliente : str, optional
        Notas o instrucciones del cliente para el pedido.
    notas_cocina : str, optional
        Notas internas para la cocina.
    fecha_confirmado : datetime, optional
        Fecha y hora de confirmación del pedido.
    fecha_en_preparacion : datetime, optional
        Fecha y hora cuando comenzó la preparación.
    fecha_listo : datetime, optional
        Fecha y hora cuando el pedido estuvo listo.
    fecha_entregado : datetime, optional
        Fecha y hora de entrega del pedido.
    fecha_cancelado : datetime, optional
        Fecha y hora de cancelación del pedido.
    """

    __tablename__ = "pedido"

    # Foreign Key - Relación con mesa
    id_mesa: Mapped[str] = mapped_column(
        ForeignKey("mesas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Columnas específicas del modelo
    numero_pedido: Mapped[Optional[str]] = mapped_column(
        VARCHAR(50), nullable=True, unique=True, index=True
    )
    estado: Mapped[EstadoPedido] = mapped_column(
        SQLEnum(EstadoPedido), nullable=False, default=EstadoPedido.PENDIENTE, index=True
    )

    # Campos financieros
    subtotal: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    impuestos: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    descuentos: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00")
    )
    total: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2), nullable=False, default=Decimal("0.00"), index=True
    )

    # Notas
    notas_cliente: Mapped[Optional[str]] = mapped_column(VARCHAR(200), nullable=True)
    notas_cocina: Mapped[Optional[str]] = mapped_column(VARCHAR(200), nullable=True)

    # Timestamps de seguimiento
    fecha_confirmado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_en_preparacion: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_listo: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_entregado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_cancelado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)

    # Relaciones
    mesa: Mapped["MesaModel"] = relationship(
        "MesaModel", lazy="selectin"
    )
    pedido_productos: Mapped[List["PedidoProductoModel"]] = relationship(
        "PedidoProductoModel",
        back_populates="pedido",
        lazy="selectin",
        cascade="all, delete-orphan"
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
        """Representación en string del modelo Pedido."""
        return (
            f"<PedidoModel(id={self.id}, numero_pedido='{self.numero_pedido}', "
            f"estado='{self.estado}', total={self.total})>"
        )

