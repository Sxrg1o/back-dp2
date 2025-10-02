from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Ingrediente
from app.models.menu_y_carta.enums import EtiquetaPlato, TipoAlergeno
from app.models.gestion_pedidos.domain import Orden, Mesero, GrupoMesa, ResumenOrden, EstadisticasPedidos
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa
from app.repositories.interfaces import IMenuRepository, IPedidosRepository
from app.data.menu_data import (
    obtener_todos_los_items, 
    obtener_platos_por_tipo, 
    obtener_bebidas_sin_alcohol, 
    obtener_bebidas_con_alcohol,
    PLATOS,
    BEBIDAS,
    INGREDIENTES
)

class MockMenuRepository(IMenuRepository):
    """Repositorio mock para datos de menú en memoria"""
    
    def obtener_todos_los_items(self) -> Dict[int, Item]:
        """Obtiene todos los items del menú"""
        return obtener_todos_los_items()

    def obtener_item_por_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item específico por ID"""
        items = self.obtener_todos_los_items()
        return items.get(item_id)

    def obtener_platos(self) -> List[Plato]:
        """Obtiene todos los platos"""
        return list(PLATOS.values())

    def obtener_platos_por_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """Obtiene platos filtrados por tipo"""
        return obtener_platos_por_tipo(tipo)

    def obtener_bebidas(self) -> List[Bebida]:
        """Obtiene todas las bebidas"""
        return list(BEBIDAS.values())

    def obtener_bebidas_sin_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas sin alcohol"""
        return obtener_bebidas_sin_alcohol()

    def obtener_bebidas_con_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas con alcohol"""
        return obtener_bebidas_con_alcohol()

    def buscar_items_por_nombre(self, nombre: str) -> List[Item]:
        """Busca items por nombre (búsqueda parcial)"""
        items = self.obtener_todos_los_items()
        nombre_lower = nombre.lower()
        return [
            item for item in items.values() 
            if nombre_lower in item.nombre.lower()
        ]

    def filtrar_por_categoria(self, categoria: str) -> List[Item]:
        """Filtra items por categoría"""
        items = self.obtener_todos_los_items()
        return [
            item for item in items.values() 
            if categoria.lower() in item.categoria.lower()
        ]

    def filtrar_por_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que contengan los alérgenos especificados"""
        items = self.obtener_todos_los_items()
        alergenos_str = [alergeno.value for alergeno in alergenos]
        
        return [
            item for item in items.values()
            if any(alergeno in item.alergenos.upper() for alergeno in alergenos_str)
        ]

    def filtrar_sin_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que NO contengan los alérgenos especificados"""
        items = self.obtener_todos_los_items()
        alergenos_str = [alergeno.value for alergeno in alergenos]
        
        return [
            item for item in items.values()
            if not any(alergeno in item.alergenos.upper() for alergeno in alergenos_str)
        ]

    def obtener_items_disponibles(self) -> List[Item]:
        """Obtiene solo items que están disponibles y tienen stock"""
        items = self.obtener_todos_los_items()
        return [
            item for item in items.values()
            if item.verificar_stock()
        ]

    def obtener_ingredientes(self) -> List[Ingrediente]:
        """Obtiene todos los ingredientes"""
        return list(INGREDIENTES.values())

    def obtener_ingrediente_por_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """Obtiene un ingrediente por ID"""
        return INGREDIENTES.get(ingrediente_id)

    def buscar_ingredientes_por_nombre(self, nombre: str) -> List[Ingrediente]:
        """Busca ingredientes por nombre"""
        nombre_lower = nombre.lower()
        return [
            ingrediente for ingrediente in INGREDIENTES.values()
            if nombre_lower in ingrediente.nombre.lower()
        ]

    def obtener_items_por_ingrediente(self, ingrediente_id: int) -> List[Item]:
        """Obtiene items que contengan un ingrediente específico"""
        items = self.obtener_todos_los_items()
        return [
            item for item in items.values()
            if any(ing.id == ingrediente_id for ing in item.ingredientes)
        ]

    def verificar_disponibilidad_item(self, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        """Verifica si un item está disponible en la cantidad solicitada"""
        item = self.obtener_item_por_id(item_id)
        if not item:
            return False, "Item no encontrado"
        
        if not item.disponible:
            return False, "Item no disponible"
        
        if item.stock < cantidad:
            return False, f"Stock insuficiente (disponible: {item.stock})"
        
        return True, "Disponible"

class MockPedidosRepository(IPedidosRepository):
    """Repositorio mock para datos de pedidos en memoria"""
    
    def __init__(self):
        self.ordenes: Dict[int, Orden] = {}
        self.meseros: Dict[int, Mesero] = {}
        self.mesas: Dict[int, GrupoMesa] = {}
        self._inicializar_datos_mock()
    
    def _inicializar_datos_mock(self):
        """Inicializa datos de ejemplo para testing"""
        # Crear meseros de ejemplo
        self.meseros[1] = Mesero(id=1, nombre="Carlos Mendoza", activo=True)
        self.meseros[2] = Mesero(id=2, nombre="Ana García", activo=True)
        self.meseros[3] = Mesero(id=3, nombre="Luis Rodríguez", activo=False)
        
        # Crear mesas de ejemplo
        self.mesas[1] = GrupoMesa(
            id=1, nombre="Mesa 1", capacidad=4, 
            tipo=TipoMesa.FAMILIAR, ubicacion="Sala principal"
        )
        self.mesas[2] = GrupoMesa(
            id=2, nombre="Mesa 2", capacidad=2, 
            tipo=TipoMesa.PAREJA, ubicacion="Terraza"
        )
        self.mesas[3] = GrupoMesa(
            id=3, nombre="Mesa VIP", capacidad=8, 
            tipo=TipoMesa.VIP, ubicacion="Sala VIP"
        )
        
        # Crear órdenes de ejemplo
        self._crear_ordenes_ejemplo()
    
    def _crear_ordenes_ejemplo(self):
        """Crea órdenes de ejemplo para testing"""
        from app.services.menu_service import MenuService
        menu_service = MenuService()
        
        # Orden 1 - Mesa 1, Mesero Carlos
        orden1 = Orden(
            id=1,
            numero_orden=1001,
            mesa=self.mesas[1],
            estado=EstadoOrden.EN_COLA,
            comentarios="Sin cebolla en el ceviche",
            meseros=[self.meseros[1]]
        )
        
        # Agregar items a la orden 1
        ceviche = menu_service.obtener_item_por_id(1)
        if ceviche:
            orden1.agregar_item(ceviche, 2, "Sin cebolla")
        
        self.ordenes[1] = orden1
        
        # Orden 2 - Mesa 2, Mesero Ana
        orden2 = Orden(
            id=2,
            numero_orden=1002,
            mesa=self.mesas[2],
            estado=EstadoOrden.EN_PREPARACION,
            comentarios="",
            meseros=[self.meseros[2]]
        )
        
        # Agregar items a la orden 2
        lomo = menu_service.obtener_item_por_id(3)
        cerveza = menu_service.obtener_item_por_id(6)
        if lomo and cerveza:
            orden2.agregar_item(lomo, 1)
            orden2.agregar_item(cerveza, 2)
        
        self.ordenes[2] = orden2
        
        # Orden 3 - Sin mesa asignada
        orden3 = Orden(
            id=3,
            numero_orden=1003,
            estado=EstadoOrden.LISTO_PARA_SALIR,
            comentarios="Para llevar",
            meseros=[self.meseros[1]]
        )
        
        # Agregar items a la orden 3
        causa = menu_service.obtener_item_por_id(4)
        suspiro = menu_service.obtener_item_por_id(5)
        if causa and suspiro:
            orden3.agregar_item(causa, 1)
            orden3.agregar_item(suspiro, 2)
        
        self.ordenes[3] = orden3

    def crear_orden(self, orden: Orden) -> Orden:
        """Crea una nueva orden"""
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
        
        # Filtros de fecha (implementación básica)
        if fecha_desde:
            fecha_desde_dt = datetime.fromisoformat(fecha_desde)
            ordenes = [o for o in ordenes if o.hora_registro >= fecha_desde_dt]
        
        if fecha_hasta:
            fecha_hasta_dt = datetime.fromisoformat(fecha_hasta)
            ordenes = [o for o in ordenes if o.hora_registro <= fecha_hasta_dt]
        
        return ordenes

    def crear_mesero(self, mesero: Mesero) -> Mesero:
        """Crea un nuevo mesero"""
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
        
        # Items más pedidos
        items_count = {}
        for orden in ordenes:
            for item_orden in orden.linea_pedidos:
                item_nombre = item_orden.item.nombre
                items_count[item_nombre] = items_count.get(item_nombre, 0) + item_orden.cant_pedida
        
        items_mas_pedidos = [{"item": k, "cantidad": v} for k, v in sorted(items_count.items(), key=lambda x: x[1], reverse=True)[:5]]
        
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

