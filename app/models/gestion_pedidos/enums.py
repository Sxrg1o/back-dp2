from enum import Enum

class EstadoOrden(str, Enum):
    """Estados posibles de una orden"""
    EN_COLA = "EN_COLA"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO_PARA_SALIR = "LISTO_PARA_SALIR"
    DESPACHADO = "DESPACHADO"
    CANCELADO = "CANCELADO"

class TipoMesa(str, Enum):
    """Tipos de mesas disponibles"""
    INDIVIDUAL = "INDIVIDUAL"
    PAREJA = "PAREJA"
    FAMILIAR = "FAMILIAR"
    GRUPO = "GRUPO"
    VIP = "VIP"
    TERRAZA = "TERRAZA"

class PrioridadOrden(str, Enum):
    """Prioridades de órdenes"""
    BAJA = "BAJA"
    NORMAL = "NORMAL"
    ALTA = "ALTA"
    URGENTE = "URGENTE"

class TipoPago(str, Enum):
    """Tipos de pago"""
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    QR = "QR"
    DIVIDIDO = "DIVIDIDO"

class EstadoCuenta(str, Enum):
    """Estados de cuentas separadas"""
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    CANCELADA = "CANCELADA"

class TipoNotificacion(str, Enum):
    """Tipos de notificaciones"""
    ORDEN_NUEVA = "ORDEN_NUEVA"
    ORDEN_LISTA = "ORDEN_LISTA"
    ORDEN_CANCELADA = "ORDEN_CANCELADA"
    STOCK_BAJO = "STOCK_BAJO"
    MESA_LIBRE = "MESA_LIBRE"
