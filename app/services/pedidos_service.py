from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from app.models.gestion_pedidos.domain import (
    Orden, ItemOrden, Mesero, GrupoMesa, 
    ResumenOrden, EstadisticasPedidos
)
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa
from app.models.menu_y_carta.domain import Item
from app.services.menu_service import MenuService

class PedidosService:
    """Servicio para gestión de pedidos y órdenes"""
    
    def __init__(self):
        self.menu_service = MenuService()
        self.ordenes: Dict[int, Orden] = {}
        self.meseros: Dict[int, Mesero] = {}
        self.mesas: Dict[int, GrupoMesa] = {}
        # clientes: Dict[int, Cliente] = {}  # Estará en módulo estancia_cliente
        self._inicializar_datos_mock()
    
    def _inicializar_datos_mock(self):
        """Inicializa datos de prueba"""
        # Crear meseros
        self.meseros = {
            1: Mesero(id=1, nombre="Carlos Mendoza", activo=True),
            2: Mesero(id=2, nombre="Ana García", activo=True),
            3: Mesero(id=3, nombre="Luis Rodríguez", activo=True),
        }
        
        # Crear mesas
        self.mesas = {
            1: GrupoMesa(id=1, nombre="Mesa 1", capacidad=2, tipo=TipoMesa.PAREJA, ubicacion="Interior"),
            2: GrupoMesa(id=2, nombre="Mesa 2", capacidad=4, tipo=TipoMesa.FAMILIAR, ubicacion="Interior"),
            3: GrupoMesa(id=3, nombre="Mesa 3", capacidad=6, tipo=TipoMesa.GRUPO, ubicacion="Terraza"),
            4: GrupoMesa(id=4, nombre="Mesa VIP", capacidad=8, tipo=TipoMesa.VIP, ubicacion="Salón Privado"),
        }
        
        # Clientes estarán en módulo estancia_cliente
        # self.clientes = {
        #     1: Cliente(id=1, nombre="Juan Pérez", telefono="987654321", email="juan@email.com"),
        #     2: Cliente(id=2, nombre="María López", telefono="987654322", email="maria@email.com"),
        #     3: Cliente(id=3, nombre="Carlos Silva", telefono="987654323"),
        # }
        
        # Crear algunas órdenes de ejemplo
        self._crear_ordenes_ejemplo()
    
    def _crear_ordenes_ejemplo(self):
        """Crea órdenes de ejemplo para testing"""
        # Orden 1 - En cola
        orden1 = Orden(
            id=1,
            numero_orden=1001,
            mesa=self.mesas[1],
            # clientes=[self.clientes[1]],  # Estará en módulo estancia_cliente
            estado=EstadoOrden.EN_COLA,
            comentarios="Sin cebolla en el ceviche",
            meseros=[self.meseros[1]]
        )
        
        # Agregar items a la orden
        items = self.menu_service.obtener_todos_los_items()
        if 1 in items:  # Ceviche
            orden1.agregar_item(items[1], 2, "Sin cebolla")
        if 2 in items:  # Arroz con mariscos
            orden1.agregar_item(items[2], 1)
        
        self.ordenes[1] = orden1
        
        # Orden 2 - En preparación
        orden2 = Orden(
            id=2,
            numero_orden=1002,
            mesa=self.mesas[2],
            # clientes=[self.clientes[2], self.clientes[3]],  # Estará en módulo estancia_cliente
            estado=EstadoOrden.EN_PREPARACION,
            meseros=[self.meseros[2]]
        )
        
        if 3 in items:  # Lomo saltado
            orden2.agregar_item(items[3], 2)
        if 6 in items:  # Cerveza
            orden2.agregar_item(items[6], 3)
        
        self.ordenes[2] = orden2
    
    # =========================
    # Gestión de Órdenes
    # =========================
    
    def crear_orden(self, mesa_id: Optional[int] = None, 
                   comentarios: str = "", mesero_ids: List[int] = None) -> Orden:
        """Crea una nueva orden"""
        mesero_ids = mesero_ids or []
        
        # Generar número de orden único
        numero_orden = max([o.numero_orden for o in self.ordenes.values()], default=1000) + 1
        
        # Obtener mesa si se especifica
        mesa = self.mesas.get(mesa_id) if mesa_id else None
        
        # Obtener meseros
        meseros = [self.meseros[mid] for mid in mesero_ids if mid in self.meseros]
        
        # Crear orden
        orden = Orden(
            id=len(self.ordenes) + 1,
            numero_orden=numero_orden,
            mesa=mesa,
            # clientes=clientes,  # Estará en módulo estancia_cliente
            comentarios=comentarios,
            meseros=meseros
        )
        
        self.ordenes[orden.id] = orden
        return orden
    
    def obtener_orden_por_id(self, orden_id: int) -> Optional[Orden]:
        """Obtiene una orden por su ID"""
        return self.ordenes.get(orden_id)
    
    def obtener_todas_las_ordenes(self) -> List[Orden]:
        """Obtiene todas las órdenes"""
        return list(self.ordenes.values())
    
    def obtener_ordenes_por_estado(self, estado: EstadoOrden) -> List[Orden]:
        """Obtiene órdenes filtradas por estado"""
        return [orden for orden in self.ordenes.values() if orden.estado == estado]
    
    def obtener_ordenes_por_mesa(self, mesa_id: int) -> List[Orden]:
        """Obtiene órdenes de una mesa específica"""
        return [orden for orden in self.ordenes.values() 
                if orden.mesa and orden.mesa.id == mesa_id]
    
    def obtener_ordenes_por_mesero(self, mesero_id: int) -> List[Orden]:
        """Obtiene órdenes de un mesero específico"""
        return [orden for orden in self.ordenes.values() 
                if any(mesero.id == mesero_id for mesero in orden.meseros)]
    
    def filtrar_ordenes(self, estado: Optional[EstadoOrden] = None,
                       mesa_id: Optional[int] = None,
                       mesero_id: Optional[int] = None,
                       fecha_desde: Optional[datetime] = None,
                       fecha_hasta: Optional[datetime] = None) -> List[Orden]:
        """Filtra órdenes según criterios"""
        ordenes = list(self.ordenes.values())
        
        if estado:
            ordenes = [o for o in ordenes if o.estado == estado]
        
        if mesa_id:
            ordenes = [o for o in ordenes if o.mesa and o.mesa.id == mesa_id]
        
        if mesero_id:
            ordenes = [o for o in ordenes if any(m.id == mesero_id for m in o.meseros)]
        
        if fecha_desde:
            ordenes = [o for o in ordenes if o.hora_registro >= fecha_desde]
        
        if fecha_hasta:
            ordenes = [o for o in ordenes if o.hora_registro <= fecha_hasta]
        
        return ordenes
    
    def cambiar_estado_orden(self, orden_id: int, nuevo_estado: EstadoOrden) -> bool:
        """Cambia el estado de una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        return orden.cambiar_estado(nuevo_estado)
    
    def cancelar_orden(self, orden_id: int, razon: str = "") -> bool:
        """Cancela una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Solo se puede cancelar si está en cola o preparación
        if orden.estado in [EstadoOrden.EN_COLA, EstadoOrden.EN_PREPARACION]:
            orden.estado = EstadoOrden.CANCELADO
            orden.comentarios += f" | Cancelada: {razon}" if razon else " | Cancelada"
            return True
        
        return False
    
    # =========================
    # Gestión de Items en Órdenes
    # =========================
    
    def agregar_item_a_orden(self, orden_id: int, item_id: int, cantidad: int,
                            comentarios: str = "", acompanamientos: List[int] = None,
                            opciones_adicionales: List[int] = None) -> bool:
        """Agrega un item a una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Obtener item del menú
        item = self.menu_service.obtener_item_por_id(item_id)
        if not item:
            return False
        
        # Validar disponibilidad
        if not item.verificar_stock() or item.stock < cantidad:
            return False
        
        # Obtener opciones de personalización
        acompanamientos_opciones = []
        opciones_adicionales_opciones = []
        
        if item.grupo_personalizacion:
            if acompanamientos:
                for opcion_id in acompanamientos:
                    if opcion_id < len(item.grupo_personalizacion.opciones):
                        acompanamientos_opciones.append(item.grupo_personalizacion.opciones[opcion_id])
        
        # Agregar item a la orden
        return orden.agregar_item(
            item=item,
            cantidad=cantidad,
            comentarios=comentarios,
            acompanamientos=acompanamientos_opciones,
            opciones_adicionales=opciones_adicionales_opciones
        )
    
    def modificar_item_orden(self, orden_id: int, item_orden_id: int, 
                            cantidad: Optional[int] = None,
                            comentarios: Optional[str] = None) -> bool:
        """Modifica un item en una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        # Buscar el item en la orden
        for item_orden in orden.linea_pedidos:
            if item_orden.id == item_orden_id:
                if cantidad is not None:
                    # Validar nueva cantidad
                    if not item_orden.item.verificar_stock() or item_orden.item.stock < cantidad:
                        return False
                    item_orden.cant_pedida = cantidad
                
                if comentarios is not None:
                    item_orden.comentarios = comentarios
                
                # Recalcular subtotal
                item_orden.calcular_subtotal()
                orden.calcular_monto_total()
                orden.calcular_num_items()
                return True
        
        return False
    
    def remover_item_orden(self, orden_id: int, item_orden_id: int) -> bool:
        """Remueve un item de una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False
        
        return orden.remover_item(item_orden_id)
    
    def validar_disponibilidad_orden(self, orden_id: int) -> Tuple[bool, List[Dict]]:
        """Valida la disponibilidad de todos los items de una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        if not orden:
            return False, []
        
        items_no_disponibles = []
        todos_disponibles = True
        
        for item_orden in orden.linea_pedidos:
            disponible = (
                item_orden.item.disponible and 
                item_orden.item.stock >= item_orden.cant_pedida
            )
            
            if not disponible:
                todos_disponibles = False
                items_no_disponibles.append({
                    "item_orden_id": item_orden.id,
                    "item_nombre": item_orden.item.nombre,
                    "cantidad_pedida": item_orden.cant_pedida,
                    "stock_disponible": item_orden.item.stock,
                    "disponible": item_orden.item.disponible
                })
        
        return todos_disponibles, items_no_disponibles
    
    # =========================
    # Gestión de Meseros
    # =========================
    
    def crear_mesero(self, nombre: str, activo: bool = True) -> Mesero:
        """Crea un nuevo mesero"""
        mesero = Mesero(
            id=len(self.meseros) + 1,
            nombre=nombre,
            activo=activo
        )
        self.meseros[mesero.id] = mesero
        return mesero
    
    def obtener_mesero_por_id(self, mesero_id: int) -> Optional[Mesero]:
        """Obtiene un mesero por ID"""
        return self.meseros.get(mesero_id)
    
    def obtener_todos_los_meseros(self) -> List[Mesero]:
        """Obtiene todos los meseros"""
        return list(self.meseros.values())
    
    def asignar_mesero_a_orden(self, orden_id: int, mesero_id: int) -> bool:
        """Asigna un mesero a una orden"""
        orden = self.obtener_orden_por_id(orden_id)
        mesero = self.obtener_mesero_por_id(mesero_id)
        
        if not orden or not mesero:
            return False
        
        return orden.asignar_mesero(mesero)
    
    # =========================
    # Gestión de Mesas
    # =========================
    
    def crear_grupo_mesa(self, nombre: str, capacidad: int, tipo: TipoMesa, 
                        ubicacion: Optional[str] = None) -> GrupoMesa:
        """Crea un nuevo grupo de mesa"""
        mesa = GrupoMesa(
            id=len(self.mesas) + 1,
            nombre=nombre,
            capacidad=capacidad,
            tipo=tipo,
            ubicacion=ubicacion
        )
        self.mesas[mesa.id] = mesa
        return mesa
    
    def obtener_mesa_por_id(self, mesa_id: int) -> Optional[GrupoMesa]:
        """Obtiene una mesa por ID"""
        return self.mesas.get(mesa_id)
    
    def obtener_todas_las_mesas(self) -> List[GrupoMesa]:
        """Obtiene todas las mesas"""
        return list(self.mesas.values())
    
    def obtener_mesas_disponibles(self) -> List[GrupoMesa]:
        """Obtiene mesas que no tienen órdenes activas"""
        mesas_ocupadas = set()
        for orden in self.ordenes.values():
            if orden.activo and orden.mesa and orden.estado != EstadoOrden.DESPACHADO:
                mesas_ocupadas.add(orden.mesa.id)
        
        return [mesa for mesa in self.mesas.values() 
                if mesa.activa and mesa.id not in mesas_ocupadas]
    
    # =========================
    # Gestión de Clientes - Estará en módulo estancia_cliente
    # =========================
    
    # def crear_cliente(self, nombre: str, telefono: Optional[str] = None, 
    #                  email: Optional[str] = None) -> Cliente:
    #     """Crea un nuevo cliente"""
    #     cliente = Cliente(
    #         id=len(self.clientes) + 1,
    #         nombre=nombre,
    #         telefono=telefono,
    #         email=email
    #     )
    #     self.clientes[cliente.id] = cliente
    #     return cliente
    
    # def obtener_cliente_por_id(self, cliente_id: int) -> Optional[Cliente]:
    #     """Obtiene un cliente por ID"""
    #     return self.clientes.get(cliente_id)
    
    # def obtener_todos_los_clientes(self) -> List[Cliente]:
    #     """Obtiene todos los clientes"""
    #     return list(self.clientes.values())
    
    # =========================
    # Estadísticas y Reportes
    # =========================
    
    def obtener_estadisticas_pedidos(self) -> EstadisticasPedidos:
        """Obtiene estadísticas de pedidos"""
        ordenes = self.obtener_todas_las_ordenes()
        
        estadisticas = EstadisticasPedidos(
            total_ordenes=len(ordenes),
            ordenes_en_cola=len([o for o in ordenes if o.estado == EstadoOrden.EN_COLA]),
            ordenes_en_preparacion=len([o for o in ordenes if o.estado == EstadoOrden.EN_PREPARACION]),
            ordenes_listas=len([o for o in ordenes if o.estado == EstadoOrden.LISTO_PARA_SALIR]),
            ordenes_despachadas=len([o for o in ordenes if o.estado == EstadoOrden.DESPACHADO]),
            ordenes_canceladas=len([o for o in ordenes if o.estado == EstadoOrden.CANCELADO]),
            monto_total_dia=sum(o.monto_total for o in ordenes if o.estado != EstadoOrden.CANCELADO),
            promedio_tiempo_preparacion=0.0,  # TODO: Implementar cálculo real
            items_mas_pedidos=[]
        )
        
        return estadisticas
    
    def obtener_resumen_ordenes(self) -> List[ResumenOrden]:
        """Obtiene resumen de todas las órdenes"""
        resumenes = []
        
        for orden in self.ordenes.values():
            resumen = ResumenOrden(
                id=orden.id,
                numero_orden=orden.numero_orden,
                mesa_nombre=orden.mesa.nombre if orden.mesa else None,
                estado=orden.estado.value,
                num_items=orden.num_items,
                monto_total=orden.monto_total,
                hora_registro=orden.hora_registro,
                meseros_nombres=[mesero.nombre for mesero in orden.meseros],
                tiempo_estimado=orden.obtener_tiempo_estimado()
            )
            resumenes.append(resumen)
        
        return resumenes
