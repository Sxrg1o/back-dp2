#!/usr/bin/env python3
"""
Script de test para el repositorio de base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_database_repository():
    """Prueba el repositorio de base de datos"""
    print("🗄️ Probando repositorio de base de datos...")
    
    try:
        from app.services.menu_service import MenuService
        
        # Crear servicio con repositorio de base de datos
        print("  - Creando MenuService con repositorio database...")
        menu_service = MenuService("database")
        
        # Probar operaciones básicas
        print("  - Probando obtener_todos_los_items...")
        items = menu_service.obtener_todos_los_items()
        print(f"    ✅ Items obtenidos: {len(items)}")
        
        print("  - Probando obtener_platos...")
        platos = menu_service.obtener_platos()
        print(f"    ✅ Platos obtenidos: {len(platos)}")
        
        print("  - Probando obtener_bebidas...")
        bebidas = menu_service.obtener_bebidas()
        print(f"    ✅ Bebidas obtenidas: {len(bebidas)}")
        
        print("  - Probando obtener_ingredientes...")
        ingredientes = menu_service.obtener_ingredientes()
        print(f"    ✅ Ingredientes obtenidos: {len(ingredientes)}")
        
        print("  - Probando buscar_items_por_nombre...")
        items_buscados = menu_service.buscar_items_por_nombre("ceviche")
        print(f"    ✅ Items encontrados: {len(items_buscados)}")
        
        print("  - Probando verificar_disponibilidad_item...")
        disponible, mensaje = menu_service.verificar_disponibilidad_item(1, 2)
        print(f"    ✅ Disponibilidad: {disponible} - {mensaje}")
        
        print("✅ Repositorio de base de datos funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error probando repositorio de base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_repository_switching():
    """Prueba cambiar entre diferentes tipos de repositorio"""
    print("\n🔄 Probando cambio entre repositorios...")
    
    try:
        from app.services.menu_service import MenuService
        
        # Probar con repositorio mock
        print("  - Probando con repositorio MOCK...")
        menu_service_mock = MenuService("mock")
        items_mock = menu_service_mock.obtener_todos_los_items()
        print(f"    ✅ Items mock: {len(items_mock)}")
        
        # Probar con repositorio database
        print("  - Probando con repositorio DATABASE...")
        menu_service_db = MenuService("database")
        items_db = menu_service_db.obtener_todos_los_items()
        print(f"    ✅ Items database: {len(items_db)}")
        
        # Comparar resultados
        print(f"  - Comparación: Mock={len(items_mock)}, Database={len(items_db)}")
        
        print("✅ Cambio entre repositorios funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error probando cambio de repositorios: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Prueba los endpoints de la API"""
    print("\n🌐 Probando endpoints de la API...")
    
    try:
        import requests
        import time
        
        # Iniciar servidor en background
        print("  - Iniciando servidor...")
        import subprocess
        import threading
        
        def start_server():
            subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "127.0.0.1", 
                "--port", "8001"
            ], capture_output=True)
        
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Esperar a que el servidor inicie
        time.sleep(3)
        
        # Probar endpoints
        base_url = "http://127.0.0.1:8001"
        
        print("  - Probando endpoint raíz...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ API funcionando - Repository: {data.get('repository_type')}")
        else:
            print(f"    ❌ Error en endpoint raíz: {response.status_code}")
            return False
        
        print("  - Probando health check...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("    ✅ Health check OK")
        else:
            print(f"    ❌ Error en health check: {response.status_code}")
            return False
        
        print("  - Probando endpoint de items...")
        response = requests.get(f"{base_url}/api/menu/items")
        if response.status_code == 200:
            items = response.json()
            print(f"    ✅ Items obtenidos: {len(items)}")
        else:
            print(f"    ❌ Error en items: {response.status_code}")
            return False
        
        print("✅ Endpoints de la API funcionando correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error probando API: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 TEST COMPLETO DEL PATRÓN REPOSITORY")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Repositorio de base de datos
    if test_database_repository():
        tests_passed += 1
    
    # Test 2: Cambio entre repositorios
    if test_repository_switching():
        tests_passed += 1
    
    # Test 3: API endpoints
    if test_api_endpoints():
        tests_passed += 1
    
    print(f"\n📊 RESULTADOS: {tests_passed}/{total_tests} tests pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("\n✅ Implementación del patrón Repository COMPLETA y FUNCIONAL")
        print("✅ Repositorio Mock funcionando")
        print("✅ Repositorio Database funcionando")
        print("✅ Cambio entre repositorios funcionando")
        print("✅ API endpoints funcionando")
    else:
        print("❌ Algunos tests fallaron. Revisar errores arriba.")
        sys.exit(1)

if __name__ == "__main__":
    main()



