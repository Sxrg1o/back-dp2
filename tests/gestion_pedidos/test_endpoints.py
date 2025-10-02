"""
Tests del módulo Gestión de Pedidos - Actualizados con la nueva estructura.
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

class TestGestionPedidosEndpoints:
    """Tests organizados para el módulo Gestión de Pedidos"""
    
    def setup_method(self):
        """Setup para cada test"""
        client = client
    
    # =========================
    # Tests de Gestión de Órdenes
    # =========================
    
    def test_crear_orden(self):
        """Test para crear una nueva orden"""
        orden_data = {"mesa_id": 1, "comentarios": "Orden de prueba"}
        response = client.post('/api/pedidos/ordenes', json=orden_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "numero_orden" in data
        assert data["comentarios"] == "Orden de prueba"
        # Verificar que no hay tiempo_estimado
        assert "tiempo_estimado" not in data
        print("OK Crear orden")
    
    def test_obtener_ordenes(self):
        """Test para obtener todas las órdenes"""
        response = client.get('/api/pedidos/ordenes')
        assert response.status_code == 200
        data = response.json()
        assert "ordenes" in data
        assert "total" in data
        assert isinstance(data["ordenes"], list)
        # Verificar que no hay tiempo_estimado en las órdenes
        for orden in data["ordenes"]:
            assert "tiempo_estimado" not in orden
        print(f"OK Obtener órdenes: {data['total']} órdenes encontradas")
    
    def test_obtener_orden_por_id(self):
        """Test para obtener orden por ID"""
        # Usar una orden existente (ID 1)
        response = client.get('/api/pedidos/ordenes/1')
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        # Verificar que no hay tiempo_estimado
        assert "tiempo_estimado" not in data
        print("OK Obtener orden por ID")
    
    def test_agregar_item_a_orden(self):
        """Test para agregar item a una orden"""
        # Usar orden existente (ID 1)
        item_data = {"item_id": 7, "cantidad": 1, "comentarios": "Test chicha"}
        response = client.post('/api/pedidos/ordenes/1/items', json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        print("OK Agregar item a orden")
    
    def test_cambiar_estado_orden(self):
        """Test para cambiar estado de orden"""
        # Usar orden existente (ID 1)
        estado_data = {
            "orden_id": 1,
            "nuevo_estado": "EN_PREPARACION"
        }
        response = client.put('/api/pedidos/ordenes/1/estado', json=estado_data)
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        print("OK Cambiar estado de orden")
    
    def test_validar_disponibilidad_orden(self):
        """Test para validar disponibilidad de orden"""
        # Usar orden existente (ID 1)
        response = client.get('/api/pedidos/ordenes/1/validar-disponibilidad')
        assert response.status_code == 200
        data = response.json()
        assert "orden_id" in data
        assert "todos_disponibles" in data
        print("OK Validar disponibilidad de orden")
    
    # =========================
    # Tests de Gestión de Meseros
    # =========================
    
    def test_obtener_meseros(self):
        """Test para obtener meseros"""
        response = client.get('/api/pedidos/meseros')
        assert response.status_code == 200
        data = response.json()
        assert "meseros" in data
        assert "total" in data
        assert isinstance(data["meseros"], list)
        print(f"OK Obtener meseros: {data['total']} meseros encontrados")
    
    def test_crear_mesero(self):
        """Test para crear mesero"""
        mesero_data = {"nombre": "Test Mesero", "activo": True}
        response = client.post('/api/pedidos/meseros', json=mesero_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Test Mesero"
        assert data["activo"] == True
        print("OK Crear mesero")
    
    def test_obtener_mesero_por_id(self):
        """Test para obtener mesero por ID"""
        # Crear mesero primero
        mesero_data = {"nombre": "Test Mesero ID", "activo": True}
        create_response = client.post('/api/pedidos/meseros', json=mesero_data)
        mesero_id = create_response.json()["id"]
        
        # Obtener mesero
        response = client.get(f'/api/pedidos/meseros/{mesero_id}')
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mesero_id
        print("OK Obtener mesero por ID")
    
    def test_asignar_mesero_a_orden(self):
        """Test para asignar mesero a orden"""
        # Crear mesero
        mesero_data = {"nombre": "Mesero Test", "activo": True}
        create_mesero_response = client.post('/api/pedidos/meseros', json=mesero_data)
        mesero_id = create_mesero_response.json()["id"]
        
        # Asignar mesero a orden existente (ID 1)
        asignar_data = {"orden_id": 1, "mesero_id": mesero_id}
        response = client.post('/api/pedidos/ordenes/1/meseros', json=asignar_data)
        assert response.status_code == 200
        print("OK Asignar mesero a orden")
    
    # =========================
    # Tests de Gestión de Mesas
    # =========================
    
    def test_obtener_mesas(self):
        """Test para obtener mesas"""
        response = client.get('/api/pedidos/mesas')
        assert response.status_code == 200
        data = response.json()
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        print(f"OK Obtener mesas: {data['total']} mesas encontradas")
    
    def test_obtener_mesas_disponibles(self):
        """Test para obtener mesas disponibles"""
        response = client.get('/api/pedidos/mesas/disponibles')
        assert response.status_code == 200
        data = response.json()
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        print(f"OK Obtener mesas disponibles: {data['total']} mesas disponibles")
    
    def test_crear_grupo_mesa(self):
        """Test para crear grupo de mesa"""
        mesa_data = {"nombre": "Mesa Test", "capacidad": 4, "tipo": "FAMILIAR", "ubicacion": "Interior"}
        response = client.post('/api/pedidos/mesas', json=mesa_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Mesa Test"
        assert data["capacidad"] == 4
        print("OK Crear grupo de mesa")
    
    def test_obtener_mesa_por_id(self):
        """Test para obtener mesa por ID"""
        # Crear mesa primero
        mesa_data = {"nombre": "Mesa Test ID", "capacidad": 2, "tipo": "PAREJA", "ubicacion": "Interior"}
        create_response = client.post('/api/pedidos/mesas', json=mesa_data)
        mesa_id = create_response.json()["id"]
        
        # Obtener mesa
        response = client.get(f'/api/pedidos/mesas/{mesa_id}')
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mesa_id
        print("OK Obtener mesa por ID")
    
    # =========================
    # Tests de Estadísticas y Reportes
    # =========================
    
    def test_obtener_estadisticas_pedidos(self):
        """Test para obtener estadísticas de pedidos"""
        response = client.get('/api/pedidos/estadisticas')
        assert response.status_code == 200
        data = response.json()
        assert "total_ordenes" in data
        assert "ordenes_en_cola" in data
        assert "monto_total_dia" in data
        print("OK Obtener estadísticas de pedidos")
    
    def test_obtener_resumen_ordenes(self):
        """Test para obtener resumen de órdenes"""
        response = client.get('/api/pedidos/resumen')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que no hay tiempo_estimado en los resúmenes
        for resumen in data:
            assert "tiempo_estimado" not in resumen
        print(f"OK Obtener resumen de órdenes: {len(data)} resúmenes")
    
    # =========================
    # Tests de Modificación de Items en Órdenes
    # =========================
    
    def test_modificar_item_orden(self):
        """Test para modificar item en orden"""
        # Agregar item a orden existente (ID 1)
        item_data = {"item_id": 2, "cantidad": 2, "comentarios": "Original"}
        add_item_response = client.post('/api/pedidos/ordenes/1/items', json=item_data)
        assert add_item_response.status_code == 200
        
        # Modificar item (asumir ID 1 para el item_orden)
        modificar_data = {
            "item_orden_id": 1,
            "cantidad": 3,
            "comentarios": "Modificado"
        }
        response = client.put('/api/pedidos/ordenes/1/items/1', json=modificar_data)
        assert response.status_code == 200
        print("OK Modificar item en orden")
    
    def test_remover_item_orden(self):
        """Test para remover item de orden"""
        # Agregar item a orden existente (ID 1)
        item_data = {"item_id": 3, "cantidad": 1}
        add_item_response = client.post('/api/pedidos/ordenes/1/items', json=item_data)
        assert add_item_response.status_code == 200
        
        # Remover item (asumir ID 1 para el item_orden)
        response = client.delete('/api/pedidos/ordenes/1/items/1')
        assert response.status_code == 200
        print("OK Remover item de orden")
    
    def test_cancelar_orden(self):
        """Test para cancelar orden"""
        # Crear orden para cancelar
        orden_data = {"mesa_id": 1, "comentarios": "Test cancelar"}
        create_response = client.post('/api/pedidos/ordenes', json=orden_data)
        orden_id = create_response.json()["id"]
        
        # Cancelar orden
        response = client.delete(f'/api/pedidos/ordenes/{orden_id}/cancelar?razon=Test')
        assert response.status_code == 200
        print("OK Cancelar orden")

def run_all_tests():
    """Función para ejecutar todos los tests del módulo Gestión de Pedidos"""
    print(" Iniciando tests de endpoints - Módulo Gestión de Pedidos...")
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
        print(f"\n {category_name}")
        print("-" * 40)
        
        category_passed = 0
        category_failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                category_passed += 1
            except Exception as e:
                print(f"ERROR Error en {test_method.__name__}: {str(e)}")
                failed += 1
                category_failed += 1
        
        category_results[category_name] = {
            'passed': category_passed,
            'failed': category_failed,
            'total': category_passed + category_failed
        }
    
    print("\n" + "=" * 60)
    print(f" Resumen por categorías:")
    for category, results in category_results.items():
        success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"  {category}: {results['passed']}/{results['total']} ({success_rate:.1f}%)")
    
    print(f"\n Resumen general:")
    print(f"OK Exitosos: {passed}")
    print(f"ERROR Fallidos: {failed}")
    print(f" Total: {passed + failed}")
    print(f" Tasa de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print(" ¡Todos los tests del módulo Gestión de Pedidos pasaron exitosamente!")
    else:
        print("  Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()