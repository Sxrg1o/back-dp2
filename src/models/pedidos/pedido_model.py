"""
Modelo de pedidos/órdenes del restaurante.

Implementa la estructura de datos para los pedidos de los clientes,
adaptado para coincidir con el esquema existente de MySQL restaurant_dp2.pedido.
"""

from typing import Any, Dict, Optional, Type, TypeVar, List, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Numeric, TIMESTAMP, Enum as SQLEnum, ForeignKey, CheckConstraint, inspect
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin
from src.core.enums.pedido_enums import EstadoPedido

if TYPE_CHECKING:
    from src.models.pagos.division_cuenta_model import DivisionCuentaModel

# Definimos un TypeVar para el tipado genérico
T = TypeVar("T", bound="PedidoModel")


class PedidoModel(BaseModel, AuditMixin):
    """Modelo para representar pedidos/órdenes en el sistema.

    Define los pedidos que pueden ser realizados por los clientes en las mesas,
    incluyendo seguimiento de estados, totales y notas.

    Attributes
    ----------
    id : str
        Identificador único ULID del pedido (heredado de BaseModel).
    id_mesa : str
        Identificador ULID de la mesa asociada al pedido.
    numero_pedido : str
        Número único del pedido, generado automáticamente con formato YYYYMMDD-M{numero}-{seq}.
    estado : EstadoPedido
        Estado actual del pedido (pendiente, confirmado, en_preparacion, listo, entregado, cancelado).
    subtotal : Decimal
        Subtotal del pedido antes de impuestos y descuentos.
    impuestos : Decimal
        Monto de impuestos aplicados al pedido.
    descuentos : Decimal
        Monto de descuentos aplicados al pedido.
    total : Decimal
        Total final del pedido.
    notas_cliente : str, optional
        Notas o comentarios del cliente sobre el pedido.
    notas_cocina : str, optional
        Notas especiales para la cocina.
    fecha_confirmado : datetime, optional
        Fecha y hora cuando el pedido fue confirmado.
    fecha_en_preparacion : datetime, optional
        Fecha y hora cuando el pedido entró en preparación.
    fecha_listo : datetime, optional
        Fecha y hora cuando el pedido estuvo listo.
    fecha_entregado : datetime, optional
        Fecha y hora cuando el pedido fue entregado.
    fecha_cancelado : datetime, optional
        Fecha y hora cuando el pedido fue cancelado.
    fecha_creacion : datetime
        Fecha y hora de creación del registro (heredado de AuditMixin).
    fecha_modificacion : datetime
        Fecha y hora de última modificación (heredado de AuditMixin).
    creado_por : str, optional
        Usuario que creó el registro (heredado de AuditMixin).
    modificado_por : str, optional
        Usuario que realizó la última modificación (heredado de AuditMixin).
    """

    __tablename__ = "pedido"

    # Foreign Keys
    id_mesa: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("mesas.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Campos específicos del modelo de pedido
    numero_pedido: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True
    )

    estado: Mapped[EstadoPedido] = mapped_column(
        SQLEnum(EstadoPedido),
        nullable=False,
        default=EstadoPedido.PENDIENTE
    )

    # Campos monetarios
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    impuestos: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        default=Decimal("0.00")
    )

    descuentos: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        default=Decimal("0.00")
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    # Notas
    notas_cliente: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notas_cocina: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps de estados
    fecha_confirmado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_en_preparacion: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_listo: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_entregado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)
    fecha_cancelado: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, nullable=True)

    # Relaciones
    divisiones_cuenta: Mapped[List["DivisionCuentaModel"]] = relationship(
        "DivisionCuentaModel",
        back_populates="pedido",
        cascade="all, delete-orphan",
        lazy="select"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="chk_subtotal_positivo"),
        CheckConstraint("total >= 0", name="chk_total_positivo"),
    )

    # Métodos comunes para todos los modelos
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la instancia del modelo a un diccionario.

        Transforma todos los atributos del modelo en un diccionario para
        facilitar su serialización y uso en APIs.

        Returns
        -------
        Dict[str, Any]
            Diccionario con los nombres de columnas como claves y sus valores correspondientes.
        """
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            # Convertir Decimal a float para serialización JSON
            if isinstance(value, Decimal):
                value = float(value)
            # Convertir Enum a string
            elif isinstance(value, EstadoPedido):
                value = value.value
            result[c.name] = value
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Crea una instancia del modelo a partir de un diccionario.

        Parameters
        ----------
        data : Dict[str, Any]
            Diccionario con los datos para crear la instancia.

        Returns
        -------
        T
            Nueva instancia del modelo con los datos proporcionados.
        """
        return cls(
            **{k: v for k, v in data.items() if k in inspect(cls).columns.keys()}
        )

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Actualiza la instancia con datos de un diccionario.

        Parameters
        ----------
        data : Dict[str, Any]
            Diccionario con los datos para actualizar la instancia.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return f"<Pedido(id={self.id}, numero_pedido={self.numero_pedido}, estado={self.estado.value}, total={self.total})>"
