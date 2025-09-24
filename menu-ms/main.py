"""
Microservicio de Menú y Carta para el restaurante Domótica.
Gestiona todos los elementos relacionados con los productos alimenticios.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

from infrastructure.db import create_tables
from infrastructure.handlers import item_router, ingrediente_router
from infrastructure.handlers.platos_handler import router as platos_router
from infrastructure.handlers.bebidas_handler import router as bebidas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    """
    # Startup
    print("🚀 Iniciando microservicio de Menú y Carta...")
    create_tables()
    print("✅ Base de datos inicializada")
    yield
    # Shutdown
    print("🛑 Cerrando microservicio de Menú y Carta...")


# Crear la aplicación FastAPI
app = FastAPI(
    title="Menú y Carta API",
    description="""
    ## Microservicio de Menú y Carta para el restaurante Domótica
    
    Este microservicio gestiona todos los elementos relacionados con los productos alimenticios del restaurante, incluyendo:
    
    - **Platos**: Entradas, platos principales y postres
    - **Bebidas**: Alcohólicas y no alcohólicas
    - **Ingredientes**: Gestión de inventario de ingredientes
    - **Información nutricional**: Valores nutricionales y etiquetas especiales
    
    ### Características principales:
    - ✅ Gestión completa de menú y carta
    - ✅ Control de stock e inventario
    - ✅ Información nutricional detallada
    - ✅ Sistema de etiquetas para filtrado
    - ✅ Búsqueda y filtros avanzados
    - ✅ Arquitectura hexagonal (Clean Architecture)
    - ✅ Documentación automática con Swagger
    
    ### Endpoints principales:
    - `/items/` - Gestión de ítems del menú
    - `/ingredientes/` - Gestión de ingredientes
    - `/health` - Estado del servicio
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo Domótica",
        "email": "dev@domotica.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(item_router)
app.include_router(ingrediente_router)
app.include_router(platos_router)
app.include_router(bebidas_router)


@app.get("/health", tags=["health"])
def health_check():
    """
    Verifica el estado del microservicio.
    
    Returns:
        dict: Estado del servicio
    """
    return {
        "status": "healthy",
        "service": "menu-ms",
        "version": "1.0.0",
        "message": "Microservicio de Menú y Carta funcionando correctamente"
    }


@app.get("/", tags=["root"])
def root():
    """
    Endpoint raíz del microservicio.
    
    Returns:
        dict: Información básica del servicio
    """
    return {
        "message": "🍽️ API de Menú y Carta funcionando 🚀",
        "service": "menu-ms",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/info", tags=["info"])
def service_info():
    """
    Información detallada del microservicio.
    
    Returns:
        dict: Información completa del servicio
    """
    return {
        "service": "menu-ms",
        "version": "1.0.0",
        "description": "Microservicio de Menú y Carta para el restaurante Domótica",
        "features": [
            "Gestión de platos (entradas, principales, postres)",
            "Gestión de bebidas (alcohólicas y no alcohólicas)",
            "Control de ingredientes e inventario",
            "Información nutricional completa",
            "Sistema de etiquetas y filtros",
            "Búsqueda avanzada",
            "Arquitectura hexagonal"
        ],
        "endpoints": {
            "items": "/items/",
            "platos": "/platos/",
            "bebidas": "/bebidas/",
            "ingredientes": "/ingredientes/",
            "health": "/health",
            "docs": "/docs"
        },
        "database": "SQLite (desarrollo) / PostgreSQL (producción)"
    }


@app.post("/seed-data", tags=["admin"])
def seed_peruvian_data():
    """
    Pobla la base de datos con datos de prueba típicos de Perú.
    Incluye platos, bebidas e ingredientes tradicionales peruanos.
    """
    try:
        from seed_data_peru import seed_database
        seed_database()
        return {
            "message": "Base de datos poblada exitosamente con datos peruanos",
            "success": True,
            "data": {
                "ingredientes": "Ingredientes típicos peruanos (ají amarillo, rocoto, lúcuma, etc.)",
                "platos": "Platos tradicionales (ceviche, lomo saltado, causa limeña, etc.)",
                "bebidas": "Bebidas peruanas (chicha morada, pisco sour, Inca Kola, etc.)"
            }
        }
    except Exception as e:
        error_msg = str(e)
        if "UNIQUE constraint failed" in error_msg:
            return {
                "message": "Los datos ya existen en la base de datos",
                "success": True,
                "warning": "No se agregaron datos duplicados",
                "data": {
                    "ingredientes": "Ingredientes típicos peruanos ya presentes",
                    "platos": "Platos tradicionales ya presentes", 
                    "bebidas": "Bebidas peruanas ya presentes"
                }
            }
        else:
            raise HTTPException(
                status_code=500, 
                detail=f"Error al poblar la base de datos: {error_msg}"
            )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))  # Puerto por defecto 8002
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 Iniciando servidor en {host}:{port}")
    print(f"📚 Documentación disponible en: http://{host}:{port}/docs")
    print(f"🔍 Health check en: http://{host}:{port}/health")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )