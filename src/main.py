"""
Main FastAPI application entry point.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import init_database, create_tables, get_settings
from src.core.logging import configure_logging
from src.core.dependencies import ErrorHandlerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    """
    # Startup
    print("Starting Restaurant Backend API...")

    # Configure logging
    configure_logging()

    # Initialize database
    init_database()

    # Create tables if they don't exist
    await create_tables()

    print("Restaurant Backend API started successfully")

    yield

    # Shutdown
    print("Shutting down Restaurant Backend API...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application
    """
    settings = get_settings()

    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    # Add error handling middleware
    app.add_middleware(ErrorHandlerMiddleware)

    # Include routers
    # Carga solo los routers que no tienen errores de importación
    try:
        from src.api.controllers.roles_controller import router as roles_router
        app.include_router(roles_router, prefix="/api/v1", tags=["Roles"])
    except Exception as e:
        print(f"Error loading roles_controller: {e}")

    # TODO: Revisar schemas faltantes en otros controladores
    # from src.api.controllers.usuarios_controller import router as usuarios_router
    # from src.api.controllers.alergenos_controller import router as alergenos_router
    # from src.api.controllers.categorias_controller import router as categorias_router
    # from src.api.controllers.cliente_controller import router as cliente_router

    # TODO: Add other routers when created
    # app.include_router(menu_router, prefix="/api/v1/menu", tags=["Menu"])
    # app.include_router(pedidos_router, prefix="/api/v1/pedidos", tags=["Orders"])

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Restaurant Backend API",
            "version": settings.app_version,
            "environment": settings.environment,
            "docs": "/docs",
            "redoc": "/redoc"
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "restaurant-backend",
            "version": settings.app_version,
            "environment": settings.environment
        }

    return app


# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )