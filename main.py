"""
Main FastAPI application entry point.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_database, create_tables, get_settings
from app.config.logging import configure_logging
from app.presentation.middleware.error_middleware import ErrorHandlerMiddleware


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
    from app.presentation.api.v1.endpoints.usuarios import router as usuarios_router
    from app.presentation.api.v1.endpoints.roles import router as roles_router
    from app.presentation.api.v1.endpoints.alergenos import router as alergenos_router
    from app.presentation.api.v1.endpoints.categorias import router as categorias_router

    app.include_router(usuarios_router, prefix="/api/v1", tags=["Usuarios"])
    app.include_router(roles_router, prefix="/api/v1", tags=["Roles"])
    app.include_router(alergenos_router, prefix="/api/v1", tags=["Alergenos"])
    app.include_router(categorias_router, prefix="/api/v1", tags=["Categorias"])

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
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )