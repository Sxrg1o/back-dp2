"""
Script para ejecutar el seed de datos en el servidor online
URL: https://back-dp2.onrender.com/
Basado en los datos del script seed_cevicheria_data.py
"""

import requests
import json
import time
from typing import Dict, List, Any

class OnlineSeedExecutor:
    """Ejecutor del seed para el servidor online."""
    
    def __init__(self):
        self.base_url = "https://back-dp2.onrender.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Contadores para verificar datos creados
        self.counts = {
            'roles': 0,
            'categorias': 0,
            'alergenos': 0,
            'productos': 0,
            'tipos_opciones': 0,
            'producto_opciones': 0,
            'productos_alergenos': 0
        }
    
    def log_step(self, step: str, message: str):
        """Log de pasos del proceso."""
        print(f"\n{'='*60}")
        print(f"🔄 {step}")
        print(f"📝 {message}")
        print(f"{'='*60}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Hacer petición HTTP con manejo de errores."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Método no soportado: {method}")
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return {}
    
    def check_seed_status(self) -> bool:
        """Verificar si ya existen datos de seed."""
        self.log_step("VERIFICANDO ESTADO", "Revisando si la base de datos ya tiene datos de seed")
        
        response = self.make_request('GET', '/api/v1/seed/status')
        
        if response:
            has_data = response.get('has_data', False)
            if has_data:
                print("✅ La base de datos ya contiene datos de seed")
                return True
            else:
                print("📝 La base de datos está vacía, procediendo con el seed")
                return False
        else:
            print("⚠️ No se pudo verificar el estado del seed, procediendo de todas formas")
            return False
    
    def execute_seed(self) -> bool:
        """Ejecutar el seed de datos."""
        self.log_step("EJECUTANDO SEED", "Iniciando el proceso de seed de datos")
        
        response = self.make_request('POST', '/api/v1/seed/execute', {'force': False})
        
        if response:
            success = response.get('result', {}).get('success', False)
            if success:
                print("✅ Seed ejecutado exitosamente")
                data_created = response.get('result', {}).get('data_created', {})
                print(f"📊 Datos creados: {json.dumps(data_created, indent=2, ensure_ascii=False)}")
                return True
            else:
                print("❌ El seed falló")
                return False
        else:
            print("❌ No se pudo ejecutar el seed")
            return False
    
    def verify_roles(self) -> bool:
        """Verificar que se crearon los roles del seed."""
        self.log_step("VERIFICANDO ROLES", "Revisando roles creados")
        
        response = self.make_request('GET', '/api/v1/roles', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            roles = response['items']
            self.counts['roles'] = len(roles)
            
            print(f"✅ Se encontraron {len(roles)} roles:")
            for rol in roles:
                print(f"   👤 {rol['nombre']} - {rol['descripcion']}")
            
            # Verificar roles específicos del seed
            expected_roles = ['Administrador', 'Mesero', 'Cocinero', 'Cajero', 'Cliente']
            found_roles = [rol['nombre'] for rol in roles]
            
            missing_roles = [role for role in expected_roles if role not in found_roles]
            if missing_roles:
                print(f"⚠️ Roles faltantes: {missing_roles}")
                return False
            else:
                print("✅ Todos los roles esperados están presentes")
                return True
        else:
            print("❌ No se encontraron roles")
            return False
    
    def verify_categorias(self) -> bool:
        """Verificar que se crearon las categorías del seed."""
        self.log_step("VERIFICANDO CATEGORÍAS", "Revisando categorías creadas")
        
        response = self.make_request('GET', '/api/v1/categorias', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            categorias = response['items']
            self.counts['categorias'] = len(categorias)
            
            print(f"✅ Se encontraron {len(categorias)} categorías:")
            for categoria in categorias:
                print(f"   📂 {categoria['nombre']} - {categoria['descripcion']}")
            
            # Verificar categorías específicas del seed
            expected_categorias = ['Ceviches', 'Tiraditos', 'Chicharrones', 'Arroces', 'Causas', 'Bebidas', 'Postres']
            found_categorias = [cat['nombre'] for cat in categorias]
            
            missing_categorias = [cat for cat in expected_categorias if cat not in found_categorias]
            if missing_categorias:
                print(f"⚠️ Categorías faltantes: {missing_categorias}")
                return False
            else:
                print("✅ Todas las categorías esperadas están presentes")
                return True
        else:
            print("❌ No se encontraron categorías")
            return False
    
    def verify_alergenos(self) -> bool:
        """Verificar que se crearon los alérgenos del seed."""
        self.log_step("VERIFICANDO ALÉRGENOS", "Revisando alérgenos creados")
        
        response = self.make_request('GET', '/api/v1/alergenos', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            alergenos = response['items']
            self.counts['alergenos'] = len(alergenos)
            
            print(f"✅ Se encontraron {len(alergenos)} alérgenos:")
            for alergeno in alergenos:
                print(f"   ⚠️ {alergeno['nombre']} - {alergeno['descripcion']}")
            
            # Verificar alérgenos específicos del seed
            expected_alergenos = ['Mariscos', 'Pescado', 'Moluscos', 'Gluten', 'Lácteos', 'Ají', 'Soja', 'Frutos Secos']
            found_alergenos = [alg['nombre'] for alg in alergenos]
            
            missing_alergenos = [alg for alg in expected_alergenos if alg not in found_alergenos]
            if missing_alergenos:
                print(f"⚠️ Alérgenos faltantes: {missing_alergenos}")
                return False
            else:
                print("✅ Todos los alérgenos esperados están presentes")
                return True
        else:
            print("❌ No se encontraron alérgenos")
            return False
    
    def verify_productos(self) -> bool:
        """Verificar que se crearon los productos del seed."""
        self.log_step("VERIFICANDO PRODUCTOS", "Revisando productos creados")
        
        response = self.make_request('GET', '/api/v1/productos', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            productos = response['items']
            self.counts['productos'] = len(productos)
            
            print(f"✅ Se encontraron {len(productos)} productos:")
            
            # Agrupar por categoría para mejor visualización
            productos_por_categoria = {}
            for producto in productos:
                # Necesitamos obtener la categoría del producto
                cat_response = self.make_request('GET', f'/api/v1/productos/{producto["id"]}')
                if cat_response and 'id_categoria' in cat_response:
                    # Obtener nombre de la categoría
                    cat_id = cat_response['id_categoria']
                    cat_name = "Sin categoría"
                    for cat in self.get_categorias():
                        if cat['id'] == cat_id:
                            cat_name = cat['nombre']
                            break
                    
                    if cat_name not in productos_por_categoria:
                        productos_por_categoria[cat_name] = []
                    productos_por_categoria[cat_name].append(producto['nombre'])
            
            for categoria, productos_list in productos_por_categoria.items():
                print(f"   📂 {categoria}:")
                for producto in productos_list[:3]:  # Mostrar solo los primeros 3
                    print(f"      🍽️ {producto}")
                if len(productos_list) > 3:
                    print(f"      ... y {len(productos_list) - 3} más")
            
            # Verificar algunos productos específicos del seed
            expected_productos = [
                'Ceviche Clásico', 'Ceviche Mixto', 'Tiradito Clásico', 
                'Chicha Morada', 'Suspiro Limeño'
            ]
            found_productos = [prod['nombre'] for prod in productos]
            
            found_expected = [prod for prod in expected_productos if prod in found_productos]
            print(f"✅ Productos específicos encontrados: {len(found_expected)}/{len(expected_productos)}")
            
            return len(productos) > 0
        else:
            print("❌ No se encontraron productos")
            return False
    
    def get_categorias(self) -> List[Dict]:
        """Obtener lista de categorías para referencia."""
        response = self.make_request('GET', '/api/v1/categorias', params={'skip': 0, 'limit': 100})
        return response.get('items', []) if response else []
    
    def verify_tipos_opciones(self) -> bool:
        """Verificar que se crearon los tipos de opciones del seed."""
        self.log_step("VERIFICANDO TIPOS DE OPCIONES", "Revisando tipos de opciones creados")
        
        response = self.make_request('GET', '/api/v1/tipos-opciones', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            tipos = response['items']
            self.counts['tipos_opciones'] = len(tipos)
            
            print(f"✅ Se encontraron {len(tipos)} tipos de opciones:")
            for tipo in tipos:
                print(f"   ⚙️ {tipo['nombre']} ({tipo['codigo']}) - {tipo['descripcion']}")
            
            # Verificar tipos específicos del seed
            expected_tipos = ['nivel_aji', 'acompanamiento', 'temperatura', 'tamano']
            found_tipos = [tipo['codigo'] for tipo in tipos]
            
            missing_tipos = [tipo for tipo in expected_tipos if tipo not in found_tipos]
            if missing_tipos:
                print(f"⚠️ Tipos de opciones faltantes: {missing_tipos}")
                return False
            else:
                print("✅ Todos los tipos de opciones esperados están presentes")
                return True
        else:
            print("❌ No se encontraron tipos de opciones")
            return False
    
    def verify_producto_opciones(self) -> bool:
        """Verificar que se crearon las opciones de productos del seed."""
        self.log_step("VERIFICANDO OPCIONES DE PRODUCTOS", "Revisando opciones de productos creadas")
        
        response = self.make_request('GET', '/api/v1/producto-opciones', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            opciones = response['items']
            self.counts['producto_opciones'] = len(opciones)
            
            print(f"✅ Se encontraron {len(opciones)} opciones de productos:")
            
            # Mostrar algunas opciones de ejemplo
            for i, opcion in enumerate(opciones[:10]):  # Mostrar solo las primeras 10
                print(f"   🎛️ {opcion['nombre']} - Precio adicional: ${opcion['precio_adicional']}")
            
            if len(opciones) > 10:
                print(f"   ... y {len(opciones) - 10} opciones más")
            
            return len(opciones) > 0
        else:
            print("❌ No se encontraron opciones de productos")
            return False
    
    def verify_productos_alergenos(self) -> bool:
        """Verificar que se crearon las relaciones producto-alérgeno del seed."""
        self.log_step("VERIFICANDO RELACIONES PRODUCTO-ALÉRGENO", "Revisando relaciones creadas")
        
        response = self.make_request('GET', '/api/v1/productos-alergenos', params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            relaciones = response['items']
            self.counts['productos_alergenos'] = len(relaciones)
            
            print(f"✅ Se encontraron {len(relaciones)} relaciones producto-alérgeno:")
            
            # Mostrar algunas relaciones de ejemplo
            for i, relacion in enumerate(relaciones[:10]):  # Mostrar solo las primeras 10
                print(f"   🔗 Producto {relacion['id_producto'][:8]}... - Alérgeno {relacion['id_alergeno'][:8]}... - Nivel: {relacion['nivel_presencia']}")
            
            if len(relaciones) > 10:
                print(f"   ... y {len(relaciones) - 10} relaciones más")
            
            return len(relaciones) > 0
        else:
            print("❌ No se encontraron relaciones producto-alérgeno")
            return False
    
    def run_complete_seed_verification(self):
        """Ejecutar verificación completa del seed."""
        print("🚀 INICIANDO VERIFICACIÓN COMPLETA DEL SEED")
        print(f"🌐 Servidor: {self.base_url}")
        print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. Verificar estado actual
            has_data = self.check_seed_status()
            
            # 2. Ejecutar seed si es necesario
            if not has_data:
                success = self.execute_seed()
                if not success:
                    print("❌ No se pudo ejecutar el seed")
                    return False
                
                # Esperar un poco para que se complete
                print("⏳ Esperando a que se complete el seed...")
                time.sleep(5)
            
            # 3. Verificar todos los datos
            results = {
                'roles': self.verify_roles(),
                'categorias': self.verify_categorias(),
                'alergenos': self.verify_alergenos(),
                'productos': self.verify_productos(),
                'tipos_opciones': self.verify_tipos_opciones(),
                'producto_opciones': self.verify_producto_opciones(),
                'productos_alergenos': self.verify_productos_alergenos()
            }
            
            # 4. Resumen final
            self.log_step("RESUMEN FINAL", "Resultados de la verificación del seed")
            
            total_checks = len(results)
            passed_checks = sum(1 for result in results.values() if result)
            
            print(f"📊 Verificaciones completadas: {passed_checks}/{total_checks}")
            print(f"📈 Porcentaje de éxito: {(passed_checks/total_checks)*100:.1f}%")
            
            print("\n📋 Detalles por módulo:")
            for module, result in results.items():
                status = "✅ OK" if result else "❌ FALLO"
                count = self.counts.get(module, 0)
                print(f"   {module}: {status} ({count} registros)")
            
            if passed_checks == total_checks:
                print("\n🎉 ¡SEED COMPLETADO EXITOSAMENTE!")
                print("✅ Todos los datos del seed están presentes en el servidor")
            else:
                print(f"\n⚠️ SEED PARCIALMENTE COMPLETADO")
                print(f"❌ {total_checks - passed_checks} módulos fallaron")
            
            return passed_checks == total_checks
            
        except Exception as e:
            print(f"\n❌ Error durante la verificación: {e}")
            return False

def main():
    """Función principal."""
    executor = OnlineSeedExecutor()
    success = executor.run_complete_seed_verification()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
        exit(0)
    else:
        print("\n❌ Proceso falló")
        exit(1)

if __name__ == "__main__":
    main()
