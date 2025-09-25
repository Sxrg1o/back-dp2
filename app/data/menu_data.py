from typing import Dict, List
from app.models.domain import Item, Plato, Bebida, Ingrediente, GrupoPersonalizacion, Opcion
from app.models.enums import EtiquetaPlato, TipoAlergeno

# =========================
# Catálogo de ingredientes
# =========================
INGREDIENTES: Dict[int, Ingrediente] = {
    1: Ingrediente(id=1, nombre="Pescado", categoria_alergeno=TipoAlergeno.PESCADO),
    2: Ingrediente(id=2, nombre="Limón", categoria_alergeno=None),
    3: Ingrediente(id=3, nombre="Cebolla", categoria_alergeno=None),
    4: Ingrediente(id=4, nombre="Arroz", categoria_alergeno=None),
    5: Ingrediente(id=5, nombre="Mariscos", categoria_alergeno=TipoAlergeno.MARISCOS),
    6: Ingrediente(id=6, nombre="Camarones", categoria_alergeno=TipoAlergeno.MARISCOS),
    7: Ingrediente(id=7, nombre="Pulpo", categoria_alergeno=TipoAlergeno.MOLUSCOS),
    8: Ingrediente(id=8, nombre="Ají", categoria_alergeno=None),
    9: Ingrediente(id=9, nombre="Cilantro", categoria_alergeno=None),
    10: Ingrediente(id=10, nombre="Ajo", categoria_alergeno=None),
    11: Ingrediente(id=11, nombre="Lomo de res", categoria_alergeno=None),
    12: Ingrediente(id=12, nombre="Tomate", categoria_alergeno=None),
    13: Ingrediente(id=13, nombre="Papas", categoria_alergeno=None),
    14: Ingrediente(id=14, nombre="Cebada", categoria_alergeno=TipoAlergeno.GLUTEN),
    15: Ingrediente(id=15, nombre="Lúpulo", categoria_alergeno=None),
}

# =========================
# Grupos de personalización
# =========================
def crear_grupo_acompanamientos() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        etiqueta="Acompañamientos",
        tipo="acompanamiento",
        opciones=[
            Opcion(etiqueta="Camote", precio_adicional=3.0, es_default=False),
            Opcion(etiqueta="Choclo", precio_adicional=2.5, es_default=False),
            Opcion(etiqueta="Papas fritas", precio_adicional=4.0, es_default=False),
            Opcion(etiqueta="Sin acompañamiento", precio_adicional=0.0, es_default=True),
        ],
        max_selecciones=2
    )

def crear_grupo_salsas() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        etiqueta="Salsas",
        tipo="salsa",
        opciones=[
            Opcion(etiqueta="Ají extra", precio_adicional=1.0, es_default=False),
            Opcion(etiqueta="Salsa de la casa", precio_adicional=1.5, es_default=False),
            Opcion(etiqueta="Cebolla extra", precio_adicional=0.5, es_default=False),
            Opcion(etiqueta="Sin salsas", precio_adicional=0.0, es_default=True),
        ],
        max_selecciones=3
    )

def crear_grupo_tamaño_bebida() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        etiqueta="Tamaño",
        tipo="tamaño",
        opciones=[
            Opcion(etiqueta="Pequeña (330ml)", precio_adicional=0.0, es_default=True),
            Opcion(etiqueta="Mediana (500ml)", precio_adicional=3.0, es_default=False),
            Opcion(etiqueta="Grande (750ml)", precio_adicional=5.0, es_default=False),
        ],
        max_selecciones=1
    )

