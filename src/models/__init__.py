"""
Modelos de datos del sistema de restaurante.

Este módulo contiene todos los modelos de SQLAlchemy utilizados en el sistema.
Las importaciones están ordenadas para evitar dependencias circulares.
"""

# Importaciones base
from src.models.base_model import BaseModel

# Modelos principales (sin dependencias externas)
from src.models.local_model import LocalModel
from src.models.zona_model import ZonaModel

# Modelos de mesas
from src.models.mesas.mesa_model import MesaModel

# Modelos de menú
from src.models.menu.categoria_model import CategoriaModel
from src.models.menu.alergeno_model import AlergenoModel
from src.models.menu.producto_model import ProductoModel
from src.models.menu.producto_alergeno_model import ProductoAlergenoModel

# Modelos de pedidos (orden importante)
from src.models.pedidos.tipo_opciones_model import TipoOpcionModel
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel
from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.pedidos.pedido_opcion_model import PedidoOpcionModel

# Modelos de pagos (después de pedidos)
from src.models.pagos.division_cuenta_model import DivisionCuentaModel
from src.models.pagos.division_cuenta_detalle_model import DivisionCuentaDetalleModel

# Modelos de autenticación (solo los que existen)
from src.models.auth.rol_model import RolModel

# Modelo de sesión
from src.models.sesion_model import SesionModel

__all__ = [
    "BaseModel",
    "LocalModel",
    "ZonaModel",
    "MesaModel",
    "CategoriaModel", 
    "AlergenoModel",
    "ProductoModel",
    "ProductoAlergenoModel",
    "TipoOpcionModel",
    "ProductoOpcionModel",
    "PedidoModel",
    "PedidoProductoModel",
    "PedidoOpcionModel",
    "DivisionCuentaModel",
    "DivisionCuentaDetalleModel",
    "RolModel",
    "SesionModel",
]