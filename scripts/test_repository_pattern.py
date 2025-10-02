#!/usr/bin/env python3
"""
Script de ejemplo para demostrar el patrón Repository
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.menu_service import MenuService
from app.services.pedidos_service import PedidosService
from app.repositories.repository_factory import RepositoryFactory

def test_mock_repository():
    """Prueba el repositorio mock"""
    print("🧪 Probando repositorio MOCK...")
    
    # Crear servicios con repositorio mock
    menu_service = MenuService("mock")
    pedidos_service = PedidosService("mock")
    
    # Probar menú
    print("\n📋 Probando MenuService:")
    items = menu_service.obtener_todos_los_items()
    print(f"  - Total de items: {len(items)}")
    
    platos = menu_service.obtener_platos()
    print(f"  - Total de platos: {len(platos)}")
    
    bebidas = menu_service.obtener_bebidas()
    print(f"  - Total de bebidas: {len(bebidas)}")
    
    # Probar pedidos
    print("\n🛒 Probando PedidosService:")
    ordenes = pedidos_service.obtener_todas_las_ordenes()
    print(f"  - Total de órdenes: {len(ordenes)}")
    
    meseros = pedidos_service.obtener_todos_los_meseros()
    print(f"  - Total de meseros: {len(meseros)}")
    
    mesas = pedidos_service.obtener_todas_las_mesas()
    print(f"  - Total de mesas: {len(mesas)}")
    
    print("✅ Repositorio mock funcionando correctamente!")

def test_repository_factory():
    """Prueba el factory de repositorios"""
    print("\n🏭 Probando RepositoryFactory...")
    
    # Obtener tipos disponibles
    available_types = RepositoryFactory.get_available_repository_types()
    print("  - Tipos de repositorio disponibles:")
    for repo_type, info in available_types.items():
        status = "✅" if info["menu"] and info["pedidos"] else "🚧"
        print(f"    {status} {repo_type}: {info['description']}")
    
    # Probar creación de repositorios
    try:
        menu_repo = RepositoryFactory.create_menu_repository("mock")
        print("  ✅ Repositorio de menú mock creado")
    except Exception as e:
        print(f"  ❌ Error creando repositorio de menú: {e}")
    
    try:
        pedidos_repo = RepositoryFactory.create_pedidos_repository("mock")
        print("  ✅ Repositorio de pedidos mock creado")
    except Exception as e:
        print(f"  ❌ Error creando repositorio de pedidos: {e}")
    
    # Probar tipo no soportado
    try:
        RepositoryFactory.create_menu_repository("invalid")
        print("  ❌ No debería crear repositorio inválido")
    except ValueError as e:
        print(f"  ✅ Correctamente rechazó tipo inválido: {e}")

def test_service_with_different_repositories():
    """Prueba servicios con diferentes tipos de repositorio"""
    print("\n🔄 Probando servicios con diferentes repositorios...")
    
    # Probar con repositorio mock
    print("  - Usando repositorio MOCK:")
    menu_service_mock = MenuService("mock")
    items_mock = menu_service_mock.obtener_todos_los_items()
    print(f"    Items obtenidos: {len(items_mock)}")
    
    # Probar con repositorio database (debería fallar)
    print("  - Intentando usar repositorio DATABASE:")
    try:
        menu_service_db = MenuService("database")
        print("    ❌ No debería crear repositorio de base de datos")
    except NotImplementedError as e:
        print(f"    ✅ Correctamente rechazó repositorio no implementado: {e}")
    
    # Probar con repositorio api (debería fallar)
    print("  - Intentando usar repositorio API:")
    try:
        menu_service_api = MenuService("api")
        print("    ❌ No debería crear repositorio de API")
    except NotImplementedError as e:
        print(f"    ✅ Correctamente rechazó repositorio no implementado: {e}")

def main():
    """Función principal"""
    print("🚀 Demostración del Patrón Repository")
    print("=" * 50)
    
    try:
        test_mock_repository()
        test_repository_factory()
        test_service_with_different_repositories()
        
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n📚 Para más información, consulta: REPOSITORY_PATTERN_GUIDE.md")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

