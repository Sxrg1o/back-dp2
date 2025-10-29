"""
Script para probar el flujo completo de pedidos.

Este script demuestra:
1. Seleccionar un pedido (o crear uno nuevo)
2. Seleccionar opciones para los productos
3. Insertar productos con opciones en la tabla pedidos
4. Calcular totales y actualizar el estado

Ejecutar con:
    python -m scripts.borradores.test_pedidos_flow
"""

import asyncio
import sys
from pathlib import Path
from decimal import Decimal
import os
from datetime import datetime

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from src.core.database import BaseModel
from src.models.mesas.mesa_model import MesaModel
from src.models.menu.producto_model import ProductoModel
from src.models.pedidos.tipo_opciones_model import TipoOpcionModel
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel
from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.pedidos.pedido_opcion_model import PedidoOpcionModel
from src.core.enums.pedido_enums import EstadoPedido


def get_database_url() -> str:
    """
    Obtiene la URL de la base de datos desde variables de entorno.
    
    Returns:
        str: URL de conexión a la base de datos
    """
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        database_url = "sqlite+aiosqlite:///instance/restaurant.db"
    
    return database_url


class PedidosFlowTester:
    """Clase para probar el flujo completo de pedidos."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def test_complete_flow(self):
        """Ejecuta el flujo completo de prueba de pedidos."""
        print("=" * 80)
        print("🍽️  FLUJO COMPLETO DE PEDIDOS - PRUEBA")
        print("=" * 80)
        
        try:
            # Paso 1: Obtener o crear una mesa
            print("\n📍 PASO 1: Seleccionando una mesa...")
            mesa = await self.get_or_create_mesa()
            print(f"   ✓ Mesa seleccionada: {mesa.numero} (ID: {mesa.id})")
            
            # Paso 2: Crear un nuevo pedido
            print("\n📋 PASO 2: Creando un nuevo pedido...")
            pedido = await self.create_pedido(mesa.id)
            print(f"   ✓ Pedido creado: {pedido.numero_pedido} (ID: {pedido.id})")
            print(f"   - Estado: {pedido.estado.value}")
            print(f"   - Total inicial: S/. {pedido.total}")
            
            # Paso 3: Obtener productos disponibles
            print("\n🍲 PASO 3: Obteniendo productos disponibles...")
            productos = await self.get_productos()
            print(f"   ✓ Se encontraron {len(productos)} productos")
            
            if not productos:
                print("   ⚠️  No hay productos disponibles. Abortando prueba.")
                return
            
            # Paso 4: Obtener tipos de opciones y opciones disponibles
            print("\n⚙️  PASO 4: Obteniendo opciones disponibles...")
            tipos_opciones = await self.get_tipos_opciones()
            print(f"   ✓ Se encontraron {len(tipos_opciones)} tipos de opciones")
            
            opciones_disponibles = await self.get_opciones_disponibles()
            print(f"   ✓ Se encontraron {len(opciones_disponibles)} opciones disponibles")
            
            # Paso 5: Agregar productos al pedido con opciones
            print("\n🛒 PASO 5: Agregando productos al pedido con opciones...")
            
            # Seleccionar los primeros 2 productos
            productos_a_agregar = productos[:2]
            total_pedido = Decimal("0.00")
            
            for idx, producto in enumerate(productos_a_agregar, 1):
                print(f"\n   Producto {idx}: {producto.nombre}")
                print(f"   - Precio: S/. {producto.precio}")
                
                # Crear item de pedido
                pedido_producto = await self.create_pedido_producto(
                    pedido.id,
                    producto.id,
                    cantidad=1,
                    precio_unitario=producto.precio
                )
                print(f"   - Item creado (ID: {pedido_producto.id})")
                
                # Seleccionar opciones para este producto
                opciones_seleccionadas = []
                precio_opciones = Decimal("0.00")
                
                # Filtrar opciones disponibles para este producto
                opciones_del_producto = [
                    op for op in opciones_disponibles 
                    if op.id_producto == producto.id
                ]
                
                if opciones_del_producto:
                    # Seleccionar hasta 2 opciones
                    for opcion in opciones_del_producto[:2]:
                        print(f"     - Opción: {opcion.nombre} (S/. {opcion.precio_adicional})")
                        
                        # Crear registro de opción en el pedido
                        pedido_opcion = await self.create_pedido_opcion(
                            pedido_producto.id,
                            opcion.id,
                            opcion.precio_adicional
                        )
                        
                        opciones_seleccionadas.append(pedido_opcion)
                        precio_opciones += opcion.precio_adicional
                
                # Actualizar precio de opciones en el item
                await self.update_pedido_producto_opciones(
                    pedido_producto.id,
                    precio_opciones
                )
                
                # Calcular subtotal del item
                subtotal_item = Decimal(str(pedido_producto.cantidad)) * (
                    pedido_producto.precio_unitario + precio_opciones
                )
                total_pedido += subtotal_item
                
                print(f"   - Opciones seleccionadas: {len(opciones_seleccionadas)}")
                print(f"   - Precio opciones: S/. {precio_opciones}")
                print(f"   - Subtotal item: S/. {subtotal_item}")
            
            # Paso 6: Actualizar totales del pedido
            print(f"\n💰 PASO 6: Actualizando totales del pedido...")
            await self.update_pedido_totales(pedido.id, total_pedido)
            
            # Paso 7: Confirmar el pedido
            print(f"\n✅ PASO 7: Confirmando el pedido...")
            await self.confirm_pedido(pedido.id)
            
            # Paso 8: Obtener el pedido actualizado
            print(f"\n📊 PASO 8: Obteniendo detalles finales del pedido...")
            pedido_final = await self.get_pedido_by_id(pedido.id)
            
            print("\n" + "=" * 80)
            print("📋 RESUMEN FINAL DEL PEDIDO")
            print("=" * 80)
            print(f"Número de pedido: {pedido_final.numero_pedido}")
            print(f"Mesa: {mesa.numero}")
            print(f"Estado: {pedido_final.estado.value}")
            print(f"Subtotal: S/. {pedido_final.subtotal}")
            print(f"Impuestos: S/. {pedido_final.impuestos}")
            print(f"Descuentos: S/. {pedido_final.descuentos}")
            print(f"Total: S/. {pedido_final.total}")
            print(f"Fecha creación: {pedido_final.fecha_creacion}")
            print(f"Fecha confirmado: {pedido_final.fecha_confirmado}")
            print("=" * 80)
            print("\n✅ ¡Flujo de pedidos completado exitosamente!")
            
        except Exception as e:
            print(f"\n❌ Error durante la prueba: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def get_or_create_mesa(self) -> MesaModel:
        """Obtiene una mesa existente o crea una nueva."""
        # Intentar obtener una mesa existente
        result = await self.session.execute(select(MesaModel).limit(1))
        mesa = result.scalars().first()
        
        if mesa:
            return mesa
        
        # Si no existe, crear una nueva
        mesa = MesaModel(
            numero=1,
            capacidad=4,
            ubicacion="Zona A",
            activo=True
        )
        self.session.add(mesa)
        await self.session.commit()
        await self.session.refresh(mesa)
        return mesa
    
    async def create_pedido(self, id_mesa: str) -> PedidoModel:
        """Crea un nuevo pedido."""
        # Generar número de pedido único
        numero_pedido = f"{datetime.now().strftime('%Y%m%d')}-M1-001"
        
        pedido = PedidoModel(
            id_mesa=id_mesa,
            numero_pedido=numero_pedido,
            estado=EstadoPedido.PENDIENTE,
            subtotal=Decimal("0.00"),
            impuestos=Decimal("0.00"),
            descuentos=Decimal("0.00"),
            total=Decimal("0.00"),
            notas_cliente="Prueba de flujo de pedidos"
        )
        self.session.add(pedido)
        await self.session.commit()
        await self.session.refresh(pedido)
        return pedido
    
    async def get_productos(self) -> list:
        """Obtiene todos los productos disponibles."""
        result = await self.session.execute(
            select(ProductoModel).where(ProductoModel.activo == True).limit(5)
        )
        return result.scalars().all()
    
    async def get_tipos_opciones(self) -> list:
        """Obtiene todos los tipos de opciones disponibles."""
        result = await self.session.execute(
            select(TipoOpcionModel).where(TipoOpcionModel.activo == True)
        )
        return result.scalars().all()
    
    async def get_opciones_disponibles(self) -> list:
        """Obtiene todas las opciones de productos disponibles."""
        result = await self.session.execute(
            select(ProductoOpcionModel).limit(10)
        )
        return result.scalars().all()
    
    async def create_pedido_producto(
        self,
        id_pedido: str,
        id_producto: str,
        cantidad: int = 1,
        precio_unitario: Decimal = Decimal("0.00")
    ) -> PedidoProductoModel:
        """Crea un item de producto en el pedido."""
        subtotal = Decimal(str(cantidad)) * precio_unitario
        
        pedido_producto = PedidoProductoModel(
            id_pedido=id_pedido,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            precio_opciones=Decimal("0.00"),
            subtotal=subtotal,
            notas_personalizacion="Sin notas especiales"
        )
        self.session.add(pedido_producto)
        await self.session.commit()
        await self.session.refresh(pedido_producto)
        return pedido_producto
    
    async def create_pedido_opcion(
        self,
        id_pedido_producto: str,
        id_producto_opcion: str,
        precio_adicional: Decimal = Decimal("0.00")
    ) -> PedidoOpcionModel:
        """Crea una opción para un item del pedido."""
        pedido_opcion = PedidoOpcionModel(
            id_pedido_producto=id_pedido_producto,
            id_producto_opcion=id_producto_opcion,
            precio_adicional=precio_adicional
        )
        self.session.add(pedido_opcion)
        await self.session.commit()
        await self.session.refresh(pedido_opcion)
        return pedido_opcion
    
    async def update_pedido_producto_opciones(
        self,
        id_pedido_producto: str,
        precio_opciones: Decimal
    ) -> None:
        """Actualiza el precio de opciones en un item del pedido."""
        result = await self.session.execute(
            select(PedidoProductoModel).where(
                PedidoProductoModel.id == id_pedido_producto
            )
        )
        pedido_producto = result.scalars().first()
        
        if pedido_producto:
            pedido_producto.precio_opciones = precio_opciones
            # Recalcular subtotal
            pedido_producto.subtotal = Decimal(str(pedido_producto.cantidad)) * (
                pedido_producto.precio_unitario + precio_opciones
            )
            await self.session.commit()
    
    async def update_pedido_totales(
        self,
        id_pedido: str,
        subtotal: Decimal
    ) -> None:
        """Actualiza los totales del pedido."""
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == id_pedido)
        )
        pedido = result.scalars().first()
        
        if pedido:
            pedido.subtotal = subtotal
            pedido.impuestos = subtotal * Decimal("0.18")  # 18% de impuestos
            pedido.descuentos = Decimal("0.00")
            pedido.total = subtotal + pedido.impuestos - pedido.descuentos
            await self.session.commit()
    
    async def confirm_pedido(self, id_pedido: str) -> None:
        """Confirma un pedido cambiando su estado."""
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == id_pedido)
        )
        pedido = result.scalars().first()
        
        if pedido:
            pedido.estado = EstadoPedido.CONFIRMADO
            pedido.fecha_confirmado = datetime.now()
            await self.session.commit()
    
    async def get_pedido_by_id(self, id_pedido: str) -> PedidoModel:
        """Obtiene un pedido por su ID."""
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == id_pedido)
        )
        return result.scalars().first()


async def main():
    """Función principal."""
    database_url = get_database_url()
    print(f"📦 Conectando a base de datos: {database_url}\n")
    
    # Crear engine
    engine = create_async_engine(
        database_url,
        echo=False,  # Cambiar a True para ver las queries SQL
        future=True
    )
    
    # Crear tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    # Crear sesión
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        tester = PedidosFlowTester(session)
        await tester.test_complete_flow()
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
