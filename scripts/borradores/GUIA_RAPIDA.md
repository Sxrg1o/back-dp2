# Guía Rápida - Scripts de Prueba de Pedidos

## 📋 Resumen

Tienes dos scripts principales para probar el sistema de pedidos:

1. **`test_pedidos_flow.py`** - Flujo completo automático
2. **`ejemplos_operaciones.py`** - Ejemplos individuales de operaciones CRUD

## 🚀 Inicio Rápido

### Prerequisitos

```bash
# Asegúrate de tener la base de datos configurada
# En .env debe estar:
DATABASE_URL=sqlite+aiosqlite:///instance/restaurant.db
# O tu URL de MySQL

# Carga datos de prueba (si no los tienes)
python -m scripts.seed_cevicheria_data
```

### Ejecutar el Flujo Completo

```bash
python -m scripts.borradores.test_pedidos_flow
```

**Salida esperada:**
```
================================================================================
🍽️  FLUJO COMPLETO DE PEDIDOS - PRUEBA
================================================================================

📍 PASO 1: Seleccionando una mesa...
   ✓ Mesa seleccionada: 1 (ID: ...)

📋 PASO 2: Creando un nuevo pedido...
   ✓ Pedido creado: 20250129-M1-001 (ID: ...)
   
... (más pasos)

✅ ¡Flujo de pedidos completado exitosamente!
```

### Ejecutar Ejemplos Individuales

```bash
python -m scripts.borradores.ejemplos_operaciones
```

**Salida esperada:**
```
🎯 EJECUTANDO EJEMPLOS DE OPERACIONES CRUD

📝 EJEMPLO 1: CREAR UN NUEVO PEDIDO
✓ Pedido creado exitosamente
  - ID: ...
  - Número: 20250129-M1-001
  - Mesa: 1
  - Estado: pendiente
  - Total: S/. 0.00

... (más ejemplos)

✅ Ejemplos completados
```

## 📚 Documentación Disponible

- **`README.md`** - Documentación completa de los scripts
- **`ESTRUCTURA_DATOS.md`** - Descripción detallada de tablas y relaciones
- **`GUIA_RAPIDA.md`** - Este archivo

## 🔍 Qué Hace Cada Script

### test_pedidos_flow.py

Simula un flujo realista completo:

```
1. Selecciona una mesa
2. Crea un nuevo pedido
3. Obtiene productos disponibles
4. Obtiene opciones disponibles
5. Agrega 2 productos al pedido
6. Selecciona opciones para cada producto
7. Calcula totales (subtotal, impuestos, total)
8. Confirma el pedido
9. Muestra resumen final
```

**Duración:** ~2-5 segundos

**Ideal para:** Validar que el flujo completo funciona correctamente

### ejemplos_operaciones.py

Muestra 10 ejemplos de operaciones individuales:

```
1. Crear un pedido
2. Agregar un producto a un pedido
3. Agregar opciones a un producto
4. Obtener un pedido por ID
5. Obtener productos de un pedido
6. Obtener opciones de un producto
7. Listar todos los pedidos
8. Actualizar estado de un pedido
9. Actualizar totales de un pedido
10. Eliminar una opción de un producto
```

**Duración:** ~2-5 segundos

**Ideal para:** Entender cómo usar cada operación individualmente

## 💡 Casos de Uso Comunes

### Crear un Pedido Completo

```python
# 1. Obtener mesa
mesa = await session.execute(select(MesaModel).limit(1))
mesa = mesa.scalars().first()

# 2. Crear pedido
pedido = PedidoModel(
    id_mesa=mesa.id,
    numero_pedido="20250129-M1-001",
    estado=EstadoPedido.PENDIENTE,
    subtotal=Decimal("0.00"),
    impuestos=Decimal("0.00"),
    descuentos=Decimal("0.00"),
    total=Decimal("0.00")
)
session.add(pedido)
await session.commit()

# 3. Agregar producto
pedido_producto = PedidoProductoModel(
    id_pedido=pedido.id,
    id_producto=producto.id,
    cantidad=1,
    precio_unitario=producto.precio,
    precio_opciones=Decimal("0.00"),
    subtotal=producto.precio
)
session.add(pedido_producto)
await session.commit()

# 4. Agregar opción
pedido_opcion = PedidoOpcionModel(
    id_pedido_producto=pedido_producto.id,
    id_producto_opcion=opcion.id,
    precio_adicional=opcion.precio_adicional
)
session.add(pedido_opcion)
await session.commit()

# 5. Actualizar totales
pedido.subtotal = pedido_producto.subtotal
pedido.impuestos = pedido.subtotal * Decimal("0.18")
pedido.total = pedido.subtotal + pedido.impuestos
await session.commit()

# 6. Confirmar
pedido.estado = EstadoPedido.CONFIRMADO
pedido.fecha_confirmado = datetime.now()
await session.commit()
```

