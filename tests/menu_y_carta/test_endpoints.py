"""
Tests del módulo Menu y Carta - Reorganizados con mejor estructura.
"""
import sys
import os
from typing import Dict, List
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app

# Configurar cliente de prueba
client = TestClient(app)

class TestMenuYCartaEndpoints:
    """Tests organizados para el módulo Menu y Carta"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.client = client
    
    # =========================
    # Tests de Endpoints Básicos
    # =========================
    
    def test_root_endpoint(self):
        """Test para el endpoint raíz"""
        response = self.make_request('GET', '/')
        self.assert_success_response(response)
        assert 'message' in response['data']
        assert 'version' in response['data']
        assert response['data']['version'] == "1.0.0"
        self.print_test_result("Root endpoint", True)
    
    def test_health_check(self):
        """Test para el health check"""
        response = self.make_request('GET', '/health')
        self.assert_success_response(response)
        assert response['data']['status'] == "ok"
        self.print_test_result("Health check", True)
    
    # =========================
    # Tests de Items
    # =========================
    
    def test_obtener_todos_los_items(self):
        """Test para obtener todos los items"""
        response = self.client.get('/api/menu/items')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"Obtener todos los items: {len(data)} items encontrados")
    
    def test_obtener_item_por_id(self):
        """Test para obtener item por ID"""
        # Test con ID válido
        response = self.make_request('GET', '/api/menu/items/1')
        self.assert_success_response(response)
        assert response['data']['id'] == 1
        assert 'nombre' in response['data']
        self.print_test_result("Obtener item por ID (válido)", True)
        
        # Test con ID inválido
        response = self.make_request('GET', '/api/menu/items/999')
        self.assert_error_response(response, 404)
        self.print_test_result("Obtener item por ID (inválido)", True, "Maneja error correctamente")
    
    def test_obtener_items_disponibles(self):
        """Test para obtener items disponibles"""
        response = self.make_request('GET', '/api/menu/items/disponibles')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        # Verificar que todos los items están disponibles
        for item in response['data']:
            assert item["disponible"] == True
            assert item["stock"] > 0
        self.print_test_result("Obtener items disponibles", True, f"{len(response['data'])} items disponibles")
    
    def test_buscar_items_por_nombre(self):
        """Test para buscar items por nombre"""
        response = self.make_request('GET', '/api/menu/items/buscar?nombre=ceviche')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        # Verificar que al menos un resultado contiene "ceviche"
        assert any("ceviche" in item["nombre"].lower() for item in response['data'])
        self.print_test_result("Buscar items por nombre", True, f"{len(response['data'])} resultados para 'ceviche'")
    
    # =========================
    # Tests de Platos
    # =========================
    
    def test_obtener_platos(self):
        """Test para obtener todos los platos"""
        response = self.make_request('GET', '/api/menu/platos')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        assert len(response['data']) > 0
        self.print_test_result("Obtener todos los platos", True, f"{len(response['data'])} platos encontrados")
    
    def test_obtener_entradas(self):
        """Test para obtener entradas"""
        response = self.make_request('GET', '/api/menu/platos/entradas')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener entradas", True, f"{len(response['data'])} entradas encontradas")
    
    def test_obtener_platos_principales(self):
        """Test para obtener platos principales"""
        response = self.make_request('GET', '/api/menu/platos/principales')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener platos principales", True, f"{len(response['data'])} platos encontrados")
    
    def test_obtener_postres(self):
        """Test para obtener postres"""
        response = self.make_request('GET', '/api/menu/platos/postres')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener postres", True, f"{len(response['data'])} postres encontrados")
    
    def test_obtener_platos_por_tipo(self):
        """Test para obtener platos por tipo"""
        # Test con tipo FONDO
        response = self.make_request('GET', '/api/menu/platos/tipo/FONDO')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener platos por tipo FONDO", True, f"{len(response['data'])} platos")
        
        # Test con tipo ENTRADA
        response = self.make_request('GET', '/api/menu/platos/tipo/ENTRADA')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener platos por tipo ENTRADA", True, f"{len(response['data'])} platos")
    
    # =========================
    # Tests de Bebidas
    # =========================
    
    def test_obtener_bebidas(self):
        """Test para obtener todas las bebidas"""
        response = self.make_request('GET', '/api/menu/bebidas')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener todas las bebidas", True, f"{len(response['data'])} bebidas encontradas")
    
    def test_obtener_bebidas_sin_alcohol(self):
        """Test para obtener bebidas sin alcohol"""
        response = self.make_request('GET', '/api/menu/bebidas/sin-alcohol')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        # Verificar que todas las bebidas no tienen alcohol
        for bebida in response['data']:
            assert bebida["con_alcohol"] == False
        self.print_test_result("Obtener bebidas sin alcohol", True, f"{len(response['data'])} bebidas")
    
    def test_obtener_bebidas_con_alcohol(self):
        """Test para obtener bebidas con alcohol"""
        response = self.make_request('GET', '/api/menu/bebidas/con-alcohol')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        # Verificar que todas las bebidas tienen alcohol
        for bebida in response['data']:
            assert bebida["con_alcohol"] == True
        self.print_test_result("Obtener bebidas con alcohol", True, f"{len(response['data'])} bebidas")
    
    # =========================
    # Tests de Ingredientes
    # =========================
    
    def test_obtener_ingredientes(self):
        """Test para obtener todos los ingredientes"""
        response = self.make_request('GET', '/api/menu/ingredientes')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        assert len(response['data']) > 0
        self.print_test_result("Obtener ingredientes", True, f"{len(response['data'])} ingredientes encontrados")
    
    def test_obtener_ingrediente_por_id(self):
        """Test para obtener ingrediente por ID"""
        # Test con ID válido
        response = self.make_request('GET', '/api/menu/ingredientes/1')
        self.assert_success_response(response)
        assert response['data']['id'] == 1
        assert 'nombre' in response['data']
        self.print_test_result("Obtener ingrediente por ID (válido)", True)
        
        # Test con ID inválido
        response = self.make_request('GET', '/api/menu/ingredientes/999')
        self.assert_error_response(response, 404)
        self.print_test_result("Obtener ingrediente por ID (inválido)", True, "Maneja error correctamente")
    
    def test_buscar_ingredientes_por_nombre(self):
        """Test para buscar ingredientes por nombre"""
        response = self.make_request('GET', '/api/menu/ingredientes/buscar?nombre=pescado')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        # Verificar que al menos un resultado contiene "pescado"
        assert any("pescado" in ing["nombre"].lower() for ing in response['data'])
        self.print_test_result("Buscar ingredientes por nombre", True, f"{len(response['data'])} resultados para 'pescado'")
    
    # =========================
    # Tests de Filtros
    # =========================
    
    def test_filtrar_por_categoria(self):
        """Test para filtrar por categoría"""
        response = self.make_request('GET', '/api/menu/filtrar/categoria?categoria=Plato principal')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Filtrar por categoría", True, f"{len(response['data'])} items en 'Plato principal'")
    
    def test_filtrar_por_alergenos(self):
        """Test para filtrar por alérgenos"""
        response = self.make_request('GET', '/api/menu/filtrar/alergenos?alergenos=PESCADO')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Filtrar por alérgenos", True, f"{len(response['data'])} items con PESCADO")
    
    def test_filtrar_sin_alergenos(self):
        """Test para filtrar sin alérgenos"""
        response = self.make_request('GET', '/api/menu/filtrar/sin-alergenos?alergenos=PESCADO,MARISCOS')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Filtrar sin alérgenos", True, f"{len(response['data'])} items sin PESCADO/MARISCOS")
    
    def test_obtener_items_por_ingrediente(self):
        """Test para obtener items por ingrediente"""
        response = self.make_request('GET', '/api/menu/items/ingrediente/1')
        self.assert_success_response(response)
        assert isinstance(response['data'], list)
        self.print_test_result("Obtener items por ingrediente", True, f"{len(response['data'])} items con ingrediente ID 1")
    
    # =========================
    # Tests de Menú Completo
    # =========================
    
    def test_obtener_menu_completo(self):
        """Test para obtener menú completo organizado"""
        response = self.make_request('GET', '/api/menu/completo')
        self.assert_success_response(response)
        data = response['data']
        assert "entradas" in data
        assert "platos_principales" in data
        assert "postres" in data
        assert "bebidas_sin_alcohol" in data
        assert "bebidas_con_alcohol" in data
        self.print_test_result("Obtener menú completo", True, "Menú organizado correctamente")
    
    def test_obtener_estadisticas_menu(self):
        """Test para obtener estadísticas del menú"""
        response = self.make_request('GET', '/api/menu/estadisticas')
        self.assert_success_response(response)
        data = response['data']
        assert "total_items" in data
        assert "total_platos" in data
        assert "total_bebidas" in data
        assert "items_disponibles" in data
        self.print_test_result("Obtener estadísticas del menú", True)
    
    # =========================
    # Tests de Acompañamientos
    # =========================
    
    def test_obtener_acompanamientos_item(self):
        """Test para obtener acompañamientos de un item"""
        response = self.make_request('GET', '/api/menu/items/1/acompanamientos')
        self.assert_success_response(response)
        data = response['data']
        assert "item_id" in data
        assert "acompanamientos" in data
        self.print_test_result("Obtener acompañamientos de item", True)
    
    def test_obtener_todos_acompanamientos(self):
        """Test para obtener todos los acompañamientos"""
        response = self.make_request('GET', '/api/menu/acompanamientos')
        self.assert_success_response(response)
        data = response['data']
        assert "acompanamientos" in data
        assert "total_acompanamientos" in data
        self.print_test_result("Obtener todos los acompañamientos", True)
    
    # =========================
    # Tests de Validación
    # =========================
    
    def test_validar_disponibilidad_item(self):
        """Test para validar disponibilidad de item"""
        response = self.make_request('GET', '/api/menu/validar-disponibilidad/1?cantidad=1')
        self.assert_success_response(response)
        data = response['data']
        assert "item_id" in data
        assert "disponible" in data
        assert "mensaje" in data
        self.print_test_result("Validar disponibilidad de item", True)
    
    def test_validar_disponibilidad_multiple(self):
        """Test para validar disponibilidad de múltiples items"""
        items_data = [
            {"item_id": 1, "cantidad": 1},
            {"item_id": 2, "cantidad": 2}
        ]
        response = self.make_request('POST', '/api/menu/validar-disponibilidad-multiple', json=items_data)
        self.assert_success_response(response)
        data = response['data']
        assert "todos_disponibles" in data
        assert "resultados" in data
        assert "total_items" in data
        self.print_test_result("Validar disponibilidad múltiple", True)

def run_all_tests():
    """Función para ejecutar todos los tests del módulo Menu y Carta"""
    print("🚀 Iniciando tests de endpoints - Módulo Menu y Carta...")
    print("=" * 60)
    
    test_instance = TestMenuYCartaEndpoints()
    
    # Lista de todos los métodos de test organizados por categoría
    test_categories = {
        "Endpoints Básicos": [
            test_instance.test_root_endpoint,
            test_instance.test_health_check,
        ],
        "Gestión de Items": [
            test_instance.test_obtener_todos_los_items,
            test_instance.test_obtener_item_por_id,
            test_instance.test_obtener_items_disponibles,
            test_instance.test_buscar_items_por_nombre,
        ],
        "Gestión de Platos": [
            test_instance.test_obtener_platos,
            test_instance.test_obtener_entradas,
            test_instance.test_obtener_platos_principales,
            test_instance.test_obtener_postres,
            test_instance.test_obtener_platos_por_tipo,
        ],
        "Gestión de Bebidas": [
            test_instance.test_obtener_bebidas,
            test_instance.test_obtener_bebidas_sin_alcohol,
            test_instance.test_obtener_bebidas_con_alcohol,
        ],
        "Gestión de Ingredientes": [
            test_instance.test_obtener_ingredientes,
            test_instance.test_obtener_ingrediente_por_id,
            test_instance.test_buscar_ingredientes_por_nombre,
        ],
        "Filtros y Búsquedas": [
            test_instance.test_filtrar_por_categoria,
            test_instance.test_filtrar_por_alergenos,
            test_instance.test_filtrar_sin_alergenos,
            test_instance.test_obtener_items_por_ingrediente,
        ],
        "Menú Completo": [
            test_instance.test_obtener_menu_completo,
            test_instance.test_obtener_estadisticas_menu,
        ],
        "Acompañamientos": [
            test_instance.test_obtener_acompanamientos_item,
            test_instance.test_obtener_todos_acompanamientos,
        ],
        "Validaciones": [
            test_instance.test_validar_disponibilidad_item,
            test_instance.test_validar_disponibilidad_multiple,
        ]
    }
    
    passed = 0
    failed = 0
    category_results = {}
    
    for category_name, test_methods in test_categories.items():
        print(f"\n📂 {category_name}")
        print("-" * 40)
        
        category_passed = 0
        category_failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                category_passed += 1
            except Exception as e:
                print(f"❌ Error en {test_method.__name__}: {str(e)}")
                failed += 1
                category_failed += 1
        
        category_results[category_name] = {
            'passed': category_passed,
            'failed': category_failed,
            'total': category_passed + category_failed
        }
    
    print("\n" + "=" * 60)
    print(f"📊 Resumen por categorías:")
    for category, results in category_results.items():
        success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"  {category}: {results['passed']}/{results['total']} ({success_rate:.1f}%)")
    
    print(f"\n📊 Resumen general:")
    print(f"✅ Exitosos: {passed}")
    print(f"❌ Fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Tasa de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("🎉 ¡Todos los tests del módulo Menu y Carta pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()
