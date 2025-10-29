# Índice - Scripts de Prueba de Pedidos

## 📁 Archivos Creados

```
scripts/borradores/
├── __init__.py                    (78 bytes)
├── test_pedidos_flow.py           (14.5 KB)
├── ejemplos_operaciones.py        (17.1 KB)
├── README.md                      (4.8 KB)
├── ESTRUCTURA_DATOS.md            (14.3 KB)
├── GUIA_RAPIDA.md                 (8.2 KB)
└── INDICE.md                      (este archivo)
```

## 🎯 Descripción de Archivos

### 1. `test_pedidos_flow.py` (14.5 KB)

**Propósito:** Ejecutar un flujo completo y realista de pedidos

**Contenido:**
- Clase `PedidosFlowTester` con 8 pasos
- Selecciona mesa → Crea pedido → Agrega productos → Agrega opciones → Calcula totales → Confirma
- Muestra resumen final con todos los detalles

**Cómo ejecutar:**
```bash
python -m scripts.borradores.test_pedidos_flow
```

**Tiempo de ejecución:** 2-5 segundos

**Ideal para:** Validar que el flujo completo funciona correctamente

---

### 2. `ejemplos_operaciones.py` (17.1 KB)

**Propósito:** Mostrar ejemplos de operaciones CRUD individuales

**Contenido:**
- Clase `EjemplosOperaciones` con 10 métodos de ejemplo
- Crear pedido, agregar producto, agregar opciones
- Obtener pedidos, productos, opciones
- Actualizar estado, actualizar totales
- Eliminar opciones

**Cómo ejecutar:**
```bash
python -m scripts.borradores.ejemplos_operaciones
```

**Tiempo de ejecución:** 2-5 segundos

**Ideal para:** Entender cómo usar cada operación individualmente

---

### 3. `README.md` (4.8 KB)

**Propósito:** Documentación completa de los scripts

**Contenido:**
- ¿Qué hace cada script?
- Estructura del flujo
- Cómo ejecutar
- Requisitos
- Salida esperada
- Modelos utilizados
- Tablas de base de datos
- Notas importantes
- Troubleshooting
- Extensiones futuras

**Ideal para:** Entender el propósito y funcionamiento de los scripts

---

### 4. `ESTRUCTURA_DATOS.md` (14.3 KB)

**Propósito:** Documentación técnica de la estructura de datos

**Contenido:**
- Diagrama de relaciones entre tablas
- Descripción detallada de cada tabla
- Campos, tipos y descripciones
- Flujo de datos con ejemplo completo
- Cálculos importantes
- Estados del pedido
- Restricciones y validaciones
- Índices principales
- Cascadas de eliminación
- Consideraciones de diseño

**Ideal para:** Entender la arquitectura de datos del sistema

---

### 5. `GUIA_RAPIDA.md` (8.2 KB)

**Propósito:** Guía rápida para empezar

**Contenido:**
- Resumen de scripts disponibles
- Inicio rápido (prerequisitos, cómo ejecutar)
- Documentación disponible
- Qué hace cada script
- Casos de uso comunes con código
- Troubleshooting
- Estructura de carpetas
- Próximos pasos
- Notas importantes

**Ideal para:** Empezar rápidamente sin leer toda la documentación

---

### 6. `__init__.py` (78 bytes)

**Propósito:** Marcar la carpeta como paquete Python

**Contenido:**
- Docstring del paquete

---

## 🚀 Cómo Empezar

### Opción 1: Flujo Completo (Recomendado)

```bash
# 1. Cargar datos de prueba
python -m scripts.seed_cevicheria_data

# 2. Ejecutar flujo completo
python -m scripts.borradores.test_pedidos_flow

# 3. Ver ejemplos individuales
python -m scripts.borradores.ejemplos_operaciones
```

### Opción 2: Solo Leer Documentación

1. Comienza con `GUIA_RAPIDA.md`
2. Luego lee `ESTRUCTURA_DATOS.md`
3. Finalmente revisa `README.md`

### Opción 3: Estudiar el Código

1. Abre `test_pedidos_flow.py`
2. Abre `ejemplos_operaciones.py`
3. Revisa los comentarios y docstrings

## 📊 Resumen de Funcionalidades

### test_pedidos_flow.py

| Funcionalidad | Método | Descripción |
|---------------|--------|-------------|
| Obtener mesa | `get_or_create_mesa()` | Obtiene o crea una mesa |
| Crear pedido | `create_pedido()` | Crea un nuevo pedido |
| Obtener productos | `get_productos()` | Obtiene productos disponibles |
| Obtener opciones | `get_opciones_disponibles()` | Obtiene opciones disponibles |
| Agregar producto | `create_pedido_producto()` | Agrega un producto al pedido |
| Agregar opción | `create_pedido_opcion()` | Agrega una opción a un producto |
| Actualizar opciones | `update_pedido_producto_opciones()` | Actualiza precio de opciones |
| Actualizar totales | `update_pedido_totales()` | Calcula y actualiza totales |
| Confirmar pedido | `confirm_pedido()` | Confirma el pedido |
| Obtener pedido | `get_pedido_by_id()` | Obtiene un pedido por ID |

