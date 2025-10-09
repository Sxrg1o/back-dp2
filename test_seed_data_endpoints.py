"""
Script simple para probar los endpoints usando los datos del seed
URL: https://back-dp2.onrender.com/
"""

import requests
import json
import time

class SeedDataTester:
    """Tester simple para probar endpoints con datos del seed."""
    
    def __init__(self):
        self.base_url = "https://back-dp2.onrender.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def make_request(self, method, endpoint, data=None, params=None):
        """Hacer petición HTTP con logging simple."""
        url = f"{self.base_url}{endpoint}"
        
        print(f"\n🔗 {method} {endpoint}")
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Método no soportado: {method}")
            
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    print(f"✅ Success: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
                    return data
                except:
                    print(f"✅ Success: {response.text[:200]}...")
                    return response.text
            else:
                print(f"❌ Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return None
    
    def test_seed_status(self):
        """Verificar estado del seed."""
        print("\n🌱 VERIFICANDO ESTADO DEL SEED")
        return self.make_request('GET', '/api/v1/seed/status')
    
    def test_execute_seed(self):
        """Ejecutar seed si es necesario."""
        print("\n🔄 EJECUTANDO SEED")
        return self.make_request('POST', '/api/v1/seed/execute', {'force': False})
    
    def test_categorias(self):
        """Probar endpoints de categorías."""
        print("\n📂 PROBANDO CATEGORÍAS")
        
        # Listar categorías
        categorias = self.make_request('GET', '/api/v1/categorias', params={'skip': 0, 'limit': 10})
        
        if categorias and categorias.get('items'):
            categoria_id = categorias['items'][0]['id']
            print(f"📋 Usando categoría: {categorias['items'][0]['nombre']} (ID: {categoria_id})")
            
            # Obtener categoría específica
            self.make_request('GET', f'/api/v1/categorias/{categoria_id}')
            
            return categoria_id
        
        return None
    
    def test_productos(self, categoria_id=None):
        """Probar endpoints de productos."""
        print("\n🍽️ PROBANDO PRODUCTOS")
        
        # Listar todos los productos
        productos = self.make_request('GET', '/api/v1/productos', params={'skip': 0, 'limit': 10})
        
        if productos and productos.get('items'):
            producto_id = productos['items'][0]['id']
            print(f"🍽️ Usando producto: {productos['items'][0]['nombre']} (ID: {producto_id})")
            
            # Obtener producto específico
            self.make_request('GET', f'/api/v1/productos/{producto_id}')
            
            # Productos en formato cards
            self.make_request('GET', '/api/v1/productos/cards', params={'skip': 0, 'limit': 5})
            
            # Productos por categoría si tenemos categoria_id
            if categoria_id:
                self.make_request('GET', f'/api/v1/productos/categoria/{categoria_id}/cards', 
                                params={'skip': 0, 'limit': 5})
            
            return producto_id
        
        return None
    
    def test_alergenos(self):
        """Probar endpoints de alérgenos."""
        print("\n⚠️ PROBANDO ALÉRGENOS")
        
        # Listar alérgenos
        alergenos = self.make_request('GET', '/api/v1/alergenos', params={'skip': 0, 'limit': 10})
        
        if alergenos and alergenos.get('items'):
            alergeno_id = alergenos['items'][0]['id']
            print(f"⚠️ Usando alérgeno: {alergenos['items'][0]['nombre']} (ID: {alergeno_id})")
            
            # Obtener alérgeno específico
            self.make_request('GET', f'/api/v1/alergenos/{alergeno_id}')
            
            return alergeno_id
        
        return None
    
    def test_roles(self):
        """Probar endpoints de roles."""
        print("\n👥 PROBANDO ROLES")
        
        # Listar roles
        roles = self.make_request('GET', '/api/v1/roles', params={'skip': 0, 'limit': 10})
        
        if roles and roles.get('items'):
            rol_id = roles['items'][0]['id']
            print(f"👥 Usando rol: {roles['items'][0]['nombre']} (ID: {rol_id})")
            
            # Obtener rol específico
            self.make_request('GET', f'/api/v1/roles/{rol_id}')
            
            return rol_id
        
        return None
    
    def test_tipos_opciones(self):
        """Probar endpoints de tipos de opciones."""
        print("\n⚙️ PROBANDO TIPOS DE OPCIONES")
        
        # Listar tipos de opciones
        tipos = self.make_request('GET', '/api/v1/tipos-opciones', params={'skip': 0, 'limit': 10})
        
        if tipos and tipos.get('items'):
            tipo_id = tipos['items'][0]['id']
            print(f"⚙️ Usando tipo: {tipos['items'][0]['nombre']} (ID: {tipo_id})")
            
            # Obtener tipo específico
            self.make_request('GET', f'/api/v1/tipos-opciones/{tipo_id}')
            
            return tipo_id
        
        return None
    
    def test_producto_opciones(self, producto_id=None, tipo_opcion_id=None):
        """Probar endpoints de opciones de productos."""
        print("\n🎛️ PROBANDO OPCIONES DE PRODUCTOS")
        
        # Listar opciones de productos
        opciones = self.make_request('GET', '/api/v1/producto-opciones', params={'skip': 0, 'limit': 10})
        
        if opciones and opciones.get('items'):
            opcion_id = opciones['items'][0]['id']
            print(f"🎛️ Usando opción: {opciones['items'][0]['nombre']} (ID: {opcion_id})")
            
            # Obtener opción específica
            self.make_request('GET', f'/api/v1/producto-opciones/{opcion_id}')
            
            return opcion_id
        
        return None
    
    def test_productos_alergenos(self, producto_id=None, alergeno_id=None):
        """Probar endpoints de relaciones producto-alérgeno."""
        print("\n🔗 PROBANDO RELACIONES PRODUCTO-ALÉRGENO")
        
        # Listar relaciones
        relaciones = self.make_request('GET', '/api/v1/productos-alergenos', params={'skip': 0, 'limit': 10})
        
        if relaciones and relaciones.get('items'):
            relacion = relaciones['items'][0]
            print(f"🔗 Usando relación: {relacion['id_producto']} - {relacion['id_alergeno']}")
            
            # Obtener relación específica
            self.make_request('GET', f'/api/v1/productos-alergenos/{relacion["id_producto"]}/{relacion["id_alergeno"]}')
            
            return relacion
        
        return None
    
    def test_categorias_con_productos(self):
        """Probar endpoint especial de categorías con productos."""
        print("\n📂 PROBANDO CATEGORÍAS CON PRODUCTOS (CARDS)")
        return self.make_request('GET', '/api/v1/categorias/productos/cards', params={'skip': 0, 'limit': 5})
    
    def run_complete_test(self):
        """Ejecutar prueba completa."""
        print("🚀 INICIANDO PRUEBA COMPLETA DE LA API")
        print(f"🌐 URL: {self.base_url}")
        
        try:
            # 1. Verificar estado del seed
            seed_status = self.test_seed_status()
            time.sleep(1)
            
            # 2. Ejecutar seed si es necesario
            if seed_status and not seed_status.get('has_data', False):
                self.test_execute_seed()
                time.sleep(3)  # Esperar a que se complete el seed
            
            # 3. Probar endpoints básicos
            self.make_request('GET', '/health')
            self.make_request('GET', '/')
            time.sleep(1)
            
            # 4. Probar módulos principales
            categoria_id = self.test_categorias()
            time.sleep(1)
            
            producto_id = self.test_productos(categoria_id)
            time.sleep(1)
            
            alergeno_id = self.test_alergenos()
            time.sleep(1)
            
            rol_id = self.test_roles()
            time.sleep(1)
            
            tipo_opcion_id = self.test_tipos_opciones()
            time.sleep(1)
            
            opcion_id = self.test_producto_opciones(producto_id, tipo_opcion_id)
            time.sleep(1)
            
            relacion = self.test_productos_alergenos(producto_id, alergeno_id)
            time.sleep(1)
            
            # 5. Probar endpoint especial
            self.test_categorias_con_productos()
            
            print("\n🎉 ¡PRUEBA COMPLETA FINALIZADA!")
            print("\n📊 RESUMEN:")
            print(f"  ✅ Categorías: {'OK' if categoria_id else 'Sin datos'}")
            print(f"  ✅ Productos: {'OK' if producto_id else 'Sin datos'}")
            print(f"  ✅ Alérgenos: {'OK' if alergeno_id else 'Sin datos'}")
            print(f"  ✅ Roles: {'OK' if rol_id else 'Sin datos'}")
            print(f"  ✅ Tipos de opciones: {'OK' if tipo_opcion_id else 'Sin datos'}")
            print(f"  ✅ Opciones de productos: {'OK' if opcion_id else 'Sin datos'}")
            print(f"  ✅ Relaciones producto-alérgeno: {'OK' if relacion else 'Sin datos'}")
            
        except Exception as e:
            print(f"\n❌ Error durante la prueba: {e}")

def main():
    """Función principal."""
    tester = SeedDataTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main()
