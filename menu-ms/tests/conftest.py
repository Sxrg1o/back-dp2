"""
Configuración de pytest para los tests del microservicio de menú.
"""

import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.db import Base
from infrastructure.models.item_model import ItemModel, PlatoModel, BebidaModel, IngredienteModel


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que proporciona una sesión de base de datos para testing.
    """
    # Crear una base de datos en memoria para testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_plato():
    """
    Fixture que proporciona un plato de muestra para testing.
    """
    from domain.entities import Plato
    from domain.entities.enums import EtiquetaPlato, EtiquetaItem
    
    return Plato(
        descripcion="Pasta Carbonara",
        precio=Decimal('15.50'),
        peso=Decimal('300.0'),
        tipo=EtiquetaPlato.FONDO,
        valor_nutricional="Alto en carbohidratos y proteínas",
        tiempo_preparacion=Decimal('20.0'),
        comentarios="Plato tradicional italiano",
        receta="Cocer pasta, preparar salsa con huevos y panceta",
        disponible=True,
        unidades_disponibles=10,
        num_ingredientes=5,
        kcal=600,
        calorias=Decimal('600.0'),
        proteinas=Decimal('25.0'),
        azucares=Decimal('5.0'),
        etiquetas=[EtiquetaItem.CON_GLUTEN]
    )


@pytest.fixture
def sample_bebida():
    """
    Fixture que proporciona una bebida de muestra para testing.
    """
    from domain.entities import Bebida
    from domain.entities.enums import EtiquetaItem
    
    return Bebida(
        descripcion="Coca Cola",
        precio=Decimal('3.50'),
        litros=Decimal('0.5'),
        alcoholico=False,
        valor_nutricional="Alto en azúcares",
        tiempo_preparacion=Decimal('0.0'),
        comentarios="Bebida refrescante",
        receta="Servir fría",
        disponible=True,
        unidades_disponibles=50,
        num_ingredientes=1,
        kcal=200,
        calorias=Decimal('200.0'),
        proteinas=Decimal('0.0'),
        azucares=Decimal('50.0'),
        etiquetas=[EtiquetaItem.FRIO]
    )


@pytest.fixture
def sample_ingrediente():
    """
    Fixture que proporciona un ingrediente de muestra para testing.
    """
    from domain.entities import Ingrediente
    from domain.entities.enums import EtiquetaIngrediente
    
    return Ingrediente(
        nombre="Tomate",
        stock=Decimal('20.0'),
        peso=Decimal('0.2'),
        tipo=EtiquetaIngrediente.VERDURA
    )


@pytest.fixture
def sample_platos():
    """
    Fixture que proporciona múltiples platos de muestra para testing.
    """
    from domain.entities import Plato
    from domain.entities.enums import EtiquetaPlato, EtiquetaItem
    
    return [
        Plato(
            descripcion="Ensalada César",
            precio=Decimal('8.50'),
            peso=Decimal('200.0'),
            tipo=EtiquetaPlato.ENTRADA,
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO,
            etiquetas=[EtiquetaItem.CON_GLUTEN]
        ),
        Plato(
            descripcion="Tiramisú",
            precio=Decimal('6.00'),
            peso=Decimal('150.0'),
            tipo=EtiquetaPlato.POSTRE,
            etiquetas=[EtiquetaItem.FRIO]
        )
    ]


@pytest.fixture
def sample_bebidas():
    """
    Fixture que proporciona múltiples bebidas de muestra para testing.
    """
    from domain.entities import Bebida
    from domain.entities.enums import EtiquetaItem
    
    return [
        Bebida(
            descripcion="Coca Cola",
            precio=Decimal('3.50'),
            litros=Decimal('0.5'),
            alcoholico=False,
            etiquetas=[EtiquetaItem.FRIO]
        ),
        Bebida(
            descripcion="Cerveza Corona",
            precio=Decimal('4.50'),
            litros=Decimal('0.33'),
            alcoholico=True,
            etiquetas=[EtiquetaItem.FRIO]
        ),
        Bebida(
            descripcion="Agua Mineral",
            precio=Decimal('2.00'),
            litros=Decimal('0.5'),
            alcoholico=False,
            etiquetas=[EtiquetaItem.FRIO]
        )
    ]


@pytest.fixture
def sample_ingredientes():
    """
    Fixture que proporciona múltiples ingredientes de muestra para testing.
    """
    from domain.entities import Ingrediente
    from domain.entities.enums import EtiquetaIngrediente
    
    return [
        Ingrediente(
            nombre="Tomate",
            stock=Decimal('20.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Pollo",
            stock=Decimal('5.0'),
            peso=Decimal('1.0'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        Ingrediente(
            nombre="Manzana",
            stock=Decimal('15.0'),
            peso=Decimal('0.3'),
            tipo=EtiquetaIngrediente.FRUTA
        )
    ]
