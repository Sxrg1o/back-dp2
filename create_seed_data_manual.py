"""
Script para crear manualmente los datos del seed usando los endpoints disponibles
URL: https://back-dp2.onrender.com/
Basado en los datos del script seed_cevicheria_data.py
"""

import requests
import json
import time
from typing import Dict, List, Any

class ManualSeedCreator:
    """Creador manual de datos de seed."""
    
    def __init__(self):
        self.base_url = "https://back-dp2.onrender.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # IDs creados para referencias
        self.created_ids = {
            'roles': [],
            'categorias': [],
            'alergenos': [],
            'productos': [],
            'tipos_opciones': [],
            'producto_opciones': []
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
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
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
    
    def check_existing_data(self, endpoint: str, name_field: str = 'nombre') -> List[Dict]:
        """Verificar datos existentes."""
        response = self.make_request('GET', endpoint, params={'skip': 0, 'limit': 100})
        
        if response and response.get('items'):
            existing_items = response['items']
            print(f"📋 Se encontraron {len(existing_items)} elementos existentes:")
            for item in existing_items:
                print(f"   - {item.get(name_field, 'Sin nombre')}")
            return existing_items
        else:
            print("📝 No se encontraron elementos existentes")
            return []
    
    def create_roles(self):
        """Crear roles del sistema."""
        self.log_step("CREANDO ROLES", "Creando roles del sistema")
        
        # Verificar roles existentes
        existing_roles = self.check_existing_data('/api/v1/roles')
        existing_names = [role['nombre'] for role in existing_roles]
        
        roles_data = [
            {
                "nombre": "Administrador",
                "descripcion": "Acceso completo al sistema, gestión de usuarios y configuración",
                "activo": True
            },
            {
                "nombre": "Mesero",
                "descripcion": "Toma pedidos, gestiona mesas y atiende clientes",
                "activo": True
            },
            {
                "nombre": "Cocinero",
                "descripcion": "Prepara los platos y gestiona el inventario de cocina",
                "activo": True
            },
            {
                "nombre": "Cajero",
                "descripcion": "Procesa pagos y cierre de caja",
                "activo": True
            },
            {
                "nombre": "Cliente",
                "descripcion": "Cliente registrado con acceso a pedidos online",
                "activo": True
            }
        ]
        
        created_count = 0
        for rol_data in roles_data:
            if rol_data['nombre'] not in existing_names:
                response = self.make_request('POST', '/api/v1/roles', rol_data)
                if response and 'id' in response:
                    self.created_ids['roles'].append(response['id'])
                    print(f"✅ Rol creado: {rol_data['nombre']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando rol: {rol_data['nombre']}")
            else:
                print(f"⏭️ Rol ya existe: {rol_data['nombre']}")
                # Agregar ID del rol existente
                for existing_role in existing_roles:
                    if existing_role['nombre'] == rol_data['nombre']:
                        self.created_ids['roles'].append(existing_role['id'])
                        break
        
        print(f"📊 Roles procesados: {created_count} nuevos, {len(existing_roles)} existentes")
    
    def create_categorias(self):
        """Crear categorías de productos."""
        self.log_step("CREANDO CATEGORÍAS", "Creando categorías de productos")
        
        # Verificar categorías existentes
        existing_categorias = self.check_existing_data('/api/v1/categorias')
        existing_names = [cat['nombre'] for cat in existing_categorias]
        
        categorias_data = [
            {
                "nombre": "Ceviches",
                "descripcion": "Ceviches frescos del día con pescados y mariscos selectos",
                "imagen_path": "https://drive.google.com/file/d/1ZaYA_c1ZGfl6tsPe80-fwSzpHR_LYzSZ/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Tiraditos",
                "descripcion": "Finas láminas de pescado fresco con salsas especiales",
                "imagen_path": "https://drive.google.com/file/d/10xFfoYsezQRTC3EvLKm28BJGnImhAJjO/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Chicharrones",
                "descripcion": "Chicharrones crujientes de pescado y mariscos",
                "imagen_path": "https://drive.google.com/file/d/1FYmm0IoKTx3tAgumxpZfSIx4GIrPtD4G/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Arroces",
                "descripcion": "Arroces marinos con mariscos frescos",
                "imagen_path": "https://drive.google.com/file/d/14xM_kLEcGtsOORHEp5MCDMCJIGgzs45J/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Causas",
                "descripcion": "Causas rellenas de diferentes mariscos",
                "imagen_path": "https://drive.google.com/file/d/1kRcHUgMqWTHDEX5XVUYNlGPTnkMOQRsa/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Bebidas",
                "descripcion": "Bebidas refrescantes, chicha morada, limonada y más",
                "imagen_path": "https://drive.google.com/file/d/1AhNWmlJwuWb0XzXV8Zjs0xD2ZPHT6jzm/view?usp=sharing",
                "activo": True
            },
            {
                "nombre": "Postres",
                "descripcion": "Postres tradicionales peruanos",
                "imagen_path": "https://drive.google.com/file/d/1gxaT1PCMx1lQ-Hvcug9ujWr3RnVK3WPd/view?usp=sharing",
                "activo": True
            }
        ]
        
        created_count = 0
        for categoria_data in categorias_data:
            if categoria_data['nombre'] not in existing_names:
                response = self.make_request('POST', '/api/v1/categorias', categoria_data)
                if response and 'id' in response:
                    self.created_ids['categorias'].append(response['id'])
                    print(f"✅ Categoría creada: {categoria_data['nombre']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando categoría: {categoria_data['nombre']}")
            else:
                print(f"⏭️ Categoría ya existe: {categoria_data['nombre']}")
                # Agregar ID de la categoría existente
                for existing_cat in existing_categorias:
                    if existing_cat['nombre'] == categoria_data['nombre']:
                        self.created_ids['categorias'].append(existing_cat['id'])
                        break
        
        print(f"📊 Categorías procesadas: {created_count} nuevas, {len(existing_categorias)} existentes")
    
    def create_alergenos(self):
        """Crear alérgenos comunes."""
        self.log_step("CREANDO ALÉRGENOS", "Creando alérgenos alimentarios")
        
        # Verificar alérgenos existentes
        existing_alergenos = self.check_existing_data('/api/v1/alergenos')
        existing_names = [alg['nombre'] for alg in existing_alergenos]
        
        alergenos_data = [
            {
                "nombre": "Mariscos",
                "descripcion": "Langostinos, camarones, pulpo, calamar, conchas negras",
                "icono": "🦐",
                "nivel_riesgo": "alto",
                "activo": True
            },
            {
                "nombre": "Pescado",
                "descripcion": "Lenguado, corvina, mero, bonito, atún",
                "icono": "🐟",
                "nivel_riesgo": "alto",
                "activo": True
            },
            {
                "nombre": "Moluscos",
                "descripcion": "Conchas de abanico, pulpo, calamar",
                "icono": "🐙",
                "nivel_riesgo": "alto",
                "activo": True
            },
            {
                "nombre": "Gluten",
                "descripcion": "Presente en masas, panes y algunos aderezos",
                "icono": "🌾",
                "nivel_riesgo": "medio",
                "activo": True
            },
            {
                "nombre": "Lácteos",
                "descripcion": "Leche, queso, crema de leche",
                "icono": "🥛",
                "nivel_riesgo": "medio",
                "activo": True
            },
            {
                "nombre": "Ají",
                "descripcion": "Rocoto, ají amarillo, ají limo",
                "icono": "🌶️",
                "nivel_riesgo": "bajo",
                "activo": True
            },
            {
                "nombre": "Soja",
                "descripcion": "Salsa de soja y derivados",
                "icono": "🫘",
                "nivel_riesgo": "medio",
                "activo": True
            },
            {
                "nombre": "Frutos Secos",
                "descripcion": "Maní, nueces, almendras",
                "icono": "🥜",
                "nivel_riesgo": "alto",
                "activo": True
            }
        ]
        
        created_count = 0
        for alergeno_data in alergenos_data:
            if alergeno_data['nombre'] not in existing_names:
                response = self.make_request('POST', '/api/v1/alergenos', alergeno_data)
                if response and 'id' in response:
                    self.created_ids['alergenos'].append(response['id'])
                    print(f"✅ Alérgeno creado: {alergeno_data['nombre']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando alérgeno: {alergeno_data['nombre']}")
            else:
                print(f"⏭️ Alérgeno ya existe: {alergeno_data['nombre']}")
                # Agregar ID del alérgeno existente
                for existing_alg in existing_alergenos:
                    if existing_alg['nombre'] == alergeno_data['nombre']:
                        self.created_ids['alergenos'].append(existing_alg['id'])
                        break
        
        print(f"📊 Alérgenos procesados: {created_count} nuevos, {len(existing_alergenos)} existentes")
    
    def create_tipos_opciones(self):
        """Crear tipos de opciones para productos."""
        self.log_step("CREANDO TIPOS DE OPCIONES", "Creando tipos de opciones para productos")
        
        # Verificar tipos de opciones existentes
        existing_tipos = self.check_existing_data('/api/v1/tipos-opciones', 'codigo')
        existing_codes = [tipo['codigo'] for tipo in existing_tipos]
        
        tipos_data = [
            {
                "codigo": "nivel_aji",
                "nombre": "Nivel de Ají",
                "descripcion": "Intensidad del picante en el plato",
                "activo": True,
                "orden": 1
            },
            {
                "codigo": "acompanamiento",
                "nombre": "Acompañamiento",
                "descripcion": "Extras que complementan el plato",
                "activo": True,
                "orden": 2
            },
            {
                "codigo": "temperatura",
                "nombre": "Temperatura",
                "descripcion": "Temperatura de la bebida",
                "activo": True,
                "orden": 3
            },
            {
                "codigo": "tamano",
                "nombre": "Tamaño",
                "descripcion": "Tamaño de la porción",
                "activo": True,
                "orden": 4
            }
        ]
        
        created_count = 0
        for tipo_data in tipos_data:
            if tipo_data['codigo'] not in existing_codes:
                response = self.make_request('POST', '/api/v1/tipos-opciones', tipo_data)
                if response and 'id' in response:
                    self.created_ids['tipos_opciones'].append(response['id'])
                    print(f"✅ Tipo de opción creado: {tipo_data['nombre']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando tipo de opción: {tipo_data['nombre']}")
            else:
                print(f"⏭️ Tipo de opción ya existe: {tipo_data['nombre']}")
                # Agregar ID del tipo existente
                for existing_tipo in existing_tipos:
                    if existing_tipo['codigo'] == tipo_data['codigo']:
                        self.created_ids['tipos_opciones'].append(existing_tipo['id'])
                        break
        
        print(f"📊 Tipos de opciones procesados: {created_count} nuevos, {len(existing_tipos)} existentes")
    
    def create_productos_sample(self):
        """Crear algunos productos de ejemplo."""
        self.log_step("CREANDO PRODUCTOS", "Creando productos de ejemplo")
        
        if not self.created_ids['categorias']:
            print("❌ No hay categorías disponibles para crear productos")
            return
        
        # Verificar productos existentes
        existing_productos = self.check_existing_data('/api/v1/productos')
        existing_names = [prod['nombre'] for prod in existing_productos]
        
        # Usar la primera categoría disponible
        categoria_id = self.created_ids['categorias'][0]
        
        productos_data = [
            {
                "nombre": "Ceviche Clásico",
                "descripcion": "Pescado fresco del día marinado en limón, cebolla morada, ají limo y cilantro. Acompañado de camote, choclo y cancha",
                "precio_base": 25.00,
                "imagen_path": "https://drive.google.com/file/d/14MotvG3-NJLZO5bUJjGqyMkOMMSzOZ7L/view?usp=sharing",
                "imagen_alt_text": "Ceviche clásico peruano",
                "id_categoria": categoria_id,
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Chicha Morada",
                "descripcion": "Chicha morada natural preparada con maíz morado, piña y especias",
                "precio_base": 8.00,
                "imagen_path": "https://drive.google.com/file/d/1_w-Wk393ouoSeZdlkSLrWGbNMA7N61xj/view?usp=sharing",
                "imagen_alt_text": "Chicha morada peruana",
                "id_categoria": categoria_id,
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Suspiro Limeño",
                "descripcion": "Manjar blanco con merengue italiano y oporto",
                "precio_base": 12.00,
                "imagen_path": "https://drive.google.com/file/d/156YIcyAetJUtoqk-8b07LWETKNdjp4IO/view?usp=sharing",
                "imagen_alt_text": "Suspiro limeño tradicional",
                "id_categoria": categoria_id,
                "disponible": True,
                "destacado": True
            }
        ]
        
        created_count = 0
        for producto_data in productos_data:
            if producto_data['nombre'] not in existing_names:
                response = self.make_request('POST', '/api/v1/productos', producto_data)
                if response and 'id' in response:
                    self.created_ids['productos'].append(response['id'])
                    print(f"✅ Producto creado: {producto_data['nombre']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando producto: {producto_data['nombre']}")
            else:
                print(f"⏭️ Producto ya existe: {producto_data['nombre']}")
                # Agregar ID del producto existente
                for existing_prod in existing_productos:
                    if existing_prod['nombre'] == producto_data['nombre']:
                        self.created_ids['productos'].append(existing_prod['id'])
                        break
        
        print(f"📊 Productos procesados: {created_count} nuevos, {len(existing_productos)} existentes")
    
    def create_producto_opciones_sample(self):
        """Crear algunas opciones de productos de ejemplo."""
        self.log_step("CREANDO OPCIONES DE PRODUCTOS", "Creando opciones de productos de ejemplo")
        
        if not self.created_ids['productos'] or not self.created_ids['tipos_opciones']:
            print("❌ No hay productos o tipos de opciones disponibles")
            return
        
        # Verificar opciones existentes
        existing_opciones = self.check_existing_data('/api/v1/producto-opciones')
        
        # Usar el primer producto y tipo de opción disponibles
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
            },
            {
                "id_producto": producto_id,
                "id_tipo_opcion": tipo_opcion_id,
                "nombre": "Ají normal",
                "precio_adicional": 0.00,
                "activo": True,
                "orden": 3
            }
        ]
        
        created_count = 0
        for opcion_data in opciones_data:
            response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
            if response and 'id' in response:
                self.created_ids['producto_opciones'].append(response['id'])
                print(f"✅ Opción creada: {opcion_data['nombre']}")
                created_count += 1
            else:
                print(f"❌ Error creando opción: {opcion_data['nombre']}")
        
        print(f"📊 Opciones de productos creadas: {created_count}")
    
    def run_complete_seed(self):
        """Ejecutar el seed completo."""
        print("🚀 INICIANDO CREACIÓN MANUAL DE DATOS DE SEED")
        print(f"🌐 Servidor: {self.base_url}")
        print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Crear datos en orden
            self.create_roles()
            time.sleep(1)
            
            self.create_categorias()
            time.sleep(1)
            
            self.create_alergenos()
            time.sleep(1)
            
            self.create_tipos_opciones()
            time.sleep(1)
            
            self.create_productos_sample()
            time.sleep(1)
            
            self.create_producto_opciones_sample()
            
            # Resumen final
            self.log_step("RESUMEN FINAL", "Datos creados exitosamente")
            
            total_created = sum(len(ids) for ids in self.created_ids.values())
            
            print(f"📊 Total de elementos procesados: {total_created}")
            print("\n📋 Detalles por módulo:")
            for module, ids in self.created_ids.items():
                print(f"   {module}: {len(ids)} elementos")
                for i, id_val in enumerate(ids[:3]):  # Mostrar solo los primeros 3
                    print(f"     {i+1}. {id_val}")
                if len(ids) > 3:
                    print(f"     ... y {len(ids) - 3} más")
            
            print("\n🎉 ¡DATOS DE SEED CREADOS EXITOSAMENTE!")
            print("✅ Los datos están disponibles en el servidor")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante la creación: {e}")
            return False

def main():
    """Función principal."""
    creator = ManualSeedCreator()
    success = creator.run_complete_seed()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
        exit(0)
    else:
        print("\n❌ Proceso falló")
        exit(1)

if __name__ == "__main__":
    main()
