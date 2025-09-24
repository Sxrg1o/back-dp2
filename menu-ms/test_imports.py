#!/usr/bin/env python3
"""
Script para probar las importaciones del microservicio de menú.
"""

def test_imports():
    """Prueba todas las importaciones principales."""
    try:
        print("🧪 Probando importaciones...")
        
        # Probar importaciones del dominio
        from domain.entities import Item, Plato, Bebida, Ingrediente
        from domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato
        print("✅ Entidades del dominio importadas correctamente")
        
        # Probar importaciones de repositorios
        from domain.repositories import ItemRepository, IngredienteRepository
        print("✅ Repositorios del dominio importados correctamente")
        
        # Probar importaciones de casos de uso
        from domain.use_cases import CreateItemUseCase, GetItemUseCase
        print("✅ Casos de uso importados correctamente")
        
        # Probar importaciones de servicios
        from application.services import ItemService, IngredienteService
        print("✅ Servicios de aplicación importados correctamente")
        
        # Probar importaciones de infraestructura
        from infrastructure.db import get_db, create_tables
        from infrastructure.models.item_model import ItemModel, IngredienteModel
        print("✅ Infraestructura importada correctamente")
        
        # Probar importaciones de handlers
        from infrastructure.handlers import item_router, ingrediente_router
        print("✅ Handlers importados correctamente")
        
        print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)