### ejemplos_operaciones.py

| Ejemplo | Método | Descripción |
|---------|--------|-------------|
| 1 | `ejemplo_crear_pedido()` | Crear un nuevo pedido |
| 2 | `ejemplo_agregar_producto_a_pedido()` | Agregar producto |
| 3 | `ejemplo_agregar_opcion_a_producto()` | Agregar opciones |
| 4 | `ejemplo_obtener_pedido_por_id()` | Obtener pedido por ID |
| 5 | `ejemplo_obtener_productos_de_pedido()` | Obtener productos |
| 6 | `ejemplo_obtener_opciones_de_producto()` | Obtener opciones |
| 7 | `ejemplo_listar_todos_los_pedidos()` | Listar todos los pedidos |
| 8 | `ejemplo_actualizar_estado_pedido()` | Cambiar estado |
| 9 | `ejemplo_actualizar_totales_pedido()` | Actualizar totales |
| 10 | `ejemplo_eliminar_opcion_de_producto()` | Eliminar opción |

## 🔗 Relaciones Entre Documentos

```
INDICE.md (estás aquí)
├── GUIA_RAPIDA.md (empieza aquí si es tu primera vez)
├── README.md (documentación completa)
├── ESTRUCTURA_DATOS.md (referencia técnica)
├── test_pedidos_flow.py (código del flujo completo)
└── ejemplos_operaciones.py (código de ejemplos)
```

## 💡 Casos de Uso

### Validar que el Sistema Funciona
```bash
python -m scripts.borradores.test_pedidos_flow
```

### Entender Cómo Usar la API
```bash
python -m scripts.borradores.ejemplos_operaciones
```

### Aprender la Estructura de Datos
Leer `ESTRUCTURA_DATOS.md`

### Integrar en tu Aplicación
Copiar código de `ejemplos_operaciones.py`

### Depurar Problemas
Leer `README.md` sección "Troubleshooting"

## 📈 Estadísticas

| Métrica | Valor |
|---------|-------|
| Archivos Python | 2 |
| Archivos Markdown | 4 |
| Líneas de código Python | ~800 |
| Líneas de documentación | ~1000 |
| Métodos en test_pedidos_flow.py | 10 |
| Métodos en ejemplos_operaciones.py | 10 |
| Ejemplos de operaciones CRUD | 10 |
| Tablas de base de datos documentadas | 7 |

## 🎓 Aprendizaje Progresivo

### Nivel 1: Principiante
1. Lee `GUIA_RAPIDA.md`
2. Ejecuta `python -m scripts.borradores.test_pedidos_flow`
3. Revisa la salida

### Nivel 2: Intermedio
1. Lee `ESTRUCTURA_DATOS.md`
2. Ejecuta `python -m scripts.borradores.ejemplos_operaciones`
3. Estudia el código de `ejemplos_operaciones.py`

### Nivel 3: Avanzado
1. Lee `README.md` completamente
2. Estudia `test_pedidos_flow.py` línea por línea
3. Modifica los scripts para tus necesidades
4. Integra en tu aplicación

## ✅ Checklist de Uso

- [ ] He leído `GUIA_RAPIDA.md`
- [ ] He ejecutado `test_pedidos_flow.py`
- [ ] He ejecutado `ejemplos_operaciones.py`
- [ ] He leído `ESTRUCTURA_DATOS.md`
- [ ] He leído `README.md`
- [ ] Entiendo el flujo de pedidos
- [ ] Entiendo la estructura de datos
- [ ] Puedo crear un pedido manualmente
- [ ] Puedo agregar productos a un pedido
- [ ] Puedo agregar opciones a un producto
- [ ] Estoy listo para integrar en mi aplicación

## 🔧 Modificaciones Comunes

### Cambiar cantidad de productos
En `test_pedidos_flow.py`, línea ~180:
```python
productos_a_agregar = productos[:2]  # Cambiar 2 por el número deseado
```

### Cambiar porcentaje de impuestos
En `test_pedidos_flow.py`, línea ~230:
```python
pedido.impuestos = subtotal * Decimal("0.18")  # Cambiar 0.18 por el porcentaje
```

### Agregar más ejemplos
En `ejemplos_operaciones.py`, agregar más métodos `ejemplo_*()` y llamarlos en `main()`

## 📞 Soporte

Si tienes problemas:

1. Revisa `README.md` sección "Troubleshooting"
2. Verifica que la base de datos está disponible
3. Asegúrate de que los datos de prueba están cargados
4. Revisa los logs de la aplicación

## 📝 Notas Finales

- Estos scripts son para **prueba y desarrollo**
- No están optimizados para producción
- Puedes usarlos como base para tus propios scripts
- Adapta el código según tus necesidades
- Mantén la documentación actualizada

---

**Última actualización:** 2025-01-29
**Versión:** 1.0
**Estado:** ✅ Completo y funcional
