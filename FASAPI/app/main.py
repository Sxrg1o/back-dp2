"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import setup_logging
from app.infrastructure.web.controllers.menu_controller import router as menu_router
from app.infrastructure.web.controllers.item_controller import router as item_router
from app.infrastructure.web.controllers.bebida_controller import router as bebida_router
from app.infrastructure.web.controllers.ingrediente_controller import router as ingrediente_router
from app.infrastructure.web.controllers.plato_controller import router as plato_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging()

    yield

    # Shutdown
    # Add cleanup logic here if needed
    pass


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Backend archetype for restaurant platform",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add security middleware
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    # Set up exception handlers
    setup_exception_handlers(app)

    # Include routers from infrastructure layer
    app.include_router(menu_router, prefix=f"{settings.API_V1_STR}/menu", tags=["menu"])
    app.include_router(item_router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])
    app.include_router(bebida_router, prefix=f"{settings.API_V1_STR}/bebidas", tags=["bebidas"])
    app.include_router(ingrediente_router, prefix=f"{settings.API_V1_STR}/ingredientes", tags=["ingredientes"])
    app.include_router(plato_router, prefix=f"{settings.API_V1_STR}/platos", tags=["platos"])

    return app


# Create the application instance
app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }