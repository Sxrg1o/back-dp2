# Módulo: Sincronización

[⬅ Volver al Índice](../../README.md)

## Descripción

Endpoints de sincronización con el sistema externo **Domótica INC**. Permite recibir datos de platos y mesas mediante scraping, y ejecutar operaciones de enriquecimiento de datos.

## Recurso Base

```
/api/v1/sync
```

## Endpoints Disponibles

- **[POST /sync/platos](endpoints/POST_sync_platos.md)** — Sincroniza platos desde Domótica
- **[POST /sync/mesas](endpoints/POST_sync_mesas.md)** — Sincroniza mesas desde Domótica
- **[POST /sync/enrich](endpoints/POST_sync_enrich.md)** — Enriquece datos existentes (alérgenos, opciones, roles, imágenes)

## Características

### POST /sync/platos
- Crea o actualiza **categorías** y **productos** en lote
- Mapea productos del sistema externo a la base de datos local
- Marca como inactivos los productos que ya no existen en Domótica
- Operaciones optimizadas por **batch processing**

### POST /sync/mesas
- Recibe datos de mesas del sistema externo
- Actualmente solo registra la recepción (funcionalidad futura)

### POST /sync/enrich
- Ejecuta el script de **enriquecimiento** de datos
- Debe ejecutarse **DESPUÉS** de sincronizar productos
- Operaciones:
  1. Crea **alérgenos comunes** (8 tipos: mariscos, gluten, lácteos, etc.)
  2. Crea **tipos de opciones** (nivel de ají, acompañamientos, bebidas, extras)
  3. Asocia **alérgenos a productos** usando reglas inteligentes
  4. Crea **opciones de productos**
  5. Crea **roles de usuario** (Admin, Mesero, Cliente, Cocina)
  6. Actualiza **imágenes** de productos y categorías desde seed data

## Esquemas de Entrada

### ProductoDomotica (para `/sync/platos`)
```json
{
  "nombre": "Ceviche Clásico",
  "precio": "25.00",
  "categoria": "Ceviches"
}
```

### MesaDomotica (para `/sync/mesas`)
```json
{
  "numero": "M01",
  "capacidad": 4,
  "estado": "disponible"
}
```

## Respuestas de Éxito

### POST /sync/platos (200 OK)
```json
{
  "status": "success",
  "message": "Sincronización completada correctamente con operaciones por lotes",
  "resultados": {
    "categorias_creadas": 3,
    "categorias_actualizadas": 5,
    "productos_creados": 45,
    "productos_actualizados": 120,
    "productos_desactivados": 8
  }
}
```

### POST /sync/enrich (200 OK)
```json
{
  "status": "success",
  "message": "Enriquecimiento completado exitosamente",
  "data": {
    "productos_procesados": 274,
    "alergenos_creados": 8,
    "alergenos_totales": 8,
    "tipos_opciones_creados": 4,
    "tipos_opciones_totales": 4
  }
}
```

## Casos de Uso

**HU-A02:** Admin — Mapear un producto con un ID externo 1:1

## Errores Comunes

| HTTP | Code | Descripción |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Payload inválido o incompleto |
| 409 | `CONFLICT` | Conflicto de datos (nombres duplicados) |
| 500 | `INTERNAL_ERROR` | Error durante sincronización/enriquecimiento |

## Notas Técnicas

- ⚠️ Estos endpoints son **internos** y normalmente son llamados por el scraper
- ✅ Las operaciones de **sincronización** usan **batch processing** para mejor rendimiento
- ✅ El **enriquecimiento** es **idempotente** (puede ejecutarse múltiples veces)
- ⚠️ El enriquecimiento requiere que existan productos en la BD
