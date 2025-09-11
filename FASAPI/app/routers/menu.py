"""
Menu module router configuration.
"""
from fastapi import APIRouter

from app.infrastructure.web.controllers.menu_controller import router as menu_router
from app.infrastructure.web.controllers.item_controller import router as item_router
from app.infrastructure.web.controllers.ingrediente_controller import router as ingrediente_router
from app.infrastructure.web.controllers.plato_controller import router as plato_router
from app.infrastructure.web.controllers.bebida_controller import router as bebida_router

# Create main menu router
router = APIRouter()

# Include all menu-related sub-routers
router.include_router(menu_router)
router.include_router(item_router)
router.include_router(ingrediente_router)
router.include_router(plato_router)
router.include_router(bebida_router)