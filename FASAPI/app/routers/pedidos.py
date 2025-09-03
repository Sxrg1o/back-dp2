"""
Pedido (Order) API endpoints.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_pedidos():
    """Get pedidos - placeholder endpoint."""
    return {"message": "Pedidos endpoint - to be implemented"}


@router.post("/")
async def create_pedido():
    """Create pedido - placeholder endpoint."""
    return {"message": "Create pedido endpoint - to be implemented"}