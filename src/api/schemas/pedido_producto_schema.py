"""
Pydantic schemas for PedidoProducto (Order Item) entities.
"""

from typing import Optional, ClassVar
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class PedidoProductoBase(BaseModel):
    """Base schema for PedidoProducto."""

    id_pedido: str = Field(description="Order ID")
    id_producto: str = Field(description="Product ID")
    cantidad: int = Field(description="Quantity", ge=1)
    precio_unitario: Decimal = Field(description="Unit price", ge=0)
    precio_opciones: Optional[Decimal] = Field(default=Decimal("0.00"), description="Options price", ge=0)
    subtotal: Optional[Decimal] = Field(default=Decimal("0.00"), description="Subtotal", ge=0)
    notas_personalizacion: Optional[str] = Field(default=None, description="Customization notes", max_length=200)


class PedidoProductoCreate(PedidoProductoBase):
    """Schema for creating a new pedido_producto."""

    pass


class PedidoProductoUpdate(BaseModel):
    """Schema for updating pedido_producto."""

    id_pedido: Optional[str] = Field(default=None, description="Order ID")
    id_producto: Optional[str] = Field(default=None, description="Product ID")
    cantidad: Optional[int] = Field(default=None, description="Quantity", ge=1)
    precio_unitario: Optional[Decimal] = Field(default=None, description="Unit price", ge=0)
    precio_opciones: Optional[Decimal] = Field(default=None, description="Options price", ge=0)
    subtotal: Optional[Decimal] = Field(default=None, description="Subtotal", ge=0)
    notas_personalizacion: Optional[str] = Field(default=None, description="Customization notes", max_length=200)


class PedidoProductoResponse(PedidoProductoBase):
    """Schema for pedido_producto responses."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: str = Field(description="Order item ID")
    fecha_creacion: Optional[datetime] = Field(default=None, description="Creation timestamp")
    fecha_modificacion: Optional[datetime] = Field(default=None, description="Last modification timestamp")


class PedidoProductoSummary(BaseModel):
    """Schema for summarized pedido_producto information in lists."""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    id: str = Field(description="Order item ID")
    id_producto: str = Field(description="Product ID")
    cantidad: int = Field(description="Quantity")
    subtotal: Decimal = Field(description="Subtotal")