### Consultar un Pedido Completo

```python
# Obtener pedido
result = await session.execute(
    select(PedidoModel).where(PedidoModel.id == pedido_id)
)
pedido = result.scalars().first()

# Obtener productos
result = await session.execute(
    select(PedidoProductoModel).where(
        PedidoProductoModel.id_pedido == pedido.id
    )
)
productos = result.scalars().all()

# Para cada producto, obtener opciones
for pp in productos:
    result = await session.execute(
        select(PedidoOpcionModel).where(
            PedidoOpcionModel.id_pedido_producto == pp.id
        )
    )
    opciones = result.scalars().all()
```

### Actualizar Estado de Pedido

```python
# Obtener pedido
result = await session.execute(
    select(PedidoModel).where(PedidoModel.id == pedido_id)
)
pedido = result.scalars().first()

# Cambiar estado
pedido.estado = EstadoPedido.EN_PREPARACION
pedido.fecha_en_preparacion = datetime.now()
await session.commit()
```

### Eliminar una Opción

```python
# Obtener opción
result = await session.execute(
    select(PedidoOpcionModel).where(PedidoOpcionModel.id == opcion_id)
)
opcion = result.scalars().first()

# Obtener el producto para actualizar precios
result = await session.execute(
    select(PedidoProductoModel).where(
        PedidoProductoModel.id == opcion.id_pedido_producto
    )
)
pp = result.scalars().first()

# Eliminar opción
await session.delete(opcion)

# Actualizar precios del producto
pp.precio_opciones -= opcion.precio_adicional
pp.subtotal = Decimal(str(pp.cantidad)) * (
    pp.precio_unitario + pp.precio_opciones
)
await session.commit()
```

## 🐛 Troubleshooting

### Error: "No hay productos disponibles"

**Causa:** La base de datos no tiene datos de prueba

**Solución:**
```bash
python -m scripts.seed_cevicheria_data
```

### Error: "No se puede conectar a la base de datos"

**Causa:** `DATABASE_URL` no está configurada o la BD no está disponible

**Solución:**
1. Verifica que `.env` existe en la raíz del proyecto
2. Verifica que `DATABASE_URL` está configurada correctamente
3. Para SQLite: asegúrate de que la carpeta `instance/` existe

### Error: "Foreign key constraint failed"

**Causa:** Intentas crear un pedido sin una mesa válida

**Solución:** Asegúrate de que la mesa existe:
```bash
python -m scripts.seed_cevicheria_data
```

### Error: "Opción no encontrada"

**Causa:** El ID de la opción no existe

**Solución:** Verifica que el ID sea correcto y que la opción exista en la BD

## 📊 Estructura de Carpetas

```
scripts/
├── borradores/
│   ├── __init__.py                    # Inicialización del paquete
│   ├── test_pedidos_flow.py           # Flujo completo
│   ├── ejemplos_operaciones.py        # Ejemplos CRUD
│   ├── README.md                      # Documentación completa
│   ├── ESTRUCTURA_DATOS.md            # Descripción de tablas
│   └── GUIA_RAPIDA.md                 # Este archivo
├── seed_cevicheria_data.py            # Cargar datos de prueba
├── clear_database.py                  # Limpiar BD
└── ...
```

## 🎯 Próximos Pasos

1. **Ejecuta el flujo completo:**
   ```bash
   python -m scripts.borradores.test_pedidos_flow
   ```

2. **Revisa los ejemplos individuales:**
   ```bash
   python -m scripts.borradores.ejemplos_operaciones
   ```

3. **Modifica los scripts según tus necesidades:**
   - Cambia cantidades de productos
   - Prueba diferentes combinaciones de opciones
   - Agrega validaciones adicionales

4. **Integra en tu aplicación:**
   - Usa los modelos en tus controladores
   - Adapta la lógica a tus endpoints API
   - Añade validaciones de negocio

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs de la aplicación
2. Verifica que la base de datos está disponible
3. Asegúrate de que los datos de prueba están cargados
4. Revisa la estructura de datos en `ESTRUCTURA_DATOS.md`

## 📝 Notas

- Los IDs se generan automáticamente usando ULID
- Los precios se almacenan como Decimal para precisión
- Los estados de pedido siguen un flujo específico
- Las opciones son independientes por item de pedido
- Los totales se calculan automáticamente
