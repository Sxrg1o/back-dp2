"""
Ejemplos de cómo usar los fixtures de Fake Data en tus tests.

Este archivo muestra las diferentes formas de generar datos de prueba
usando los fixtures disponibles en conftest.py

NOTA: Los ejemplos usan modelos existentes (Rol, Producto, Categoria, Alergeno)
"""

import pytest
from ulid import ULID
from decimal import Decimal
from src.models.auth.rol_model import RolModel
from src.models.menu.producto_model import ProductoModel
from src.models.menu.categoria_model import CategoriaModel
from src.models.menu.alergeno_model import AlergenoModel


# =============================================================================
# EJEMPLO 1: Usar un fixture simple
# =============================================================================
def test_ejemplo_fixture_simple(fake_rol_data):
    """
    Muestra cómo usar un fixture simple que genera datos fake.
    
    ANTES (manual):
        data = {
            "id": str(ULID()),
            "nombre": "Admin",
            "descripcion": "Administrador del sistema",
            "activo": True
        }
    
    AHORA (con fake_rol_data):
        ¡Solo 1 línea! Los datos se generan automáticamente.
    """
    rol = RolModel(**fake_rol_data)
    
    assert rol.nombre is not None
    assert len(rol.nombre) <= 50
    assert rol.descripcion is not None
    print(f"✅ Rol creado: {rol.nombre}")


# =============================================================================
# EJEMPLO 2: Usar factory para crear múltiples instancias
# =============================================================================
def test_ejemplo_factory_multiple_roles(create_fake_rol):
    """
    Muestra cómo usar un factory para crear varios roles con datos diferentes.
    
    El factory 'create_fake_rol' es una FUNCIÓN que genera datos fake
    cada vez que la llamas.
    """
    # Crear 5 roles diferentes con 1 sola línea
    roles_data = [create_fake_rol() for _ in range(5)]
    
    # Verificar que todos tienen IDs diferentes
    ids = [r["id"] for r in roles_data]
    assert len(set(ids)) == 5  # ✅ Todos son únicos
    
    # Verificar que todos tienen nombres diferentes
    nombres = [r["nombre"] for r in roles_data]
    assert len(set(nombres)) == 5  # ✅ Todos son únicos
    
    print(f"✅ Creados {len(roles_data)} roles con datos únicos")


# =============================================================================
# EJEMPLO 3: Customizar datos del factory
# =============================================================================
def test_ejemplo_factory_con_custom_data(create_fake_rol):
    """
    Muestra cómo personalizar algunos campos mientras otros se generan automáticamente.
    
    Útil cuando necesitas valores específicos para tu test pero quieres
    que el resto de datos sea fake.
    """
    # Crear un rol con nombre específico pero otros datos fake
    rol_data = create_fake_rol(
        nombre="Administrador",
        activo=True
    )
    
    assert rol_data["nombre"] == "Administrador"  # ✅ Tu valor
    assert rol_data["activo"] is True  # ✅ Tu valor
    assert rol_data["descripcion"] is not None  # ✅ Generado automáticamente
    assert rol_data["id"] is not None  # ✅ Generado automáticamente
    
    print(f"✅ Rol '{rol_data['nombre']}' con descripción fake: {rol_data['descripcion']}")


# =============================================================================
# EJEMPLO 4: Combinar fixtures simples y factories
# =============================================================================
def test_ejemplo_combinado(fake_categoria_data, create_fake_producto):
    """
    Muestra cómo combinar un fixture simple con un factory.
    
    Usamos fake_categoria_data (fixture) y creamos múltiples productos
    para esa categoría (factory).
    """
    categoria = CategoriaModel(**fake_categoria_data)
    
    # Crear 3 productos para esta categoría
    productos_data = [
        create_fake_producto(id_categoria=categoria.id)
        for _ in range(3)
    ]
    
    # Verificar que todos pertenecen a la misma categoría
    for prod_data in productos_data:
        assert prod_data["id_categoria"] == categoria.id
    
    print(f"✅ Categoría '{categoria.nombre}' con {len(productos_data)} productos")


# =============================================================================
# EJEMPLO 5: Usar datos fake con modelos SQLAlchemy
# =============================================================================
def test_producto_model_with_fake_data(fake_producto_data):
    """
    Muestra cómo los datos fake funcionan perfectamente con modelos SQLAlchemy.
    
    Los tipos de datos generados (UUID, Decimal, str) coinciden exactamente
    con los que espera el modelo.
    """
    producto = ProductoModel(**fake_producto_data)
    
    # Validar que el modelo se creó correctamente
    assert producto.id is not None
    assert producto.nombre is not None
    assert producto.precio_base > 0
    assert isinstance(producto.precio_base, Decimal)  # ✅ Tipo correcto
    assert producto.imagen_path is not None and producto.imagen_path.endswith('.jpg')
    
    print(f"✅ Producto '{producto.nombre}' - ${producto.precio_base}")


# =============================================================================
# EJEMPLO 6: Parametrizar tests con factories
# =============================================================================
@pytest.mark.parametrize("cantidad", [1, 5, 10])
def test_crear_multiples_productos(create_fake_producto, cantidad):
    """
    Muestra cómo usar factories en tests parametrizados.
    
    Este test se ejecuta 3 veces con diferentes cantidades (1, 5, 10).
    Perfecto para probar funcionalidad con distintos volúmenes de datos.
    """
    productos = [create_fake_producto() for _ in range(cantidad)]
    
    assert len(productos) == cantidad
    
    # Verificar que todos tienen IDs únicos
    ids = [p["id"] for p in productos]
    assert len(set(ids)) == cantidad
    
    print(f"✅ Test con {cantidad} productos - todos únicos")


# =============================================================================
# EJEMPLO 7: Crear escenarios específicos
# =============================================================================
def test_escenarios_especificos(create_fake_producto):
    """
    Muestra cómo crear escenarios de prueba específicos para tu lógica de negocio.
    
    Combinas datos fake (nombre, descripción) con valores específicos
    que necesitas probar (disponible, destacado, precio).
    """
    # Producto disponible y destacado
    producto_premium = create_fake_producto(
        disponible=True,
        destacado=True,
        precio_base=Decimal("25.99")
    )
    
    # Producto no disponible
    producto_agotado = create_fake_producto(
        disponible=False,
        destacado=False
    )
    
    # Producto económico
    producto_economico = create_fake_producto(
        precio_base=Decimal("5.99")
    )
    
    assert producto_premium["destacado"] is True
    assert producto_premium["precio_base"] == Decimal("25.99")
    assert producto_agotado["disponible"] is False
    assert producto_economico["precio_base"] < Decimal("10.00")
    
    print(f"✅ 3 escenarios diferentes creados exitosamente")


# =============================================================================
# EJEMPLO 8: Trabajar con relaciones
# =============================================================================
def test_ejemplo_relaciones(fake_categoria_data, fake_producto_data, fake_alergeno_data):
    """
    Muestra cómo los fixtures manejan automáticamente las relaciones.
    
    fake_producto_data ya incluye un id_categoria del fake_categoria_data.
    """
    categoria = CategoriaModel(**fake_categoria_data)
    producto = ProductoModel(**fake_producto_data)
    
    # ✅ La relación se estableció automáticamente
    assert producto.id_categoria == categoria.id
    
    print(f"✅ Producto '{producto.nombre}' en categoría '{categoria.nombre}'")


# =============================================================================
# EJEMPLO 9: Comparación ANTES vs DESPUÉS
# =============================================================================
def test_comparacion_antes_despues(fake_rol_data, create_fake_rol):
    """
    ANTES (manual - 10 líneas por cada rol):
        rol1_data = {
            "id": str(ULID()),
            "nombre": "Admin",
            "descripcion": "Administrador del sistema",
            "activo": True
        }
        rol2_data = {
            "id": str(ULID()),
            "nombre": "Usuario",
            "descripcion": "Usuario normal",
            "activo": True
        }
        rol3_data = {
            "id": str(ULID()),
            "nombre": "Invitado",
            "descripcion": "Usuario invitado",
            "activo": False
        }
    
    DESPUÉS (con fixtures - 1 línea):
        roles = [create_fake_rol() for _ in range(3)]
    
    ✅ 30 líneas → 1 línea
    ✅ Datos más realistas
    ✅ Sin riesgo de IDs duplicados
    ✅ Mantenimiento más fácil
    """
    # La nueva forma:
    roles = [create_fake_rol() for _ in range(3)]
    
    assert len(roles) == 3
    assert all(r["id"] is not None for r in roles)
    assert all(r["nombre"] is not None for r in roles)
    
    print("✅ Comparación exitosa: Fake data es MUCHO mejor")


