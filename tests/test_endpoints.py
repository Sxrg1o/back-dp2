import json
import sys
import os
from typing import Dict, List
from fastapi.testclient import TestClient

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Configurar cliente de prueba
client = TestClient(app)

class TestEndpoints:
    """Clase para probar todos los endpoints de la API"""
    
    def test_root_endpoint(self):
        """Test para el endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
        print("✅ Root endpoint funcionando correctamente")
    
    def test_health_check(self):
        """Test para el health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        print("✅ Health check funcionando correctamente")
    
    # =========================
    # Tests de Items
    # =========================
    
    def test_obtener_todos_los_items(self):
        """Test para obtener todos los items"""
        response = client.get("/api/menu/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ Todos los items: {len(data)} items encontrados")
    
    def test_obtener_item_por_id(self):
        """Test para obtener item por ID"""
        # Test con ID válido
        response = client.get("/api/menu/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "nombre" in data
        print("✅ Item por ID (válido) funcionando")
        
        # Test con ID inválido
        response = client.get("/api/menu/items/999")
        assert response.status_code == 404
        print("✅ Item por ID (inválido) maneja error correctamente")
    
    def test_obtener_items_disponibles(self):
        """Test para obtener items disponibles"""
        response = client.get("/api/menu/items/disponibles")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todos los items están disponibles
        for item in data:
            assert item["disponible"] == True
            assert item["stock"] > 0
        print(f"✅ Items disponibles: {len(data)} items")
    
    def test_buscar_items_por_nombre(self):
        """Test para buscar items por nombre"""
        response = client.get("/api/menu/items/buscar?nombre=ceviche")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que al menos un resultado contiene "ceviche"
        assert any("ceviche" in item["nombre"].lower() for item in data)
        print(f"✅ Búsqueda por nombre: {len(data)} resultados para 'ceviche'")
    
    # =========================
    # Tests de Platos
    # =========================
    
    def test_obtener_platos(self):
        """Test para obtener todos los platos"""
        response = client.get("/api/menu/platos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ Todos los platos: {len(data)} platos encontrados")
    
    def test_obtener_entradas(self):
        """Test para obtener entradas"""
        response = client.get("/api/menu/platos/entradas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Entradas: {len(data)} entradas encontradas")
    
    def test_obtener_platos_principales(self):
        """Test para obtener platos principales"""
        response = client.get("/api/menu/platos/principales")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Platos principales: {len(data)} platos encontrados")
    
    def test_obtener_postres(self):
        """Test para obtener postres"""
        response = client.get("/api/menu/platos/postres")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Postres: {len(data)} postres encontrados")
    
    def test_obtener_platos_por_tipo(self):
        """Test para obtener platos por tipo"""
        # Test con tipo FONDO
        response = client.get("/api/menu/platos/tipo/FONDO")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Platos por tipo FONDO: {len(data)} platos")
        
        # Test con tipo ENTRADA
        response = client.get("/api/menu/platos/tipo/ENTRADA")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Platos por tipo ENTRADA: {len(data)} platos")
    
    # =========================
    # Tests de Bebidas
    # =========================
    
    def test_obtener_bebidas(self):
        """Test para obtener todas las bebidas"""
        response = client.get("/api/menu/bebidas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Todas las bebidas: {len(data)} bebidas encontradas")
    
    def test_obtener_bebidas_sin_alcohol(self):
        """Test para obtener bebidas sin alcohol"""
        response = client.get("/api/menu/bebidas/sin-alcohol")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todas las bebidas no tienen alcohol
        for bebida in data:
            assert bebida["con_alcohol"] == False
        print(f"✅ Bebidas sin alcohol: {len(data)} bebidas")
    
    def test_obtener_bebidas_con_alcohol(self):
        """Test para obtener bebidas con alcohol"""
        response = client.get("/api/menu/bebidas/con-alcohol")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todas las bebidas tienen alcohol
        for bebida in data:
            assert bebida["con_alcohol"] == True
        print(f"✅ Bebidas con alcohol: {len(data)} bebidas")
    
    # =========================
    # Tests de Ingredientes
    # =========================
    
    def test_obtener_ingredientes(self):
        """Test para obtener todos los ingredientes"""
        response = client.get("/api/menu/ingredientes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ Ingredientes: {len(data)} ingredientes encontrados")
    
    def test_obtener_ingrediente_por_id(self):
        """Test para obtener ingrediente por ID"""
        # Test con ID válido
        response = client.get("/api/menu/ingredientes/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "nombre" in data
        print("✅ Ingrediente por ID (válido) funcionando")
        
        # Test con ID inválido
        response = client.get("/api/menu/ingredientes/999")
        assert response.status_code == 404
        print("✅ Ingrediente por ID (inválido) maneja error correctamente")
    
    def test_buscar_ingredientes_por_nombre(self):
        """Test para buscar ingredientes por nombre"""
        response = client.get("/api/menu/ingredientes/buscar?nombre=pescado")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que al menos un resultado contiene "pescado"
        assert any("pescado" in ing["nombre"].lower() for ing in data)
        print(f"✅ Búsqueda de ingredientes: {len(data)} resultados para 'pescado'")
    
    # =========================
    # Tests de Filtros
    # =========================
    
    def test_filtrar_por_categoria(self):
        """Test para filtrar por categoría"""
        response = client.get("/api/menu/filtrar/categoria?categoria=Plato principal")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Filtro por categoría: {len(data)} items en 'Plato principal'")
    
    def test_filtrar_por_alergenos(self):
        """Test para filtrar por alérgenos"""
        response = client.get("/api/menu/filtrar/alergenos?alergenos=PESCADO")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Filtro por alérgenos: {len(data)} items con PESCADO")
    
    def test_filtrar_sin_alergenos(self):
        """Test para filtrar sin alérgenos"""
        response = client.get("/api/menu/filtrar/sin-alergenos?alergenos=PESCADO,MARISCOS")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Filtro sin alérgenos: {len(data)} items sin PESCADO/MARISCOS")
    
    def test_obtener_items_por_ingrediente(self):
        """Test para obtener items por ingrediente"""
        response = client.get("/api/menu/items/ingrediente/1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Items por ingrediente: {len(data)} items con ingrediente ID 1")
    
    # =========================
    # Tests de Menú Completo
    # =========================
    
    def test_obtener_menu_completo(self):
        """Test para obtener menú completo organizado"""
        response = client.get("/api/menu/completo")
        assert response.status_code == 200
        data = response.json()
        assert "entradas" in data
        assert "platos_principales" in data
        assert "postres" in data
        assert "bebidas_sin_alcohol" in data
        assert "bebidas_con_alcohol" in data
        print("✅ Menú completo organizado funcionando")
    
    def test_obtener_estadisticas_menu(self):
        """Test para obtener estadísticas del menú"""
        response = client.get("/api/menu/estadisticas")
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert "total_platos" in data
        assert "total_bebidas" in data
        assert "items_disponibles" in data
        print("✅ Estadísticas del menú funcionando")
    
    # =========================
    # Tests de Acompañamientos
    # =========================
    
    def test_obtener_acompanamientos_item(self):
        """Test para obtener acompañamientos de un item"""
        response = client.get("/api/menu/items/1/acompanamientos")
        assert response.status_code == 200
        data = response.json()
        assert "item_id" in data
        assert "acompanamientos" in data
        print("✅ Acompañamientos de item funcionando")
    
    def test_obtener_todos_acompanamientos(self):
        """Test para obtener todos los acompañamientos"""
        response = client.get("/api/menu/acompanamientos")
        assert response.status_code == 200
        data = response.json()
        assert "acompanamientos" in data
        assert "total_acompanamientos" in data
        print("✅ Todos los acompañamientos funcionando")
    
    # =========================
    # Tests de Validación
    # =========================
    
    def test_validar_disponibilidad_item(self):
        """Test para validar disponibilidad de item"""
        response = client.get("/api/menu/validar-disponibilidad/1?cantidad=1")
        assert response.status_code == 200
        data = response.json()
        assert "item_id" in data
        assert "disponible" in data
        assert "mensaje" in data
        print("✅ Validación de disponibilidad funcionando")
    
    def test_validar_disponibilidad_multiple(self):
        """Test para validar disponibilidad de múltiples items"""
        items_data = [
            {"item_id": 1, "cantidad": 1},
            {"item_id": 2, "cantidad": 2}
        ]
        response = client.post("/api/menu/validar-disponibilidad-multiple", json=items_data)
        assert response.status_code == 200
        data = response.json()
        assert "todos_disponibles" in data
        assert "resultados" in data
        assert "total_items" in data
        print("✅ Validación múltiple funcionando")

def run_all_tests():
    """Función para ejecutar todos los tests"""
    print("🚀 Iniciando tests de endpoints...")
    print("=" * 50)
    
    test_instance = TestEndpoints()
    
    # Lista de todos los métodos de test
    test_methods = [
        test_instance.test_root_endpoint,
        test_instance.test_health_check,
        test_instance.test_obtener_todos_los_items,
        test_instance.test_obtener_item_por_id,
        test_instance.test_obtener_items_disponibles,
        test_instance.test_buscar_items_por_nombre,
        test_instance.test_obtener_platos,
        test_instance.test_obtener_entradas,
        test_instance.test_obtener_platos_principales,
        test_instance.test_obtener_postres,
        test_instance.test_obtener_platos_por_tipo,
        test_instance.test_obtener_bebidas,
        test_instance.test_obtener_bebidas_sin_alcohol,
        test_instance.test_obtener_bebidas_con_alcohol,
        test_instance.test_obtener_ingredientes,
        test_instance.test_obtener_ingrediente_por_id,
        test_instance.test_buscar_ingredientes_por_nombre,
        test_instance.test_filtrar_por_categoria,
        test_instance.test_filtrar_por_alergenos,
        test_instance.test_filtrar_sin_alergenos,
        test_instance.test_obtener_items_por_ingrediente,
        test_instance.test_obtener_menu_completo,
        test_instance.test_obtener_estadisticas_menu,
        test_instance.test_obtener_acompanamientos_item,
        test_instance.test_obtener_todos_acompanamientos,
        test_instance.test_validar_disponibilidad_item,
        test_instance.test_validar_disponibilidad_multiple,
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
    
    print("=" * 50)
    print(f"📊 Resumen de tests:")
    print(f"✅ Exitosos: {passed}")
    print(f"❌ Fallidos: {failed}")
    print(f"📈 Total: {passed + failed}")
    print(f"🎯 Tasa de éxito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("🎉 ¡Todos los tests pasaron exitosamente!")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()
