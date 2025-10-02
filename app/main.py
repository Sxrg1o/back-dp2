from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel

from app.models.menu_y_carta.domain import Item, Plato, Bebida, Categoria
from app.models.gestion_pedidos.domain import Orden, ItemOrden, Mesero, GrupoMesa, ResumenOrden, EstadisticasPedidos
from app.models.gestion_pedidos.enums import EstadoOrden, TipoMesa
from app.models.gestion_pedidos.dto import (
    CrearOrdenRequest, AgregarItemOrdenRequest, ModificarItemOrdenRequest,
    CambiarEstadoOrdenRequest, AsignarMeseroRequest, CrearMeseroRequest,
    CrearGrupoMesaRequest, FiltrarOrdenesRequest,
    OrdenResponse, ItemOrdenResponse, ResumenOrdenResponse, MeseroResponse,
    GrupoMesaResponse, EstadisticasPedidosResponse, ValidacionDisponibilidadResponse,
    ListaOrdenesResponse, ListaMeserosResponse, ListaMesasResponse
)
from app.services.menu_service import MenuService
from app.services.pedidos_service import PedidosService

# Inicializar FastAPI
app = FastAPI(
    title="Menu API - Sistema de Gestión de Menú y Carta",
    description="API para gestión completa del menú, platos, bebidas e ingredientes",
    version="1.0.0"
)

# Inicializar servicios
menu_service = MenuService()
pedidos_service = PedidosService()

# =========================
# DTOs para respuestas
# =========================
class ItemResponse(BaseModel):
    id: int
    nombre: str
    imagen: str
    precio: float
    stock: int
    disponible: bool
    categoria: str
    alergenos: List[str]
    tiempo_preparacion: float
    descripcion: str
    ingredientes: List[str]
    grupo_personalizacion: Optional[Dict] = None
    tipo_item: str

class PlatoResponse(ItemResponse):
    peso: float
    tipo: str

class BebidaResponse(ItemResponse):
    litros: float
    con_alcohol: bool

# IngredienteResponse eliminado - ahora se usan strings directamente

class CategoriaResponse(BaseModel):
    nombre: str
    descripcion: str

class MenuCompletoResponse(BaseModel):
    entradas: List[PlatoResponse]
    platos_principales: List[PlatoResponse]
    postres: List[PlatoResponse]
    bebidas_sin_alcohol: List[BebidaResponse]
    bebidas_con_alcohol: List[BebidaResponse]

class EstadisticasMenuResponse(BaseModel):
    total_items: int
    total_platos: int
    total_bebidas: int
    items_disponibles: int
    entradas: int
    platos_principales: int
    postres: int
    bebidas_sin_alcohol: int
    bebidas_con_alcohol: int

# =========================
# Endpoints principales
# =========================

@app.get("/", summary="Información de la API")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API de Gestión de Menú y Carta",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", summary="Health check")
def health_check():
    """Endpoint de health check"""
    return {"status": "ok", "message": "API funcionando correctamente"}

# =========================
# Endpoints de Items
# =========================

@app.get("/api/menu/items", response_model=List[ItemResponse], summary="Obtener todos los items")
def obtener_todos_los_items():
    """Obtiene todos los items del menú (platos y bebidas)"""
    items = menu_service.obtener_todos_los_items()
    return [convertir_item_a_response(item) for item in items.values()]

@app.get("/api/menu/items/disponibles", response_model=List[ItemResponse], summary="Obtener items disponibles")
def obtener_items_disponibles():
    """Obtiene solo los items que están disponibles y tienen stock"""
    items = menu_service.obtener_items_disponibles()
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/items/buscar", response_model=List[ItemResponse], summary="Buscar items por nombre")
def buscar_items_por_nombre(nombre: str = Query(..., description="Nombre a buscar")):
    """Busca items por nombre (búsqueda parcial)"""
    items = menu_service.buscar_items_por_nombre(nombre)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/items/{item_id}", response_model=ItemResponse, summary="Obtener item por ID")
