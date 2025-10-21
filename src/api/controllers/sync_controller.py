"""
Endpoints para sincronización con sistema externo Domotica INC.

Este módulo proporciona rutas para recibir datos de sincronización del sistema Domotica
a través del scrapper, y procesarlos para actualizar la base de datos local.
"""

from typing import List, Dict, Any, Set, Tuple
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from decimal import Decimal

from src.core.database import get_database_session
from src.api.schemas.scrapper_schemas import ProductoDomotica, MesaDomotica
from src.business_logic.menu.categoria_service import CategoriaService
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoBase
from src.api.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate

# Configuración del logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sync", tags=["Sincronización"])


@router.post(
    "/platos",
    status_code=status.HTTP_200_OK,
    summary="Sincronizar platos desde Domotica",
    description="Recibe datos de platos extraídos mediante scraping del sistema Domotica y los sincroniza con la base de datos local utilizando operaciones por lotes para mejor rendimiento.",
)
async def sync_platos(
    productos_domotica: List[ProductoDomotica] = Body(...),
    session: AsyncSession = Depends(get_database_session),
) -> Dict[str, Any]:
    """
    Sincroniza los platos extraídos del sistema Domotica con la base de datos local.

    Realiza las siguientes operaciones:
    1. Obtiene todas las categorías y productos existentes
    2. Crea las categorías nuevas en lote
    3. Actualiza las categorías existentes en lote
    4. Crea los productos nuevos en lote
    5. Actualiza los productos existentes en lote
    6. Marca como inactivos los productos que ya no existen en Domotica

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

        categorias_response = await categoria_service.get_categorias(skip=0, limit=1000)
        categorias_dict = {
            categoria.nombre.upper(): categoria for categoria in categorias_response.items
        }
        productos_response = await producto_service.get_productos(skip=0, limit=10000)
        productos_dict = {
            producto.nombre: producto for producto in productos_response.items
        }

        categorias_a_crear: List[CategoriaCreate] = []
        productos_a_crear: List[ProductoCreate] = []
        productos_a_actualizar: List[Tuple[UUID, ProductoUpdate]] = []
        
        categorias_nuevas: Set[str] = set()
        
        for producto_domotica in productos_domotica:
            nombre_categoria = producto_domotica.categoria.upper()
            if nombre_categoria not in categorias_dict and nombre_categoria not in categorias_nuevas:
                nueva_categoria = CategoriaCreate(nombre=producto_domotica.categoria)
                categorias_a_crear.append(nueva_categoria)
                categorias_nuevas.add(nombre_categoria)
        
        categorias_creadas = await categoria_service.batch_create_categorias(categorias_a_crear)
        resultados["categorias_creadas"] += len(categorias_a_crear)
        
        # Actualizar el diccionario de categorías con las recién creadas
        for categoria in categorias_creadas:
            categorias_dict[categoria.nombre.upper()] = categoria

        # Procesar productos
        for producto_domotica in productos_domotica:
            # Convertir precio de string a decimal si es necesario
            try:
                precio = Decimal(producto_domotica.precio.replace(",", ".")) if isinstance(producto_domotica.precio, str) else producto_domotica.precio
            except (ValueError, TypeError):
                precio = Decimal("0.0")
                logger.warning(f"Error al convertir precio para '{producto_domotica.nombre}': {producto_domotica.precio}")
            
            if producto_domotica.nombre not in productos_dict:
                # Nuevo producto - preparamos el objeto ProductoCreate
                try:
                    # Intentar obtener la categoría
                    nombre_categoria = producto_domotica.categoria.upper()
                    if nombre_categoria in categorias_dict:
                        id_categoria = categorias_dict[nombre_categoria].id
                    else:
                        id_categoria = None
                    
                    if id_categoria:
                        nuevo_producto = ProductoCreate(
                            nombre=producto_domotica.nombre,
                            precio_base=precio,
                            descripcion=f"Producto importado desde Domotica: {producto_domotica.nombre}",
                            id_categoria=id_categoria
                        )
                        productos_a_crear.append(nuevo_producto)
                    else:
                        logger.warning(f"No se pudo crear el producto {producto_domotica.nombre} porque su categoría {producto_domotica.categoria} no existe")
                except Exception as e:
                    logger.error(f"Error preparando producto para crear: {str(e)}")
            else:
                # Producto existente - preparamos la tupla (id, ProductoUpdate) para actualización
                producto_existente = productos_dict[producto_domotica.nombre]
                try:
                    # Intentar obtener la categoría
                    nombre_categoria = producto_domotica.categoria.upper()
                    if nombre_categoria in categorias_dict:
                        id_categoria = categorias_dict[nombre_categoria].id
                    else:
                        id_categoria = None
                    
                    if id_categoria:
                        producto_actualizado = ProductoUpdate(
                            id_categoria=id_categoria,
                            precio_base=precio
                        )
                        productos_a_actualizar.append((producto_existente.id, producto_actualizado))
                    else:
                        logger.warning(f"No se pudo actualizar el producto {producto_domotica.nombre} porque su categoría {producto_domotica.categoria} no existe")
                except Exception as e:
                    logger.error(f"Error preparando producto para actualizar: {str(e)}")

        # Ejecutar operaciones en lote
        if productos_a_crear:
            try:
                productos_creados = await producto_service.batch_create_productos(productos_a_crear)
                resultados["productos_creados"] += len(productos_creados)
                logger.info(f"Productos creados en lote: {len(productos_creados)}")
            except Exception as e:
                logger.error(f"Error al crear productos en lote: {str(e)}")

        if productos_a_actualizar:
            try:
                productos_actualizados = await producto_service.batch_update_productos(productos_a_actualizar)
                resultados["productos_actualizados"] += len(productos_actualizados)
                logger.info(f"Productos actualizados en lote: {len(productos_actualizados)}")
            except Exception as e:
                logger.error(f"Error al actualizar productos en lote: {str(e)}")

        # Marcar productos inactivos
        productos_vistos = set(producto.nombre for producto in productos_domotica)
        productos_a_desactivar = []
        
        # Crear lista de tuplas (id, ProductoUpdate) para desactivar productos
        for nombre, producto in productos_dict.items():
            if nombre not in productos_vistos and producto.disponible:
                productos_a_desactivar.append((producto.id, ProductoUpdate(disponible=False)))
        
        if productos_a_desactivar:
            try:
                productos_desactivados = await producto_service.batch_update_productos(productos_a_desactivar)
                resultados["productos_desactivados"] += len(productos_desactivados)
                logger.info(f"Productos desactivados en lote: {len(productos_desactivados)}")
            except Exception as e:
                logger.error(f"Error al desactivar productos en lote: {str(e)}")

        return {
            "status": "success",
            "message": "Sincronización completada correctamente con operaciones por lotes",
            "resultados": resultados
        }

    except Exception as e:
        logger.exception(f"Error durante la sincronización de platos: {str(e)}")

        # Mensaje de error más informativo según el tipo de error
        error_message = str(e)
        if "ya exist" in error_message.lower():
            error_detail = "Uno o más elementos ya existen en la base de datos. Por favor revise los nombres de categorías y productos."
        elif "foreign key" in error_message.lower():
            error_detail = "Error de referencia: no se puede crear/actualizar un registro porque depende de otro que no existe."
        elif "timeout" in error_message.lower():
            error_detail = "Tiempo de espera agotado en la operación de base de datos."
        else:
            error_detail = f"Error durante la sincronización: {str(e)}"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
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
