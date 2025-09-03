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
from app.middlewares.request_id import RequestIdMiddleware
from app.middlewares.idempotency import IdempotencyMiddleware
from app.routers import api_router
from app.scheduler.setup import setup_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    setup_logging()
    if settings.SCHEDULER_ENABLED:
        setup_scheduler()
    
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
    
    # Add custom middlewares
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(IdempotencyMiddleware)

    # Set up exception handlers
    setup_exception_handlers(app)

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

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