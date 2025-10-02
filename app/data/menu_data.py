from typing import Dict, List, Optional
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Categoria, GrupoPersonalizacion, Opcion

# =========================
# Catálogo de categorías
# =========================
CATEGORIAS: Dict[str, Categoria] = {
    "entrada": Categoria(nombre="Entrada", descripcion="Platos para comenzar la comida"),
    "plato_principal": Categoria(nombre="Plato Principal", descripcion="Platos principales del menú"),
    "postre": Categoria(nombre="Postre", descripcion="Dulces para finalizar la comida"),
    "bebida_sin_alcohol": Categoria(nombre="Bebida Sin Alcohol", descripcion="Bebidas refrescantes"),
    "bebida_alcoholica": Categoria(nombre="Bebida Alcohólica", descripcion="Bebidas con contenido alcohólico"),
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
        categoria=CATEGORIAS["plato_principal"],
        alergenos=["PESCADO"],
        descripcion="Clásico ceviche peruano con pescado fresco marinado en limón",
        ingredientes=["Pescado", "Limón", "Cebolla", "Ají", "Cilantro"],
        grupo_personalizacion=[crear_grupo_acompanamientos()],
        peso=350.0,
        tipo="FONDO"
    ),
    2: Plato(
        id=2,
        nombre="Arroz con mariscos",
        imagen="https://example.com/arroz.jpg",
        precio=32.0,
        stock=4,
        disponible=True,
        categoria=CATEGORIAS["plato_principal"],
        alergenos=["MARISCOS", "MOLUSCOS"],
        descripcion="Arroz con mariscos mixtos y salsa criolla",
        ingredientes=["Arroz", "Mariscos", "Camarones", "Pulpo", "Cebolla", "Ajo"],
        grupo_personalizacion=[crear_grupo_salsas()],
        peso=450.0,
        tipo="FONDO"
    ),
    3: Plato(
        id=3,
        nombre="Lomo saltado",
        imagen="https://example.com/lomo.jpg",
        precio=35.0,
        stock=8,
        disponible=True,
        categoria=CATEGORIAS["plato_principal"],
        alergenos=[],
        descripcion="Lomo de res salteado con cebolla, tomate y papas fritas",
        ingredientes=["Lomo de res", "Cebolla", "Tomate", "Papas", "Ajo"],
        grupo_personalizacion=[crear_grupo_salsas()],
        peso=400.0,
        tipo="FONDO"
    ),
    4: Plato(
        id=4,
        nombre="Causa limeña",
        imagen="https://example.com/causa.jpg",
        precio=18.0,
        stock=6,
        disponible=True,
        categoria=CATEGORIAS["entrada"],
        alergenos=[],
        descripcion="Causa limeña con pollo y palta",
        ingredientes=["Papas", "Cebolla", "Ají"],
        grupo_personalizacion=[crear_grupo_salsas()],
        peso=250.0,
        tipo="ENTRADA"
    ),
    5: Plato(
        id=5,
        nombre="Suspiro limeño",
        imagen="https://example.com/suspiro.jpg",
        precio=12.0,
        stock=15,
        disponible=True,
        categoria=CATEGORIAS["postre"],
        alergenos=["LACTEOS"],
        descripcion="Postre tradicional peruano",
        ingredientes=[],
        grupo_personalizacion=None,
        peso=150.0,
        tipo="POSTRE"
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
        categoria=CATEGORIAS["bebida_alcoholica"],
        alergenos=["GLUTEN"],
        descripcion="Cerveza artesanal peruana",
        ingredientes=["Cebada", "Lúpulo"],
        grupo_personalizacion=[crear_grupo_tamaño_bebida()],
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
        categoria=CATEGORIAS["bebida_sin_alcohol"],
        alergenos=[],
        descripcion="Bebida tradicional peruana de maíz morado",
        ingredientes=[],
        grupo_personalizacion=[crear_grupo_tamaño_bebida()],
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
        categoria=CATEGORIAS["bebida_sin_alcohol"],
        alergenos=[],
        descripcion="Gaseosa peruana tradicional",
        ingredientes=[],
        grupo_personalizacion=[crear_grupo_tamaño_bebida()],
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

def obtener_platos_por_tipo(tipo: str) -> List[Plato]:
    """Retorna platos filtrados por tipo"""
    return [plato for plato in PLATOS.values() if plato.tipo == tipo]

def obtener_bebidas_sin_alcohol() -> List[Bebida]:
    """Retorna bebidas sin alcohol"""
    return [bebida for bebida in BEBIDAS.values() if not bebida.con_alcohol]

def obtener_bebidas_con_alcohol() -> List[Bebida]:
    """Retorna bebidas con alcohol"""
    return [bebida for bebida in BEBIDAS.values() if bebida.con_alcohol]

def obtener_categorias() -> List[Categoria]:
    """Retorna todas las categorías"""
    return list(CATEGORIAS.values())

def obtener_categoria_por_nombre(nombre: str) -> Optional[Categoria]:
    """Retorna una categoría por nombre"""
    for categoria in CATEGORIAS.values():
        if categoria.nombre.lower() == nombre.lower():
            return categoria
    return None