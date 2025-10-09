"""
Script para mostrar un resumen completo de los datos del seed creados
URL: https://back-dp2.onrender.com/
"""

import requests
import json
from typing import Dict, List

class SeedSummary:
    """Mostrar resumen de los datos del seed."""
    
    def __init__(self):
        self.base_url = "https://back-dp2.onrender.com"
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
    
    def get_data(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Obtener datos de un endpoint."""
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", params=params or {})
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                print(f"❌ Error {response.status_code} en {endpoint}")
                return []
        except Exception as e:
            print(f"❌ Error en {endpoint}: {e}")
            return []
    
    def show_roles(self):
        """Mostrar roles creados."""
        print("\n👥 ROLES CREADOS")
        print("="*50)
        
        roles = self.get_data('/api/v1/roles', {'limit': 100})
        
        if roles:
            print(f"📊 Total: {len(roles)} roles")
            for i, rol in enumerate(roles, 1):
                print(f"{i:2d}. {rol['nombre']}")
                print(f"    📝 {rol.get('descripcion', 'Sin descripción')}")
                print(f"    🆔 ID: {rol['id']}")
                print(f"    ✅ Activo: {rol.get('activo', False)}")
                print()
        else:
            print("❌ No se encontraron roles")
    
    def show_categorias(self):
        """Mostrar categorías creadas."""
        print("\n📂 CATEGORÍAS CREADAS")
        print("="*50)
        
        categorias = self.get_data('/api/v1/categorias', {'limit': 100})
        
        if categorias:
            print(f"📊 Total: {len(categorias)} categorías")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i:2d}. {categoria['nombre']}")
                print(f"    📝 {categoria.get('descripcion', 'Sin descripción')}")
                print(f"    🖼️ Imagen: {categoria.get('imagen_path', 'Sin imagen')[:50]}...")
                print(f"    🆔 ID: {categoria['id']}")
                print(f"    ✅ Activo: {categoria.get('activo', False)}")
                print()
        else:
            print("❌ No se encontraron categorías")
    
    def show_alergenos(self):
        """Mostrar alérgenos creados."""
        print("\n⚠️ ALÉRGENOS CREADOS")
        print("="*50)
        
        alergenos = self.get_data('/api/v1/alergenos', {'limit': 100})
        
        if alergenos:
            print(f"📊 Total: {len(alergenos)} alérgenos")
            for i, alergeno in enumerate(alergenos, 1):
                print(f"{i:2d}. {alergeno['nombre']} {alergeno.get('icono', '')}")
                print(f"    📝 {alergeno.get('descripcion', 'Sin descripción')}")
                print(f"    🚨 Nivel de riesgo: {alergeno.get('nivel_riesgo', 'No especificado')}")
                print(f"    🆔 ID: {alergeno['id']}")
                print(f"    ✅ Activo: {alergeno.get('activo', False)}")
                print()
        else:
            print("❌ No se encontraron alérgenos")
    
    def show_productos(self):
        """Mostrar productos creados."""
        print("\n🍽️ PRODUCTOS CREADOS")
        print("="*50)
        
        productos = self.get_data('/api/v1/productos', {'limit': 100})
        
        if productos:
            print(f"📊 Total: {len(productos)} productos")
            for i, producto in enumerate(productos, 1):
                print(f"{i:2d}. {producto['nombre']}")
                print(f"    💰 Precio: S/ {producto.get('precio_base', '0.00')}")
                print(f"    📝 {producto.get('descripcion', 'Sin descripción')[:80]}...")
                print(f"    🖼️ Imagen: {producto.get('imagen_path', 'Sin imagen')[:50]}...")
                print(f"    🆔 ID: {producto['id']}")
                print(f"    ✅ Disponible: {producto.get('disponible', False)}")
                print(f"    ⭐ Destacado: {producto.get('destacado', False)}")
                print()
        else:
            print("❌ No se encontraron productos")
    
    def show_tipos_opciones(self):
        """Mostrar tipos de opciones creados."""
        print("\n⚙️ TIPOS DE OPCIONES CREADOS")
        print("="*50)
        
        tipos = self.get_data('/api/v1/tipos-opciones', {'limit': 100})
        
        if tipos:
            print(f"📊 Total: {len(tipos)} tipos de opciones")
            for i, tipo in enumerate(tipos, 1):
                print(f"{i:2d}. {tipo['nombre']} ({tipo.get('codigo', 'Sin código')})")
                print(f"    📝 {tipo.get('descripcion', 'Sin descripción')}")
                print(f"    🔢 Orden: {tipo.get('orden', 'No especificado')}")
                print(f"    🆔 ID: {tipo['id']}")
                print(f"    ✅ Activo: {tipo.get('activo', False)}")
                print()
        else:
            print("❌ No se encontraron tipos de opciones")
    
    def show_producto_opciones(self):
        """Mostrar opciones de productos creadas."""
        print("\n🎛️ OPCIONES DE PRODUCTOS CREADAS")
        print("="*50)
        
        opciones = self.get_data('/api/v1/producto-opciones', {'limit': 100})
        
        if opciones:
            print(f"📊 Total: {len(opciones)} opciones de productos")
            for i, opcion in enumerate(opciones, 1):
                print(f"{i:2d}. {opcion['nombre']}")
                print(f"    💰 Precio adicional: S/ {opcion.get('precio_adicional', '0.00')}")
                print(f"    🔢 Orden: {opcion.get('orden', 'No especificado')}")
                print(f"    🆔 ID: {opcion['id']}")
                print(f"    🍽️ Producto ID: {opcion.get('id_producto', 'No especificado')}")
                print(f"    ⚙️ Tipo ID: {opcion.get('id_tipo_opcion', 'No especificado')}")
                print(f"    ✅ Activo: {opcion.get('activo', False)}")
                print()
        else:
            print("❌ No se encontraron opciones de productos")
    
    def show_categorias_con_productos(self):
        """Mostrar categorías con sus productos."""
        print("\n📂 CATEGORÍAS CON PRODUCTOS")
        print("="*50)
        
        categorias_con_productos = self.get_data('/api/v1/categorias/productos/cards', {'limit': 100})
        
        if categorias_con_productos:
            print(f"📊 Total: {len(categorias_con_productos)} categorías con productos")
            for i, categoria in enumerate(categorias_con_productos, 1):
                print(f"{i:2d}. {categoria['nombre']}")
                print(f"    🖼️ Imagen: {categoria.get('imagen_path', 'Sin imagen')[:50]}...")
                print(f"    🆔 ID: {categoria['id']}")
                
                productos = categoria.get('productos', [])
                if productos:
                    print(f"    🍽️ Productos ({len(productos)}):")
                    for j, producto in enumerate(productos[:5], 1):  # Mostrar solo los primeros 5
                        print(f"       {j}. {producto['nombre']} (ID: {producto['id'][:8]}...)")
                    if len(productos) > 5:
                        print(f"       ... y {len(productos) - 5} productos más")
                else:
                    print("    🍽️ Sin productos")
                print()
        else:
            print("❌ No se encontraron categorías con productos")
    
    def show_productos_cards(self):
        """Mostrar productos en formato cards."""
        print("\n🍽️ PRODUCTOS EN FORMATO CARDS")
        print("="*50)
        
        productos_cards = self.get_data('/api/v1/productos/cards', {'limit': 20})
        
        if productos_cards:
            print(f"📊 Total: {len(productos_cards)} productos (mostrando primeros 20)")
            for i, producto in enumerate(productos_cards, 1):
                print(f"{i:2d}. {producto['nombre']}")
                print(f"    💰 Precio: S/ {producto.get('precio_base', '0.00')}")
                print(f"    🖼️ Imagen: {producto.get('imagen_path', 'Sin imagen')[:50]}...")
                print(f"    🆔 ID: {producto['id']}")
                categoria = producto.get('categoria', {})
                if categoria:
                    print(f"    📂 Categoría: {categoria.get('nombre', 'Sin nombre')} (ID: {categoria.get('id', 'Sin ID')[:8]}...)")
                print()
        else:
            print("❌ No se encontraron productos en formato cards")
    
    def show_statistics(self):
        """Mostrar estadísticas generales."""
        print("\n📊 ESTADÍSTICAS GENERALES")
        print("="*50)
        
        endpoints = {
            'Roles': '/api/v1/roles',
            'Categorías': '/api/v1/categorias',
            'Alérgenos': '/api/v1/alergenos',
            'Productos': '/api/v1/productos',
            'Tipos de Opciones': '/api/v1/tipos-opciones',
            'Opciones de Productos': '/api/v1/producto-opciones'
        }
        
        total_records = 0
        
        for nombre, endpoint in endpoints.items():
            data = self.get_data(endpoint, {'limit': 1})
            if data:
                # Obtener el total real
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}", params={'limit': 1})
                    if response.status_code == 200:
                        total = response.json().get('total', 0)
                        print(f"📋 {nombre}: {total} registros")
                        total_records += total
                    else:
                        print(f"❌ {nombre}: Error al obtener total")
                except:
                    print(f"❌ {nombre}: Error de conexión")
            else:
                print(f"❌ {nombre}: Sin datos")
        
        print(f"\n🎯 TOTAL GENERAL: {total_records} registros")
    
    def run_complete_summary(self):
        """Ejecutar resumen completo."""
        print("🚀 RESUMEN COMPLETO DE DATOS DE SEED")
        print(f"🌐 Servidor: {self.base_url}")
        print("="*60)
        
        try:
            # Mostrar estadísticas generales
            self.show_statistics()
            
            # Mostrar detalles por módulo
            self.show_roles()
            self.show_categorias()
            self.show_alergenos()
            self.show_productos()
            self.show_tipos_opciones()
            self.show_producto_opciones()
            
            # Mostrar vistas especiales
            self.show_categorias_con_productos()
            self.show_productos_cards()
            
            print("\n🎉 RESUMEN COMPLETADO")
            print("✅ Todos los datos del seed están disponibles en el servidor")
            print("🔗 Puedes acceder a la documentación en: https://back-dp2.onrender.com/docs")
            
        except Exception as e:
            print(f"\n❌ Error durante el resumen: {e}")

def main():
    """Función principal."""
    summary = SeedSummary()
    summary.run_complete_summary()

if __name__ == "__main__":
    main()
