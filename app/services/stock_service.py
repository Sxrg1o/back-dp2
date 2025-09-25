from typing import Tuple
from app.data.catalog import ITEMS

# =========================
# Agente 3: Stock/validación
# =========================

def tiene_stock(producto_id: str, cantidad: int) -> Tuple[bool, str]:
    """
    Valida si hay stock suficiente para un producto
    
    Args:
        producto_id: ID del producto a validar
        cantidad: Cantidad solicitada
        
    Returns:
        Tuple[bool, str]: (tiene_stock, razon)
    """
    item = ITEMS.get(producto_id)
    if not item:
        return False, "Producto no existe"
    if not item["disponible"]:
        return False, "Producto no disponible"
    if item["stock"] < cantidad:
        return False, f"Stock insuficiente (disponible: {item['stock']})"
    return True, "OK"

def descontar_stock(producto_id: str, cantidad: int) -> bool:
    """
    Descuenta stock de un producto
    
    Args:
        producto_id: ID del producto
        cantidad: Cantidad a descontar
        
    Returns:
        bool: True si se pudo descontar, False en caso contrario
    """
    item = ITEMS.get(producto_id)
    if not item:
        return False
    if item["stock"] < cantidad:
        return False
    
    item["stock"] -= cantidad
    return True

def obtener_stock_disponible(producto_id: str) -> int:
    """
    Obtiene el stock disponible de un producto
    
    Args:
        producto_id: ID del producto
        
    Returns:
        int: Stock disponible (0 si no existe)
    """
    item = ITEMS.get(producto_id)
    if not item:
        return 0
    return item["stock"]
