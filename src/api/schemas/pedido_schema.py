"""
Pydantic schemas for Pedido (Order) entities.
"""

from typing import Optional, ClassVar, List, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from src.core.enums.pedido_enums import EstadoPedido


class PedidoBase(BaseModel):
    """Base schema for Pedido."""

    id_mesa: str = Field(description="Table ID")
    numero_pedido: Optional[str] = Field(default=None, description="Order number", max_length=50)
    estado: Optional[EstadoPedido] = Field(default=EstadoPedido.PENDIENTE, description="Order status")
    subtotal: Optional[Decimal] = Field(default=Decimal("0.00"), description="Subtotal")
    impuestos: Optional[Decimal] = Field(default=Decimal("0.00"), description="Taxes")
    descuentos: Optional[Decimal] = Field(default=Decimal("0.00"), description="Discounts")
    total: Optional[Decimal] = Field(default=Decimal("0.00"), description="Total")
    notas_cliente: Optional[str] = Field(default=None, description="Customer notes", max_length=200)
    notas_cocina: Optional[str] = Field(default=None, description="Kitchen notes", max_length=200)


class PedidoCreate(PedidoBase):
    """Schema for creating a new pedido."""

    pass


class PedidoUpdate(BaseModel):
    """Schema for updating pedido."""

    id_mesa: Optional[str] = Field(default=None, description="Table ID")
    numero_pedido: Optional[str] = Field(default=None, description="Order number", max_length=50)
    estado: Optional[EstadoPedido] = Field(default=None, description="Order status")
    subtotal: Optional[Decimal] = Field(default=None, description="Subtotal")
    impuestos: Optional[Decimal] = Field(default=None, description="Taxes")
    descuentos: Optional[Decimal] = Field(default=None, description="Discounts")
    total: Optional[Decimal] = Field(default=None, description="Total")
    notas_cliente: Optional[str] = Field(default=None, description="Customer notes", max_length=200)
    notas_cocina: Optional[str] = Field(default=None, description="Kitchen notes", max_length=200)
    fecha_confirmado: Optional[datetime] = Field(default=None, description="Confirmed at")
    fecha_en_preparacion: Optional[datetime] = Field(default=None, description="Preparation started at")
    fecha_listo: Optional[datetime] = Field(default=None, description="Ready at")
    fecha_entregado: Optional[datetime] = Field(default=None, description="Delivered at")
    fecha_cancelado: Optional[datetime] = Field(default=None, description="Cancelled at")


class PedidoResponse(PedidoBase):
    """Schema for pedido responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: str = Field(description="Order ID")
    fecha_confirmado: Optional[datetime] = Field(default=None, description="Confirmed at")
    fecha_en_preparacion: Optional[datetime] = Field(default=None, description="Preparation started at")
    fecha_listo: Optional[datetime] = Field(default=None, description="Ready at")
    fecha_entregado: Optional[datetime] = Field(default=None, description="Delivered at")
    fecha_cancelado: Optional[datetime] = Field(default=None, description="Cancelled at")
    fecha_creacion: Optional[datetime] = Field(default=None, description="Creation timestamp")
    fecha_modificacion: Optional[datetime] = Field(default=None, description="Last modification timestamp")


class PedidoSummary(BaseModel):
    """Schema for summarized pedido information in lists."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: str = Field(description="Order ID")
    id_mesa: str = Field(description="Table ID")
    numero_pedido: Optional[str] = Field(default=None, description="Order number")
    estado: EstadoPedido = Field(description="Order status")
    total: Decimal = Field(description="Total amount")
    fecha_creacion: Optional[datetime] = Field(default=None, description="Creation timestamp")


class PedidoList(BaseModel):
    """Schema for paginated list of pedidos."""

    items: List[PedidoSummary]
    total: int = Field(description="Total number of orders")


class PedidoConProductosResponse(PedidoResponse):
    """Schema for pedido with its products."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    pedido_productos: List[Any] = Field(  # type: ignore
        default_factory=list,
        description="List of order items"
    )

# Import and update after definition
from src.api.schemas.pedido_producto_schema import PedidoProductoResponse  # noqa: E402
PedidoConProductosResponse.model_rebuild()

