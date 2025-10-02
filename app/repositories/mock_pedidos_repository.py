from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models.gestion_pedidos.domain import (
    Orden, ItemOrden, Mesero, GrupoMesa, 
    ResumenOrden, EstadisticasPedidos
)
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa
from app.repositories.pedidos_repository_interface import IPedidosRepository
# Importación movida para evitar circular import

class MockPedidosRepository(IPedidosRepository):
    """Implementación mock del repositorio de pedidos usando datos en memoria"""
    
    def __init__(self):
        # Importación local para evitar circular import
        from app.services.menu_service import MenuService
        self.menu_service = MenuService()
        self.ordenes: Dict[int, Orden] = {}
        self.meseros: Dict[int, Mesero] = {}
        self.mesas: Dict[int, GrupoMesa] = {}
        self._inicializar_datos_mock()
    
    def _inicializar_datos_mock(self):
        """Inicializa datos de ejemplo para testing"""
        # Crear meseros de ejemplo
        mesero1 = Mesero(id=1, nombre="Carlos Mendoza", activo=True)
        mesero2 = Mesero(id=2, nombre="Ana García", activo=True)
        mesero3 = Mesero(id=3, nombre="Luis Rodríguez", activo=False)
        
        self.meseros = {
            1: mesero1,
            2: mesero2,
            3: mesero3
        }
        
        # Crear mesas de ejemplo
        mesa1 = GrupoMesa(id=1, nombre="Mesa 1", capacidad=4, tipo=TipoMesa.FAMILIAR, ubicacion="Interior")
        mesa2 = GrupoMesa(id=2, nombre="Mesa 2", capacidad=2, tipo=TipoMesa.PAREJA, ubicacion="Terraza")
        mesa3 = GrupoMesa(id=3, nombre="Mesa 3", capacidad=6, tipo=TipoMesa.GRUPO, ubicacion="Interior")
        mesa4 = GrupoMesa(id=4, nombre="Mesa VIP", capacidad=8, tipo=TipoMesa.VIP, ubicacion="Salón VIP")
        
        self.mesas = {
            1: mesa1,
            2: mesa2,
            3: mesa3,
            4: mesa4
        }
        
        # Crear órdenes de ejemplo
        self._crear_ordenes_ejemplo()
    
    def _crear_ordenes_ejemplo(self):
        """Crea órdenes de ejemplo para testing"""
        # Obtener items del menú
        items = self.menu_service.obtener_todos_los_items()
        
        # Orden 1: Mesa 1 con ceviche y cerveza
        orden1 = Orden(
            id=1,
            numero_orden=1001,
            mesa=self.mesas[1],
            estado=EstadoOrden.EN_COLA,
            comentarios="Sin cebolla en el ceviche",
            hora_registro=datetime.now() - timedelta(minutes=30)
        )
        
        # Agregar items a la orden
        if 1 in items:  # Ceviche
            orden1.agregar_item(items[1], 2, "Sin cebolla")
        if 6 in items:  # Cerveza
            orden1.agregar_item(items[6], 1)
        
        # Asignar mesero
        orden1.asignar_mesero(self.meseros[1])
        
        # Orden 2: Mesa 2 con arroz con mariscos
        orden2 = Orden(
            id=2,
            numero_orden=1002,
            mesa=self.mesas[2],
            estado=EstadoOrden.EN_PREPARACION,
            comentarios="",
            hora_registro=datetime.now() - timedelta(minutes=15)
        )
        
        if 2 in items:  # Arroz con mariscos
            orden2.agregar_item(items[2], 1)
        
        orden2.asignar_mesero(self.meseros[2])
        
        # Orden 3: Mesa 3 con lomo saltado y chicha
        orden3 = Orden(
            id=3,
            numero_orden=1003,
            mesa=self.mesas[3],
            estado=EstadoOrden.LISTO_PARA_SALIR,
            comentarios="Bien cocido",
            hora_registro=datetime.now() - timedelta(minutes=45)
        )
        
        if 3 in items:  # Lomo saltado
            orden3.agregar_item(items[3], 2, "Bien cocido")
        if 7 in items:  # Chicha morada
            orden3.agregar_item(items[7], 3)
        
        orden3.asignar_mesero(self.meseros[1])
        
        self.ordenes = {
            1: orden1,
            2: orden2,
            3: orden3
        }
    
    def crear_orden(self, orden: Orden) -> Orden:
        """Crea una nueva orden"""
        # Asignar ID si no tiene
        if not orden.id:
            orden.id = max(self.ordenes.keys()) + 1 if self.ordenes else 1
        
        # Asignar número de orden si no tiene
        if not orden.numero_orden:
            orden.numero_orden = 1000 + orden.id
        
        self.ordenes[orden.id] = orden
        return orden
    
    def obtener_orden_por_id(self, orden_id: int) -> Optional[Orden]:
        """Obtiene una orden por su ID"""
        return self.ordenes.get(orden_id)
    
    def obtener_todas_las_ordenes(self) -> List[Orden]:
        """Obtiene todas las órdenes"""
        return list(self.ordenes.values())
    
    def actualizar_orden(self, orden: Orden) -> bool:
        """Actualiza una orden existente"""
        if orden.id in self.ordenes:
            self.ordenes[orden.id] = orden
            return True
        return False
    
    def eliminar_orden(self, orden_id: int) -> bool:
        """Elimina una orden"""
        if orden_id in self.ordenes:
            del self.ordenes[orden_id]
            return True
        return False
    
    def filtrar_ordenes(self, estado: Optional[EstadoOrden] = None,
                       mesa_id: Optional[int] = None,
                       mesero_id: Optional[int] = None,
                       fecha_desde: Optional[str] = None,
                       fecha_hasta: Optional[str] = None) -> List[Orden]:
        """Filtra órdenes según criterios"""
        ordenes = list(self.ordenes.values())
        
        if estado:
            ordenes = [o for o in ordenes if o.estado == estado]
        
        if mesa_id:
            ordenes = [o for o in ordenes if o.mesa and o.mesa.id == mesa_id]
        
        if mesero_id:
            ordenes = [o for o in ordenes if any(m.id == mesero_id for m in o.meseros)]
        
        # TODO: Implementar filtros de fecha si es necesario
        # if fecha_desde:
        #     ordenes = [o for o in ordenes if o.hora_registro >= fecha_desde]
        # if fecha_hasta:
        #     ordenes = [o for o in ordenes if o.hora_registro <= fecha_hasta]
        
        return ordenes
    
    def crear_mesero(self, mesero: Mesero) -> Mesero:
        """Crea un nuevo mesero"""
        if not mesero.id:
            mesero.id = max(self.meseros.keys()) + 1 if self.meseros else 1
        
        self.meseros[mesero.id] = mesero
        return mesero
    
    def obtener_mesero_por_id(self, mesero_id: int) -> Optional[Mesero]:
        """Obtiene un mesero por ID"""
        return self.meseros.get(mesero_id)
    
    def obtener_todos_los_meseros(self) -> List[Mesero]:
        """Obtiene todos los meseros"""
        return list(self.meseros.values())
    
    def actualizar_mesero(self, mesero: Mesero) -> bool:
        """Actualiza un mesero"""
        if mesero.id in self.meseros:
            self.meseros[mesero.id] = mesero
            return True
        return False
    
    def crear_grupo_mesa(self, mesa: GrupoMesa) -> GrupoMesa:
        """Crea un nuevo grupo de mesa"""
        if not mesa.id:
            mesa.id = max(self.mesas.keys()) + 1 if self.mesas else 1
        
        self.mesas[mesa.id] = mesa
        return mesa
    
    def obtener_mesa_por_id(self, mesa_id: int) -> Optional[GrupoMesa]:
        """Obtiene una mesa por ID"""
        return self.mesas.get(mesa_id)
    
    def obtener_todas_las_mesas(self) -> List[GrupoMesa]:
        """Obtiene todas las mesas"""
        return list(self.mesas.values())
    
    def actualizar_mesa(self, mesa: GrupoMesa) -> bool:
        """Actualiza una mesa"""
        if mesa.id in self.mesas:
            self.mesas[mesa.id] = mesa
            return True
        return False
    
    def obtener_estadisticas_pedidos(self) -> EstadisticasPedidos:
        """Obtiene estadísticas de pedidos"""
        ordenes = self.obtener_todas_las_ordenes()
        
        total_ordenes = len(ordenes)
        ordenes_en_cola = len([o for o in ordenes if o.estado == EstadoOrden.EN_COLA])
        ordenes_en_preparacion = len([o for o in ordenes if o.estado == EstadoOrden.EN_PREPARACION])
        ordenes_listas = len([o for o in ordenes if o.estado == EstadoOrden.LISTO_PARA_SALIR])
        ordenes_despachadas = len([o for o in ordenes if o.estado == EstadoOrden.DESPACHADO])
        ordenes_canceladas = len([o for o in ordenes if o.estado == EstadoOrden.CANCELADO])
        
        monto_total_dia = sum(o.monto_total for o in ordenes)
        
        # Calcular tiempo promedio de preparación
        tiempos = [o.obtener_tiempo_estimado() for o in ordenes if o.obtener_tiempo_estimado() > 0]
        promedio_tiempo_preparacion = sum(tiempos) / len(tiempos) if tiempos else 0.0
        
        # Items más pedidos (simplificado)
        items_mas_pedidos = []
        for orden in ordenes:
            for item_orden in orden.linea_pedidos:
                items_mas_pedidos.append({
                    "item_nombre": item_orden.item.nombre,
                    "cantidad": item_orden.cant_pedida
                })
        
        return EstadisticasPedidos(
            total_ordenes=total_ordenes,
            ordenes_en_cola=ordenes_en_cola,
            ordenes_en_preparacion=ordenes_en_preparacion,
            ordenes_listas=ordenes_listas,
            ordenes_despachadas=ordenes_despachadas,
            ordenes_canceladas=ordenes_canceladas,
            monto_total_dia=monto_total_dia,
            promedio_tiempo_preparacion=promedio_tiempo_preparacion,
            items_mas_pedidos=items_mas_pedidos
        )
    
    def obtener_resumen_ordenes(self) -> List[ResumenOrden]:
        """Obtiene resumen de órdenes"""
        resumenes = []
        for orden in self.obtener_todas_las_ordenes():
            resumen = ResumenOrden(
                id=orden.id,
                numero_orden=orden.numero_orden,
                mesa_nombre=orden.mesa.nombre if orden.mesa else None,
                estado=orden.estado.value,
                num_items=orden.num_items,
                monto_total=orden.monto_total,
                hora_registro=orden.hora_registro,
                meseros_nombres=[m.nombre for m in orden.meseros],
                tiempo_estimado=orden.obtener_tiempo_estimado()
            )
            resumenes.append(resumen)
        
        return resumenes
