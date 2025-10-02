import os
from typing import Dict, Any

class Config:
    """Configuración de la aplicación"""
    
    # Tipo de repositorio por defecto
    REPOSITORY_TYPE = os.getenv("REPOSITORY_TYPE", "mock")
    
    # Configuración de la API
    API_TITLE = "Menu API - Sistema de Gestión de Menú y Carta"
    API_DESCRIPTION = "API para gestión completa del menú, platos, bebidas e ingredientes"
    API_VERSION = "1.0.0"
    
    # Configuración de base de datos (para futuras implementaciones)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./menu.db")
    
    # Configuración de APIs externas (para futuras implementaciones)
    EXTERNAL_API_BASE_URL = os.getenv("EXTERNAL_API_BASE_URL", "")
    EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")
    
    @classmethod
    def get_repository_config(cls) -> Dict[str, Any]:
        """Retorna la configuración del repositorio"""
        return {
            "type": cls.REPOSITORY_TYPE,
            "database_url": cls.DATABASE_URL,
            "external_api_url": cls.EXTERNAL_API_BASE_URL,
            "external_api_key": cls.EXTERNAL_API_KEY
        }
    
    @classmethod
    def is_mock_repository(cls) -> bool:
        """Verifica si se está usando el repositorio mock"""
        return cls.REPOSITORY_TYPE == "mock"
    
    @classmethod
    def is_database_repository(cls) -> bool:
        """Verifica si se está usando el repositorio de base de datos"""
        return cls.REPOSITORY_TYPE == "database"
    
    @classmethod
    def is_api_repository(cls) -> bool:
        """Verifica si se está usando el repositorio de API externa"""
        return cls.REPOSITORY_TYPE == "api"

