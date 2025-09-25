from typing import List, Dict, Optional, Tuple
from app.models.domain import Item, Plato, Bebida, Ingrediente
from app.models.enums import EtiquetaPlato, TipoAlergeno
from app.data.menu_data import (
    obtener_todos_los_items, 
    obtener_platos_por_tipo, 
    obtener_bebidas_sin_alcohol, 
    obtener_bebidas_con_alcohol,
    PLATOS,
    BEBIDAS,
    INGREDIENTES
)

class MenuService:
    """Servicio para gestión del menú y carta"""

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
