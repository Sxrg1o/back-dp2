"""
Ejemplos individuales de operaciones CRUD para pedidos.

Este script muestra cómo realizar operaciones específicas:
- Crear un pedido
- Agregar productos a un pedido
- Agregar opciones a un producto
- Actualizar un pedido
- Consultar pedidos
- Eliminar un pedido

Ejecutar con:
    python -m scripts.borradores.ejemplos_operaciones
"""

import asyncio
import sys
from pathlib import Path
from decimal import Decimal
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from src.core.database import BaseModel
from src.models.mesas.mesa_model import MesaModel
from src.models.menu.producto_model import ProductoModel
from src.models.pedidos.pedido_model import PedidoModel
from src.models.pedidos.pedido_producto_model import PedidoProductoModel
from src.models.pedidos.pedido_opcion_model import PedidoOpcionModel
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel
from src.core.enums.pedido_enums import EstadoPedido


def get_database_url() -> str:
    """Obtiene la URL de la base de datos."""
    database_url = os.getenv("DATABASE_URL")
    return database_url or "sqlite+aiosqlite:///instance/restaurant.db"


class EjemplosOperaciones:
    """Ejemplos de operaciones CRUD para pedidos."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ==================== EJEMPLOS DE CREACIÓN ====================
    
    async def ejemplo_crear_pedido(self):
        """Ejemplo: Crear un nuevo pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 1: CREAR UN NUEVO PEDIDO")
        print("=" * 80)
        
        # Obtener una mesa
        result = await self.session.execute(select(MesaModel).limit(1))
        mesa = result.scalars().first()
        
        if not mesa:
            print("❌ No hay mesas disponibles")
            return None
        
        # Crear pedido
        numero_pedido = f"{datetime.now().strftime('%Y%m%d')}-M{mesa.numero}-001"
        
        pedido = PedidoModel(
            id_mesa=mesa.id,
            numero_pedido=numero_pedido,
            estado=EstadoPedido.PENDIENTE,
            subtotal=Decimal("0.00"),
            impuestos=Decimal("0.00"),
            descuentos=Decimal("0.00"),
            total=Decimal("0.00"),
            notas_cliente="Ejemplo de creación"
        )
        
        self.session.add(pedido)
        await self.session.commit()
        await self.session.refresh(pedido)
        
        print(f"✓ Pedido creado exitosamente")
        print(f"  - ID: {pedido.id}")
        print(f"  - Número: {pedido.numero_pedido}")
        print(f"  - Mesa: {mesa.numero}")
        print(f"  - Estado: {pedido.estado.value}")
        print(f"  - Total: S/. {pedido.total}")
        
        return pedido
    
    async def ejemplo_agregar_producto_a_pedido(self, pedido: PedidoModel):
        """Ejemplo: Agregar un producto a un pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 2: AGREGAR UN PRODUCTO A UN PEDIDO")
        print("=" * 80)
        
        # Obtener un producto
        result = await self.session.execute(
            select(ProductoModel).where(ProductoModel.activo == True).limit(1)
        )
        producto = result.scalars().first()
        
        if not producto:
            print("❌ No hay productos disponibles")
            return None
        
        # Crear item de pedido
        pedido_producto = PedidoProductoModel(
            id_pedido=pedido.id,
            id_producto=producto.id,
            cantidad=2,
            precio_unitario=producto.precio,
            precio_opciones=Decimal("0.00"),
            subtotal=Decimal(str(2)) * producto.precio,
            notas_personalizacion="Sin cebolla"
        )
        
        self.session.add(pedido_producto)
        await self.session.commit()
        await self.session.refresh(pedido_producto)
        
        print(f"✓ Producto agregado al pedido")
        print(f"  - ID Item: {pedido_producto.id}")
        print(f"  - Producto: {producto.nombre}")
        print(f"  - Cantidad: {pedido_producto.cantidad}")
        print(f"  - Precio unitario: S/. {pedido_producto.precio_unitario}")
        print(f"  - Subtotal: S/. {pedido_producto.subtotal}")
        print(f"  - Notas: {pedido_producto.notas_personalizacion}")
        
        return pedido_producto
    
    async def ejemplo_agregar_opcion_a_producto(self, pedido_producto: PedidoProductoModel):
        """Ejemplo: Agregar opciones a un producto del pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 3: AGREGAR OPCIONES A UN PRODUCTO")
        print("=" * 80)
        
        # Obtener opciones disponibles
        result = await self.session.execute(
            select(ProductoOpcionModel).limit(2)
        )
        opciones = result.scalars().all()
        
        if not opciones:
            print("❌ No hay opciones disponibles")
            return []
        
        opciones_creadas = []
        precio_total_opciones = Decimal("0.00")
        
        for opcion in opciones:
            # Crear opción en el pedido
            pedido_opcion = PedidoOpcionModel(
                id_pedido_producto=pedido_producto.id,
                id_producto_opcion=opcion.id,
                precio_adicional=opcion.precio_adicional
            )
            
            self.session.add(pedido_opcion)
            opciones_creadas.append(pedido_opcion)
            precio_total_opciones += opcion.precio_adicional
            
            print(f"✓ Opción agregada: {opcion.nombre}")
            print(f"  - Precio adicional: S/. {opcion.precio_adicional}")
        
        # Actualizar precio de opciones en el producto
        pedido_producto.precio_opciones = precio_total_opciones
        pedido_producto.subtotal = Decimal(str(pedido_producto.cantidad)) * (
            pedido_producto.precio_unitario + precio_total_opciones
        )
        
        await self.session.commit()
        
        print(f"\n✓ Total opciones agregadas: {len(opciones_creadas)}")
        print(f"  - Precio total opciones: S/. {precio_total_opciones}")
        print(f"  - Nuevo subtotal del item: S/. {pedido_producto.subtotal}")
        
        return opciones_creadas
    
    # ==================== EJEMPLOS DE LECTURA ====================
    
    async def ejemplo_obtener_pedido_por_id(self, pedido_id: str):
        """Ejemplo: Obtener un pedido por su ID."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 4: OBTENER UN PEDIDO POR ID")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == pedido_id)
        )
        pedido = result.scalars().first()
        
        if not pedido:
            print(f"❌ Pedido no encontrado: {pedido_id}")
            return None
        
        print(f"✓ Pedido encontrado")
        print(f"  - ID: {pedido.id}")
        print(f"  - Número: {pedido.numero_pedido}")
        print(f"  - Estado: {pedido.estado.value}")
        print(f"  - Subtotal: S/. {pedido.subtotal}")
        print(f"  - Impuestos: S/. {pedido.impuestos}")
        print(f"  - Descuentos: S/. {pedido.descuentos}")
        print(f"  - Total: S/. {pedido.total}")
        
        return pedido
    
    async def ejemplo_obtener_productos_de_pedido(self, pedido_id: str):
        """Ejemplo: Obtener todos los productos de un pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 5: OBTENER PRODUCTOS DE UN PEDIDO")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoProductoModel).where(
                PedidoProductoModel.id_pedido == pedido_id
            )
        )
        productos = result.scalars().all()
        
        print(f"✓ Se encontraron {len(productos)} productos")
        
        for idx, pp in enumerate(productos, 1):
            print(f"\n  Producto {idx}:")
            print(f"    - ID: {pp.id}")
            print(f"    - Cantidad: {pp.cantidad}")
            print(f"    - Precio unitario: S/. {pp.precio_unitario}")
            print(f"    - Precio opciones: S/. {pp.precio_opciones}")
            print(f"    - Subtotal: S/. {pp.subtotal}")
            print(f"    - Notas: {pp.notas_personalizacion}")
        
        return productos
    
    async def ejemplo_obtener_opciones_de_producto(self, pedido_producto_id: str):
        """Ejemplo: Obtener todas las opciones de un producto del pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 6: OBTENER OPCIONES DE UN PRODUCTO")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoOpcionModel).where(
                PedidoOpcionModel.id_pedido_producto == pedido_producto_id
            )
        )
        opciones = result.scalars().all()
        
        print(f"✓ Se encontraron {len(opciones)} opciones")
        
        for idx, po in enumerate(opciones, 1):
            print(f"\n  Opción {idx}:")
            print(f"    - ID: {po.id}")
            print(f"    - ID Producto Opción: {po.id_producto_opcion}")
            print(f"    - Precio adicional: S/. {po.precio_adicional}")
            print(f"    - Fecha creación: {po.fecha_creacion}")
        
        return opciones
    
    async def ejemplo_listar_todos_los_pedidos(self):
        """Ejemplo: Listar todos los pedidos."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 7: LISTAR TODOS LOS PEDIDOS")
        print("=" * 80)
        
        result = await self.session.execute(select(PedidoModel).limit(10))
        pedidos = result.scalars().all()
        
        print(f"✓ Se encontraron {len(pedidos)} pedidos")
        
        for idx, pedido in enumerate(pedidos, 1):
            print(f"\n  Pedido {idx}:")
            print(f"    - Número: {pedido.numero_pedido}")
            print(f"    - Estado: {pedido.estado.value}")
            print(f"    - Total: S/. {pedido.total}")
            print(f"    - Fecha creación: {pedido.fecha_creacion}")
        
        return pedidos
    
    # ==================== EJEMPLOS DE ACTUALIZACIÓN ====================
    
    async def ejemplo_actualizar_estado_pedido(self, pedido_id: str, nuevo_estado: EstadoPedido):
        """Ejemplo: Actualizar el estado de un pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 8: ACTUALIZAR ESTADO DE UN PEDIDO")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == pedido_id)
        )
        pedido = result.scalars().first()
        
        if not pedido:
            print(f"❌ Pedido no encontrado")
            return None
        
        estado_anterior = pedido.estado.value
        pedido.estado = nuevo_estado
        
        # Actualizar timestamp según el nuevo estado
        if nuevo_estado == EstadoPedido.CONFIRMADO:
            pedido.fecha_confirmado = datetime.now()
        elif nuevo_estado == EstadoPedido.EN_PREPARACION:
            pedido.fecha_en_preparacion = datetime.now()
        elif nuevo_estado == EstadoPedido.LISTO:
            pedido.fecha_listo = datetime.now()
        elif nuevo_estado == EstadoPedido.ENTREGADO:
            pedido.fecha_entregado = datetime.now()
        elif nuevo_estado == EstadoPedido.CANCELADO:
            pedido.fecha_cancelado = datetime.now()
        
        await self.session.commit()
        
        print(f"✓ Estado actualizado")
        print(f"  - Estado anterior: {estado_anterior}")
        print(f"  - Nuevo estado: {pedido.estado.value}")
        
        return pedido
    
    async def ejemplo_actualizar_totales_pedido(self, pedido_id: str, subtotal: Decimal):
        """Ejemplo: Actualizar los totales de un pedido."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 9: ACTUALIZAR TOTALES DE UN PEDIDO")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoModel).where(PedidoModel.id == pedido_id)
        )
        pedido = result.scalars().first()
        
        if not pedido:
            print(f"❌ Pedido no encontrado")
            return None
        
        # Calcular totales
        impuestos = subtotal * Decimal("0.18")  # 18% IGV
        descuentos = Decimal("0.00")
        total = subtotal + impuestos - descuentos
        
        pedido.subtotal = subtotal
        pedido.impuestos = impuestos
        pedido.descuentos = descuentos
        pedido.total = total
        
        await self.session.commit()
        
        print(f"✓ Totales actualizados")
        print(f"  - Subtotal: S/. {pedido.subtotal}")
        print(f"  - Impuestos (18%): S/. {pedido.impuestos}")
        print(f"  - Descuentos: S/. {pedido.descuentos}")
        print(f"  - Total: S/. {pedido.total}")
        
        return pedido
    
    # ==================== EJEMPLOS DE ELIMINACIÓN ====================
    
    async def ejemplo_eliminar_opcion_de_producto(self, pedido_opcion_id: str):
        """Ejemplo: Eliminar una opción de un producto."""
        print("\n" + "=" * 80)
        print("📝 EJEMPLO 10: ELIMINAR UNA OPCIÓN DE UN PRODUCTO")
        print("=" * 80)
        
        result = await self.session.execute(
            select(PedidoOpcionModel).where(PedidoOpcionModel.id == pedido_opcion_id)
        )
        pedido_opcion = result.scalars().first()
        
        if not pedido_opcion:
            print(f"❌ Opción no encontrada")
            return
        
        id_pedido_producto = pedido_opcion.id_pedido_producto
        precio_eliminado = pedido_opcion.precio_adicional
        
        await self.session.delete(pedido_opcion)
        await self.session.commit()
        
        # Actualizar el precio de opciones del producto
        result = await self.session.execute(
            select(PedidoProductoModel).where(
                PedidoProductoModel.id == id_pedido_producto
            )
        )
        pedido_producto = result.scalars().first()
        
        if pedido_producto:
            pedido_producto.precio_opciones -= precio_eliminado
            pedido_producto.subtotal = Decimal(str(pedido_producto.cantidad)) * (
                pedido_producto.precio_unitario + pedido_producto.precio_opciones
            )
            await self.session.commit()
        
        print(f"✓ Opción eliminada")
        print(f"  - Precio eliminado: S/. {precio_eliminado}")
        print(f"  - Nuevo precio de opciones: S/. {pedido_producto.precio_opciones if pedido_producto else 'N/A'}")


