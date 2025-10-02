from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from app.models.gestion_pedidos.domain import Orden, Mesero, GrupoMesa, ResumenOrden, EstadisticasPedidos
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa

class IPedidosRepository(ABC):
    """Interfaz abstracta para repositorio de pedidos"""
    
    @abstractmethod
    def crear_orden(self, orden: Orden) -> Orden:
        """Crea una nueva orden"""
        pass
    
    @abstractmethod
    def obtener_orden_por_id(self, orden_id: int) -> Optional[Orden]:
        """Obtiene una orden por su ID"""
        pass
    
    @abstractmethod
    def obtener_todas_las_ordenes(self) -> List[Orden]:
        """Obtiene todas las órdenes"""
        pass
    
    @abstractmethod
    def actualizar_orden(self, orden: Orden) -> bool:
        """Actualiza una orden existente"""
        pass
    
    @abstractmethod
    def eliminar_orden(self, orden_id: int) -> bool:
        """Elimina una orden"""
        pass
    
    @abstractmethod
    def filtrar_ordenes(self, estado: Optional[EstadoOrden] = None,
                       mesa_id: Optional[int] = None,
                       mesero_id: Optional[int] = None,
                       fecha_desde: Optional[str] = None,
                       fecha_hasta: Optional[str] = None) -> List[Orden]:
        """Filtra órdenes según criterios"""
        pass
    
    @abstractmethod
    def crear_mesero(self, mesero: Mesero) -> Mesero:
        """Crea un nuevo mesero"""
        pass
    
    @abstractmethod
    def obtener_mesero_por_id(self, mesero_id: int) -> Optional[Mesero]:
        """Obtiene un mesero por ID"""
        pass
    
    @abstractmethod
    def obtener_todos_los_meseros(self) -> List[Mesero]:
        """Obtiene todos los meseros"""
        pass
    
    @abstractmethod
    def actualizar_mesero(self, mesero: Mesero) -> bool:
        """Actualiza un mesero"""
        pass
    
    @abstractmethod
    def crear_grupo_mesa(self, mesa: GrupoMesa) -> GrupoMesa:
        """Crea un nuevo grupo de mesa"""
        pass
    
    @abstractmethod
    def obtener_mesa_por_id(self, mesa_id: int) -> Optional[GrupoMesa]:
        """Obtiene una mesa por ID"""
        pass
    
    @abstractmethod
    def obtener_todas_las_mesas(self) -> List[GrupoMesa]:
        """Obtiene todas las mesas"""
        pass
    
    @abstractmethod
    def actualizar_mesa(self, mesa: GrupoMesa) -> bool:
        """Actualiza una mesa"""
        pass
    
    @abstractmethod
    def obtener_estadisticas_pedidos(self) -> EstadisticasPedidos:
        """Obtiene estadísticas de pedidos"""
        pass
    
    @abstractmethod
    def obtener_resumen_ordenes(self) -> List[ResumenOrden]:
        """Obtiene resumen de órdenes"""
        pass

