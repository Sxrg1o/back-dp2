"""
Endpoints específicos para las pantallas del cliente.
Organizados por flujo de pantallas del frontend.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.business_logic.menu.categoria_service import CategoriaService
from src.business_logic.menu.alergeno_service import AlergenoService
from src.business_logic.exceptions.base_exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/cliente", tags=["Cliente"])

# Service instances
categoria_service = CategoriaService()
alergeno_service = AlergenoService()


@router.get("/landing")
async def get_landing_page_data(
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Landing Page
    Datos que necesita la página de aterrizaje.
    Retorna: Lista de categorías para navegación inicial.
    """
    try:
        # Obtener categorías activas ordenadas
        categorias = await categoria_service.list_categorias(
            db=db,
            skip=0,
            limit=100,
            activo_only=True,
            order_by_orden=True
        )

        # Formato específico para landing page
        categorias_data = []
        for categoria in categorias:
            categorias_data.append({
                "id": categoria.id_categoria,
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion,
                "imagen_path": categoria.imagen_path,
                "orden": categoria.orden
            })

        return {
            "categorias": categorias_data,
            "total_categorias": len(categorias_data)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading landing page data: {str(e)}"
        )


@router.get("/home")
async def get_home_page_data(
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Home Page (Página de Inicio)
    Datos que necesita la página principal después del landing.
    Retorna: Categorías + productos con información básica.
    """
    try:
        # Obtener categorías activas
        categorias = await categoria_service.list_categorias(
            db=db,
            skip=0,
            limit=100,
            activo_only=True,
            order_by_orden=True
        )

        # Obtener alérgenos para filtros
        alergenos = await alergeno_service.list_alergenos(
            db=db,
            skip=0,
            limit=100,
            activo_only=True,
            order_by_orden=True
        )

        # Formato para categorías
        categorias_data = []
        for categoria in categorias:
            categorias_data.append({
                "id": categoria.id_categoria,
                "nombre": categoria.nombre,
                "descripcion": categoria.descripcion,
                "imagen_path": categoria.imagen_path,
                "orden": categoria.orden
            })

        # Formato para alérgenos (para filtros)
        alergenos_data = []
        for alergeno in alergenos:
            alergenos_data.append({
                "id": alergeno.id_alergeno,
                "nombre": alergeno.nombre,
                "icono": alergeno.icono,
                "nivel_riesgo": alergeno.nivel_riesgo
            })

        # TODO: Cuando implementes productos, agregar:
        # productos_destacados = await producto_service.get_featured_products(db, limit=6)

        return {
            "categorias": categorias_data,
            "alergenos_filtros": alergenos_data,
            "productos_destacados": [],  # TODO: Implementar cuando tengas productos
            "mensaje": "Datos para página de inicio cargados correctamente"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading home page data: {str(e)}"
        )


@router.get("/producto/detalle/{producto_id}")
async def get_product_detail(
    producto_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Detalle del Producto
    Datos que necesita la pantalla de detalle de un producto específico.
    Retorna: Información completa del producto + alérgenos + ingredientes.
    """
    try:
        # TODO: Cuando implementes productos, usar producto_service.get_by_id()

        # Por ahora devolver estructura mock basada en el producto_id
        producto_mock = {
            "id": producto_id,
            "nombre": f"Producto {producto_id}",
            "descripcion": "Descripción detallada del producto con todos sus ingredientes y preparación.",
            "precio_base": 25.50,
            "imagen_principal": f"/images/producto_{producto_id}.jpg",
            "imagenes_adicionales": [
                f"/images/producto_{producto_id}_1.jpg",
                f"/images/producto_{producto_id}_2.jpg"
            ],
            "categoria": {
                "id": 1,
                "nombre": "Platos Principales"
            },
            "alergenos": [
                {"id": 1, "nombre": "Gluten", "icono": "🌾", "nivel_riesgo": "alto"},
                {"id": 2, "nombre": "Lactosa", "icono": "🥛", "nivel_riesgo": "medio"}
            ],
            "ingredientes": ["Pollo", "Arroz", "Verduras", "Salsa especial"],
            "tiempo_preparacion": "15-20 minutos",
            "disponible": True,
            "stock": 10,
            "informacion_nutricional": {
                "calorias": 450,
                "proteinas": "25g",
                "carbohidratos": "35g",
                "grasas": "18g"
            },
            "tiene_personalizacion": True
        }

        return producto_mock

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading product detail: {str(e)}"
        )


