# Especificación (breve) — POST Sync Platos

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/sync/platos`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)
- **Notas:** Endpoint **interno** para sincronización con Domótica

**URL patrón:** `{HOST}{BASE_PATH}/sync/platos`

## DESCRIPCIÓN

Recibe datos de platos extraídos mediante scraping del sistema **Domótica** y los sincroniza con la base de datos local.

**Operaciones:**
1. Obtiene todas las categorías y productos existentes
2. Crea las categorías nuevas en lote
3. Actualiza las categorías existentes en lote
4. Crea los productos nuevos en lote
5. Actualiza los productos existentes en lote
6. Marca como inactivos los productos que ya no existen en Domótica

## ENTRADA

### BODY

```json
[
  {
    "nombre": "Ceviche Clásico",
    "precio": "25.00",
    "categoria": "Ceviches"
  },
  {
    "nombre": "Tiradito de Pescado",
    "precio": "28.00",
    "categoria": "Tiraditos"
  }
]
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `[].nombre` | string | YES | | Nombre del producto en Domótica. |
| `[].precio` | string/number | YES | decimal | Precio del producto. Acepta "S/. 25.00" o 25.00. |
| `[].categoria` | string | YES | | Nombre de la categoría en Domótica. |

## SALIDA (200 OK)

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

**DICTIONARY (OUTPUT)**

| Field | Data Type | Comment |
|-------|-----------|---------|
| `status` | string | Estado de la operación ("success"). |
| `message` | string | Mensaje descriptivo. |
| `resultados.categorias_creadas` | integer | Cantidad de categorías nuevas creadas. |
| `resultados.categorias_actualizadas` | integer | Cantidad de categorías actualizadas. |
| `resultados.productos_creados` | integer | Cantidad de productos nuevos creados. |
| `resultados.productos_actualizados` | integer | Cantidad de productos actualizados. |
| `resultados.productos_desactivados` | integer | Cantidad de productos marcados como inactivos. |

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Payload malformado. |
| 409 | `CONFLICT` | Conflicto | Nombres duplicados. |
| 500 | `INTERNAL_ERROR` | Error interno | Error durante sincronización. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/sync/platos`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/sync/platos" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '[{"nombre": "Ceviche Clásico", "precio": "25.00", "categoria": "Ceviches"}]'
```

## Notas Técnicas

- ✅ Usa **batch processing** para mejor rendimiento
- ✅ Operación **parcialmente transaccional** (por lotes)
- ⚠️ No sincroniza ni altera precios/impuestos en el POS externo
- ⚠️ Los productos desactivados mantienen su registro en BD
