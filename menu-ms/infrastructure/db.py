"""
Configuración de base de datos para el microservicio de menú.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./menu.db"
)

# Crear el motor de base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Obtiene una sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crea todas las tablas en la base de datos.
    """
    # Importar modelos para registrar metadata en Base
    from infrastructure.models.item_model import (
        ItemModel, PlatoModel, BebidaModel, IngredienteModel, ItemEtiquetaModel
    )
    Base.metadata.create_all(bind=engine)