def obtener_item_por_id(item_id: int):
    """Obtiene un item específico por su ID"""
    item = menu_service.obtener_item_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return convertir_item_a_response(item)

# =========================
# Endpoints de Platos
# =========================

@app.get("/api/menu/platos", response_model=List[PlatoResponse], summary="Obtener todos los platos")
def obtener_platos():
    """Obtiene todos los platos"""
    platos = menu_service.obtener_platos()
    return [convertir_plato_a_response(plato) for plato in platos]

@app.get("/api/menu/platos/entradas", response_model=List[PlatoResponse], summary="Obtener entradas")
def obtener_entradas():
    """Obtiene todas las entradas"""
    entradas = menu_service.obtener_entradas()
    return [convertir_plato_a_response(plato) for plato in entradas]

@app.get("/api/menu/platos/principales", response_model=List[PlatoResponse], summary="Obtener platos principales")
def obtener_platos_principales():
    """Obtiene todos los platos principales (fondos)"""
    platos = menu_service.obtener_platos_principales()
    return [convertir_plato_a_response(plato) for plato in platos]

@app.get("/api/menu/platos/postres", response_model=List[PlatoResponse], summary="Obtener postres")
def obtener_postres():
    """Obtiene todos los postres"""
    postres = menu_service.obtener_postres()
    return [convertir_plato_a_response(plato) for plato in postres]

@app.get("/api/menu/platos/tipo/{tipo}", response_model=List[PlatoResponse], summary="Obtener platos por tipo")
def obtener_platos_por_tipo(tipo: str):
    """Obtiene platos filtrados por tipo (ENTRADA, FONDO, POSTRE)"""
    platos = menu_service.obtener_platos_por_tipo(tipo)
    return [convertir_plato_a_response(plato) for plato in platos]

# =========================
# Endpoints de Bebidas
# =========================

@app.get("/api/menu/bebidas", response_model=List[BebidaResponse], summary="Obtener todas las bebidas")
def obtener_bebidas():
    """Obtiene todas las bebidas"""
    bebidas = menu_service.obtener_bebidas()
    return [convertir_bebida_a_response(bebida) for bebida in bebidas]

@app.get("/api/menu/bebidas/sin-alcohol", response_model=List[BebidaResponse], summary="Obtener bebidas sin alcohol")
def obtener_bebidas_sin_alcohol():
    """Obtiene bebidas sin alcohol"""
    bebidas = menu_service.obtener_bebidas_sin_alcohol()
    return [convertir_bebida_a_response(bebida) for bebida in bebidas]

@app.get("/api/menu/bebidas/con-alcohol", response_model=List[BebidaResponse], summary="Obtener bebidas con alcohol")
def obtener_bebidas_con_alcohol():
    """Obtiene bebidas con alcohol"""
    bebidas = menu_service.obtener_bebidas_con_alcohol()
    return [convertir_bebida_a_response(bebida) for bebida in bebidas]

# =========================
# Endpoints de Ingredientes
# =========================

@app.get("/api/menu/ingredientes", response_model=List[str], summary="Obtener todos los ingredientes")
def obtener_ingredientes():
    """Obtiene todos los ingredientes únicos de todos los items"""
    items = menu_service.obtener_todos_los_items()
    ingredientes_unicos = set()
    
    for item in items.values():
        ingredientes_unicos.update(item.ingredientes)
    
    return sorted(ingredientes_unicos)

@app.get("/api/menu/ingredientes/buscar", response_model=List[str], summary="Buscar ingredientes por nombre")
def buscar_ingredientes_por_nombre(nombre: str = Query(..., description="Nombre a buscar")):
    """Busca ingredientes por nombre"""
    ingredientes = menu_service.buscar_ingredientes_por_nombre(nombre)
    return ingredientes

# Endpoint eliminado - ya no hay IDs de ingredientes

# =========================
# Endpoints de Categorías
# =========================

