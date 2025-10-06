"""
Models module - imports all SQLAlchemy models.
"""

# Base model
from .base_model import BaseModel

# Mixins
from .mixins.timestamp_mixin import TimestampMixin
from .mixins.soft_delete_mixin import SoftDeleteMixin

# Auth models
from .auth.rol_model import RolModel
from .auth.usuario_model import UsuarioModel

# Menu models
from .menu.alergeno_model import AlergenoModel
from .menu.categoria_model import CategoriaModel
from .menu.producto_model import ProductoModel
from .menu.producto_alergeno_model import ProductoAlergenoModel
from .menu.tipo_opcion_model import TipoOpcionModel
from .menu.producto_opcion_model import ProductoOpcionModel

# Table models
from .mesas.mesa_model import MesaModel
from .mesas.sesion_mesa_model import SesionMesaModel

# Order models
from .pedidos.pedido_model import PedidoModel
from .pedidos.pedido_producto_model import PedidoProductoModel
from .pedidos.pedido_opcion_model import PedidoOpcionModel

# Payment models
from .pagos.division_cuenta_model import DivisionCuentaModel
from .pagos.division_cuenta_detalle_model import DivisionCuentaDetalleModel
from .pagos.pago_model import PagoModel

__all__ = [
    # Base
    "BaseModel",
    # Mixins
    "TimestampMixin",
    "SoftDeleteMixin",
    # Auth
    "RolModel",
    "UsuarioModel",
    # Menu
    "AlergenoModel",
    "CategoriaModel",
    "ProductoModel",
    "ProductoAlergenoModel",
    "TipoOpcionModel",
    "ProductoOpcionModel",
    # Tables
    "MesaModel",
    "SesionMesaModel",
    # Orders
    "PedidoModel",
    "PedidoProductoModel",
    "PedidoOpcionModel",
    # Payments
    "DivisionCuentaModel",
    "DivisionCuentaDetalleModel",
    "PagoModel",
]