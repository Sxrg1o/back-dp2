from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from app.models.gestion_pedidos.domain import (
    Orden, ItemOrden, Mesero, GrupoMesa, 
    ResumenOrden, EstadisticasPedidos
)
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa
from app.models.menu_y_carta.domain import Item
from app.repositories.interfaces import IPedidosRepository
from app.repositories.repository_factory import RepositoryFactory
from app.services.menu_service import MenuService

class PedidosService:
    """Servicio para gestión de pedidos y órdenes"""
    
    def __init__(self, repository_type: str = "mock"):
        """
        Inicializa el servicio con un repositorio específico
        
        Args:
            repository_type: Tipo de repositorio a usar ("mock", "database", "api")
        """
        self.menu_service = MenuService(repository_type)
        self.repository: IPedidosRepository = RepositoryFactory.create_pedidos_repository(repository_type)
    
    def crear_orden(self, mesa_id: Optional[int] = None, 
                   comentarios: str = "", mesero_ids: List[int] = None) -> Orden:
        """Crea una nueva orden"""
        # Obtener mesa si se proporciona ID
        mesa = None
        if mesa_id:
            mesa = self.repository.obtener_mesa_por_id(mesa_id)
            if not mesa:
                raise ValueError(f"Mesa con ID {mesa_id} no encontrada")
        
        # Crear orden
        orden = Orden(
            id=0,  # Se asignará en el repositorio
            numero_orden=0,  # Se asignará en el repositorio
            mesa=mesa,
            comentarios=comentarios,
            estado=EstadoOrden.EN_COLA
        )
        
        # Asignar meseros si se proporcionan IDs
        if mesero_ids:
            for mesero_id in mesero_ids:
                mesero = self.repository.obtener_mesero_por_id(mesero_id)
                if mesero:
                    orden.asignar_mesero(mesero)
        
        # Guardar en repositorio
        return self.repository.crear_orden(orden)
    
    def obtener_orden_por_id(self, orden_id: int) -> Optional[Orden]:
        """Obtiene una orden por su ID"""
        return self.repository.obtener_orden_por_id(orden_id)
    
    def obtener_todas_las_ordenes(self) -> List[Orden]:
        """Obtiene todas las órdenes"""
        return self.repository.obtener_todas_las_ordenes()
    
    def obtener_ordenes_por_estado(self, estado: EstadoOrden) -> List[Orden]:
        """Obtiene órdenes filtradas por estado"""
        return self.repository.filtrar_ordenes(estado=estado)
    
    def obtener_ordenes_por_mesa(self, mesa_id: int) -> List[Orden]:
        """Obtiene órdenes filtradas por mesa"""
        return self.repository.filtrar_ordenes(mesa_id=mesa_id)
    
    def obtener_ordenes_por_mesero(self, mesero_id: int) -> List[Orden]:
        """Obtiene órdenes filtradas por mesero"""
        return self.repository.filtrar_ordenes(mesero_id=mesero_id)
    
    def filtrar_ordenes(self, estado: Optional[EstadoOrden] = None,
                       mesa_id: Optional[int] = None,
                       mesero_id: Optional[int] = None,
                       fecha_desde: Optional[datetime] = None,
                       fecha_hasta: Optional[datetime] = None) -> List[Orden]:
        """Filtra órdenes según criterios"""
        return self.repository.filtrar_ordenes(
            estado=estado,
            mesa_id=mesa_id,
            mesero_id=mesero_id,
            fecha_desde=fecha_desde.isoformat() if fecha_desde else None,
            fecha_hasta=fecha_hasta.isoformat() if fecha_hasta else None
        )
    
    def cambiar_estado_orden(self, orden_id: int, nuevo_estado: EstadoOrden) -> bool:
        """Cambia el estado de una orden"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        if orden.cambiar_estado(nuevo_estado):
            return self.repository.actualizar_orden(orden)
        return False
    
    def cancelar_orden(self, orden_id: int, razon: str = "") -> bool:
        """Cancela una orden"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Cambiar estado a cancelado
        if orden.cambiar_estado(EstadoOrden.CANCELADO):
            orden.comentarios += f" - Cancelada: {razon}" if razon else " - Cancelada"
            return self.repository.actualizar_orden(orden)
        return False
    
    def agregar_item_a_orden(self, orden_id: int, item_id: int, cantidad: int,
                            comentarios: str = "", acompanamientos: List[int] = None,
                            opciones_adicionales: List[int] = None) -> bool:
        """Agrega un item a una orden existente"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Obtener item del menú
        item = self.menu_service.obtener_item_por_id(item_id)
        if not item:
            return False
        
        # Verificar disponibilidad
        disponible, mensaje = self.menu_service.verificar_disponibilidad_item(item_id, cantidad)
        if not disponible:
            return False
        
        # TODO: Procesar acompañamientos y opciones adicionales
        # Por ahora solo agregamos el item básico
        if orden.agregar_item(item, cantidad, comentarios):
            return self.repository.actualizar_orden(orden)
        return False
    
    def modificar_item_orden(self, orden_id: int, item_orden_id: int, 
                            cantidad: Optional[int] = None,
                            comentarios: Optional[str] = None) -> bool:
        """Modifica un item en una orden existente"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Buscar el item en la orden
        for item_orden in orden.linea_pedidos:
            if item_orden.id == item_orden_id:
                if cantidad is not None:
                    # Verificar disponibilidad si se cambia la cantidad
                    disponible, _ = self.menu_service.verificar_disponibilidad_item(
                        item_orden.item.id, cantidad
                    )
                    if not disponible:
                        return False
                    item_orden.cant_pedida = cantidad
                
                if comentarios is not None:
                    item_orden.comentarios = comentarios
                
                # Recalcular totales
                item_orden.calcular_subtotal()
                orden.calcular_monto_total()
                orden.calcular_num_items()
                
                return self.repository.actualizar_orden(orden)
        
        return False
    
    def remover_item_orden(self, orden_id: int, item_orden_id: int) -> bool:
        """Remueve un item de una orden"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        if orden.remover_item(item_orden_id):
            return self.repository.actualizar_orden(orden)
        return False
    
    def validar_disponibilidad_orden(self, orden_id: int) -> Tuple[bool, List[Dict]]:
        """Valida la disponibilidad de todos los items de una orden"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        if not orden:
            return False, []
        
        items_no_disponibles = []
        todos_disponibles = True
        
        for item_orden in orden.linea_pedidos:
            disponible, mensaje = self.menu_service.verificar_disponibilidad_item(
                item_orden.item.id, item_orden.cant_pedida
            )
            
            if not disponible:
                todos_disponibles = False
                items_no_disponibles.append({
                    "item_id": item_orden.item.id,
                    "item_nombre": item_orden.item.nombre,
                    "cantidad": item_orden.cant_pedida,
                    "mensaje": mensaje
                })
        
        return todos_disponibles, items_no_disponibles
    
    def crear_mesero(self, nombre: str, activo: bool = True) -> Mesero:
        """Crea un nuevo mesero"""
        mesero = Mesero(
            id=0,  # Se asignará en el repositorio
            nombre=nombre,
            activo=activo
        )
        return self.repository.crear_mesero(mesero)
    
    def obtener_mesero_por_id(self, mesero_id: int) -> Optional[Mesero]:
        """Obtiene un mesero por ID"""
        return self.repository.obtener_mesero_por_id(mesero_id)
    
    def obtener_todos_los_meseros(self) -> List[Mesero]:
        """Obtiene todos los meseros"""
        return self.repository.obtener_todos_los_meseros()
    
    def asignar_mesero_a_orden(self, orden_id: int, mesero_id: int) -> bool:
        """Asigna un mesero a una orden"""
        orden = self.repository.obtener_orden_por_id(orden_id)
        mesero = self.repository.obtener_mesero_por_id(mesero_id)
        
        if not orden or not mesero:
            return False
        
        if orden.asignar_mesero(mesero):
            return self.repository.actualizar_orden(orden)
        return False
    
    def crear_grupo_mesa(self, nombre: str, capacidad: int, tipo: TipoMesa, 
                        ubicacion: Optional[str] = None) -> GrupoMesa:
        """Crea un nuevo grupo de mesa"""
        mesa = GrupoMesa(
            id=0,  # Se asignará en el repositorio
            nombre=nombre,
            capacidad=capacidad,
            tipo=tipo,
            ubicacion=ubicacion
        )
        return self.repository.crear_grupo_mesa(mesa)
    
    def obtener_mesa_por_id(self, mesa_id: int) -> Optional[GrupoMesa]:
        """Obtiene una mesa por ID"""
        return self.repository.obtener_mesa_por_id(mesa_id)
    
    def obtener_todas_las_mesas(self) -> List[GrupoMesa]:
        """Obtiene todas las mesas"""
        return self.repository.obtener_todas_las_mesas()
    
    def obtener_mesas_disponibles(self) -> List[GrupoMesa]:
        """Obtiene mesas que no tienen órdenes activas"""
        todas_las_mesas = self.obtener_todas_las_mesas()
        ordenes_activas = self.filtrar_ordenes(
            estado=EstadoOrden.EN_COLA
        ) + self.filtrar_ordenes(
            estado=EstadoOrden.EN_PREPARACION
        ) + self.filtrar_ordenes(
            estado=EstadoOrden.LISTO_PARA_SALIR
        )
        
        # Obtener IDs de mesas ocupadas
        mesas_ocupadas = set()
        for orden in ordenes_activas:
            if orden.mesa:
                mesas_ocupadas.add(orden.mesa.id)
        
        # Retornar mesas no ocupadas
        return [mesa for mesa in todas_las_mesas if mesa.id not in mesas_ocupadas]
    
    def obtener_estadisticas_pedidos(self) -> EstadisticasPedidos:
        """Obtiene estadísticas de pedidos"""
        return self.repository.obtener_estadisticas_pedidos()
    
    def obtener_resumen_ordenes(self) -> List[ResumenOrden]:
        """Obtiene resumen de órdenes"""
        return self.repository.obtener_resumen_ordenes()