@router.get("/producto/personalizacion/{producto_id}")
async def get_product_customization(
    producto_id: int,
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Personalización del Producto
    Datos que necesita la pantalla de personalización/opciones del producto.
    Retorna: Opciones de personalización + precios adicionales.
    """
    try:
        # TODO: Cuando implementes opciones de productos, usar option_service

        # Estructura mock de personalización
        personalizacion_mock = {
            "producto_id": producto_id,
            "producto_nombre": f"Producto {producto_id}",
            "precio_base": 25.50,
            "grupos_personalizacion": [
                {
                    "id": 1,
                    "etiqueta": "Nivel de Picante",
                    "tipo": "seleccion_unica",
                    "obligatorio": True,
                    "max_selecciones": 1,
                    "opciones": [
                        {"id": 1, "nombre": "Sin picante", "precio_adicional": 0.0},
                        {"id": 2, "nombre": "Poco picante", "precio_adicional": 0.0},
                        {"id": 3, "nombre": "Picante", "precio_adicional": 1.0},
                        {"id": 4, "nombre": "Muy picante", "precio_adicional": 2.0}
                    ]
                },
                {
                    "id": 2,
                    "etiqueta": "Acompañamientos",
                    "tipo": "seleccion_multiple",
                    "obligatorio": False,
                    "max_selecciones": 3,
                    "opciones": [
                        {"id": 5, "nombre": "Papas fritas", "precio_adicional": 3.0},
                        {"id": 6, "nombre": "Ensalada", "precio_adicional": 2.5},
                        {"id": 7, "nombre": "Arroz extra", "precio_adicional": 2.0},
                        {"id": 8, "nombre": "Yuca frita", "precio_adicional": 3.5}
                    ]
                },
                {
                    "id": 3,
                    "etiqueta": "Bebidas",
                    "tipo": "seleccion_unica",
                    "obligatorio": False,
                    "max_selecciones": 1,
                    "opciones": [
                        {"id": 9, "nombre": "Sin bebida", "precio_adicional": 0.0},
                        {"id": 10, "nombre": "Gaseosa", "precio_adicional": 4.0},
                        {"id": 11, "nombre": "Jugo natural", "precio_adicional": 5.0},
                        {"id": 12, "nombre": "Agua", "precio_adicional": 2.0}
                    ]
                }
            ]
        }

        return personalizacion_mock

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading product customization: {str(e)}"
        )


@router.post("/carrito/calcular-precio")
async def calculate_cart_item_price(
    item_data: dict,
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Carrito / Cálculo de precios
    Calcula el precio total de un item con sus personalizaciones.
    Recibe: producto_id, cantidad, opciones seleccionadas
    Retorna: Precio calculado con desglose.
    """
    try:
        producto_id = item_data.get("producto_id")
        cantidad = item_data.get("cantidad", 1)
        opciones_seleccionadas = item_data.get("opciones_seleccionadas", [])

        # TODO: Implementar cálculo real con base de datos
        precio_base = 25.50
        precio_opciones = sum([opcion.get("precio_adicional", 0) for opcion in opciones_seleccionadas])
        precio_unitario = precio_base + precio_opciones
        precio_total = precio_unitario * cantidad

        return {
            "producto_id": producto_id,
            "cantidad": cantidad,
            "precio_base": precio_base,
            "precio_opciones": precio_opciones,
            "precio_unitario": precio_unitario,
            "precio_total": precio_total,
            "desglose_opciones": opciones_seleccionadas
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating cart price: {str(e)}"
        )


@router.get("/carrito/resumen")
async def get_cart_summary(
    session_id: str = Query(..., description="ID de sesión del carrito"),
    db: AsyncSession = Depends(get_database_session)
):
    """
    PANTALLA: Carrito - Resumen
    Datos que necesita la pantalla del carrito de compras.
    Retorna: Items del carrito + totales + información de entrega.
    """
    try:
        # TODO: Implementar gestión real de carrito con session_id

        # Mock de carrito por ahora
        carrito_mock = {
            "session_id": session_id,
            "items": [
                {
                    "id": 1,
                    "producto_id": 1,
                    "producto_nombre": "Ceviche de Pescado",
                    "cantidad": 2,
                    "precio_unitario": 28.50,
                    "precio_total": 57.00,
                    "personalizaciones": [
                        {"nombre": "Picante", "precio": 1.0},
                        {"nombre": "Papas fritas", "precio": 3.0}
                    ],
                    "imagen": "/images/ceviche.jpg"
                },
                {
                    "id": 2,
                    "producto_id": 5,
                    "producto_nombre": "Arroz con Pollo",
                    "cantidad": 1,
                    "precio_unitario": 22.00,
                    "precio_total": 22.00,
                    "personalizaciones": [
                        {"nombre": "Sin picante", "precio": 0.0}
                    ],
                    "imagen": "/images/arroz_pollo.jpg"
                }
            ],
            "resumen": {
                "subtotal": 79.00,
                "impuestos": 7.90,
                "delivery": 5.00,
                "total": 91.90,
                "total_items": 3
            },
            "estimado_entrega": "25-35 minutos"
        }

        return carrito_mock

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading cart summary: {str(e)}"
        )