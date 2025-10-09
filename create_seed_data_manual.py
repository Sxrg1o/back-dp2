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
                "activo": True
            },
            {
                "nombre": "Pescado",
                "descripcion": "Lenguado, corvina, mero, bonito, atún",
                "activo": True
            },
            {
                "nombre": "Moluscos",
                "descripcion": "Conchas de abanico, pulpo, calamar",
                "activo": True
            },
            {
                "nombre": "Gluten",
                "descripcion": "Presente en masas, panes y algunos aderezos",
                "activo": True
            },
            {
                "nombre": "Lácteos",
                "descripcion": "Leche, queso, crema de leche",
                "activo": True
            },
            {
                "nombre": "Ají",
                "descripcion": "Rocoto, ají amarillo, ají limo",
                "activo": True
            },
            {
                "nombre": "Soja",
                "descripcion": "Salsa de soja y derivados",
                "activo": True
            },
            {
                "nombre": "Frutos Secos",
                "descripcion": "Maní, nueces, almendras",
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
    
    def create_productos_completos(self):
        """Crear todos los productos de la cevichería."""
        self.log_step("CREANDO PRODUCTOS COMPLETOS", "Creando todos los productos del menú")
        
        if not self.created_ids['categorias']:
            print("❌ No hay categorías disponibles para crear productos")
            return
        
        # Verificar productos existentes
        existing_productos = self.check_existing_data('/api/v1/productos')
        existing_names = [prod['nombre'] for prod in existing_productos]
        
        # Obtener categorías por nombre para asignar correctamente
        categorias_response = self.make_request('GET', '/api/v1/categorias', params={'skip': 0, 'limit': 100})
        categorias_map = {}
        if categorias_response and 'items' in categorias_response:
            for cat in categorias_response['items']:
                categorias_map[cat['nombre']] = cat['id']
        
        productos_data = [
            # CEVICHES
            {
                "nombre": "Ceviche Clásico",
                "descripcion": "Pescado fresco del día marinado en limón, cebolla morada, ají limo y cilantro. Acompañado de camote, choclo y cancha",
                "precio_base": 25.00,
                "imagen_path": "https://drive.google.com/file/d/14MotvG3-NJLZO5bUJjGqyMkOMMSzOZ7L/view?usp=sharing",
                "id_categoria": categorias_map.get("Ceviches", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Ceviche Mixto",
                "descripcion": "Combinación de pescado, pulpo, calamar y langostinos marinados en limón con rocoto molido",
                "precio_base": 35.00,
                "imagen_path": "https://drive.google.com/file/d/18wtI2hmnm2mDhV73cU-ow6XJUUgzXVnP/view?usp=sharing",
                "id_categoria": categorias_map.get("Ceviches", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Ceviche de Conchas Negras",
                "descripcion": "Conchas negras frescas con su jugo natural, marinadas en limón y ají limo",
                "precio_base": 45.00,
                "imagen_path": "https://drive.google.com/file/d/1qsrha511qKobIjyCV91PDmJxPcOz8tOd/view?usp=sharing",
                "id_categoria": categorias_map.get("Ceviches", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Ceviche de Pulpo",
                "descripcion": "Pulpo tierno marinado en limón con cebolla morada y ají amarillo",
                "precio_base": 38.00,
                "imagen_path": "https://drive.google.com/file/d/1dIm4pjLo3E2g_Zop6rvNXc8OErAmHuBd/view?usp=sharing",
                "id_categoria": categorias_map.get("Ceviches", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            # TIRADITOS
            {
                "nombre": "Tiradito Clásico",
                "descripcion": "Finas láminas de pescado con salsa de ají amarillo, rocoto y limón",
                "precio_base": 28.00,
                "imagen_path": "https://drive.google.com/file/d/1gXlCGBSnduNLxla2WA1kDnMnci7WpJHh/view?usp=sharing",
                "id_categoria": categorias_map.get("Tiraditos", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Tiradito Nikkei",
                "descripcion": "Láminas de pescado con salsa de ají amarillo, sillao y aceite de sésamo",
                "precio_base": 32.00,
                "imagen_path": "https://drive.google.com/file/d/1QNR6LydeY06cg_71gw376Iep3dZddvsI/view?usp=sharing",
                "id_categoria": categorias_map.get("Tiraditos", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Tiradito de Atún",
                "descripcion": "Láminas de atún fresco con salsa de maracuyá y ají limo",
                "precio_base": 40.00,
                "imagen_path": "https://drive.google.com/file/d/1Nv1fxVvE4zoEzdnQ44hoAhfQnRKiI2ov/view?usp=sharing",
                "id_categoria": categorias_map.get("Tiraditos", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            # CHICHARRONES
            {
                "nombre": "Chicharrón de Pescado",
                "descripcion": "Trozos de pescado empanizados y fritos, servido con yucas y sarsa criolla",
                "precio_base": 30.00,
                "imagen_path": "https://drive.google.com/file/d/1-7MmcqQ0cWRFJUj2uuiXhGHHzGOZseDn/view?usp=sharing",
                "id_categoria": categorias_map.get("Chicharrones", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Chicharrón de Calamar",
                "descripcion": "Anillos de calamar fritos crujientes con salsa tártara",
                "precio_base": 32.00,
                "imagen_path": "https://drive.google.com/file/d/1i0KzBtnznRC71VMMT5ZUPnIbPky7vJYo/view?usp=sharing",
                "id_categoria": categorias_map.get("Chicharrones", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Chicharrón Mixto",
                "descripcion": "Combinación de pescado, calamar y langostinos fritos con yucas",
                "precio_base": 38.00,
                "imagen_path": "https://drive.google.com/file/d/1eoiQJqdR3SHjeBqcufrNGNnzZJKwgaUf/view?usp=sharing",
                "id_categoria": categorias_map.get("Chicharrones", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            # ARROCES
            {
                "nombre": "Arroz con Mariscos",
                "descripcion": "Arroz marinero con langostinos, conchas, calamar y pulpo en salsa especial",
                "precio_base": 35.00,
                "imagen_path": "https://drive.google.com/file/d/1f5J4b16DYg2YYQ3dR4sH5DJzF9HsT2pq/view?usp=sharing",
                "id_categoria": categorias_map.get("Arroces", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Arroz Chaufa de Mariscos",
                "descripcion": "Arroz frito al wok con mariscos, cebolla china y sillao",
                "precio_base": 32.00,
                "imagen_path": "https://drive.google.com/file/d/13YU5MJXp2ai1-Utyo5v9IpS5Dg2te0gw/view?usp=sharing",
                "id_categoria": categorias_map.get("Arroces", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            {
                "nombre": "Tacu Tacu con Mariscos",
                "descripcion": "Tacu tacu de frijoles con mariscos salteados y salsa criolla",
                "precio_base": 38.00,
                "imagen_path": "https://drive.google.com/file/d/1UUncdgoiAw-af4HLBKz7_S0AiJAqDaV_/view?usp=sharing",
                "id_categoria": categorias_map.get("Arroces", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            # CAUSAS
            {
                "nombre": "Causa Rellena de Langostinos",
                "descripcion": "Causa de papa amarilla rellena de langostinos en mayonesa, aguacate y huevo",
                "precio_base": 28.00,
                "imagen_path": "https://drive.google.com/file/d/1Q6PhiC41IaNk4-rzTf5hPJOS_UcXlxSi/view?usp=sharing",
                "id_categoria": categorias_map.get("Causas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Causa de Pulpo",
                "descripcion": "Causa rellena de pulpo al olivo con aceitunas y palta",
                "precio_base": 30.00,
                "imagen_path": "https://drive.google.com/file/d/1qdxy8MH-XXac8cWwRWeMm2_GHsESYp_g/view?usp=sharing",
                "id_categoria": categorias_map.get("Causas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            {
                "nombre": "Causa Especial",
                "descripcion": "Triple causa: langostinos, atún y palta con salsa golf",
                "precio_base": 35.00,
                "imagen_path": "https://drive.google.com/file/d/1busoPwLfMp0FgxAo9g1pc0kcPZazw1ln/view?usp=sharing",
                "id_categoria": categorias_map.get("Causas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            # BEBIDAS
            {
                "nombre": "Chicha Morada",
                "descripcion": "Chicha morada natural preparada con maíz morado, piña y especias",
                "precio_base": 8.00,
                "imagen_path": "https://drive.google.com/file/d/1_w-Wk393ouoSeZdlkSLrWGbNMA7N61xj/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Limonada Frozen",
                "descripcion": "Limonada frozen con hielo y hierba buena",
                "precio_base": 10.00,
                "imagen_path": "https://drive.google.com/file/d/1fbXhbre-TzuqinCYw5637T375-a8f1Go/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Pisco Sour",
                "descripcion": "Clásico pisco sour con pisco quebranta, limón, jarabe y clara de huevo",
                "precio_base": 18.00,
                "imagen_path": "https://drive.google.com/file/d/1V5NGG5U4HCbPTEOZkC3UC8OZQlQLSrlQ/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Chilcano de Pisco",
                "descripcion": "Pisco, ginger ale, limón y hielo",
                "precio_base": 15.00,
                "imagen_path": "https://drive.google.com/file/d/1QlMnH9bRnnJGrZT6MU8Yj2ddOkl9knKK/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            {
                "nombre": "Inca Kola 1.5L",
                "descripcion": "Gaseosa Inca Kola botella de 1.5 litros",
                "precio_base": 7.00,
                "imagen_path": "https://drive.google.com/file/d/14KIxsU03UQhq80ijLqdEDJXB0HLgLqr7/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            {
                "nombre": "Agua Mineral San Luis",
                "descripcion": "Agua mineral sin gas 625ml",
                "precio_base": 4.00,
                "imagen_path": "https://drive.google.com/file/d/1yJ9gMthGnBnaV6kXLM7pENmiFT5K5u3Z/view?usp=sharing",
                "id_categoria": categorias_map.get("Bebidas", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            # POSTRES
            {
                "nombre": "Suspiro Limeño",
                "descripcion": "Manjar blanco con merengue italiano y oporto",
                "precio_base": 12.00,
                "imagen_path": "https://drive.google.com/file/d/156YIcyAetJUtoqk-8b07LWETKNdjp4IO/view?usp=sharing",
                "id_categoria": categorias_map.get("Postres", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Mazamorra Morada",
                "descripcion": "Mazamorra de maíz morado con frutas y arroz con leche",
                "precio_base": 10.00,
                "imagen_path": "https://drive.google.com/file/d/1rXynhqY70wt9UNn0haszs2y0s_5Me6ZF/view?usp=sharing",
                "id_categoria": categorias_map.get("Postres", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
            },
            {
                "nombre": "Picarones",
                "descripcion": "Picarones de zapallo y camote con miel de chancaca",
                "precio_base": 12.00,
                "imagen_path": "https://drive.google.com/file/d/1SnEdVTnPECzLKSRwnEHuErbMPDAHFi5h/view?usp=sharing",
                "id_categoria": categorias_map.get("Postres", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": True
            },
            {
                "nombre": "Crema Volteada",
                "descripcion": "Flan de huevo con caramelo",
                "precio_base": 10.00,
                "imagen_path": "https://drive.google.com/file/d/1WxJ46tSOhXDVaVi92_4NRx5lk5NHc80e/view?usp=sharing",
                "id_categoria": categorias_map.get("Postres", self.created_ids['categorias'][0]),
                "disponible": True,
                "destacado": False
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
    
    def create_producto_opciones_completas(self):
        """Crear opciones completas para productos."""
        self.log_step("CREANDO OPCIONES DE PRODUCTOS", "Creando opciones completas de productos")
        
        if not self.created_ids['productos'] or not self.created_ids['tipos_opciones']:
            print("❌ No hay productos o tipos de opciones disponibles")
            return
        
        # Verificar opciones existentes
        existing_opciones = self.check_existing_data('/api/v1/producto-opciones')
        
        # Obtener productos y tipos de opciones por nombre
        productos_response = self.make_request('GET', '/api/v1/productos', params={'skip': 0, 'limit': 100})
        productos_map = {}
        if productos_response and 'items' in productos_response:
            for prod in productos_response['items']:
                productos_map[prod['nombre']] = prod['id']
        
        tipos_response = self.make_request('GET', '/api/v1/tipos-opciones', params={'skip': 0, 'limit': 100})
        tipos_map = {}
        if tipos_response and 'items' in tipos_response:
            for tipo in tipos_response['items']:
                tipos_map[tipo['codigo']] = tipo['id']
        
        # Opciones de Nivel de Ají (aplica a ceviches, tiraditos, arroces)
        productos_con_aji = [
            "Ceviche Clásico", "Ceviche Mixto", "Ceviche de Conchas Negras", "Ceviche de Pulpo",
            "Tiradito Clásico", "Tiradito Nikkei", "Tiradito de Atún",
            "Arroz con Mariscos", "Arroz Chaufa de Mariscos", "Tacu Tacu con Mariscos"
        ]
        
        opciones_nivel_aji = [
            ("Sin ají", 0.00, 1),
            ("Ají suave", 0.00, 2),
            ("Ají normal", 0.00, 3),
            ("Ají picante", 0.00, 4),
            ("Ají extra picante", 2.00, 5),  # Cobra extra por rocoto especial
        ]
        
        created_count = 0
        for nombre_producto in productos_con_aji:
            if nombre_producto in productos_map and "nivel_aji" in tipos_map:
                for nombre, precio, orden in opciones_nivel_aji:
                    opcion_data = {
                        "id_producto": productos_map[nombre_producto],
                        "id_tipo_opcion": tipos_map["nivel_aji"],
                        "nombre": nombre,
                        "precio_adicional": precio,
                        "activo": True,
                        "orden": orden
                    }
                    response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
                    if response and 'id' in response:
                        self.created_ids['producto_opciones'].append(response['id'])
                        created_count += 1
        
        # Opciones de Acompañamiento (para ceviches y chicharrones)
        productos_con_acompanamiento = [
            "Ceviche Clásico", "Ceviche Mixto", "Ceviche de Conchas Negras", "Ceviche de Pulpo",
            "Chicharrón de Pescado", "Chicharrón de Calamar", "Chicharrón Mixto"
        ]
        
        opciones_acompanamiento = [
            ("Con camote", 3.00, 1),
            ("Con choclo", 3.00, 2),
            ("Con yuca", 3.50, 3),
            ("Con cancha", 2.00, 4),
            ("Mixto (camote + choclo)", 5.00, 5),
        ]
        
        for nombre_producto in productos_con_acompanamiento:
            if nombre_producto in productos_map and "acompanamiento" in tipos_map:
                for nombre, precio, orden in opciones_acompanamiento:
                    opcion_data = {
                        "id_producto": productos_map[nombre_producto],
                        "id_tipo_opcion": tipos_map["acompanamiento"],
                        "nombre": nombre,
                        "precio_adicional": precio,
                        "activo": True,
                        "orden": orden
                    }
                    response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
                    if response and 'id' in response:
                        self.created_ids['producto_opciones'].append(response['id'])
                        created_count += 1
        
        # Opciones de Temperatura (para bebidas)
        productos_bebidas = ["Chicha Morada", "Limonada Frozen", "Inca Kola 1.5L"]
        
        opciones_temperatura = [
            ("Natural", 0.00, 1),
            ("Helada", 1.00, 2),
            ("Con hielo", 0.50, 3),
        ]
        
        for nombre_producto in productos_bebidas:
            if nombre_producto in productos_map and "temperatura" in tipos_map:
                for nombre, precio, orden in opciones_temperatura:
                    opcion_data = {
                        "id_producto": productos_map[nombre_producto],
                        "id_tipo_opcion": tipos_map["temperatura"],
                        "nombre": nombre,
                        "precio_adicional": precio,
                        "activo": True,
                        "orden": orden
                    }
                    response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
                    if response and 'id' in response:
                        self.created_ids['producto_opciones'].append(response['id'])
                        created_count += 1
        
        # Opciones de Tamaño (para algunos platos)
        productos_con_tamano = [
            "Ceviche Clásico", "Ceviche Mixto", "Arroz con Mariscos", 
            "Chicha Morada", "Limonada Frozen"
        ]
        
        opciones_tamano = [
            ("Personal", 0.00, 1),
            ("Para 2 personas", 15.00, 2),
            ("Familiar (4 personas)", 30.00, 3),
        ]
        
        for nombre_producto in productos_con_tamano:
            if nombre_producto in productos_map and "tamano" in tipos_map:
                for nombre, precio, orden in opciones_tamano:
                    opcion_data = {
                        "id_producto": productos_map[nombre_producto],
                        "id_tipo_opcion": tipos_map["tamano"],
                        "nombre": nombre,
                        "precio_adicional": precio,
                        "activo": True,
                        "orden": orden
                    }
                    response = self.make_request('POST', '/api/v1/producto-opciones', opcion_data)
                    if response and 'id' in response:
                        self.created_ids['producto_opciones'].append(response['id'])
                        created_count += 1
        
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
            
            self.create_productos_completos()
            time.sleep(1)
            
            self.create_producto_opciones_completas()
            
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