# =============================================================================
# EJEMPLO 10: Alergenos con enum
# =============================================================================
def test_ejemplo_alergenos(create_fake_producto_alergeno):
    """
    Muestra cómo los fixtures manejan enums correctamente.
    
    El fixture fake_producto_alergeno_data genera automáticamente
    un NivelPresencia válido.
    """
    from src.core.enums.alergeno_enums import NivelPresencia
    
    # Crear 5 relaciones producto-alergeno
    relaciones = [create_fake_producto_alergeno() for _ in range(5)]
    
    for rel in relaciones:
        # Verificar que nivel_presencia es un enum válido
        assert rel["nivel_presencia"] in [
            NivelPresencia.CONTIENE,
            NivelPresencia.PUEDE_CONTENER,
            NivelPresencia.TRAZAS
        ]
    
    print(f"✅ {len(relaciones)} relaciones con niveles de presencia válidos")


# =============================================================================
# DOCUMENTACIÓN: Resumen de ventajas
# =============================================================================

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                     ¿POR QUÉ USAR FAKE DATA?                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

1️⃣  MENOS CÓDIGO
    Antes: 10 líneas por cada objeto de prueba
    Ahora: 1 línea con el fixture
    
2️⃣  DATOS MÁS REALISTAS
    ✅ Nombres reales en español (Faker locale 'es_ES')
    ✅ Emails válidos (@example.com)
    ✅ Precios con formato Decimal correcto
    ✅ Textos descriptivos convincentes
    
3️⃣  SIN DUPLICADOS
    ✅ Cada llamada genera IDs únicos
    ✅ No hay riesgo de emails duplicados
    ✅ Nombres diferentes automáticamente
    
4️⃣  FÁCIL DE MANTENER
    ✅ Cambios en el modelo → solo actualizar conftest.py
    ✅ Los tests no necesitan cambios
    ✅ Un solo lugar para modificar
    
5️⃣  TESTS MÁS LEGIBLES
    ✅ Código enfocado en LÓGICA de negocio
    ✅ No en CREAR datos de prueba
    ✅ Intención clara del test
    
6️⃣  REUTILIZABLE EN TODO EL PROYECTO
    ✅ Unit tests
    ✅ Integration tests
    ✅ E2E tests
    ✅ Todos usan los mismos fixtures

╔═══════════════════════════════════════════════════════════════════════════╗
║                        CÓMO USAR EN TUS TESTS                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

📌 OPCIÓN 1: Fixture simple (1 instancia por test)
    
    def test_mi_test(fake_producto_data):
        producto = ProductoModel(**fake_producto_data)
        assert producto.nombre is not None

📌 OPCIÓN 2: Factory (múltiples instancias)
    
    def test_mi_test(create_fake_producto):
        productos = [create_fake_producto() for _ in range(10)]
        assert len(productos) == 10

📌 OPCIÓN 3: Factory con customización
    
    def test_mi_test(create_fake_producto):
        prod = create_fake_producto(
            nombre="Pizza Especial",
            precio_base=Decimal("15.99"),
            destacado=True
        )
        assert prod["nombre"] == "Pizza Especial"

╔═══════════════════════════════════════════════════════════════════════════╗
║                     FIXTURES DISPONIBLES                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

FIXTURES SIMPLES (1 instancia):
    ├─ fake_rol_data
    ├─ fake_usuario_data (cuando se implemente UsuarioModel)
    ├─ fake_categoria_data
    ├─ fake_producto_data
    ├─ fake_alergeno_data
    └─ fake_producto_alergeno_data

FACTORIES (múltiples instancias):
    ├─ create_fake_rol()
    ├─ create_fake_usuario() (cuando se implemente UsuarioModel)
    └─ create_fake_producto()

╔═══════════════════════════════════════════════════════════════════════════╗
║                          EJECUTAR ESTOS EJEMPLOS                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

Desde la terminal:
    
    pytest tests/EJEMPLO_FAKE_DATA.py -v
    
Ver salida detallada:
    
    pytest tests/EJEMPLO_FAKE_DATA.py -v -s
    
Ejecutar solo un ejemplo:
    
    pytest tests/EJEMPLO_FAKE_DATA.py::test_ejemplo_fixture_simple -v -s

"""
