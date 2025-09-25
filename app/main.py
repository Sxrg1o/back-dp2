from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel

from app.models.domain import Item, Plato, Bebida, Ingrediente
from app.models.enums import EtiquetaPlato, TipoAlergeno
from app.services.menu_service import MenuService

# Inicializar FastAPI
app = FastAPI(
    title="Menu API - Sistema de Gestión de Menú y Carta",
    description="API para gestión completa del menú, platos, bebidas e ingredientes",
    version="1.0.0"
)

# Inicializar servicio de menú
menu_service = MenuService()

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
    alergenos: str
    tiempo_preparacion: float
    descripcion: str
    ingredientes: List[Dict]
    grupo_personalizacion: Optional[Dict] = None
    tipo_item: str

class PlatoResponse(ItemResponse):
    peso: float
    tipo: str

class BebidaResponse(ItemResponse):
    litros: float
    con_alcohol: bool

class IngredienteResponse(BaseModel):
    id: int
    nombre: str
    categoria_alergeno: Optional[str] = None

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

@app.get("/api/menu/items/{item_id}", response_model=ItemResponse, summary="Obtener item por ID")
def obtener_item_por_id(item_id: int):
    """Obtiene un item específico por su ID"""
    item = menu_service.obtener_item_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return convertir_item_a_response(item)

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
def obtener_platos_por_tipo(tipo: EtiquetaPlato):
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

@app.get("/api/menu/ingredientes", response_model=List[IngredienteResponse], summary="Obtener todos los ingredientes")
def obtener_ingredientes():
    """Obtiene todos los ingredientes"""
    ingredientes = menu_service.obtener_ingredientes()
    return [convertir_ingrediente_a_response(ing) for ing in ingredientes]

@app.get("/api/menu/ingredientes/{ingrediente_id}", response_model=IngredienteResponse, summary="Obtener ingrediente por ID")
def obtener_ingrediente_por_id(ingrediente_id: int):
    """Obtiene un ingrediente específico por su ID"""
    ingrediente = menu_service.obtener_ingrediente_por_id(ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return convertir_ingrediente_a_response(ingrediente)

@app.get("/api/menu/ingredientes/buscar", response_model=List[IngredienteResponse], summary="Buscar ingredientes por nombre")
def buscar_ingredientes_por_nombre(nombre: str = Query(..., description="Nombre a buscar")):
    """Busca ingredientes por nombre"""
    ingredientes = menu_service.buscar_ingredientes_por_nombre(nombre)
    return [convertir_ingrediente_a_response(ing) for ing in ingredientes]

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
    alergenos_list = [TipoAlergeno(alergeno.strip().upper()) for alergeno in alergenos.split(",")]
    items = menu_service.filtrar_por_alergenos(alergenos_list)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/filtrar/sin-alergenos", response_model=List[ItemResponse], summary="Filtrar sin alérgenos")
def filtrar_sin_alergenos(alergenos: str = Query(..., description="Alérgenos a excluir separados por coma")):
    """Filtra items que NO contengan los alérgenos especificados"""
    alergenos_list = [TipoAlergeno(alergeno.strip().upper()) for alergeno in alergenos.split(",")]
    items = menu_service.filtrar_sin_alergenos(alergenos_list)
    return [convertir_item_a_response(item) for item in items]

@app.get("/api/menu/items/ingrediente/{ingrediente_id}", response_model=List[ItemResponse], summary="Obtener items por ingrediente")
def obtener_items_por_ingrediente(ingrediente_id: int):
    """Obtiene items que contengan un ingrediente específico"""
    items = menu_service.obtener_items_por_ingrediente(ingrediente_id)
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
        categoria=item.categoria,
        alergenos=item.alergenos,
        tiempo_preparacion=item.tiempo_preparacion,
        descripcion=item.descripcion,
        ingredientes=[{"id": ing.id, "nombre": ing.nombre, "categoria_alergeno": ing.categoria_alergeno.value if ing.categoria_alergeno else None} for ing in item.ingredientes],
        grupo_personalizacion=convertir_grupo_personalizacion(item.grupo_personalizacion) if item.grupo_personalizacion else None,
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

def convertir_ingrediente_a_response(ingrediente: Ingrediente) -> IngredienteResponse:
    """Convierte un Ingrediente a IngredienteResponse"""
    return IngredienteResponse(
        id=ingrediente.id,
        nombre=ingrediente.nombre,
        categoria_alergeno=ingrediente.categoria_alergeno.value if ingrediente.categoria_alergeno else None
    )

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
