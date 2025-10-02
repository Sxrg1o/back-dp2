from typing import Type
from app.repositories.interfaces import IMenuRepository, IPedidosRepository
from app.repositories.mock_menu_repository import MockMenuRepository
from app.repositories.mock_pedidos_repository import MockPedidosRepository
from app.repositories.database_menu_repository import DatabaseMenuRepository

class RepositoryFactory:
    """Factory para crear instancias de repositorios"""
    
    @staticmethod
    def create_menu_repository(repository_type: str = "mock") -> IMenuRepository:
        """
        Crea una instancia del repositorio de menú
        
        Args:
            repository_type: Tipo de repositorio ("mock", "database", "api", etc.)
        
        Returns:
            Instancia del repositorio de menú
        """
        if repository_type == "mock":
            return MockMenuRepository()
        elif repository_type == "database":
            from app.config import Config
            return DatabaseMenuRepository(Config.DATABASE_URL)
        elif repository_type == "api":
            # TODO: Implementar repositorio de API externa
            # return ApiMenuRepository()
            raise NotImplementedError("Repositorio de API no implementado aún")
        else:
            raise ValueError(f"Tipo de repositorio no soportado: {repository_type}")
    
    @staticmethod
    def create_pedidos_repository(repository_type: str = "mock") -> IPedidosRepository:
        """
        Crea una instancia del repositorio de pedidos
        
        Args:
            repository_type: Tipo de repositorio ("mock", "database", "api", etc.)
        
        Returns:
            Instancia del repositorio de pedidos
        """
        if repository_type == "mock":
            return MockPedidosRepository()
        elif repository_type == "database":
            # TODO: Implementar repositorio de base de datos
            # return DatabasePedidosRepository()
            raise NotImplementedError("Repositorio de base de datos no implementado aún")
        elif repository_type == "api":
            # TODO: Implementar repositorio de API externa
            # return ApiPedidosRepository()
            raise NotImplementedError("Repositorio de API no implementado aún")
        else:
            raise ValueError(f"Tipo de repositorio no soportado: {repository_type}")
    
    @staticmethod
    def get_available_repository_types() -> dict:
        """
        Retorna los tipos de repositorio disponibles
        
        Returns:
            Diccionario con los tipos disponibles y su estado
        """
        return {
            "mock": {
                "menu": True,
                "pedidos": True,
                "description": "Repositorio en memoria para desarrollo y testing"
            },
            "database": {
                "menu": True,
                "pedidos": False,
                "description": "Repositorio de base de datos (menú implementado, pedidos pendiente)"
            },
            "api": {
                "menu": False,
                "pedidos": False,
                "description": "Repositorio de API externa (no implementado)"
            }
        }
