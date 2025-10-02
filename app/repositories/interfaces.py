# Este archivo ahora solo importa las interfaces separadas
from .menu_repository_interface import IMenuRepository
from .pedidos_repository_interface import IPedidosRepository

__all__ = ['IMenuRepository', 'IPedidosRepository']
