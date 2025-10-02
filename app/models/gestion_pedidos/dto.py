from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.gestion_pedidos.enums import EstadoOrden, PrioridadOrden, TipoPago, EstadoCuenta

# =========================
# DTOs para Requests
# =========================

class CrearOrdenRequest(BaseModel):
    """DTO para crear una nueva orden"""
    # mesa_id: Optional[int] = None  # Estará en módulo estancia_cliente
    # cliente_ids: List[int] = []  # Estará en módulo estancia_cliente
    comentarios: str = ""
    mesero_ids: List[int] = []

class AgregarItemOrdenRequest(BaseModel):
    """DTO para agregar un item a una orden"""
    item_id: int
    cantidad: int = Field(gt=0, description="Cantidad debe ser mayor a 0")
    comentarios: str = ""

class ItemOrdenCompletaRequest(BaseModel):
    """DTO para un item en una orden completa"""
    item_id: int
    cantidad: int = Field(gt=0, description="Cantidad debe ser mayor a 0")
    comentarios: str = ""
    acompanamientos_seleccionados: List[int] = []  # IDs de opciones de acompañamientos
    opciones_adicionales_seleccionadas: List[int] = []  # IDs de opciones adicionales

class CrearOrdenCompletaRequest(BaseModel):
    """DTO para crear una orden completa con todos los items"""
    # mesa_id: Optional[int] = None  # Estará en módulo estancia_cliente
    comentarios_generales: str = ""
    mesero_ids: List[int] = []
    items: List[ItemOrdenCompletaRequest] = Field(..., min_items=1, description="Debe tener al menos un item")

class ModificarItemOrdenRequest(BaseModel):
    """DTO para modificar un item en una orden"""
    item_orden_id: int
    cantidad: Optional[int] = Field(None, gt=0)
    comentarios: Optional[str] = None

class CambiarEstadoOrdenRequest(BaseModel):
    """DTO para cambiar el estado de una orden"""
    orden_id: int
    nuevo_estado: EstadoOrden
    comentarios: Optional[str] = None

# class CrearCuentaSeparadaRequest(BaseModel):
#     """DTO para crear una cuenta separada - estará en módulo division_de_cuenta"""
#     orden_id: int
#     nombre: str
#     items_ids: List[int]

class AsignarMeseroRequest(BaseModel):
    """DTO para asignar mesero a una orden"""
    orden_id: int
    mesero_id: int

class CrearMeseroRequest(BaseModel):
    """DTO para crear un mesero"""
    nombre: str
    activo: bool = True

# class CrearGrupoMesaRequest(BaseModel):
#     """DTO para crear un grupo de mesa - Estará en módulo estancia_cliente"""
#     nombre: str
#     capacidad: int = Field(gt=0)
#     tipo: TipoMesa
#     ubicacion: Optional[str] = None

# class CrearClienteRequest(BaseModel):
#     """DTO para crear un cliente - estará en módulo estancia_cliente"""
#     nombre: str
#     telefono: Optional[str] = None
#     email: Optional[str] = None

class FiltrarOrdenesRequest(BaseModel):
    """DTO para filtrar órdenes"""
    estado: Optional[EstadoOrden] = None
    # mesa_id: Optional[int] = None  # Estará en módulo estancia_cliente
    mesero_id: Optional[int] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    monto_minimo: Optional[float] = None
    monto_maximo: Optional[float] = None

# =========================
# DTOs para Responses
# =========================

class ItemOrdenResponse(BaseModel):
    """DTO de respuesta para ItemOrden"""
    id: int
    item_id: int
    item_nombre: str
    item_precio: float
    cant_pedida: int
    subtotal: float
    comentarios: str

class OrdenResponse(BaseModel):
    """DTO de respuesta para Orden"""
    id: int
    numero_orden: int
    # mesa: Optional[Dict] = None  # Estará en módulo estancia_cliente
    # clientes: List[Dict] = []  # Estará en módulo estancia_cliente
    linea_pedidos: List[ItemOrdenResponse] = []
    num_items: int
    monto_total: float
    estado: str
    comentarios: str
    activo: bool
    hora_registro: datetime
    # cuentas: List[Dict] = []  # Estará en módulo division_de_cuenta
    # num_cuentas: int
    meseros: List[Dict] = []

