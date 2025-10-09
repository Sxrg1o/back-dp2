"""
Endpoints para sincronización con sistema externo Domotica INC.

Este módulo proporciona rutas para recibir datos de sincronización del sistema Domotica
a través del scrapper, y procesarlos para actualizar la base de datos local.
"""

from typing import List, Dict, Any, Tuple
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

        # 1. Obtener todas las categorías existentes (activas) por nombre
        categorias_response = await categoria_service.get_categorias(skip=0, limit=1000)
        # Crear un diccionario con pares nombre:categoria para la creación de productos
        categorias_dict = {
            categoria.nombre: categoria for categoria in categorias_response.items
        }

        # 2. Obtener todos los productos existentes (activos) por nombre
        productos_response = await producto_service.get_productos(skip=0, limit=10000)
        productos_dict = {
            producto.nombre: producto for producto in productos_response.items
        }

        # Conjunto para rastrear qué productos se procesaron
        productos_procesados = set()

        # Preparar colecciones para operaciones en lote
        categorias_a_crear = []
        productos_a_crear = []
        productos_a_actualizar = []

        # Procesar por categoría para mantener la relación
        categorias_vistas = set()

        # Procesamos primero las categorías
        categorias_nuevas = set()

        # Primera pasada: identificar categorías nuevas y productos vistos
        for producto_domotica in productos_domotica:
            nombre_categoria = producto_domotica.categoria
            categorias_vistas.add(nombre_categoria)
            nombre_producto = producto_domotica.nombre
            productos_procesados.add(nombre_producto)

            # Identificar categorías nuevas
            if (
                nombre_categoria not in categorias_dict
                and nombre_categoria not in categorias_nuevas
            ):
                categorias_nuevas.add(nombre_categoria)
                nueva_categoria = CategoriaCreate(
                    nombre=nombre_categoria,
                    descripcion=f"Categoría importada desde Domotica: {nombre_categoria}",
                )
                categorias_a_crear.append(nueva_categoria)

        # Crear categorías nuevas en lote (solo las que no existen)
        if categorias_a_crear:
            try:
                categorias_creadas = await categoria_service.batch_create_categorias(
                    categorias_a_crear
                )
                resultados["categorias_creadas"] += len(categorias_creadas)
                logger.info(f"Categorías creadas en lote: {len(categorias_creadas)}")
            except Exception as e:
                logger.error(f"Error al crear categorías en lote: {str(e)}")
                # Enfoque alternativo: crear categorías una por una para evitar problemas con duplicados
                for nueva_categoria in categorias_a_crear:
                    try:
                        if nueva_categoria.nombre not in categorias_dict:
                            categoria_creada = await categoria_service.create_categoria(
                                nueva_categoria
                            )
                            resultados["categorias_creadas"] += 1
                            # No añadimos al diccionario, esperamos a la recarga completa
                            logger.info(
                                f"Categoría creada individualmente: {nueva_categoria.nombre}"
                            )
                    except Exception as e_inner:
                        logger.warning(
                            f"No se pudo crear la categoría {nueva_categoria.nombre}: {str(e_inner)}"
                        )
                        # La categoría probablemente ya existe, la obtendremos más adelante

            # Obtener categorías actualizadas para asegurar la consistencia de tipos
            categorias_response = await categoria_service.get_categorias(
                skip=0, limit=1000
            )
            categorias_dict = {
                categoria.nombre: categoria for categoria in categorias_response.items
            }

        # Segunda pasada: procesar productos
        for producto_domotica in productos_domotica:
            nombre_categoria = producto_domotica.categoria
            nombre_producto = producto_domotica.nombre

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
                # Producto existente: preparar para actualización en lote
                producto_existente = productos_dict[nombre_producto]
                productos_a_actualizar.append(
                    (
                        producto_existente.id,
                        ProductoUpdate(
                            id_categoria=categorias_dict[nombre_categoria].id,
                            precio_base=precio,
                            disponible=disponible,
                        ),
                    )
                )
            else:
                # Producto nuevo: preparar para creación en lote
                nuevo_producto = ProductoCreate(
                    nombre=nombre_producto,
                    id_categoria=categorias_dict[nombre_categoria].id,
                    precio_base=precio,
                    descripcion=f"Producto importado desde Domotica: {nombre_producto}",
                    # La disponibilidad se maneja por otro campo en el modelo de datos
                )
                productos_a_crear.append(nuevo_producto)

        # Ejecutar operaciones en lote
        if productos_a_crear:
            try:
                productos_creados = await producto_service.batch_create_productos(
                    productos_a_crear
                )
                resultados["productos_creados"] += len(productos_creados)
                logger.info(f"Productos creados en lote: {len(productos_creados)}")
            except Exception as e:
                logger.error(f"Error al crear productos en lote: {str(e)}")
                # Enfoque alternativo: crear productos uno por uno para evitar problemas con duplicados
                for nuevo_producto in productos_a_crear:
                    try:
                        producto_creado = await producto_service.create_producto(
                            nuevo_producto
                        )
                        resultados["productos_creados"] += 1
                        logger.info(
                            f"Producto creado individualmente: {nuevo_producto.nombre}"
                        )
                    except Exception as e_inner:
                        logger.warning(
                            f"No se pudo crear el producto {nuevo_producto.nombre}: {str(e_inner)}"
                        )
                        # Puede que el producto ya exista pero no esté en nuestro diccionario inicial
                        # Intentamos obtener por nombre y actualizar si existe
                        try:
                            # Obtenemos todos los productos nuevamente para buscar
                            productos_response = await producto_service.get_productos(
                                skip=0, limit=10000
                            )
                            productos_encontrados = [
                                p
                                for p in productos_response.items
                                if p.nombre == nuevo_producto.nombre
                            ]

                            if productos_encontrados:
                                producto_existente = productos_encontrados[0]
                                await producto_service.update_producto(
                                    producto_existente.id,
                                    ProductoUpdate(
                                        id_categoria=nuevo_producto.id_categoria,
                                        precio_base=nuevo_producto.precio_base,
                                    ),
                                )
                                resultados["productos_actualizados"] += 1
                                logger.info(
                                    f"Producto actualizado tras fallo de creación: {nuevo_producto.nombre}"
                                )
                        except Exception as e_recover:
                            logger.error(
                                f"Error en la recuperación del producto {nuevo_producto.nombre}: {str(e_recover)}"
                            )

        if productos_a_actualizar:
            try:
                productos_actualizados = await producto_service.batch_update_productos(
                    productos_a_actualizar
                )
                resultados["productos_actualizados"] += len(productos_actualizados)
                logger.info(
                    f"Productos actualizados en lote: {len(productos_actualizados)}"
                )
            except Exception as e:
                logger.error(f"Error al actualizar productos en lote: {str(e)}")
                # Enfoque alternativo: actualizar productos uno por uno
                for producto_id, producto_data in productos_a_actualizar:
                    try:
                        await producto_service.update_producto(
                            producto_id, producto_data
                        )
                        resultados["productos_actualizados"] += 1
                    except Exception as e_inner:
                        logger.warning(
                            f"Error al actualizar producto ID {producto_id}: {str(e_inner)}"
                        )

        # Desactivar productos que no estuvieron en la actualización
        productos_a_desactivar = [
            (producto.id, ProductoUpdate(disponible=False))
            for producto in productos_response.items
            if producto.nombre not in productos_procesados
            and producto.disponible  # Solo desactivamos los que están activos
        ]

        if productos_a_desactivar:
            try:
                productos_desactivados = await producto_service.batch_update_productos(
                    productos_a_desactivar
                )
                resultados["productos_desactivados"] += len(productos_desactivados)
                logger.info(
                    f"Productos desactivados en lote: {len(productos_desactivados)}"
                )
            except Exception as e:
                logger.error(f"Error al desactivar productos en lote: {str(e)}")
                # Enfoque alternativo: desactivar productos uno por uno
                for producto_id, _ in productos_a_desactivar:
                    try:
                        await producto_service.update_producto(
                            producto_id, ProductoUpdate(disponible=False)
                        )
                        resultados["productos_desactivados"] += 1
                    except Exception as e_inner:
                        logger.warning(
                            f"Error al desactivar producto ID {producto_id}: {str(e_inner)}"
                        )

        # Actualizar estado de categorías según presencia en la sincronización
        categorias_a_desactivar = [
            categoria.id
            for categoria in categorias_response.items
            if categoria.nombre not in categorias_vistas
        ]

        # Nota: Actualmente la desactivación de categorías no está implementada
        # ya que según el comentario original, esto se maneja por un endpoint separado
        # Para futuras implementaciones, podría usarse batch_update_categorias

        return {
            "status": "success",
            "message": "Sincronización completada correctamente con operaciones por lotes",
            "resultados": resultados,
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
