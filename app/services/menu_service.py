from typing import List, Dict, Optional, Tuple
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Ingrediente
from app.models.menu_y_carta.enums import EtiquetaPlato, TipoAlergeno
from app.repositories.interfaces import IMenuRepository
from app.repositories.repository_factory import RepositoryFactory

class MenuService:
    """Servicio para gestión del menú y carta"""

    def __init__(self, repository_type: str = "mock"):
        """
        Inicializa el servicio con un repositorio específico
        
        Args:
            repository_type: Tipo de repositorio a usar ("mock", "database", "api")
        """
        self.repository: IMenuRepository = RepositoryFactory.create_menu_repository(repository_type)

    def obtener_todos_los_items(self) -> Dict[int, Item]:
        """Obtiene todos los items del menú"""
        return self.repository.obtener_todos_los_items()

    def obtener_item_por_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item específico por ID"""
        return self.repository.obtener_item_por_id(item_id)

    def obtener_platos(self) -> List[Plato]:
        """Obtiene todos los platos"""
        return self.repository.obtener_platos()

    def obtener_platos_por_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """Obtiene platos filtrados por tipo"""
        return self.repository.obtener_platos_por_tipo(tipo)

    def obtener_entradas(self) -> List[Plato]:
        """Obtiene todas las entradas"""
        return self.obtener_platos_por_tipo(EtiquetaPlato.ENTRADA)

    def obtener_platos_principales(self) -> List[Plato]:
        """Obtiene todos los platos principales (fondos)"""
        return self.obtener_platos_por_tipo(EtiquetaPlato.FONDO)

    def obtener_postres(self) -> List[Plato]:
        """Obtiene todos los postres"""
        return self.obtener_platos_por_tipo(EtiquetaPlato.POSTRE)

    def obtener_bebidas(self) -> List[Bebida]:
        """Obtiene todas las bebidas"""
        return self.repository.obtener_bebidas()

    def obtener_bebidas_sin_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas sin alcohol"""
        return self.repository.obtener_bebidas_sin_alcohol()

    def obtener_bebidas_con_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas con alcohol"""
        return self.repository.obtener_bebidas_con_alcohol()

    def buscar_items_por_nombre(self, nombre: str) -> List[Item]:
        """Busca items por nombre (búsqueda parcial)"""
        return self.repository.buscar_items_por_nombre(nombre)

    def filtrar_por_categoria(self, categoria: str) -> List[Item]:
        """Filtra items por categoría"""
        return self.repository.filtrar_por_categoria(categoria)

    def filtrar_por_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que contengan los alérgenos especificados"""
        return self.repository.filtrar_por_alergenos(alergenos)

    def filtrar_sin_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que NO contengan los alérgenos especificados"""
        return self.repository.filtrar_sin_alergenos(alergenos)

    def obtener_items_disponibles(self) -> List[Item]:
        """Obtiene solo items que están disponibles y tienen stock"""
        return self.repository.obtener_items_disponibles()

    def obtener_ingredientes(self) -> List[Ingrediente]:
        """Obtiene todos los ingredientes"""
        return self.repository.obtener_ingredientes()

    def obtener_ingrediente_por_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """Obtiene un ingrediente por ID"""
        return self.repository.obtener_ingrediente_por_id(ingrediente_id)

    def buscar_ingredientes_por_nombre(self, nombre: str) -> List[Ingrediente]:
        """Busca ingredientes por nombre"""
        return self.repository.buscar_ingredientes_por_nombre(nombre)

    def obtener_items_por_ingrediente(self, ingrediente_id: int) -> List[Item]:
        """Obtiene items que contengan un ingrediente específico"""
        return self.repository.obtener_items_por_ingrediente(ingrediente_id)

    def verificar_disponibilidad_item(self, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        """Verifica si un item está disponible en la cantidad solicitada"""
        return self.repository.verificar_disponibilidad_item(item_id, cantidad)

    def obtener_menu_completo_organizado(self) -> Dict[str, List[Item]]:
        """Obtiene el menú completo organizado por categorías"""
        return {
            "entradas": self.obtener_entradas(),
            "platos_principales": self.obtener_platos_principales(),
            "postres": self.obtener_postres(),
            "bebidas_sin_alcohol": self.obtener_bebidas_sin_alcohol(),
            "bebidas_con_alcohol": self.obtener_bebidas_con_alcohol(),
        }

    def obtener_estadisticas_menu(self) -> Dict[str, int]:
        """Obtiene estadísticas del menú"""
        items = self.obtener_todos_los_items()
        platos = self.obtener_platos()
        bebidas = self.obtener_bebidas()
        
        return {
            "total_items": len(items),
            "total_platos": len(platos),
            "total_bebidas": len(bebidas),
            "items_disponibles": len(self.obtener_items_disponibles()),
            "entradas": len(self.obtener_entradas()),
            "platos_principales": len(self.obtener_platos_principales()),
            "postres": len(self.obtener_postres()),
            "bebidas_sin_alcohol": len(self.obtener_bebidas_sin_alcohol()),
            "bebidas_con_alcohol": len(self.obtener_bebidas_con_alcohol()),
        }
