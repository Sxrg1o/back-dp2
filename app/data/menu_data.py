from typing import Dict, List, Optional
from app.models.menu_y_carta.domain import Item, Categoria, GrupoPersonalizacion, Opcion

# =========================
# Catálogo de categorías
# =========================
CATEGORIAS: Dict[str, Categoria] = {
    "entrada": Categoria(id=1, nombre="Entrada", descripcion="Platos para comenzar la comida"),
    "plato_principal": Categoria(id=2, nombre="Plato Principal", descripcion="Platos principales del menú"),
    "postre": Categoria(id=3, nombre="Postre", descripcion="Dulces para finalizar la comida"),
    "bebida_sin_alcohol": Categoria(id=4, nombre="Bebida Sin Alcohol", descripcion="Bebidas refrescantes"),
    "bebida_alcoholica": Categoria(id=5, nombre="Bebida Alcohólica", descripcion="Bebidas con contenido alcohólico"),
}

# =========================
# Grupos de personalización
# =========================
def crear_grupo_acompanamientos() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        id=1,
        etiqueta="Acompañamientos",
        tipo="acompanamiento",
        opciones=[
            Opcion(id=1, etiqueta="Camote", precio_adicional=3.0, es_default=False),
            Opcion(id=2, etiqueta="Choclo", precio_adicional=2.5, es_default=False),
            Opcion(id=3, etiqueta="Papas fritas", precio_adicional=4.0, es_default=False),
            Opcion(id=4, etiqueta="Sin acompañamiento", precio_adicional=0.0, es_default=True),
        ],
        max_selecciones=2
    )

def crear_grupo_salsas() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        id=2,
        etiqueta="Salsas",
        tipo="salsa",
        opciones=[
            Opcion(id=5, etiqueta="Ají extra", precio_adicional=1.0, es_default=False),
            Opcion(id=6, etiqueta="Salsa de la casa", precio_adicional=1.5, es_default=False),
            Opcion(id=7, etiqueta="Cebolla extra", precio_adicional=0.5, es_default=False),
            Opcion(id=8, etiqueta="Sin salsas", precio_adicional=0.0, es_default=True),
        ],
        max_selecciones=3
    )

def crear_grupo_tamaño_bebida() -> GrupoPersonalizacion:
    return GrupoPersonalizacion(
        id=3,
        etiqueta="Tamaño",
        tipo="tamaño",
        opciones=[
            Opcion(id=9, etiqueta="Pequeña (330ml)", precio_adicional=0.0, es_default=True),
            Opcion(id=10, etiqueta="Mediana (500ml)", precio_adicional=3.0, es_default=False),
            Opcion(id=11, etiqueta="Grande (750ml)", precio_adicional=5.0, es_default=False),
        ],
        max_selecciones=1
    )

# =========================
# Catálogo de platos
# =========================
PLATOS: Dict[int, Item] = {
    1: Item(
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
    2: Item(
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
    3: Item(
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
    4: Item(
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
    5: Item(
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
BEBIDAS: Dict[int, Item] = {
    6: Item(
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
    7: Item(
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
    8: Item(
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

def obtener_platos_por_tipo(tipo: str) -> List[Item]:
    """Retorna platos filtrados por tipo"""
    return [plato for plato in PLATOS.values() if plato.tipo == tipo]

def obtener_bebidas_sin_alcohol() -> List[Item]:
    """Retorna bebidas sin alcohol"""
    return [bebida for bebida in BEBIDAS.values() if not bebida.con_alcohol]

def obtener_bebidas_con_alcohol() -> List[Item]:
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