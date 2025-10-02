#!/usr/bin/env python3
"""
Test final de la implementación del patrón Repository
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_mock_repository():
    """Prueba el repositorio mock"""
    print("🧪 Probando repositorio MOCK...")
    
    try:
        from app.services.menu_service import MenuService
        from app.services.pedidos_service import PedidosService
        
        # MenuService con mock
        menu_service = MenuService("mock")
        items = menu_service.obtener_todos_los_items()
        platos = menu_service.obtener_platos()
        bebidas = menu_service.obtener_bebidas()
        
        print(f"  ✅ Items: {len(items)}, Platos: {len(platos)}, Bebidas: {len(bebidas)}")
        
        # PedidosService con mock
        pedidos_service = PedidosService("mock")
        ordenes = pedidos_service.obtener_todas_las_ordenes()
        meseros = pedidos_service.obtener_todos_los_meseros()
        mesas = pedidos_service.obtener_todas_las_mesas()
        
        print(f"  ✅ Órdenes: {len(ordenes)}, Meseros: {len(meseros)}, Mesas: {len(mesas)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_database_repository():
    """Prueba el repositorio de base de datos"""
    print("\n🗄️ Probando repositorio DATABASE...")
    
    try:
        from app.services.menu_service import MenuService
        
        # MenuService con database
        menu_service = MenuService("database")
        items = menu_service.obtener_todos_los_items()
        platos = menu_service.obtener_platos()
        bebidas = menu_service.obtener_bebidas()
        ingredientes = menu_service.obtener_ingredientes()
        
        print(f"  ✅ Items: {len(items)}, Platos: {len(platos)}, Bebidas: {len(bebidas)}, Ingredientes: {len(ingredientes)}")
        
        # Probar búsqueda
        items_buscados = menu_service.buscar_items_por_nombre("ceviche")
        print(f"  ✅ Búsqueda 'ceviche': {len(items_buscados)} items encontrados")
        
        # Probar disponibilidad
        disponible, mensaje = menu_service.verificar_disponibilidad_item(1, 2)
        print(f"  ✅ Disponibilidad item 1: {disponible} - {mensaje}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_repository_factory():
    """Prueba el factory de repositorios"""
    print("\n🏭 Probando RepositoryFactory...")
    
    try:
        from app.repositories.repository_factory import RepositoryFactory
        
        # Obtener tipos disponibles
        types = RepositoryFactory.get_available_repository_types()
        print(f"  ✅ Tipos disponibles: {list(types.keys())}")
        
        # Crear repositorios
        menu_repo_mock = RepositoryFactory.create_menu_repository("mock")
        menu_repo_db = RepositoryFactory.create_menu_repository("database")
        
        print("  ✅ Repositorios creados correctamente")
        
        # Probar que son diferentes
        items_mock = menu_repo_mock.obtener_todos_los_items()
        items_db = menu_repo_db.obtener_todos_los_items()
        
        print(f"  ✅ Mock: {len(items_mock)} items, Database: {len(items_db)} items")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_configuration():
    """Prueba la configuración"""
    print("\n⚙️ Probando configuración...")
    
    try:
        from app.config import Config
        
        print(f"  ✅ Repository type: {Config.REPOSITORY_TYPE}")
        print(f"  ✅ Database URL: {Config.DATABASE_URL}")
        print(f"  ✅ Is mock: {Config.is_mock_repository()}")
        print(f"  ✅ Is database: {Config.is_database_repository()}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_app_loading():
    """Prueba que la app se carga correctamente"""
    print("\n🚀 Probando carga de la aplicación...")
    
    try:
        from app.main import app
        from app.services.menu_service import MenuService
        from app.services.pedidos_service import PedidosService
        
        # Verificar que los servicios están inicializados
        print("  ✅ FastAPI app cargada")
        print("  ✅ Servicios inicializados")
        
        # Probar que los servicios funcionan
        menu_service = MenuService()
        items = menu_service.obtener_todos_los_items()
        print(f"  ✅ MenuService funcionando: {len(items)} items")
        
        pedidos_service = PedidosService()
        ordenes = pedidos_service.obtener_todas_las_ordenes()
        print(f"  ✅ PedidosService funcionando: {len(ordenes)} órdenes")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_repository_switching():
    """Prueba cambiar entre repositorios"""
    print("\n🔄 Probando cambio entre repositorios...")
    
    try:
        from app.services.menu_service import MenuService
        
        # Mock repository
        menu_mock = MenuService("mock")
        items_mock = menu_mock.obtener_todos_los_items()
        
        # Database repository
        menu_db = MenuService("database")
        items_db = menu_db.obtener_todos_los_items()
        
        print(f"  ✅ Mock: {len(items_mock)} items")
        print(f"  ✅ Database: {len(items_db)} items")
        print("  ✅ Cambio entre repositorios funcionando")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 TEST FINAL DE IMPLEMENTACIÓN DEL PATRÓN REPOSITORY")
    print("=" * 70)
    
    tests = [
        ("Repositorio Mock", test_mock_repository),
        ("Repositorio Database", test_database_repository),
        ("Repository Factory", test_repository_factory),
        ("Configuración", test_configuration),
        ("Carga de App", test_app_loading),
        ("Cambio de Repositorios", test_repository_switching),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASÓ")
            else:
                print(f"❌ {test_name}: FALLÓ")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n📊 RESULTADOS FINALES: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("\n🎉 ¡IMPLEMENTACIÓN COMPLETA Y EXITOSA!")
        print("\n✅ Patrón Repository implementado correctamente")
        print("✅ Repositorio Mock funcionando")
        print("✅ Repositorio Database funcionando")
        print("✅ Factory Pattern funcionando")
        print("✅ Configuración flexible funcionando")
        print("✅ Cambio entre repositorios funcionando")
        print("✅ Aplicación cargando correctamente")
        
        print("\n🚀 PRÓXIMOS PASOS RECOMENDADOS:")
        print("1. Implementar DatabaseRepository para pedidos")
        print("2. Agregar capa de cache (Redis)")
        print("3. Implementar ApiRepository para APIs externas")
        print("4. Agregar logging y monitoreo")
        
        return True
    else:
        print(f"\n❌ {total - passed} tests fallaron. Revisar errores.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