async def main():
    """Función principal."""
    database_url = get_database_url()
    print(f"📦 Conectando a base de datos: {database_url}\n")
    
    engine = create_async_engine(
        database_url,
        echo=False,
        future=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        ejemplos = EjemplosOperaciones(session)
        
        # Ejecutar ejemplos en orden
        print("\n🎯 EJECUTANDO EJEMPLOS DE OPERACIONES CRUD\n")
        
        # Crear un pedido
        pedido = await ejemplos.ejemplo_crear_pedido()
        
        if pedido:
            # Agregar un producto
            pedido_producto = await ejemplos.ejemplo_agregar_producto_a_pedido(pedido)
            
            if pedido_producto:
                # Agregar opciones
                opciones = await ejemplos.ejemplo_agregar_opcion_a_producto(pedido_producto)
                
                # Obtener el pedido actualizado
                await ejemplos.ejemplo_obtener_pedido_por_id(pedido.id)
                
                # Obtener productos del pedido
                await ejemplos.ejemplo_obtener_productos_de_pedido(pedido.id)
                
                # Obtener opciones del producto
                if opciones:
                    await ejemplos.ejemplo_obtener_opciones_de_producto(pedido_producto.id)
                
                # Actualizar totales
                await ejemplos.ejemplo_actualizar_totales_pedido(
                    pedido.id,
                    pedido_producto.subtotal
                )
                
                # Cambiar estado
                await ejemplos.ejemplo_actualizar_estado_pedido(
                    pedido.id,
                    EstadoPedido.CONFIRMADO
                )
                
                # Listar todos los pedidos
                await ejemplos.ejemplo_listar_todos_los_pedidos()
        
        print("\n" + "=" * 80)
        print("✅ Ejemplos completados")
        print("=" * 80)
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
