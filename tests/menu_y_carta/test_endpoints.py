"""
Tests del módulo Menu y Carta - Actualizados con la nueva estructura.
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
        client = client
    
    # =========================
    # Tests de Endpoints Básicos
    # =========================
    
    def test_root_endpoint(self):
        """Test para el endpoint raíz"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'version' in data
        assert data['version'] == "1.0.0"
        print("OK Root endpoint")
    
    def test_health_check(self):
        """Test para el health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == "ok"
        print("OK Health check")
    
    # =========================
    # Tests de Items
    # =========================
    
    def test_obtener_todos_los_items(self):
        """Test para obtener todos los items"""
        response = client.get('/api/menu/items')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"OK Obtener todos los items: {len(data)} items encontrados")
    
    def test_obtener_item_por_id(self):
        """Test para obtener item por ID"""
        # Test con ID válido
        response = client.get('/api/menu/items/1')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 1
        assert 'nombre' in data
        assert 'categoria' in data
        assert 'alergenos' in data
        assert 'ingredientes' in data
        # Verificar que no hay campos eliminados
        assert 'tipo_item' not in data
        assert 'peso' not in data
        assert 'tipo' not in data
        assert 'litros' not in data
        assert 'con_alcohol' not in data
        print("OK Obtener item por ID (válido)")
        
        # Test con ID inválido
        response = client.get('/api/menu/items/999')
        assert response.status_code == 404
        print("OK Obtener item por ID (inválido) - maneja error correctamente")
    
    def test_obtener_items_disponibles(self):
        """Test para obtener items disponibles"""
        response = client.get('/api/menu/items/disponibles')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todos los items están disponibles
        for item in data:
            assert item["disponible"] == True
            assert item["stock"] > 0
        print(f"OK Obtener items disponibles: {len(data)} items disponibles")
    
    def test_buscar_items_por_nombre(self):
        """Test para buscar items por nombre"""
        response = client.get('/api/menu/items/buscar?nombre=ceviche')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que al menos un resultado contiene "ceviche"
        assert any("ceviche" in item["nombre"].lower() for item in data)
        print(f"OK Buscar items por nombre: {len(data)} resultados para 'ceviche'")
    
    def test_obtener_items_por_categoria(self):
        """Test para obtener items por categoría"""
        response = client.get('/api/menu/items/categoria/Plato Principal')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Verificar que todos los items pertenecen a la categoría
        for item in data:
            assert item["categoria"] == "Plato Principal"
        print(f"OK Obtener items por categoría: {len(data)} items en 'Plato Principal'")
    
    # =========================
    # Tests de Categorías
    # =========================
    
    def test_obtener_categorias(self):
        """Test para obtener todas las categorías"""
        response = client.get('/api/menu/categorias')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Verificar estructura de categoría
        for categoria in data:
            assert 'id' in categoria
            assert 'nombre' in categoria
            assert 'descripcion' in categoria
        print(f"OK Obtener categorías: {len(data)} categorías encontradas")
    
    def test_obtener_categoria_por_nombre(self):
        """Test para obtener categoría por nombre"""
        response = client.get('/api/menu/categorias/Plato Principal')
        assert response.status_code == 200
        data = response.json()
        assert data['nombre'] == "Plato Principal"
        assert 'id' in data
        assert 'descripcion' in data
        print("OK Obtener categoría por nombre")
        
        # Test con categoría inexistente
        response = client.get('/api/menu/categorias/CategoriaInexistente')
        assert response.status_code == 404
        print("OK Obtener categoría por nombre (inexistente) - maneja error correctamente")
    
    # =========================
    # Tests de Ingredientes
    # =========================
    
    def test_obtener_ingredientes(self):
        """Test para obtener todos los ingredientes"""
        response = client.get('/api/menu/ingredientes')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Verificar que son strings
        for ingrediente in data:
            assert isinstance(ingrediente, str)
        print(f"OK Obtener ingredientes: {len(data)} ingredientes encontrados")
    
    def test_buscar_ingredientes_por_nombre(self):
        """Test para buscar ingredientes por nombre"""
        response = client.get('/api/menu/ingredientes/buscar?nombre=pescado')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que al menos un resultado contiene "pescado"
        assert any("pescado" in ing.lower() for ing in data)
        print(f"OK Buscar ingredientes por nombre: {len(data)} resultados para 'pescado'")
    
    # =========================
    # Tests de Filtros
    # =========================
    
    def test_filtrar_por_categoria(self):
        """Test para filtrar por categoría"""
        response = client.get('/api/menu/filtrar/categoria?categoria=Plato principal')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"OK Filtrar por categoría: {len(data)} items en 'Plato principal'")
    
    def test_filtrar_por_alergenos(self):
        """Test para filtrar por alérgenos"""
        response = client.get('/api/menu/filtrar/alergenos?alergenos=PESCADO')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todos los items contienen el alérgeno
        for item in data:
            assert "PESCADO" in item["alergenos"]
        print(f"OK Filtrar por alérgenos: {len(data)} items con PESCADO")
    
    def test_filtrar_sin_alergenos(self):
        """Test para filtrar sin alérgenos"""
        response = client.get('/api/menu/filtrar/sin-alergenos?alergenos=PESCADO,MARISCOS')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verificar que ningún item contiene los alérgenos
        for item in data:
            assert not any(alergeno in item["alergenos"] for alergeno in ["PESCADO", "MARISCOS"])
        print(f"OK Filtrar sin alérgenos: {len(data)} items sin PESCADO/MARISCOS")
    
    def test_obtener_items_por_ingrediente(self):
        """Test para obtener items por ingrediente"""
        response = client.get('/api/menu/items/ingrediente/pescado')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"OK Obtener items por ingrediente: {len(data)} items con 'pescado'")
    
    # =========================
    # Tests de Menú Completo
    # =========================
    
    def test_obtener_menu_completo(self):
        """Test para obtener menú completo organizado"""
        response = client.get('/api/menu/completo')
        assert response.status_code == 200
        data = response.json()
        assert "entradas" in data
        assert "platos_principales" in data
        assert "postres" in data
        assert "bebidas_sin_alcohol" in data
        assert "bebidas_con_alcohol" in data
        print("OK Obtener menú completo: menú organizado correctamente")
    
    def test_obtener_estadisticas_menu(self):
        """Test para obtener estadísticas del menú"""
        response = client.get('/api/menu/estadisticas')
        assert response.status_code == 200
        data = response.json()
        assert "total_items" in data
        assert "total_platos" in data
        assert "total_bebidas" in data
        assert "items_disponibles" in data
        print("OK Obtener estadísticas del menú")
    
    # =========================
    # Tests de Acompañamientos
    # =========================
    
    def test_obtener_acompanamientos_item(self):
        """Test para obtener acompañamientos de un item"""
        response = client.get('/api/menu/items/1/acompanamientos')
        assert response.status_code == 200
        data = response.json()
        assert "item_id" in data
        assert "acompanamientos" in data
        print("OK Obtener acompañamientos de item")
    
    def test_obtener_todos_acompanamientos(self):
        """Test para obtener todos los acompañamientos"""
        response = client.get('/api/menu/acompanamientos')
        assert response.status_code == 200
        data = response.json()
        assert "acompanamientos" in data
        assert "total_acompanamientos" in data
        print("OK Obtener todos los acompañamientos")
    
    # =========================
    # Tests de Validación
    # =========================
    
    def test_validar_disponibilidad_item(self):
        """Test para validar disponibilidad de item"""
        response = client.get('/api/menu/validar-disponibilidad/1?cantidad=1')
        assert response.status_code == 200
        data = response.json()
        assert "item_id" in data
        assert "disponible" in data
        assert "mensaje" in data
        print("OK Validar disponibilidad de item")
    
    def test_validar_disponibilidad_multiple(self):
        """Test para validar disponibilidad de múltiples items"""
        items_data = [
            {"item_id": 1, "cantidad": 1},
            {"item_id": 2, "cantidad": 2}
        ]
        response = client.post('/api/menu/validar-disponibilidad-multiple', json=items_data)
        assert response.status_code == 200
        data = response.json()
        assert "todos_disponibles" in data
        assert "resultados" in data
        assert "total_items" in data
        print("OK Validar disponibilidad múltiple")

def run_all_tests():
    """Función para ejecutar todos los tests del módulo Menu y Carta"""
    print("Iniciando tests de endpoints - Modulo Menu y Carta...")
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
            test_instance.test_obtener_items_por_categoria,
        ],
        "Gestión de Categorías": [
            test_instance.test_obtener_categorias,
            test_instance.test_obtener_categoria_por_nombre,
        ],
        "Gestión de Ingredientes": [
            test_instance.test_obtener_ingredientes,
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
        print(f"\n{category_name}")
        print("-" * 40)
        
        category_passed = 0
        category_failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                category_passed += 1
            except Exception as e:
                print(f"ERROR en {test_method.__name__}: {str(e)}")
                failed += 1
                category_failed += 1
        
        category_results[category_name] = {
            'passed': category_passed,
            'failed': category_failed,
            'total': category_passed + category_failed
        }
    
    print("\n" + "=" * 60)
    print(f"Resumen por categorias:")
    for category, results in category_results.items():
        success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"  {category}: {results['passed']}/{results['total']} ({success_rate:.1f}%)")
    
    print(f"\nResumen general:")
    print(f"Exitosos: {passed}")
    print(f"Fallidos: {failed}")
    print(f"Total: {passed + failed}")
    print(f"Tasa de exito: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("Todos los tests del modulo Menu y Carta pasaron exitosamente!")
    else:
        print("Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    run_all_tests()