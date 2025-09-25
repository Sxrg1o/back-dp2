"""
Tests del módulo Gestión de Pedidos - Reorganizados con mejor estructura.
"""
import sys
import os
from typing import Dict, List
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app
from tests.utils import TestBase, create_test_data

# Configurar cliente de prueba
client = TestClient(app)

class TestGestionPedidosEndpoints(TestBase):
    """Tests organizados para el módulo Gestión de Pedidos"""
    
    def __init__(self):
        super().__init__()
        self.test_data = create_test_data()
    
    # =========================
    # Tests de Gestión de Órdenes
    # =========================
    
    def test_crear_orden(self):
        """Test para crear una nueva orden"""
        orden_data = self.test_data['test_orden']
        response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        self.assert_success_response(response)
        data = response['data']
        assert "id" in data
        assert "numero_orden" in data
        assert data["comentarios"] == "Orden de prueba"
        self.print_test_result("Crear orden", True)
    
    def test_obtener_ordenes(self):
        """Test para obtener todas las órdenes"""
        response = self.make_request('GET', '/api/pedidos/ordenes')
        self.assert_success_response(response)
        data = response['data']
        assert "ordenes" in data
        assert "total" in data
        assert isinstance(data["ordenes"], list)
        self.print_test_result("Obtener órdenes", True, f"{data['total']} órdenes encontradas")
    
    def test_obtener_orden_por_id(self):
        """Test para obtener orden por ID"""
        # Primero crear una orden
        orden_data = {"mesa_id": 2, "comentarios": "Test orden"}
        create_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response['data']["id"]
        
        # Obtener la orden
        response = self.make_request('GET', f'/api/pedidos/ordenes/{orden_id}')
        self.assert_success_response(response)
        data = response['data']
        assert data["id"] == orden_id
        self.print_test_result("Obtener orden por ID", True)
    
    def test_agregar_item_a_orden(self):
        """Test para agregar item a una orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test agregar item"}
        create_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response['data']["id"]
        
        # Agregar item
        item_data = self.test_data['test_item_orden']
        response = self.make_request('POST', f'/api/pedidos/ordenes/{orden_id}/items', json=item_data)
        self.assert_success_response(response)
        data = response['data']
        assert "mensaje" in data
        self.print_test_result("Agregar item a orden", True)
    
    def test_cambiar_estado_orden(self):
        """Test para cambiar estado de orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test cambio estado"}
        create_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response['data']["id"]
        
        # Cambiar estado
        estado_data = {
            "orden_id": orden_id,
            "nuevo_estado": "EN_PREPARACION"
        }
        response = self.make_request('PUT', f'/api/pedidos/ordenes/{orden_id}/estado', json=estado_data)
        self.assert_success_response(response)
        data = response['data']
        assert "mensaje" in data
        self.print_test_result("Cambiar estado de orden", True)
    
    def test_validar_disponibilidad_orden(self):
        """Test para validar disponibilidad de orden"""
        # Crear orden con items
        orden_data = {"mesa_id": 1, "comentarios": "Test validación"}
        create_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response['data']["id"]
        
        # Agregar item
        item_data = {"item_id": 1, "cantidad": 1}
        self.make_request('POST', f'/api/pedidos/ordenes/{orden_id}/items', json=item_data)
        
        # Validar disponibilidad
        response = self.make_request('GET', f'/api/pedidos/ordenes/{orden_id}/validar-disponibilidad')
        self.assert_success_response(response)
        data = response['data']
        assert "orden_id" in data
        assert "todos_disponibles" in data
        self.print_test_result("Validar disponibilidad de orden", True)
    
    # =========================
    # Tests de Gestión de Meseros
    # =========================
    
    def test_obtener_meseros(self):
        """Test para obtener meseros"""
        response = self.make_request('GET', '/api/pedidos/meseros')
        self.assert_success_response(response)
        data = response['data']
        assert "meseros" in data
        assert "total" in data
        assert isinstance(data["meseros"], list)
        self.print_test_result("Obtener meseros", True, f"{data['total']} meseros encontrados")
    
    def test_crear_mesero(self):
        """Test para crear mesero"""
        mesero_data = self.test_data['test_mesero']
        response = self.make_request('POST', '/api/pedidos/meseros', json=mesero_data)
        self.assert_success_response(response)
        data = response['data']
        assert data["nombre"] == "Test Mesero"
        assert data["activo"] == True
        self.print_test_result("Crear mesero", True)
    
    def test_obtener_mesero_por_id(self):
        """Test para obtener mesero por ID"""
        # Crear mesero primero
        mesero_data = {"nombre": "Test Mesero ID", "activo": True}
        create_response = self.make_request('POST', '/api/pedidos/meseros', json=mesero_data)
        mesero_id = create_response['data']["id"]
        
        # Obtener mesero
        response = self.make_request('GET', f'/api/pedidos/meseros/{mesero_id}')
        self.assert_success_response(response)
        data = response['data']
        assert data["id"] == mesero_id
        self.print_test_result("Obtener mesero por ID", True)
    
    def test_asignar_mesero_a_orden(self):
        """Test para asignar mesero a orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test asignar mesero"}
        create_orden_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_orden_response['data']["id"]
        
        # Crear mesero
        mesero_data = {"nombre": "Mesero Test", "activo": True}
        create_mesero_response = self.make_request('POST', '/api/pedidos/meseros', json=mesero_data)
        mesero_id = create_mesero_response['data']["id"]
        
        # Asignar mesero
        asignar_data = {"orden_id": orden_id, "mesero_id": mesero_id}
        response = self.make_request('POST', f'/api/pedidos/ordenes/{orden_id}/meseros', json=asignar_data)
        self.assert_success_response(response)
        self.print_test_result("Asignar mesero a orden", True)
    
    # =========================
    # Tests de Gestión de Mesas
    # =========================
    
    def test_obtener_mesas(self):
        """Test para obtener mesas"""
        response = self.make_request('GET', '/api/pedidos/mesas')
        self.assert_success_response(response)
        data = response['data']
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        self.print_test_result("Obtener mesas", True, f"{data['total']} mesas encontradas")
    
    def test_obtener_mesas_disponibles(self):
        """Test para obtener mesas disponibles"""
        response = self.make_request('GET', '/api/pedidos/mesas/disponibles')
        self.assert_success_response(response)
        data = response['data']
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        self.print_test_result("Obtener mesas disponibles", True, f"{data['total']} mesas disponibles")
    
    def test_crear_grupo_mesa(self):
        """Test para crear grupo de mesa"""
        mesa_data = self.test_data['test_mesa']
        response = self.make_request('POST', '/api/pedidos/mesas', json=mesa_data)
        self.assert_success_response(response)
        data = response['data']
        assert data["nombre"] == "Mesa Test"
        assert data["capacidad"] == 4
        self.print_test_result("Crear grupo de mesa", True)
    
    def test_obtener_mesa_por_id(self):
        """Test para obtener mesa por ID"""
        # Crear mesa primero
        mesa_data = {"nombre": "Mesa Test ID", "capacidad": 2, "tipo": "PAREJA", "ubicacion": "Interior"}
        create_response = self.make_request('POST', '/api/pedidos/mesas', json=mesa_data)
        mesa_id = create_response['data']["id"]
        
        # Obtener mesa
        response = self.make_request('GET', f'/api/pedidos/mesas/{mesa_id}')
        self.assert_success_response(response)
        data = response['data']
        assert data["id"] == mesa_id
        self.print_test_result("Obtener mesa por ID", True)
    
    # =========================
    # Tests de Estadísticas y Reportes
    # =========================
    
    def test_obtener_estadisticas_pedidos(self):
        """Test para obtener estadísticas de pedidos"""
        response = self.make_request('GET', '/api/pedidos/estadisticas')
        self.assert_success_response(response)
        data = response['data']
        assert "total_ordenes" in data
        assert "ordenes_en_cola" in data
        assert "monto_total_dia" in data
        self.print_test_result("Obtener estadísticas de pedidos", True)
    
    def test_obtener_resumen_ordenes(self):
        """Test para obtener resumen de órdenes"""
        response = self.make_request('GET', '/api/pedidos/resumen')
        self.assert_success_response(response)
        data = response['data']
        assert isinstance(data, list)
        self.print_test_result("Obtener resumen de órdenes", True, f"{len(data)} resúmenes")
    
    # =========================
    # Tests de Modificación de Items en Órdenes
    # =========================
    
    def test_modificar_item_orden(self):
        """Test para modificar item en orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test modificar item"}
        create_orden_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_orden_response['data']["id"]
        
        # Agregar item
        item_data = {"item_id": 1, "cantidad": 2, "comentarios": "Original"}
        add_item_response = self.make_request('POST', f'/api/pedidos/ordenes/{orden_id}/items', json=item_data)
        item_orden_id = add_item_response['data'].get("item_orden_id", 1)  # Asumir ID 1 si no se retorna
        
        # Modificar item
        modificar_data = {
            "item_orden_id": item_orden_id,
            "cantidad": 3,
            "comentarios": "Modificado"
        }
        response = self.make_request('PUT', f'/api/pedidos/ordenes/{orden_id}/items/{item_orden_id}', json=modificar_data)
        self.assert_success_response(response)
        self.print_test_result("Modificar item en orden", True)
    
    def test_remover_item_orden(self):
        """Test para remover item de orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test remover item"}
        create_orden_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_orden_response['data']["id"]
        
        # Agregar item
        item_data = {"item_id": 1, "cantidad": 1}
        add_item_response = self.make_request('POST', f'/api/pedidos/ordenes/{orden_id}/items', json=item_data)
        item_orden_id = add_item_response['data'].get("item_orden_id", 1)  # Asumir ID 1 si no se retorna
        
        # Remover item
        response = self.make_request('DELETE', f'/api/pedidos/ordenes/{orden_id}/items/{item_orden_id}')
        self.assert_success_response(response)
        self.print_test_result("Remover item de orden", True)
    
    def test_cancelar_orden(self):
        """Test para cancelar orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test cancelar"}
        create_response = self.make_request('POST', '/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response['data']["id"]
        
        # Cancelar orden
        response = self.make_request('DELETE', f'/api/pedidos/ordenes/{orden_id}/cancelar?razon=Test')
        self.assert_success_response(response)
        self.print_test_result("Cancelar orden", True)

def run_all_tests():
    """Función para ejecutar todos los tests del módulo Gestión de Pedidos"""
    print("🚀 Iniciando tests de endpoints - Módulo Gestión de Pedidos...")
    print("=" * 60)
    
    test_instance = TestGestionPedidosEndpoints()
    
    # Lista de todos los métodos de test organizados por categoría
    test_categories = {
        "Gestión de Órdenes": [
            test_instance.test_crear_orden,
            test_instance.test_obtener_ordenes,
            test_instance.test_obtener_orden_por_id,
            test_instance.test_agregar_item_a_orden,
            test_instance.test_cambiar_estado_orden,
            test_instance.test_validar_disponibilidad_orden,
        ],
        "Gestión de Meseros": [
            test_instance.test_obtener_meseros,
            test_instance.test_crear_mesero,
            test_instance.test_obtener_mesero_por_id,
            test_instance.test_asignar_mesero_a_orden,
        ],
        "Gestión de Mesas": [
            test_instance.test_obtener_mesas,
            test_instance.test_obtener_mesas_disponibles,
            test_instance.test_crear_grupo_mesa,
            test_instance.test_obtener_mesa_por_id,
        ],
        "Estadísticas y Reportes": [
            test_instance.test_obtener_estadisticas_pedidos,
            test_instance.test_obtener_resumen_ordenes,
        ],
        "Modificación de Items": [
            test_instance.test_modificar_item_orden,
            test_instance.test_remover_item_orden,
            test_instance.test_cancelar_orden,
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
        print("🎉 ¡Todos los tests del módulo Gestión de Pedidos pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()
