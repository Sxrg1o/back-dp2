from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.menu_y_carta.domain import Item, GrupoPersonalizacion, Opcion
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa

class Mesero(BaseModel):
    """Modelo para meseros"""
    id: int
    nombre: str
    activo: bool = True
    ordenes: List[int] = []  # IDs de órdenes asignadas

class GrupoMesa(BaseModel):
    """Modelo para grupos de mesas"""
    id: int
    nombre: str
    capacidad: int
    tipo: TipoMesa
    activa: bool = True
    ubicacion: Optional[str] = None

# Cliente y Cuenta estarán en otros módulos:
# - Cliente: módulo estancia_cliente
# - Cuenta: módulo division_de_cuenta

class ItemOrden(BaseModel):
    """Modelo para líneas de pedido (composición de Orden)"""
    id: int
    item: Item
    orden_id: int
    cant_pedida: int
    subtotal: float = 0.0
    comentarios: str = ""
    acompanamientos: List[Opcion] = []
    opciones_adicionales: List[Opcion] = []
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal incluyendo opciones adicionales"""
        subtotal_base = self.item.precio * self.cant_pedida
        
        # Sumar precios de acompañamientos
        precio_acompanamientos = sum(
            opcion.precio_adicional for opcion in self.acompanamientos
        )
        
        # Sumar precios de opciones adicionales
        precio_opciones = sum(
            opcion.precio_adicional for opcion in self.opciones_adicionales
        )
        
        self.subtotal = subtotal_base + precio_acompanamientos + precio_opciones
        return self.subtotal

class Orden(BaseModel):
    """Modelo principal para órdenes de pedidos"""
    id: int
    numero_orden: int
    mesa: Optional[GrupoMesa] = None
    # clientes: List[Cliente] = []  # Estará en módulo estancia_cliente
    linea_pedidos: List[ItemOrden] = []
    num_items: int = 0
    monto_total: float = 0.0
    estado: EstadoOrden = EstadoOrden.EN_COLA
    comentarios: str = ""
    activo: bool = True
    hora_registro: datetime = Field(default_factory=datetime.now)
    # cuentas: List[Cuenta] = []  # Estará en módulo division_de_cuenta
    # num_cuentas: int = 0
    meseros: List[Mesero] = []
    
    def calcular_monto_total(self) -> float:
        """Calcula el monto total de la orden"""
        self.monto_total = sum(item.calcular_subtotal() for item in self.linea_pedidos)
        return self.monto_total
    
    def calcular_num_items(self) -> int:
        """Calcula el número total de items"""
        self.num_items = sum(item.cant_pedida for item in self.linea_pedidos)
        return self.num_items
    
    # def calcular_num_cuentas(self) -> int:
    #     """Calcula el número de cuentas - estará en módulo division_de_cuenta"""
    #     self.num_cuentas = len(self.cuentas)
    #     return self.num_cuentas
    
    def agregar_item(self, item: Item, cantidad: int, comentarios: str = "", 
                    acompanamientos: List[Opcion] = None, 
                    opciones_adicionales: List[Opcion] = None) -> bool:
        """Agrega un item a la orden"""
        # Validar disponibilidad
        if not item.verificar_stock() or item.stock < cantidad:
            return False
        
        # Crear ItemOrden
        item_orden = ItemOrden(
            id=len(self.linea_pedidos) + 1,
            item=item,
            orden_id=self.id,
            cant_pedida=cantidad,
            comentarios=comentarios,
            acompanamientos=acompanamientos or [],
            opciones_adicionales=opciones_adicionales or []
        )
        
        # Calcular subtotal
        item_orden.calcular_subtotal()
        
        # Agregar a la orden
        self.linea_pedidos.append(item_orden)
        
        # Recalcular totales
        self.calcular_monto_total()
        self.calcular_num_items()
        
        return True
    
    def remover_item(self, item_orden_id: int) -> bool:
        """Remueve un item de la orden"""
        for i, item in enumerate(self.linea_pedidos):
            if item.id == item_orden_id:
                del self.linea_pedidos[i]
                self.calcular_monto_total()
                self.calcular_num_items()
                return True
        return False
    
    def cambiar_estado(self, nuevo_estado: EstadoOrden) -> bool:
        """Cambia el estado de la orden con validaciones"""
        transiciones_validas = {
            EstadoOrden.EN_COLA: [EstadoOrden.EN_PREPARACION, EstadoOrden.CANCELADO],
            EstadoOrden.EN_PREPARACION: [EstadoOrden.LISTO_PARA_SALIR, EstadoOrden.CANCELADO],
            EstadoOrden.LISTO_PARA_SALIR: [EstadoOrden.DESPACHADO],
            EstadoOrden.DESPACHADO: [],  # Estado final
            EstadoOrden.CANCELADO: []    # Estado final
        }
        
        if nuevo_estado in transiciones_validas.get(self.estado, []):
            self.estado = nuevo_estado
            return True
        return False
    
    # def crear_cuenta_separada(self, nombre: str, items_ids: List[int]) -> bool:
    #     """Crea una cuenta separada - estará en módulo division_de_cuenta"""
    #     # Validar que los items existen en la orden
    #     items_validos = [item for item in self.linea_pedidos if item.id in items_ids]
    #     if not items_validos:
    #         return False
    #     
    #     # Calcular monto de la cuenta
    #     monto_cuenta = sum(item.subtotal for item in items_validos)
    #     
    #     # Crear cuenta
    #     cuenta = Cuenta(
    #         id=len(self.cuentas) + 1,
    #         orden_id=self.id,
    #         nombre=nombre,
    #         items=items_ids,
    #         monto=monto_cuenta
    #     )
    #     
    #     self.cuentas.append(cuenta)
    #     self.calcular_num_cuentas()
    #     return True
    
    def asignar_mesero(self, mesero: Mesero) -> bool:
        """Asigna un mesero a la orden"""
        if mesero not in self.meseros:
            self.meseros.append(mesero)
            mesero.ordenes.append(self.id)
            return True
        return False
    
    def desasignar_mesero(self, mesero_id: int) -> bool:
        """Desasigna un mesero de la orden"""
        for i, mesero in enumerate(self.meseros):
            if mesero.id == mesero_id:
                del self.meseros[i]
                if self.id in mesero.ordenes:
                    mesero.ordenes.remove(self.id)
                return True
        return False
    
    def obtener_tiempo_estimado(self) -> float:
        """Calcula el tiempo estimado de preparación"""
        if not self.linea_pedidos:
            return 0.0
        
        # Tiempo máximo de preparación + buffer
        tiempo_max = max(item.item.tiempo_preparacion for item in self.linea_pedidos)
        buffer = 5.0  # 5 minutos de buffer
        return tiempo_max + buffer
    
    def validar_disponibilidad_items(self) -> Dict[int, bool]:
        """Valida la disponibilidad de todos los items de la orden"""
        resultados = {}
        for item_orden in self.linea_pedidos:
            disponible = (
                item_orden.item.disponible and 
                item_orden.item.stock >= item_orden.cant_pedida
            )
            resultados[item_orden.id] = disponible
        return resultados

class ResumenOrden(BaseModel):
    """Modelo para resúmenes de órdenes"""
    id: int
    numero_orden: int
    mesa_nombre: Optional[str] = None
    estado: str
    num_items: int
    monto_total: float
    hora_registro: datetime
    meseros_nombres: List[str] = []
    tiempo_estimado: float = 0.0
    # clientes_nombres: List[str] = []  # Estará en módulo estancia_cliente
    # num_cuentas: int = 0  # Estará en módulo division_de_cuenta

class EstadisticasPedidos(BaseModel):
    """Modelo para estadísticas de pedidos"""
    total_ordenes: int
    ordenes_en_cola: int
    ordenes_en_preparacion: int
    ordenes_listas: int
    ordenes_despachadas: int
    ordenes_canceladas: int
    monto_total_dia: float
    promedio_tiempo_preparacion: float
    items_mas_pedidos: List[Dict[str, int]] = []