@app.get("/api/menu/categorias", response_model=List[CategoriaResponse], summary="Obtener todas las categorías")
def obtener_categorias():
    """Obtiene todas las categorías disponibles"""
    categorias = menu_service.obtener_categorias()
    return [CategoriaResponse(nombre=cat.nombre, descripcion=cat.descripcion) for cat in categorias]

@app.get("/api/menu/categorias/{nombre_categoria}", response_model=CategoriaResponse, summary="Obtener categoría por nombre")
def obtener_categoria_por_nombre(nombre_categoria: str):
    """Obtiene una categoría específica por su nombre"""
    categoria = menu_service.obtener_categoria_por_nombre(nombre_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return CategoriaResponse(nombre=categoria.nombre, descripcion=categoria.descripcion)

# =========================
# Endpoints de Filtros
# =========================

@app.get("/api/menu/filtrar/categoria", response_model=List[ItemResponse], summary="Filtrar por categoría")
def filtrar_por_categoria(categoria: str = Query(..., description="Categoría a filtrar")):
    """Filtra items por categoría"""
    items = menu_service.filtrar_por_categoria(categoria)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/filtrar/alergenos", response_model=List[ItemResponse], summary="Filtrar por alérgenos")
def filtrar_por_alergenos(alergenos: str = Query(..., description="Alérgenos separados por coma")):
    """Filtra items que contengan los alérgenos especificados"""
    alergenos_list = [alergeno.strip().upper() for alergeno in alergenos.split(",")]
    items = menu_service.filtrar_por_alergenos(alergenos_list)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/filtrar/sin-alergenos", response_model=List[ItemResponse], summary="Filtrar sin alérgenos")
def filtrar_sin_alergenos(alergenos: str = Query(..., description="Alérgenos a excluir separados por coma")):
    """Filtra items que NO contengan los alérgenos especificados"""
    alergenos_list = [alergeno.strip().upper() for alergeno in alergenos.split(",")]
    items = menu_service.filtrar_sin_alergenos(alergenos_list)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/items/ingrediente/{ingrediente_nombre}", response_model=List[ItemResponse], summary="Obtener items por ingrediente")
def obtener_items_por_ingrediente(ingrediente_nombre: str):
    """Obtiene items que contengan un ingrediente específico"""
    items = menu_service.obtener_items_por_ingrediente(ingrediente_nombre)
    return [convertir_item_a_response(item) for item in items]

# =========================
# Endpoints de Menú Completo
# =========================

@app.get("/api/menu/completo", response_model=MenuCompletoResponse, summary="Obtener menú completo organizado")
def obtener_menu_completo():
    """Obtiene el menú completo organizado por categorías"""
    menu = menu_service.obtener_menu_completo_organizado()
    return MenuCompletoResponse(
        entradas=[convertir_plato_a_response(plato) for plato in menu["entradas"]],
        platos_principales=[convertir_plato_a_response(plato) for plato in menu["platos_principales"]],
        postres=[convertir_plato_a_response(plato) for plato in menu["postres"]],
        bebidas_sin_alcohol=[convertir_bebida_a_response(bebida) for bebida in menu["bebidas_sin_alcohol"]],
        bebidas_con_alcohol=[convertir_bebida_a_response(bebida) for bebida in menu["bebidas_con_alcohol"]]
    )

@app.get("/api/menu/estadisticas", response_model=EstadisticasMenuResponse, summary="Obtener estadísticas del menú")
def obtener_estadisticas_menu():
    """Obtiene estadísticas del menú"""
    stats = menu_service.obtener_estadisticas_menu()
    return EstadisticasMenuResponse(**stats)

# =========================
# Endpoints de Acompañamientos
# =========================

@app.get("/api/menu/items/{item_id}/acompanamientos", summary="Obtener acompañamientos de un item")
def obtener_acompanamientos_item(item_id: int):
    """Obtiene los acompañamientos disponibles para un item específico"""
    item = menu_service.obtener_item_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    if not item.grupo_personalizacion:
        return {
            "item_id": item_id,
            "item_nombre": item.nombre,
            "acompanamientos": [],
            "mensaje": "Este item no tiene acompañamientos disponibles"
        }
    
    # Filtrar solo acompañamientos del grupo de personalización
    acompanamientos = []
    if item.grupo_personalizacion.tipo == "acompanamiento":
        acompanamientos = [
            {
                "etiqueta": opcion.etiqueta,
                "precio_adicional": opcion.precio_adicional,
                "es_default": opcion.es_default,
                "seleccionado": opcion.seleccionado
            }
            for opcion in item.grupo_personalizacion.opciones
        ]
    
    return {
        "item_id": item_id,
        "item_nombre": item.nombre,
        "acompanamientos": acompanamientos,
        "max_selecciones": item.grupo_personalizacion.max_selecciones,
        "tipo_personalizacion": item.grupo_personalizacion.tipo
    }

@app.get("/api/menu/acompanamientos", summary="Obtener todos los acompañamientos disponibles")
def obtener_todos_acompanamientos():
    """Obtiene todos los acompañamientos disponibles en el menú"""
    items = menu_service.obtener_todos_los_items()
    acompanamientos_unicos = {}
    
    for item in items.values():
        if item.grupo_personalizacion and item.grupo_personalizacion.tipo == "acompanamiento":
            for opcion in item.grupo_personalizacion.opciones:
                if opcion.etiqueta not in acompanamientos_unicos:
                    acompanamientos_unicos[opcion.etiqueta] = {
                        "etiqueta": opcion.etiqueta,
                        "precio_adicional": opcion.precio_adicional,
                        "es_default": opcion.es_default,
                        "items_disponibles": []
                    }
                acompanamientos_unicos[opcion.etiqueta]["items_disponibles"].append({
                    "item_id": item.id,
                    "item_nombre": item.nombre
                })
    
    return {
        "acompanamientos": list(acompanamientos_unicos.values()),
        "total_acompanamientos": len(acompanamientos_unicos)
    }

# =========================
# Endpoints de Validación
# =========================

@app.get("/api/menu/validar-disponibilidad/{item_id}", summary="Validar disponibilidad de item")
def validar_disponibilidad_item(item_id: int, cantidad: int = Query(1, description="Cantidad a validar")):
    """Valida si un item está disponible en la cantidad solicitada"""
    disponible, mensaje = menu_service.verificar_disponibilidad_item(item_id, cantidad)
    return {
        "item_id": item_id,
        "cantidad": cantidad,
        "disponible": disponible,
        "mensaje": mensaje
    }

@app.post("/api/menu/validar-disponibilidad-multiple", summary="Validar disponibilidad de múltiples items")
def validar_disponibilidad_multiple(items: List[Dict]):
    """Valida la disponibilidad de múltiples items a la vez"""
    resultados = []
    todos_disponibles = True
    
    for item_data in items:
        item_id = item_data.get("item_id")
        cantidad = item_data.get("cantidad", 1)
        
        if not item_id:
            resultados.append({
                "item_id": None,
                "cantidad": cantidad,
                "disponible": False,
                "mensaje": "ID de item no proporcionado"
            })
            todos_disponibles = False
            continue
        
        disponible, mensaje = menu_service.verificar_disponibilidad_item(item_id, cantidad)
        resultados.append({
            "item_id": item_id,
            "cantidad": cantidad,
            "disponible": disponible,
            "mensaje": mensaje
        })
        
        if not disponible:
            todos_disponibles = False
    
    return {
        "todos_disponibles": todos_disponibles,
        "resultados": resultados,
        "total_items": len(items)
    }

# =========================
# Funciones auxiliares
# =========================

def convertir_item_a_response(item: Item) -> ItemResponse:
    """Convierte un Item a ItemResponse"""
    return ItemResponse(
        id=item.id,
        nombre=item.nombre,
        imagen=item.imagen,
        precio=item.precio,
        stock=item.stock,
        disponible=item.disponible,
        categoria=item.categoria.nombre,
        alergenos=item.alergenos,
        tiempo_preparacion=0.0,  # No está en el nuevo modelo
        descripcion=item.descripcion,
        ingredientes=item.ingredientes,
        grupo_personalizacion=convertir_grupo_personalizacion(item.grupo_personalizacion[0]) if item.grupo_personalizacion else None,
        tipo_item=item.get_tipo_item()
    )

def convertir_plato_a_response(plato: Plato) -> PlatoResponse:
    """Convierte un Plato a PlatoResponse"""
    base = convertir_item_a_response(plato)
    return PlatoResponse(
        **base.dict(),
        peso=plato.peso,
        tipo=plato.tipo.value
    )

def convertir_bebida_a_response(bebida: Bebida) -> BebidaResponse:
    """Convierte una Bebida a BebidaResponse"""
    base = convertir_item_a_response(bebida)
    return BebidaResponse(
        **base.dict(),
        litros=bebida.litros,
        con_alcohol=bebida.con_alcohol
    )

# Función eliminada - ya no hay clase Ingrediente

def convertir_grupo_personalizacion(grupo) -> Optional[Dict]:
    """Convierte un GrupoPersonalizacion a diccionario"""
    if not grupo:
        return None
    return {
        "etiqueta": grupo.etiqueta,
        "tipo": grupo.tipo,
        "max_selecciones": grupo.max_selecciones,
        "opciones": [
            {
                "etiqueta": opcion.etiqueta,
                "precio_adicional": opcion.precio_adicional,
                "es_default": opcion.es_default,
                "seleccionado": opcion.seleccionado
            }
            for opcion in grupo.opciones
        ]
    }

# =========================
# Endpoints de Gestión de Pedidos
# =========================

@app.post("/api/pedidos/ordenes", response_model=OrdenResponse, summary="Crear nueva orden")
def crear_orden(request: CrearOrdenRequest):
    """Crea una nueva orden de pedido"""
    orden = pedidos_service.crear_orden(
        mesa_id=request.mesa_id,
        comentarios=request.comentarios,
        mesero_ids=request.mesero_ids
    )
    return convertir_orden_a_response(orden)

@app.get("/api/pedidos/ordenes", response_model=ListaOrdenesResponse, summary="Obtener todas las órdenes")
def obtener_ordenes(estado: Optional[EstadoOrden] = None, mesa_id: Optional[int] = None, 
                   mesero_id: Optional[int] = None, pagina: int = 1, por_pagina: int = 10):
    """Obtiene todas las órdenes con filtros opcionales"""
    ordenes = pedidos_service.filtrar_ordenes(
        estado=estado,
        mesa_id=mesa_id,
        mesero_id=mesero_id
    )
    
    # Paginación simple
    inicio = (pagina - 1) * por_pagina
    fin = inicio + por_pagina
    ordenes_paginadas = ordenes[inicio:fin]
    
    resumenes = [convertir_resumen_orden_a_response(ResumenOrden(
        id=o.id,
        numero_orden=o.numero_orden,
        mesa_nombre=o.mesa.nombre if o.mesa else None,
        estado=o.estado.value,
        num_items=o.num_items,
        monto_total=o.monto_total,
        hora_registro=o.hora_registro,
        meseros_nombres=[m.nombre for m in o.meseros],
        tiempo_estimado=o.obtener_tiempo_estimado()
    )) for o in ordenes_paginadas]
    
    total_paginas = (len(ordenes) + por_pagina - 1) // por_pagina
    
    return ListaOrdenesResponse(
        ordenes=resumenes,
        total=len(ordenes),
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas
    )

@app.get("/api/pedidos/ordenes/{orden_id}", response_model=OrdenResponse, summary="Obtener orden por ID")
def obtener_orden_por_id(orden_id: int):
    """Obtiene una orden específica por su ID"""
    orden = pedidos_service.obtener_orden_por_id(orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return convertir_orden_a_response(orden)

@app.put("/api/pedidos/ordenes/{orden_id}/estado", summary="Cambiar estado de orden")
def cambiar_estado_orden(orden_id: int, request: CambiarEstadoOrdenRequest):
    """Cambia el estado de una orden"""
    if pedidos_service.cambiar_estado_orden(orden_id, request.nuevo_estado):
        return {"mensaje": f"Estado de orden {orden_id} cambiado a {request.nuevo_estado.value}"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo cambiar el estado de la orden")

@app.delete("/api/pedidos/ordenes/{orden_id}/cancelar", summary="Cancelar orden")
def cancelar_orden(orden_id: int, razon: str = ""):
    """Cancela una orden"""
    if pedidos_service.cancelar_orden(orden_id, razon):
        return {"mensaje": f"Orden {orden_id} cancelada exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo cancelar la orden")

@app.post("/api/pedidos/ordenes/{orden_id}/items", summary="Agregar item a orden")
def agregar_item_a_orden(orden_id: int, request: AgregarItemOrdenRequest):
    """Agrega un item a una orden existente"""
    if pedidos_service.agregar_item_a_orden(
        orden_id=orden_id,
        item_id=request.item_id,
        cantidad=request.cantidad,
        comentarios=request.comentarios,
        acompanamientos=request.acompanamientos,
        opciones_adicionales=request.opciones_adicionales
    ):
        return {"mensaje": "Item agregado a la orden exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo agregar el item a la orden")

@app.put("/api/pedidos/ordenes/{orden_id}/items/{item_orden_id}", summary="Modificar item en orden")
def modificar_item_orden(orden_id: int, item_orden_id: int, request: ModificarItemOrdenRequest):
    """Modifica un item en una orden existente"""
    if pedidos_service.modificar_item_orden(
        orden_id=orden_id,
        item_orden_id=item_orden_id,
        cantidad=request.cantidad,
        comentarios=request.comentarios
    ):
        return {"mensaje": "Item modificado exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo modificar el item")

@app.delete("/api/pedidos/ordenes/{orden_id}/items/{item_orden_id}", summary="Remover item de orden")
def remover_item_orden(orden_id: int, item_orden_id: int):
    """Remueve un item de una orden"""
    if pedidos_service.remover_item_orden(orden_id, item_orden_id):
        return {"mensaje": "Item removido de la orden exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo remover el item de la orden")

@app.get("/api/pedidos/ordenes/{orden_id}/validar-disponibilidad", response_model=ValidacionDisponibilidadResponse, summary="Validar disponibilidad de orden")
def validar_disponibilidad_orden(orden_id: int):
    """Valida la disponibilidad de todos los items de una orden"""
    todos_disponibles, items_no_disponibles = pedidos_service.validar_disponibilidad_orden(orden_id)
    
    return ValidacionDisponibilidadResponse(
        orden_id=orden_id,
        todos_disponibles=todos_disponibles,
        items_no_disponibles=items_no_disponibles,
        mensaje="Todos los items disponibles" if todos_disponibles else "Algunos items no están disponibles"
    )

# =========================
# Endpoints de Meseros
# =========================

@app.post("/api/pedidos/meseros", response_model=MeseroResponse, summary="Crear mesero")
def crear_mesero(request: CrearMeseroRequest):
    """Crea un nuevo mesero"""
    mesero = pedidos_service.crear_mesero(
        nombre=request.nombre,
        activo=request.activo
    )
    return convertir_mesero_a_response(mesero)

@app.get("/api/pedidos/meseros", response_model=ListaMeserosResponse, summary="Obtener todos los meseros")
def obtener_meseros():
    """Obtiene todos los meseros"""
    meseros = pedidos_service.obtener_todos_los_meseros()
    return ListaMeserosResponse(
        meseros=[convertir_mesero_a_response(m) for m in meseros],
        total=len(meseros)
    )

@app.get("/api/pedidos/meseros/{mesero_id}", response_model=MeseroResponse, summary="Obtener mesero por ID")
def obtener_mesero_por_id(mesero_id: int):
    """Obtiene un mesero específico por su ID"""
    mesero = pedidos_service.obtener_mesero_por_id(mesero_id)
    if not mesero:
        raise HTTPException(status_code=404, detail="Mesero no encontrado")
    return convertir_mesero_a_response(mesero)

@app.post("/api/pedidos/ordenes/{orden_id}/meseros", summary="Asignar mesero a orden")
def asignar_mesero_a_orden(orden_id: int, request: AsignarMeseroRequest):
    """Asigna un mesero a una orden"""
    if pedidos_service.asignar_mesero_a_orden(orden_id, request.mesero_id):
        return {"mensaje": "Mesero asignado a la orden exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo asignar el mesero a la orden")

# =========================
# Endpoints de Mesas
# =========================

@app.post("/api/pedidos/mesas", response_model=GrupoMesaResponse, summary="Crear grupo de mesa")
def crear_grupo_mesa(request: CrearGrupoMesaRequest):
    """Crea un nuevo grupo de mesa"""
    mesa = pedidos_service.crear_grupo_mesa(
        nombre=request.nombre,
        capacidad=request.capacidad,
        tipo=request.tipo,
        ubicacion=request.ubicacion
    )
    return convertir_grupo_mesa_a_response(mesa)

@app.get("/api/pedidos/mesas", response_model=ListaMesasResponse, summary="Obtener todas las mesas")
def obtener_mesas():
    """Obtiene todas las mesas"""
    mesas = pedidos_service.obtener_todas_las_mesas()
    return ListaMesasResponse(
        mesas=[convertir_grupo_mesa_a_response(m) for m in mesas],
        total=len(mesas)
    )

@app.get("/api/pedidos/mesas/disponibles", response_model=ListaMesasResponse, summary="Obtener mesas disponibles")
def obtener_mesas_disponibles():
    """Obtiene mesas que no tienen órdenes activas"""
    mesas = pedidos_service.obtener_mesas_disponibles()
    return ListaMesasResponse(
        mesas=[convertir_grupo_mesa_a_response(m) for m in mesas],
        total=len(mesas)
    )

@app.get("/api/pedidos/mesas/{mesa_id}", response_model=GrupoMesaResponse, summary="Obtener mesa por ID")
def obtener_mesa_por_id(mesa_id: int):
    """Obtiene una mesa específica por su ID"""
    mesa = pedidos_service.obtener_mesa_por_id(mesa_id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return convertir_grupo_mesa_a_response(mesa)

# =========================
# Endpoints de Estadísticas
# =========================

@app.get("/api/pedidos/estadisticas", response_model=EstadisticasPedidosResponse, summary="Obtener estadísticas de pedidos")
def obtener_estadisticas_pedidos():
    """Obtiene estadísticas de pedidos"""
    stats = pedidos_service.obtener_estadisticas_pedidos()
    return convertir_estadisticas_a_response(stats)

@app.get("/api/pedidos/resumen", response_model=List[ResumenOrdenResponse], summary="Obtener resumen de órdenes")
def obtener_resumen_ordenes():
    """Obtiene resumen de todas las órdenes"""
    resumenes = pedidos_service.obtener_resumen_ordenes()
    return [convertir_resumen_orden_a_response(r) for r in resumenes]

# =========================
# Funciones auxiliares para conversión
# =========================

def convertir_orden_a_response(orden: Orden) -> OrdenResponse:
    """Convierte una Orden a OrdenResponse"""
    return OrdenResponse(
        id=orden.id,
        numero_orden=orden.numero_orden,
        mesa=convertir_grupo_mesa_a_dict(orden.mesa) if orden.mesa else None,
        linea_pedidos=[convertir_item_orden_a_response(item) for item in orden.linea_pedidos],
        num_items=orden.num_items,
        monto_total=orden.monto_total,
        estado=orden.estado.value,
        comentarios=orden.comentarios,
        activo=orden.activo,
        hora_registro=orden.hora_registro,
        meseros=[convertir_mesero_a_dict(m) for m in orden.meseros],
        tiempo_estimado=orden.obtener_tiempo_estimado()
    )

def convertir_item_orden_a_response(item_orden: ItemOrden) -> ItemOrdenResponse:
    """Convierte un ItemOrden a ItemOrdenResponse"""
    return ItemOrdenResponse(
        id=item_orden.id,
        item_id=item_orden.item.id,
        item_nombre=item_orden.item.nombre,
        item_precio=item_orden.item.precio,
        cant_pedida=item_orden.cant_pedida,
        subtotal=item_orden.subtotal,
        comentarios=item_orden.comentarios,
        acompanamientos=[{"etiqueta": op.etiqueta, "precio_adicional": op.precio_adicional} for op in item_orden.acompanamientos],
        opciones_adicionales=[{"etiqueta": op.etiqueta, "precio_adicional": op.precio_adicional} for op in item_orden.opciones_adicionales]
    )

def convertir_resumen_orden_a_response(resumen: ResumenOrden) -> ResumenOrdenResponse:
    """Convierte un ResumenOrden a ResumenOrdenResponse"""
    return ResumenOrdenResponse(
        id=resumen.id,
        numero_orden=resumen.numero_orden,
        mesa_nombre=resumen.mesa_nombre,
        estado=resumen.estado,
        num_items=resumen.num_items,
        monto_total=resumen.monto_total,
        hora_registro=resumen.hora_registro,
        meseros_nombres=resumen.meseros_nombres,
        tiempo_estimado=resumen.tiempo_estimado
    )

def convertir_mesero_a_response(mesero: Mesero) -> MeseroResponse:
    """Convierte un Mesero a MeseroResponse"""
    return MeseroResponse(
        id=mesero.id,
        nombre=mesero.nombre,
        activo=mesero.activo,
        ordenes_count=len(mesero.ordenes)
    )

def convertir_mesero_a_dict(mesero: Mesero) -> Dict:
    """Convierte un Mesero a diccionario"""
    return {
        "id": mesero.id,
        "nombre": mesero.nombre,
        "activo": mesero.activo
    }

def convertir_grupo_mesa_a_response(mesa: GrupoMesa) -> GrupoMesaResponse:
    """Convierte un GrupoMesa a GrupoMesaResponse"""
    return GrupoMesaResponse(
        id=mesa.id,
        nombre=mesa.nombre,
        capacidad=mesa.capacidad,
        tipo=mesa.tipo.value,
        activa=mesa.activa,
        ubicacion=mesa.ubicacion
    )

def convertir_grupo_mesa_a_dict(mesa: GrupoMesa) -> Dict:
    """Convierte un GrupoMesa a diccionario"""
    return {
        "id": mesa.id,
        "nombre": mesa.nombre,
        "capacidad": mesa.capacidad,
        "tipo": mesa.tipo.value,
        "activa": mesa.activa,
        "ubicacion": mesa.ubicacion
    }

def convertir_estadisticas_a_response(stats: EstadisticasPedidos) -> EstadisticasPedidosResponse:
    """Convierte EstadisticasPedidos a EstadisticasPedidosResponse"""
    return EstadisticasPedidosResponse(
        total_ordenes=stats.total_ordenes,
        ordenes_en_cola=stats.ordenes_en_cola,
        ordenes_en_preparacion=stats.ordenes_en_preparacion,
        ordenes_listas=stats.ordenes_listas,
        ordenes_despachadas=stats.ordenes_despachadas,
        ordenes_canceladas=stats.ordenes_canceladas,
        monto_total_dia=stats.monto_total_dia,
        promedio_tiempo_preparacion=stats.promedio_tiempo_preparacion,
        items_mas_pedidos=stats.items_mas_pedidos
    )
