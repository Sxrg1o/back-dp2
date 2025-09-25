import json
import sys
import os
from typing import Dict, List
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app

# Configurar cliente de prueba
client = TestClient(app)

class TestPedidosEndpoints:
    """Clase para probar todos los endpoints del módulo de gestión de pedidos"""
    
    def test_crear_orden(self):
        """Test para crear una nueva orden"""
        orden_data = {
            "mesa_id": 1,
            "comentarios": "Orden de prueba",
            "mesero_ids": [1]
        }
        response = client.post("/api/pedidos/ordenes", json=orden_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "numero_orden" in data
        assert data["comentarios"] == "Orden de prueba"
        print("✅ Crear orden funcionando correctamente")
    
    def test_obtener_ordenes(self):
        """Test para obtener todas las órdenes"""
        response = client.get("/api/pedidos/ordenes")
        assert response.status_code == 200
        data = response.json()
        assert "ordenes" in data
        assert "total" in data
        assert isinstance(data["ordenes"], list)
        print(f"✅ Obtener órdenes: {data['total']} órdenes encontradas")
    
    def test_obtener_orden_por_id(self):
        """Test para obtener orden por ID"""
        # Primero crear una orden
        orden_data = {"mesa_id": 2, "comentarios": "Test orden"}
        create_response = client.post("/api/pedidos/ordenes", json=orden_data)
        orden_id = create_response.json()["id"]
        
        # Obtener la orden
        response = client.get(f"/api/pedidos/ordenes/{orden_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == orden_id
        print("✅ Obtener orden por ID funcionando")
    
    def test_agregar_item_a_orden(self):
        """Test para agregar item a una orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test agregar item"}
        create_response = client.post("/api/pedidos/ordenes", json=orden_data)
        orden_id = create_response.json()["id"]
        
        # Agregar item
        item_data = {
            "item_id": 1,  # Ceviche
            "cantidad": 2,
            "comentarios": "Sin cebolla"
        }
        response = client.post(f"/api/pedidos/ordenes/{orden_id}/items", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        print("✅ Agregar item a orden funcionando")
    
    def test_cambiar_estado_orden(self):
        """Test para cambiar estado de orden"""
        # Crear orden
        orden_data = {"mesa_id": 1, "comentarios": "Test cambio estado"}
        create_response = client.post("/api/pedidos/ordenes", json=orden_data)
        orden_id = create_response.json()["id"]
        
        # Cambiar estado
        estado_data = {
            "orden_id": orden_id,
            "nuevo_estado": "EN_PREPARACION"
        }
        response = client.put(f"/api/pedidos/ordenes/{orden_id}/estado", json=estado_data)
        assert response.status_code == 200
        data = response.json()
        assert "mensaje" in data
        print("✅ Cambiar estado de orden funcionando")
    
    def test_obtener_meseros(self):
        """Test para obtener meseros"""
        response = client.get("/api/pedidos/meseros")
        assert response.status_code == 200
        data = response.json()
        assert "meseros" in data
        assert "total" in data
        assert isinstance(data["meseros"], list)
        print(f"✅ Obtener meseros: {data['total']} meseros encontrados")
    
    def test_crear_mesero(self):
        """Test para crear mesero"""
        mesero_data = {
            "nombre": "Test Mesero",
            "activo": True
        }
        response = client.post("/api/pedidos/meseros", json=mesero_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Test Mesero"
        assert data["activo"] == True
        print("✅ Crear mesero funcionando")
    
    def test_obtener_mesas(self):
        """Test para obtener mesas"""
        response = client.get("/api/pedidos/mesas")
        assert response.status_code == 200
        data = response.json()
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        print(f"✅ Obtener mesas: {data['total']} mesas encontradas")
    
    def test_obtener_mesas_disponibles(self):
        """Test para obtener mesas disponibles"""
        response = client.get("/api/pedidos/mesas/disponibles")
        assert response.status_code == 200
        data = response.json()
        assert "mesas" in data
        assert "total" in data
        assert isinstance(data["mesas"], list)
        print(f"✅ Obtener mesas disponibles: {data['total']} mesas disponibles")
    
    def test_crear_grupo_mesa(self):
        """Test para crear grupo de mesa"""
        mesa_data = {
            "nombre": "Mesa Test",
            "capacidad": 4,
            "tipo": "FAMILIAR",
            "ubicacion": "Interior"
        }
        response = client.post("/api/pedidos/mesas", json=mesa_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Mesa Test"
        assert data["capacidad"] == 4
        print("✅ Crear grupo de mesa funcionando")
    
    def test_obtener_estadisticas_pedidos(self):
        """Test para obtener estadísticas de pedidos"""
        response = client.get("/api/pedidos/estadisticas")
        assert response.status_code == 200
        data = response.json()
        assert "total_ordenes" in data
        assert "ordenes_en_cola" in data
        assert "monto_total_dia" in data
        print("✅ Obtener estadísticas de pedidos funcionando")
    
    def test_obtener_resumen_ordenes(self):
        """Test para obtener resumen de órdenes"""
        response = client.get("/api/pedidos/resumen")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Obtener resumen de órdenes: {len(data)} resúmenes")
    
    def test_validar_disponibilidad_orden(self):
        """Test para validar disponibilidad de orden"""
        # Crear orden con items
        orden_data = {"mesa_id": 1, "comentarios": "Test validación"}
        create_response = client.post("/api/pedidos/ordenes", json=orden_data)
        orden_id = create_response.json()["id"]
        
        # Agregar item
        item_data = {"item_id": 1, "cantidad": 1}
        client.post(f"/api/pedidos/ordenes/{orden_id}/items", json=item_data)
        
        # Validar disponibilidad
        response = client.get(f"/api/pedidos/ordenes/{orden_id}/validar-disponibilidad")
        assert response.status_code == 200
        data = response.json()
        assert "orden_id" in data
        assert "todos_disponibles" in data
        print("✅ Validar disponibilidad de orden funcionando")

def run_all_tests():
    """Función para ejecutar todos los tests del módulo de gestión de pedidos"""
    print("🚀 Iniciando tests de endpoints - Módulo Gestión de Pedidos...")
    print("=" * 70)
    
    test_instance = TestPedidosEndpoints()
    
    # Lista de todos los métodos de test
    test_methods = [
        test_instance.test_crear_orden,
        test_instance.test_obtener_ordenes,
        test_instance.test_obtener_orden_por_id,
        test_instance.test_agregar_item_a_orden,
        test_instance.test_cambiar_estado_orden,
        test_instance.test_obtener_meseros,
        test_instance.test_crear_mesero,
        test_instance.test_obtener_mesas,
        test_instance.test_obtener_mesas_disponibles,
        test_instance.test_crear_grupo_mesa,
        test_instance.test_obtener_estadisticas_pedidos,
        test_instance.test_obtener_resumen_ordenes,
        test_instance.test_validar_disponibilidad_orden,
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_method()
            passed += 1
        except Exception as e:
            print(f"❌ Error en {test_method.__name__}: {str(e)}")
            failed += 1
    
    print("=" * 70)
    print(f"📊 Resumen de tests - Gestión de Pedidos:")
    print(f"✅ Exitosos: {passed}")
    print(f"❌ Fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Tasa de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("🎉 ¡Todos los tests del módulo de gestión de pedidos pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()