# =========================
# Catálogo de platos
# =========================
PLATOS: Dict[int, Plato] = {
    1: Plato(
        id=1,
        nombre="Ceviche",
        imagen="https://example.com/ceviche.jpg",
        precio=28.0,
        stock=10,
        disponible=True,
        categoria="Plato principal",
        alergenos="Pescado",
        tiempo_preparacion=10.0,
        descripcion="Clásico ceviche peruano con pescado fresco marinado en limón",
        ingredientes=[INGREDIENTES[1], INGREDIENTES[2], INGREDIENTES[3], INGREDIENTES[8], INGREDIENTES[9]],
        grupo_personalizacion=crear_grupo_acompanamientos(),
        peso=350.0,
        tipo=EtiquetaPlato.FONDO
    ),
    2: Plato(
        id=2,
        nombre="Arroz con mariscos",
        imagen="https://example.com/arroz.jpg",
        precio=32.0,
        stock=4,
        disponible=True,
        categoria="Plato principal",
        alergenos="Mariscos, Moluscos",
        tiempo_preparacion=20.0,
        descripcion="Arroz con mariscos mixtos y salsa criolla",
        ingredientes=[INGREDIENTES[4], INGREDIENTES[5], INGREDIENTES[6], INGREDIENTES[7], INGREDIENTES[3], INGREDIENTES[10]],
        grupo_personalizacion=crear_grupo_salsas(),
        peso=450.0,
        tipo=EtiquetaPlato.FONDO
    ),
    3: Plato(
        id=3,
        nombre="Lomo saltado",
        imagen="https://example.com/lomo.jpg",
        precio=35.0,
        stock=8,
        disponible=True,
        categoria="Plato principal",
        alergenos="",
        tiempo_preparacion=15.0,
        descripcion="Lomo de res salteado con cebolla, tomate y papas fritas",
        ingredientes=[INGREDIENTES[11], INGREDIENTES[3], INGREDIENTES[12], INGREDIENTES[13], INGREDIENTES[10]],
        grupo_personalizacion=crear_grupo_salsas(),
        peso=400.0,
        tipo=EtiquetaPlato.FONDO
    ),
    4: Plato(
        id=4,
        nombre="Causa limeña",
        imagen="https://example.com/causa.jpg",
        precio=18.0,
        stock=6,
        disponible=True,
        categoria="Entrada",
        alergenos="",
        tiempo_preparacion=8.0,
        descripcion="Causa limeña con pollo y palta",
        ingredientes=[INGREDIENTES[13], INGREDIENTES[3], INGREDIENTES[8]],
        grupo_personalizacion=crear_grupo_salsas(),
        peso=250.0,
        tipo=EtiquetaPlato.ENTRADA
    ),
    5: Plato(
        id=5,
        nombre="Suspiro limeño",
        imagen="https://example.com/suspiro.jpg",
        precio=12.0,
        stock=15,
        disponible=True,
        categoria="Postre",
        alergenos="Lácteos",
        tiempo_preparacion=5.0,
        descripcion="Postre tradicional peruano",
        ingredientes=[],
        grupo_personalizacion=None,
        peso=150.0,
        tipo=EtiquetaPlato.POSTRE
    ),
}

# =========================
# Catálogo de bebidas
# =========================
BEBIDAS: Dict[int, Bebida] = {
    6: Bebida(
        id=6,
        nombre="Cerveza artesanal",
        imagen="https://example.com/cerveza.jpg",
        precio=8.0,
        stock=20,
        disponible=True,
        categoria="Bebida alcohólica",
        alergenos="Gluten",
        tiempo_preparacion=2.0,
        descripcion="Cerveza artesanal peruana",
        ingredientes=[INGREDIENTES[14], INGREDIENTES[15]],
        grupo_personalizacion=crear_grupo_tamaño_bebida(),
        litros=0.5,
        con_alcohol=True
    ),
    7: Bebida(
        id=7,
        nombre="Chicha morada",
        imagen="https://example.com/chicha.jpg",
        precio=5.0,
        stock=25,
        disponible=True,
        categoria="Bebida sin alcohol",
        alergenos="",
        tiempo_preparacion=1.0,
        descripcion="Bebida tradicional peruana de maíz morado",
        ingredientes=[],
        grupo_personalizacion=crear_grupo_tamaño_bebida(),
        litros=0.5,
        con_alcohol=False
    ),
    8: Bebida(
        id=8,
        nombre="Inca Kola",
        imagen="https://example.com/inca.jpg",
        precio=4.0,
        stock=30,
        disponible=True,
        categoria="Bebida gaseosa",
        alergenos="",
        tiempo_preparacion=1.0,
        descripcion="Gaseosa peruana tradicional",
        ingredientes=[],
        grupo_personalizacion=crear_grupo_tamaño_bebida(),
        litros=0.5,
        con_alcohol=False
    ),
}

# =========================
# Catálogo unificado de items
# =========================
def obtener_todos_los_items() -> Dict[int, Item]:
    """Retorna todos los items (platos y bebidas) en un solo diccionario"""
    items = {}
    items.update(PLATOS)
    items.update(BEBIDAS)
    return items

def obtener_platos_por_tipo(tipo: EtiquetaPlato) -> List[Plato]:
    """Retorna platos filtrados por tipo"""
    return [plato for plato in PLATOS.values() if plato.tipo == tipo]

def obtener_bebidas_sin_alcohol() -> List[Bebida]:
    """Retorna bebidas sin alcohol"""
    return [bebida for bebida in BEBIDAS.values() if not bebida.con_alcohol]

def obtener_bebidas_con_alcohol() -> List[Bebida]:
    """Retorna bebidas con alcohol"""
    return [bebida for bebida in BEBIDAS.values() if bebida.con_alcohol]
