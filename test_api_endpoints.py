"""
Script para probar todos los endpoints de la API de Cevichería
Usando la URL de producción: https://back-dp2.onrender.com/
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from uuid import UUID

class CevicheriaAPITester:
    """Clase para probar todos los endpoints de la API de Cevichería."""
    
    def __init__(self, base_url: str = "https://back-dp2.onrender.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Variables para almacenar IDs creados
        self.created_ids = {
            'roles': [],
            'categorias': [],
            'alergenos': [],
            'productos': [],
            'tipos_opciones': [],
            'producto_opciones': [],
            'productos_alergenos': []
        }
    
    def log_response(self, method: str, endpoint: str, response: requests.Response, data: Any = None):
        """Log detallado de las respuestas."""
        print(f"\n{'='*60}")
        print(f"🔗 {method} {endpoint}")
        print(f"📊 Status: {response.status_code}")
        
        if data:
            print(f"📤 Request Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        try:
            response_data = response.json()
            print(f"📥 Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except:
            print(f"📥 Response (text): {response.text}")
        
        print(f"{'='*60}")
        return response
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> requests.Response:
        """Hacer una petición HTTP con logging."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
            
            return self.log_response(method, endpoint, response, data)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la petición: {e}")
            raise
    
    def test_health_endpoints(self):
        """Probar endpoints de salud e información."""
        print("\n🏥 PROBANDO ENDPOINTS DE SALUD")
        
        # Health check
        self.make_request('GET', '/health')
        
        # Root info
        self.make_request('GET', '/')
    
    def test_seed_endpoints(self):
        """Probar endpoints de seed."""
        print("\n🌱 PROBANDO ENDPOINTS DE SEED")
        
        # Verificar estado del seed
        response = self.make_request('GET', '/api/v1/seed/status')
        
        # Ejecutar seed (solo si es necesario)
        if response.status_code == 200:
            try:
                data = response.json()
                if not data.get('has_data', False):
                    print("\n🔄 Ejecutando seed...")
                    self.make_request('POST', '/api/v1/seed/execute', {'force': False})
                else:
                    print("✅ La base de datos ya tiene datos de seed")
            except:
                print("⚠️ No se pudo verificar el estado del seed")
    
    def test_roles(self):
        """Probar endpoints de roles."""
        print("\n👥 PROBANDO ENDPOINTS DE ROLES")
        
        # Listar roles existentes
        response = self.make_request('GET', '/api/v1/roles', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar el primer rol existente
                first_role = data['items'][0]
                self.created_ids['roles'].append(first_role['id'])
                print(f"✅ Usando rol existente: {first_role['nombre']} (ID: {first_role['id']})")
            else:
                # Crear un nuevo rol
                rol_data = {
                    "nombre": "Mesero Test",
                    "descripcion": "Rol creado para pruebas de API",
                    "activo": True
                }
                response = self.make_request('POST', '/api/v1/roles', rol_data)
                if response.status_code == 201:
                    data = response.json()
                    self.created_ids['roles'].append(data['id'])
                    print(f"✅ Rol creado: {data['nombre']} (ID: {data['id']})")
        
        # Obtener rol por ID
        if self.created_ids['roles']:
            rol_id = self.created_ids['roles'][0]
            self.make_request('GET', f'/api/v1/roles/{rol_id}')
    
    def test_categorias(self):
        """Probar endpoints de categorías."""
        print("\n📂 PROBANDO ENDPOINTS DE CATEGORÍAS")
        
        # Listar categorías existentes
        response = self.make_request('GET', '/api/v1/categorias', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar las primeras 3 categorías existentes
                for categoria in data['items'][:3]:
                    self.created_ids['categorias'].append(categoria['id'])
                    print(f"✅ Usando categoría existente: {categoria['nombre']} (ID: {categoria['id']})")
            else:
                # Crear categorías de ejemplo
                categorias_data = [
                    {
                        "nombre": "Ceviches Test",
                        "descripcion": "Ceviches para pruebas de API",
                        "imagen_path": "https://example.com/ceviches.jpg",
                        "activo": True
                    },
                    {
                        "nombre": "Bebidas Test",
                        "descripcion": "Bebidas para pruebas de API",
                        "imagen_path": "https://example.com/bebidas.jpg",
                        "activo": True
                    }
                ]
                
                for categoria_data in categorias_data:
                    response = self.make_request('POST', '/api/v1/categorias', categoria_data)
                    if response.status_code == 201:
                        data = response.json()
                        self.created_ids['categorias'].append(data['id'])
                        print(f"✅ Categoría creada: {data['nombre']} (ID: {data['id']})")
        
        # Obtener categoría por ID
        if self.created_ids['categorias']:
            categoria_id = self.created_ids['categorias'][0]
            self.make_request('GET', f'/api/v1/categorias/{categoria_id}')
        
        # Categorías con productos (cards)
        self.make_request('GET', '/api/v1/categorias/productos/cards', params={'skip': 0, 'limit': 100})
    
    def test_alergenos(self):
        """Probar endpoints de alérgenos."""
        print("\n⚠️ PROBANDO ENDPOINTS DE ALÉRGENOS")
        
        # Listar alérgenos existentes
        response = self.make_request('GET', '/api/v1/alergenos', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar los primeros 3 alérgenos existentes
                for alergeno in data['items'][:3]:
                    self.created_ids['alergenos'].append(alergeno['id'])
                    print(f"✅ Usando alérgeno existente: {alergeno['nombre']} (ID: {alergeno['id']})")
            else:
                # Crear alérgenos de ejemplo
                alergenos_data = [
                    {
                        "nombre": "Mariscos Test",
                        "descripcion": "Alérgeno de mariscos para pruebas",
                        "icono": "🦐",
                        "nivel_riesgo": "alto",
                        "activo": True
                    },
                    {
                        "nombre": "Gluten Test",
                        "descripcion": "Alérgeno de gluten para pruebas",
                        "icono": "🌾",
                        "nivel_riesgo": "medio",
                        "activo": True
                    }
                ]
                
                for alergeno_data in alergenos_data:
                    response = self.make_request('POST', '/api/v1/alergenos', alergeno_data)
                    if response.status_code == 201:
                        data = response.json()
                        self.created_ids['alergenos'].append(data['id'])
                        print(f"✅ Alérgeno creado: {data['nombre']} (ID: {data['id']})")
        
        # Obtener alérgeno por ID
        if self.created_ids['alergenos']:
            alergeno_id = self.created_ids['alergenos'][0]
            self.make_request('GET', f'/api/v1/alergenos/{alergeno_id}')
    
    def test_productos(self):
        """Probar endpoints de productos."""
        print("\n🍽️ PROBANDO ENDPOINTS DE PRODUCTOS")
        
        # Listar productos existentes
        response = self.make_request('GET', '/api/v1/productos', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar los primeros 3 productos existentes
                for producto in data['items'][:3]:
                    self.created_ids['productos'].append(producto['id'])
                    print(f"✅ Usando producto existente: {producto['nombre']} (ID: {producto['id']})")
            else:
                # Crear productos de ejemplo (necesitamos categorías)
                if self.created_ids['categorias']:
                    categoria_id = self.created_ids['categorias'][0]
                    productos_data = [
                        {
                            "nombre": "Ceviche Test",
                            "descripcion": "Ceviche para pruebas de API",
                            "precio_base": 25.00,
                            "imagen_path": "https://example.com/ceviche.jpg",
                            "imagen_alt_text": "Ceviche de prueba",
                            "id_categoria": categoria_id,
                            "disponible": True,
                            "destacado": True
                        },
                        {
                            "nombre": "Chicha Test",
                            "descripcion": "Chicha para pruebas de API",
                            "precio_base": 8.00,
                            "imagen_path": "https://example.com/chicha.jpg",
                            "imagen_alt_text": "Chicha de prueba",
                            "id_categoria": categoria_id,
                            "disponible": True,
                            "destacado": False
                        }
                    ]
                    
                    for producto_data in productos_data:
                        response = self.make_request('POST', '/api/v1/productos', producto_data)
                        if response.status_code == 201:
                            data = response.json()
                            self.created_ids['productos'].append(data['id'])
                            print(f"✅ Producto creado: {data['nombre']} (ID: {data['id']})")
        
        # Obtener producto por ID
        if self.created_ids['productos']:
            producto_id = self.created_ids['productos'][0]
            self.make_request('GET', f'/api/v1/productos/{producto_id}')
        
        # Productos en formato cards
        self.make_request('GET', '/api/v1/productos/cards', params={'skip': 0, 'limit': 100})
        
        # Productos por categoría
        if self.created_ids['categorias']:
            categoria_id = self.created_ids['categorias'][0]
            self.make_request('GET', f'/api/v1/productos/categoria/{categoria_id}/cards', 
                            params={'skip': 0, 'limit': 100})
    
    def test_tipos_opciones(self):
        """Probar endpoints de tipos de opciones."""
        print("\n⚙️ PROBANDO ENDPOINTS DE TIPOS DE OPCIONES")
        
        # Listar tipos de opciones existentes
        response = self.make_request('GET', '/api/v1/tipos-opciones', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar los primeros 2 tipos de opciones existentes
                for tipo_opcion in data['items'][:2]:
                    self.created_ids['tipos_opciones'].append(tipo_opcion['id'])
                    print(f"✅ Usando tipo de opción existente: {tipo_opcion['nombre']} (ID: {tipo_opcion['id']})")
            else:
                # Crear tipos de opciones de ejemplo
                tipos_data = [
                    {
                        "codigo": "nivel_aji_test",
                        "nombre": "Nivel de Ají Test",
                        "descripcion": "Intensidad del picante para pruebas",
                        "activo": True,
                        "orden": 1
                    },
                    {
                        "codigo": "temperatura_test",
                        "nombre": "Temperatura Test",
                        "descripcion": "Temperatura de bebidas para pruebas",
                        "activo": True,
                        "orden": 2
                    }
                ]
                
                for tipo_data in tipos_data:
                    response = self.make_request('POST', '/api/v1/tipos-opciones', tipo_data)
                    if response.status_code == 201:
                        data = response.json()
                        self.created_ids['tipos_opciones'].append(data['id'])
                        print(f"✅ Tipo de opción creado: {data['nombre']} (ID: {data['id']})")
        
        # Obtener tipo de opción por ID
        if self.created_ids['tipos_opciones']:
            tipo_opcion_id = self.created_ids['tipos_opciones'][0]
            self.make_request('GET', f'/api/v1/tipos-opciones/{tipo_opcion_id}')
    
    def test_producto_opciones(self):
        """Probar endpoints de opciones de productos."""
        print("\n🎛️ PROBANDO ENDPOINTS DE OPCIONES DE PRODUCTOS")
        
        # Listar opciones de productos existentes
        response = self.make_request('GET', '/api/v1/producto-opciones', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar las primeras 3 opciones existentes
                for opcion in data['items'][:3]:
                    self.created_ids['producto_opciones'].append(opcion['id'])
                    print(f"✅ Usando opción existente: {opcion['nombre']} (ID: {opcion['id']})")
            else:
                # Crear opciones de ejemplo (necesitamos productos y tipos de opciones)
                if self.created_ids['productos'] and self.created_ids['tipos_opciones']:
                    producto_id = self.created_ids['productos'][0]
                    tipo_opcion_id = self.created_ids['tipos_opciones'][0]
                    
                    opciones_data = [
                        {
                            "id_producto": producto_id,
                            "id_tipo_opcion": tipo_opcion_id,
                            "nombre": "Sin ají",
                            "precio_adicional": 0.00,
                            "activo": True,
                            "orden": 1
                        },
                        {
                            "id_producto": producto_id,
                            "id_tipo_opcion": tipo_opcion_id,
                            "nombre": "Ají suave",
                            "precio_adicional": 0.00,
                            "activo": True,
                            "orden": 2
                        }
                    ]
                    
                    for opcion_data in opciones_data:
                        response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
                        if response.status_code == 201:
                            data = response.json()
                            self.created_ids['producto_opciones'].append(data['id'])
                            print(f"✅ Opción creada: {data['nombre']} (ID: {data['id']})")
        
        # Obtener opción por ID
        if self.created_ids['producto_opciones']:
            opcion_id = self.created_ids['producto_opciones'][0]
            self.make_request('GET', f'/api/v1/producto-opciones/{opcion_id}')
    
    def test_productos_alergenos(self):
        """Probar endpoints de relaciones producto-alérgeno."""
        print("\n🔗 PROBANDO ENDPOINTS DE RELACIONES PRODUCTO-ALÉRGENO")
        
        # Listar relaciones existentes
        response = self.make_request('GET', '/api/v1/productos-alergenos', params={'skip': 0, 'limit': 100})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                # Usar las primeras 3 relaciones existentes
                for relacion in data['items'][:3]:
                    key = f"{relacion['id_producto']}_{relacion['id_alergeno']}"
                    self.created_ids['productos_alergenos'].append(key)
                    print(f"✅ Usando relación existente: {relacion['id_producto']} - {relacion['id_alergeno']}")
            else:
                # Crear relaciones de ejemplo (necesitamos productos y alérgenos)
                if self.created_ids['productos'] and self.created_ids['alergenos']:
                    producto_id = self.created_ids['productos'][0]
                    alergeno_id = self.created_ids['alergenos'][0]
                    
                    relacion_data = {
                        "id_producto": producto_id,
                        "id_alergeno": alergeno_id,
                        "nivel_presencia": "contiene",
                        "notas": "Relación creada para pruebas de API",
                        "activo": True
                    }
                    
                    response = self.make_request('POST', '/api/v1/productos-alergenos', relacion_data)
                    if response.status_code == 201:
                        data = response.json()
                        key = f"{data['id_producto']}_{data['id_alergeno']}"
                        self.created_ids['productos_alergenos'].append(key)
                        print(f"✅ Relación creada: {data['id_producto']} - {data['id_alergeno']}")
        
        # Obtener relación por IDs
        if self.created_ids['productos_alergenos']:
            key = self.created_ids['productos_alergenos'][0]
            producto_id, alergeno_id = key.split('_')
            self.make_request('GET', f'/api/v1/productos-alergenos/{producto_id}/{alergeno_id}')
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas."""
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE LA API DE CEVICHERÍA")
        print(f"🌐 URL Base: {self.base_url}")
        
        try:
            # Probar endpoints básicos
            self.test_health_endpoints()
            time.sleep(1)
            
            # Probar seed
            self.test_seed_endpoints()
            time.sleep(2)
            
            # Probar módulos principales
            self.test_roles()
            time.sleep(1)
            
            self.test_categorias()
            time.sleep(1)
            
            self.test_alergenos()
            time.sleep(1)
            
            self.test_productos()
            time.sleep(1)
            
            self.test_tipos_opciones()
            time.sleep(1)
            
            self.test_producto_opciones()
            time.sleep(1)
            
            self.test_productos_alergenos()
            
            print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS!")
            print("\n📊 RESUMEN DE IDs CREADOS/ENCONTRADOS:")
            for tipo, ids in self.created_ids.items():
                if ids:
                    print(f"  {tipo}: {len(ids)} elementos")
                    for i, id_val in enumerate(ids[:3]):  # Mostrar solo los primeros 3
                        print(f"    {i+1}. {id_val}")
                    if len(ids) > 3:
                        print(f"    ... y {len(ids) - 3} más")
                else:
                    print(f"  {tipo}: 0 elementos")
            
        except Exception as e:
            print(f"\n❌ Error durante las pruebas: {e}")
            raise

def main():
    """Función principal."""
    # Crear instancia del tester
    tester = CevicheriaAPITester("https://back-dp2.onrender.com")
    
    # Ejecutar todas las pruebas
    tester.run_all_tests()

if __name__ == "__main__":
    main()
