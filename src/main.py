"""
Punto de entrada principal de la aplicación FastAPI.
"""

import importlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import create_tables, close_database
from src.core.config import get_settings
from src.core.logging import configure_logging
from src.core.dependencies import ErrorHandlerMiddleware


# Configurar logger para este módulo
logger = logging.getLogger(__name__)


async def auto_seed_database():
    """
    Ejecuta el seed de la base de datos automáticamente si está vacía.
    
    Verifica si existen categorías en la base de datos. Si no hay ninguna,
    ejecuta el script de seed para poblar la BD con datos iniciales.
    """
    try:
        import os
        from sqlalchemy import select, func
        from src.core.database import DatabaseManager
        from src.models.menu.categoria_model import CategoriaModel
        
        logger.info("🔍 Verificando estado de la base de datos...")
        
        # Obtener sesión de base de datos
        db_manager = DatabaseManager()
        async with db_manager.session() as session:
            # Contar categorías existentes
            query = select(func.count(CategoriaModel.id))
            result = await session.execute(query)
            count = result.scalar()
            
            logger.info(f"Categorías encontradas: {count}")
            logger.info(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'No configurada')}")
            
            if count == 0:
                logger.info("🌱 Base de datos vacía detectada. Ejecutando seed automático...")
                
                # Importar y ejecutar el seeder
                from scripts.seed_cevicheria_data import CevicheriaSeeder
                
                # Crear instancia del seeder CON la sesión
                seeder = CevicheriaSeeder(session)
                await seeder.seed_all()
                
                # Commit de los cambios
                await session.commit()
                
                logger.info("✅ Seed completado exitosamente!")
            else:
                logger.info(f"✅ Base de datos ya contiene datos ({count} categorías). Skip seed.")
            
    except Exception as e:
        import traceback
        logger.error(f"❌ Error al ejecutar auto-seed: {e}")
        logger.error(f"Stack trace completo:\n{traceback.format_exc()}")
        logger.warning("⚠️ La aplicación continuará sin datos de seed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación FastAPI.

    Controla los eventos de inicio y apagado de la aplicación,
    configurando recursos necesarios al inicio y liberándolos al finalizar.

    Parameters
    ----------
    app : FastAPI
        La instancia de la aplicación FastAPI

    Notes
    -----
    Este gestor se ejecuta en estas fases:
    1. Código de inicialización (antes de yield)
    2. Aplicación en funcionamiento (durante yield)
    3. Código de limpieza (después de yield)
    """
    # Fase de inicialización
    logger.info("Iniciando Restaurant Backend API...")

    # Configurar sistema de logging
    configure_logging()

    # Crear tablas en la base de datos si no existen
    await create_tables()
    
    # Pequeña espera para asegurar que las tablas estén completamente creadas
    import asyncio
    await asyncio.sleep(0.5)

    # Ejecutar seed automáticamente si la BD está vacía
    # await auto_seed_database()

    logger.info("Restaurant Backend API iniciada correctamente")

    yield  # La aplicación está en funcionamiento

    # Fase de limpieza
    logger.info("Cerrando Restaurant Backend API...")

    # Cerrar conexiones de base de datos
    await close_database()

    logger.info("Recursos liberados correctamente")


def register_routers(app: FastAPI) -> None:
    """
    Registra todos los routers de la aplicación.

    Carga dinámicamente los controladores disponibles y los registra
    con la aplicación FastAPI.

    Parameters
    ----------
    app : FastAPI
        La instancia de la aplicación FastAPI donde registrar los routers
    """
    # Estructura de controladores a cargar: (módulo, tag)
    controllers = [
        ("src.api.controllers.rol_controller", "Roles"),
        ("src.api.controllers.categoria_controller", "Categorías"),
        ("src.api.controllers.alergeno_controller", "Alérgenos"),
        ("src.api.controllers.producto_controller", "Productos"),
        ("src.api.controllers.tipo_opciones_controller", "Tipos de Opciones"),
        ("src.api.controllers.producto_opcion_controller", "Producto Opciones"),
        ("src.api.controllers.sync_controller", "Sincronización"),
        # ("src.api.controllers.usuarios_controller", "Usuarios"),
        # ("src.api.controllers.mesas_controller", "Mesas"),
        # ("src.api.controllers.pedidos_controller", "Pedidos"),
        # ("src.api.controllers.pagos_controller", "Pagos"),
    ]

    # Prefijo API común para todas las rutas
    api_prefix = "/api/v1"

    for module_name, tag in controllers:
        try:
            # Importar dinámicamente el módulo del controlador
            module = importlib.import_module(module_name)
            router = getattr(module, "router", None)

            if router and isinstance(router, APIRouter):
                # Registrar el router con la aplicación
                app.include_router(router, prefix=api_prefix, tags=[tag])
                logger.info(f"Router '{tag}' registrado correctamente")
            else:
                logger.warning(f"No se encontró un router válido en {module_name}")
        except Exception as e:
            logger.error(f"Error al cargar el controlador {module_name}: {e}")


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.

    Configura todos los aspectos de la aplicación FastAPI, incluyendo
    middlewares, gestión de excepciones y registro de rutas.

    Returns
    -------
    FastAPI
        Instancia configurada de la aplicación FastAPI
    """
    settings = get_settings()

    # Crear la instancia de FastAPI
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Agregar middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    # Agregar middleware para manejo de errores
    app.add_middleware(ErrorHandlerMiddleware)

    # Registrar todos los routers disponibles
    register_routers(app)

    # Registrar endpoints básicos
    @app.get("/")
    async def root():
        """
        Endpoint raíz de la API.

        Proporciona información básica sobre la API y enlaces a la documentación.

        Returns
        -------
        dict
            Información básica sobre la API
        """
        return {
            "message": "Restaurant Backend API",
            "version": settings.app_version,
            "environment": settings.environment,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health")
    async def health_check():
        """
        Endpoint de verificación de salud del sistema.

        Permite monitorizar el estado de la API para herramientas
        de supervisión y balanceadores de carga.

        Returns
        -------
        dict
            Estado actual del servicio
        """
        return {
            "status": "healthy",
            "service": "restaurant-backend",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    return app


# Crear la instancia de la aplicación
app = create_app()

# Punto de entrada para ejecución directa del script
if __name__ == "__main__":
    import uvicorn

    # Obtener configuración
    settings = get_settings()

    # Iniciar servidor uvicorn
    logger.info(f"Iniciando servidor en {settings.host}:{settings.port}")
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