class ResumenOrdenResponse(BaseModel):
    """DTO de respuesta para ResumenOrden"""
    id: int
    numero_orden: int
    # mesa_nombre: Optional[str] = None  # Estará en módulo estancia_cliente
    estado: str
    num_items: int
    monto_total: float
    hora_registro: datetime
    meseros_nombres: List[str] = []

class MeseroResponse(BaseModel):
    """DTO de respuesta para Mesero"""
    id: int
    nombre: str
    activo: bool
    ordenes_count: int = 0

# class GrupoMesaResponse(BaseModel):
#     """DTO de respuesta para GrupoMesa - Estará en módulo estancia_cliente"""
#     id: int
#     nombre: str
#     capacidad: int
#     tipo: str
#     activa: bool
#     ubicacion: Optional[str] = None

# class ClienteResponse(BaseModel):
#     """DTO de respuesta para Cliente - estará en módulo estancia_cliente"""
#     id: int
#     nombre: str
#     telefono: Optional[str] = None
#     email: Optional[str] = None
#     activo: bool

# class CuentaResponse(BaseModel):
#     """DTO de respuesta para Cuenta - estará en módulo division_de_cuenta"""
#     id: int
#     orden_id: int
#     nombre: str
#     items: List[int] = []
#     monto: float
#     pagada: bool
#     activa: bool

class EstadisticasPedidosResponse(BaseModel):
    """DTO de respuesta para estadísticas"""
    total_ordenes: int
    ordenes_en_cola: int
    ordenes_en_preparacion: int
    ordenes_listas: int
    ordenes_despachadas: int
    ordenes_canceladas: int
    monto_total_dia: float
    promedio_tiempo_preparacion: float
    items_mas_pedidos: List[Dict[str, int]] = []

class ValidacionDisponibilidadResponse(BaseModel):
    """DTO de respuesta para validación de disponibilidad"""
    orden_id: int
    todos_disponibles: bool
    items_no_disponibles: List[Dict] = []
    mensaje: str

class OrdenCompletaResponse(BaseModel):
    """DTO de respuesta para orden completa con todos los detalles"""
    orden: OrdenResponse
    validacion_disponibilidad: ValidacionDisponibilidadResponse
    puede_cambiar_estado: bool
    estados_disponibles: List[str] = []

# =========================
# DTOs para Listados y Filtros
# =========================

class ListaOrdenesResponse(BaseModel):
    """DTO de respuesta para lista de órdenes"""
    ordenes: List[ResumenOrdenResponse]
    total: int
    pagina: int = 1
    por_pagina: int = 10
    total_paginas: int = 1

class ListaMeserosResponse(BaseModel):
    """DTO de respuesta para lista de meseros"""
    meseros: List[MeseroResponse]
    total: int

# class ListaMesasResponse(BaseModel):
#     """DTO de respuesta para lista de mesas - Estará en módulo estancia_cliente"""
#     mesas: List[GrupoMesaResponse]
#     total: int

# class ListaClientesResponse(BaseModel):
#     """DTO de respuesta para lista de clientes - estará en módulo estancia_cliente"""
#     clientes: List[ClienteResponse]
#     total: int

# =========================
# DTOs para Reportes
# =========================

class ReporteVentasResponse(BaseModel):
    """DTO de respuesta para reporte de ventas"""
    fecha: str
    total_ventas: float
    num_ordenes: int
    promedio_por_orden: float
    ventas_por_estado: Dict[str, float] = {}
    ventas_por_mesa: Dict[str, float] = {}
    ventas_por_mesero: Dict[str, float] = {}

class ReporteItemsResponse(BaseModel):
    """DTO de respuesta para reporte de items más pedidos"""
    periodo: str
    items_mas_pedidos: List[Dict[str, int]] = []
    items_menos_pedidos: List[Dict[str, int]] = []
    total_items_vendidos: int
    ingresos_por_item: Dict[str, float] = {}
