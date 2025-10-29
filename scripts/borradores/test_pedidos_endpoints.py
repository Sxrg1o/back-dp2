"""
Script para probar el flujo completo de pedidos usando únicamente endpoints HTTP.

Este script demuestra:
1. Obtener mesas disponibles desde la API
2. Obtener productos disponibles desde la API
3. Crear un pedido completo con productos usando el endpoint /pedidos/completo
4. Consultar el estado del pedido
5. Actualizar el estado del pedido

Ejecutar con:
    python -m scripts.borradores.test_pedidos_endpoints
"""

import asyncio
import sys
import os
from pathlib import Path
from decimal import Decimal
import json
from datetime import datetime
from typing import Dict, Any, List

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Importar la aplicación FastAPI
from src.main import app


class PedidosEndpointsTester:
    """Clase para probar el flujo completo de pedidos usando solo endpoints HTTP."""
    
    def __init__(self):
        self.client = TestClient(app)
        self.base_url = "http://localhost:8000"
    
    async def test_complete_flow(self):
        """Ejecuta el flujo completo de prueba de pedidos usando endpoints."""
        print("=" * 80)
        print("🍽️  FLUJO COMPLETO DE PEDIDOS - PRUEBA CON ENDPOINTS")
        print("=" * 80)
        
        try:
            # Paso 1: Obtener mesas disponibles
            print("\n📍 PASO 1: Obteniendo mesas disponibles...")
            mesas = await self.get_mesas()
            
            if not mesas:
                print("   ⚠️  No hay mesas disponibles. Creando una mesa...")
                mesa = await self.create_mesa()
            else:
                mesa = mesas[0]
                print(f"   ✓ Mesa seleccionada: {mesa['numero']} (ID: {mesa['id']})")
            
            # Paso 2: Obtener productos disponibles
            print("\n🍲 PASO 2: Obteniendo productos disponibles...")
            productos = await self.get_productos()
            print(f"   ✓ Se encontraron {len(productos)} productos")
            
            if len(productos) < 2:
                print("   ⚠️  Se necesitan al menos 2 productos. Abortando prueba.")
                return
            
            # Paso 3: Crear un pedido completo con productos
            print("\n🛒 PASO 3: Creando pedido completo con productos...")
            
            # Seleccionar los primeros 2 productos
            productos_seleccionados = productos[:2]
            items_pedido = []
            
            for producto in productos_seleccionados:
                # Usar precio_base que es el campo correcto del modelo
                precio = producto.get('precio_base', producto.get('precio', 0.0))
                item = {
                    "id_producto": producto['id'],
                    "cantidad": 1,
                    "precio_unitario": float(precio),
                    "precio_opciones": 2.50,  # Simulamos algunas opciones
                    "notas_personalizacion": "Sin especificaciones especiales"
                }
                items_pedido.append(item)
                print(f"   - Producto: {producto['nombre']} - S/. {precio}")
            
            # Crear el pedido usando el endpoint /pedidos/completo
            # Agregar timestamp único para evitar conflictos
            import time
            timestamp = str(int(time.time()))[-4:]  # Últimos 4 dígitos del timestamp
            pedido_data = {
                "id_mesa": mesa['id'],
                "items": items_pedido,
                "notas_cliente": f"Pedido de prueba usando endpoints - {timestamp}",
                "notas_cocina": "Sin instrucciones especiales"
            }
            
            pedido = await self.create_pedido_completo(pedido_data)
            print(f"   ✓ Pedido creado: {pedido['numero_pedido']} (ID: {pedido['id']})")
            print(f"   - Estado: {pedido['estado']}")
            print(f"   - Total: S/. {pedido['total']}")
            
            # Paso 4: Consultar el pedido creado
            print(f"\n📋 PASO 4: Consultando detalles del pedido...")
            pedido_detalles = await self.get_pedido(pedido['id'])
            print(f"   ✓ Pedido consultado exitosamente")
            print(f"   - Número de items: {len(pedido_detalles.get('items', []))}")
            print(f"   - Subtotal: S/. {pedido_detalles['subtotal']}")
            print(f"   - Impuestos: S/. {pedido_detalles['impuestos']}")
            
            # Paso 5: Cambiar estado del pedido a confirmado
            print(f"\n✅ PASO 5: Confirmando el pedido...")
            estado_data = {"estado": "confirmado"}
            pedido_confirmado = await self.update_estado_pedido(pedido['id'], estado_data)
            print(f"   ✓ Pedido confirmado exitosamente")
            print(f"   - Nuevo estado: {pedido_confirmado['estado']}")
            print(f"   - Fecha confirmado: {pedido_confirmado.get('fecha_confirmado', 'N/A')}")
            
            # Paso 6: Cambiar estado del pedido a en_preparacion
            print(f"\n👨‍🍳 PASO 6: Enviando pedido a cocina...")
            estado_data = {"estado": "en_preparacion"}
            pedido_preparacion = await self.update_estado_pedido(pedido['id'], estado_data)
            print(f"   ✓ Pedido enviado a cocina")
            print(f"   - Nuevo estado: {pedido_preparacion['estado']}")
            
            # Paso 7: Obtener lista de pedidos
            print(f"\n📊 PASO 7: Obteniendo lista de pedidos...")
            lista_pedidos = await self.get_lista_pedidos()
            print(f"   ✓ Se encontraron {lista_pedidos['total']} pedidos en total")
            print(f"   - Pedidos en la página actual: {len(lista_pedidos['items'])}")
            
            print("\n" + "=" * 80)
            print("📋 RESUMEN FINAL DEL PEDIDO")
            print("=" * 80)
            print(f"Número de pedido: {pedido_preparacion['numero_pedido']}")
            print(f"Mesa: {mesa['numero']}")
            print(f"Estado final: {pedido_preparacion['estado']}")
            print(f"Subtotal: S/. {pedido_preparacion['subtotal']}")
            print(f"Impuestos: S/. {pedido_preparacion['impuestos']}")
            print(f"Total: S/. {pedido_preparacion['total']}")
            print(f"Fecha creación: {pedido_preparacion['fecha_creacion']}")
            print("=" * 80)
            print("\n✅ ¡Flujo de pedidos con endpoints completado exitosamente!")
            
        except Exception as e:
            print(f"\n❌ Error durante la prueba: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def get_mesas(self) -> List[Dict[str, Any]]:
        """Obtiene las mesas disponibles desde la API."""
        response = self.client.get("/api/v1/mesas?limit=10")
        if response.status_code != 200:
            print(f"   ❌ Error al obtener mesas: {response.status_code} - {response.text}")
            return []
        
        data = response.json()
        return data.get('items', [])
    
    async def create_mesa(self) -> Dict[str, Any]:
        """Crea una nueva mesa usando la API."""
        mesa_data = {
            "numero": "TEST-001",
            "capacidad": 4,
            "id_zona": None,  # Sin zona por ahora
            "nota": "Mesa de prueba para endpoints",
            "activo": True,
            "estado": "disponible"
        }
        
        response = self.client.post("/api/v1/mesas", json=mesa_data)
        if response.status_code != 201:
            raise Exception(f"Error al crear mesa: {response.status_code} - {response.text}")
        
        mesa = response.json()
        print(f"   ✓ Mesa creada: {mesa['numero']} (ID: {mesa['id']})")
        return mesa
    
    async def get_productos(self) -> List[Dict[str, Any]]:
        """Obtiene los productos disponibles desde la API."""
        # Intentar primero el endpoint que el usuario mencionó
        response = self.client.get("/api/v1/productos?skip=0&limit=100")
        if response.status_code == 200:
            data = response.json()
            productos = data.get('items', [])
            if productos:
                print(f"   ✓ Usando endpoint /api/v1/productos")
                return productos
        
        # Si no funciona, intentar el endpoint de cards
        response = self.client.get("/api/v1/productos/cards?limit=10")
        if response.status_code == 200:
            data = response.json()
            productos = data.get('items', [])
            if productos:
                print(f"   ✓ Usando endpoint /api/v1/productos/cards")
                return productos
        
        print(f"   ❌ Error al obtener productos desde ambos endpoints")
        print(f"      /api/v1/productos: {response.status_code}")
        
        # Intentar obtener información de debug
        response_debug = self.client.get("/api/v1/productos/cards?limit=1")
        print(f"      /api/v1/productos/cards: {response_debug.status_code}")
        if response_debug.status_code != 200:
            print(f"      Response text: {response_debug.text}")
        
        return []
    
    async def create_pedido_completo(self, pedido_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un pedido completo usando la API."""
        response = self.client.post("/api/v1/pedidos/completo", json=pedido_data)
        if response.status_code != 201:
            raise Exception(f"Error al crear pedido completo: {response.status_code} - {response.text}")
        
        return response.json()
    
    async def get_pedido(self, pedido_id: str) -> Dict[str, Any]:
        """Obtiene un pedido por su ID usando la API."""
        response = self.client.get(f"/api/v1/pedidos/{pedido_id}")
        if response.status_code != 200:
            raise Exception(f"Error al obtener pedido: {response.status_code} - {response.text}")
        
        return response.json()
    
    async def update_estado_pedido(self, pedido_id: str, estado_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza el estado de un pedido usando la API."""
        response = self.client.patch(f"/api/v1/pedidos/{pedido_id}/estado", json=estado_data)
        if response.status_code != 200:
            raise Exception(f"Error al actualizar estado del pedido: {response.status_code} - {response.text}")
        
        return response.json()
    
    async def get_lista_pedidos(self) -> Dict[str, Any]:
        """Obtiene la lista de pedidos usando la API."""
        response = self.client.get("/api/v1/pedidos?limit=10")
        if response.status_code != 200:
            raise Exception(f"Error al obtener lista de pedidos: {response.status_code} - {response.text}")
        
        return response.json()


async def main():
    """Función principal."""
    print(f"🚀 Iniciando prueba de endpoints de pedidos\n")
    
    tester = PedidosEndpointsTester()
    await tester.test_complete_flow()


if __name__ == "__main__":
    asyncio.run(main())
