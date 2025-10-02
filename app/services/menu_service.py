from typing import List, Dict, Optional, Tuple
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Categoria
from app.data.menu_data import (
    obtener_todos_los_items, 
    obtener_platos_por_tipo, 
    obtener_bebidas_sin_alcohol, 
    obtener_bebidas_con_alcohol,
    obtener_categorias,
    obtener_categoria_por_nombre,
    PLATOS,
    BEBIDAS
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

    def obtener_platos_por_tipo(self, tipo: str) -> List[Plato]:
        """Obtiene platos filtrados por tipo"""
        return obtener_platos_por_tipo(tipo)

    def obtener_entradas(self) -> List[Plato]:
        """Obtiene todas las entradas"""
        return self.obtener_platos_por_tipo("ENTRADA")

    def obtener_platos_principales(self) -> List[Plato]:
        """Obtiene todos los platos principales (fondos)"""
        return self.obtener_platos_por_tipo("FONDO")

    def obtener_postres(self) -> List[Plato]:
        """Obtiene todos los postres"""
        return self.obtener_platos_por_tipo("POSTRE")

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
        """Busca items por nombre"""
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
            if item.categoria.nombre.lower() == categoria.lower()
        ]

    def filtrar_por_alergenos(self, alergenos: List[str]) -> List[Item]:
        """Filtra items que contienen los alérgenos especificados"""
        items = self.obtener_todos_los_items()
        alergenos_upper = [alergeno.upper() for alergeno in alergenos]
        return [
            item for item in items.values()
            if any(alergeno in [a.upper() for a in item.alergenos] for alergeno in alergenos_upper)
        ]

    def filtrar_sin_alergenos(self, alergenos: List[str]) -> List[Item]:
        """Filtra items que NO contienen los alérgenos especificados"""
        items = self.obtener_todos_los_items()
        alergenos_upper = [alergeno.upper() for alergeno in alergenos]
        return [
            item for item in items.values()
            if not any(alergeno in [a.upper() for a in item.alergenos] for alergeno in alergenos_upper)
        ]

    def obtener_items_disponibles(self) -> List[Item]:
        """Obtiene solo los items disponibles"""
        items = self.obtener_todos_los_items()
        return [
            item for item in items.values() 
            if item.disponible and item.stock > 0
        ]

    def obtener_categorias(self) -> List[Categoria]:
        """Obtiene todas las categorías"""
        return obtener_categorias()

    def obtener_categoria_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtiene una categoría por nombre"""
        return obtener_categoria_por_nombre(nombre)

    def buscar_ingredientes_por_nombre(self, nombre: str) -> List[str]:
        """Busca ingredientes por nombre en todos los items"""
        items = self.obtener_todos_los_items()
        nombre_lower = nombre.lower()
        ingredientes_encontrados = set()
        
        for item in items.values():
            for ingrediente in item.ingredientes:
                if nombre_lower in ingrediente.lower():
                    ingredientes_encontrados.add(ingrediente)
        
        return list(ingredientes_encontrados)

    def obtener_items_por_ingrediente(self, ingrediente: str) -> List[Item]:
        """Obtiene items que contienen un ingrediente específico"""
        items = self.obtener_todos_los_items()
        ingrediente_lower = ingrediente.lower()
        return [
            item for item in items.values()
            if any(ingrediente_lower in ing.lower() for ing in item.ingredientes)
        ]

    def verificar_disponibilidad_item(self, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        """Verifica si un item está disponible en la cantidad solicitada"""
        item = self.obtener_item_por_id(item_id)
        
        if not item:
            return False, "Item no encontrado"
        
        if not item.disponible:
            return False, "Item no disponible"
        
        if item.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {item.stock}, Solicitado: {cantidad}"
        
        return True, "Disponible"

    def obtener_menu_completo_organizado(self) -> Dict[str, List[Item]]:
        """Obtiene el menú completo organizado por categorías"""
        return {
            "entradas": self.obtener_entradas(),
            "platos_principales": self.obtener_platos_principales(),
            "postres": self.obtener_postres(),
            "bebidas_sin_alcohol": self.obtener_bebidas_sin_alcohol(),
            "bebidas_con_alcohol": self.obtener_bebidas_con_alcohol()
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
            "bebidas_con_alcohol": len(self.obtener_bebidas_con_alcohol())
        }