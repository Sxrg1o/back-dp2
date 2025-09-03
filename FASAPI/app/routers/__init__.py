"""API routers."""

from fastapi import APIRouter

from app.routers import mesas, pedidos, auth

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(mesas.router, prefix="/mesas", tags=["mesas"])
api_router.include_router(pedidos.router, prefix="/pedidos", tags=["pedidos"])