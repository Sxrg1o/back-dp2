"""
Endpoints para sincronización con sistema externo Domotica INC.

Este módulo proporciona rutas para recibir datos de sincronización del sistema Domotica
a través del scrapper, y procesarlos para actualizar la base de datos local.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from decimal import Decimal

from src.core.database import get_database_session
from src.api.schemas.scrapper_schemas import ProductoDomotica, MesaDomotica
from src.business_logic.menu.categoria_service import CategoriaService
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import ProductoCreate, ProductoUpdate
from src.api.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate

# Configuración del logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sync", tags=["Sincronización"])


@router.post(
    "/platos",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar platos desde Domotica",
    description="Recibe datos de platos extraídos mediante scraping del sistema Domotica y los sincroniza con la base de datos local.",
)
async def sync_platos(
    productos_domotica: List[ProductoDomotica] = Body(...),
    session: AsyncSession = Depends(get_database_session),
) -> Dict[str, Any]:
    """
    Sincroniza los platos extraídos del sistema Domotica con la base de datos local.

    Realiza las siguientes operaciones:
    1. Obtiene todas las categorías y productos existentes
    2. Crea las categorías que no existen
    3. Actualiza o crea los productos según corresponda
    4. Marca como inactivos los productos que ya no existen en Domotica

    Parameters
    ----------
    productos_domotica : List[ProductoDomotica]
        Lista de productos extraídos del sistema Domotica
    session : AsyncSession
        Sesión de base de datos

    Returns
    -------
    Dict[str, Any]
        Resumen de la operación con contadores de elementos creados/actualizados

    Raises
    ------
    HTTPException
        Si ocurre un error durante el proceso de sincronización
    """
    try:
        # Inicializar servicios
        categoria_service = CategoriaService(session)
        producto_service = ProductoService(session)

        # Contadores para el reporte final
        resultados = {
            "categorias_creadas": 0,
            "categorias_actualizadas": 0,
            "productos_creados": 0,
            "productos_actualizados": 0,
            "productos_desactivados": 0,
        }

        # 1. Obtener todas las categorías existentes (activas) por nombre
        categorias_response = await categoria_service.get_categorias(skip=0, limit=1000)
        # Crear un diccionario con pares nombre:id_categoria para la creación de productos
        categorias_dict = {}
        for categoria in categorias_response.items:
            categorias_dict[categoria.nombre] = categoria

        # 2. Obtener todos los productos existentes (activos) por nombre
        productos_response = await producto_service.get_productos(skip=0, limit=10000)
        productos_dict = {
            producto.nombre: producto for producto in productos_response.items
        }

        # Conjunto para rastrear qué productos se procesaron
        productos_procesados = set()

        # Procesar por categoría para mantener la relación
        categorias_vistas = set()

        for producto_domotica in productos_domotica:
            # Procesar la categoría si es nueva
            nombre_categoria = producto_domotica.categoria
            categorias_vistas.add(nombre_categoria)

            if nombre_categoria not in categorias_dict:
                # Crear la categoría
                nueva_categoria = CategoriaCreate(
                    nombre=nombre_categoria,
                    descripcion=f"Categoría importada desde Domotica: {nombre_categoria}",
                )
                categoria_creada = await categoria_service.create_categoria(
                    nueva_categoria
                )
                # Usar el ID de la categoría creada para futuros productos
                categorias_dict[nombre_categoria] = categoria_creada
                resultados["categorias_creadas"] += 1
                logger.info(f"Categoría creada: {nombre_categoria}")

            # Procesar el producto
            nombre_producto = producto_domotica.nombre
            productos_procesados.add(nombre_producto)

            # Convertir precio de string a decimal
            try:
                precio = Decimal(producto_domotica.precio.replace(",", "."))
            except (ValueError, TypeError):
                precio = Decimal("0.0")
                logger.warning(
                    f"Error al convertir precio para '{nombre_producto}': {producto_domotica.precio}"
                )

            # Convertir stock de string a booleano de disponibilidad
            try:
                disponible = (
                    producto_domotica.stock.lower() != "agotado"
                    and producto_domotica.stock.strip() != "0"
                )
            except (AttributeError, ValueError):
                disponible = True

            if nombre_producto in productos_dict:
                # Actualizar producto existente
                producto_existente = productos_dict[nombre_producto]

                producto_update = ProductoUpdate(
                    id_categoria=categorias_dict[nombre_categoria].id,
                    precio_base=precio,
                )

                await producto_service.update_producto(
                    producto_existente.id, producto_update
                )
                resultados["productos_actualizados"] += 1
                logger.info(f"Producto actualizado: {nombre_producto}")
            else:
                # Crear nuevo producto
                nuevo_producto = ProductoCreate(
                    nombre=nombre_producto,
                    id_categoria=categorias_dict[nombre_categoria].id,
                    precio_base=precio,
                    descripcion=f"Producto importado desde Domotica: {nombre_producto}",
                    # La disponibilidad se maneja por otro campo o endpoint
                )

                await producto_service.create_producto(nuevo_producto)
                resultados["productos_creados"] += 1
                logger.info(f"Producto creado: {nombre_producto}")

        # Desactivar productos que no estuvieron en la actualización
        productos_a_desactivar = [
            producto.id
            for producto in productos_response.items
            if producto.nombre not in productos_procesados
        ]

        for producto_id in productos_a_desactivar:
            await producto_service.update_producto(
                producto_id, ProductoUpdate(disponible=False)
            )
            resultados["productos_desactivados"] += 1

        # Actualizar estado de categorías según presencia en la sincronización
        categorias_a_desactivar = [
            categoria.id
            for categoria in categorias_response.items
            if categoria.nombre not in categorias_vistas
        ]

        for categoria_id in categorias_a_desactivar:
            # Nota: Según el comentario, activo se maneja por endpoint separado en el schema
            # así que esta parte debería usar otro método o una lógica diferente
            # Por ahora lo dejamos para futuras implementaciones
            pass

        return {
            "status": "success",
            "message": "Sincronización completada correctamente",
            "resultados": resultados,
        }

    except Exception as e:
        logger.exception(f"Error durante la sincronización de platos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la sincronización: {str(e)}",
        )


@router.post(
    "/mesas",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar mesas desde Domotica",
    description="Recibe datos de mesas extraídos mediante scraping del sistema Domotica.",
)
async def sync_mesas(
    mesas_domotica: List[MesaDomotica] = Body(...),
    session: AsyncSession = Depends(get_database_session),
) -> Dict[str, Any]:
    """
    Recibe y registra las mesas extraídas del sistema Domotica.

    Actualmente solo confirma la recepción de los datos sin procesamiento adicional.

    Parameters
    ----------
    mesas_domotica : List[MesaDomotica]
        Lista de mesas extraídas del sistema Domotica
    session : AsyncSession
        Sesión de base de datos

    Returns
    -------
    Dict[str, Any]
        Confirmación de recepción y conteo de mesas recibidas

    Raises
    ------
    HTTPException
        Si ocurre un error durante el proceso
    """
    try:
        # Por ahora solo registramos que recibimos las mesas
        mesas_count = len(mesas_domotica)

        # Aquí podrías agregar el código para procesar las mesas en el futuro

        return {
            "status": "success",
            "message": "Datos de mesas recibidos correctamente",
            "mesas_recibidas": mesas_count,
            "mesas": [mesa.model_dump() for mesa in mesas_domotica],
        }

    except Exception as e:
        logger.exception(f"Error durante la sincronización de mesas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la sincronización: {str(e)}",
        )
