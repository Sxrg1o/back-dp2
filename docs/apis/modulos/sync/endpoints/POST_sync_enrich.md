# Especificación (breve) — POST Sync Enrich

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/sync/enrich`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)
- **Notas:** Debe ejecutarse **DESPUÉS** de `/sync/platos`

**URL patrón:** `{HOST}{BASE_PATH}/sync/enrich`

## DESCRIPCIÓN

Ejecuta el script de **enriquecimiento** para agregar alérgenos, tipos de opciones y relaciones a los productos existentes.

**Operaciones:**
1. Crea **8 alérgenos comunes** (si no existen): Mariscos, Gluten, Lácteos, Frutos secos, Huevo, Soja, Pescado, Crustáceos
2. Crea **4 tipos de opciones** (si no existen): Nivel de ají, Acompañamientos, Bebidas, Extras
3. Asocia **alérgenos a productos** usando reglas inteligentes basadas en nombres
4. Crea **opciones de productos** (nivel de ají, acompañamientos, bebidas, extras)
5. Crea **roles de usuario** (si no existen): Admin, Mesero, Cliente, Cocina
6. Actualiza **imágenes** de productos y categorías desde seed data

## ENTRADA

**Body:** *(no se requiere body)*

## SALIDA (200 OK)

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

**DICTIONARY (OUTPUT)**

| Field | Data Type | Comment |
|-------|-----------|---------|
| `status` | string | Estado de la operación ("success"). |
| `message` | string | Mensaje descriptivo. |
| `data.productos_procesados` | integer | Cantidad de productos en BD al inicio. |
| `data.alergenos_creados` | integer | Cantidad de alérgenos nuevos creados. |
| `data.alergenos_totales` | integer | Total de alérgenos después del enriquecimiento. |
| `data.tipos_opciones_creados` | integer | Cantidad de tipos de opciones nuevos creados. |
| `data.tipos_opciones_totales` | integer | Total de tipos de opciones después. |

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 500 | `INTERNAL_ERROR` | Error interno | Error durante enriquecimiento. Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/sync/enrich`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/sync/enrich" \
  -H "accept: application/json"
```

## Flujo Recomendado

```mermaid
graph LR
    A[1. POST /sync/platos] --> B[2. POST /sync/enrich]
    B --> C[3. Productos enriquecidos]
```

1. **Primero:** Ejecutar `POST /sync/platos` para sincronizar productos desde Domótica
2. **Segundo:** Ejecutar `POST /sync/enrich` para agregar alérgenos y opciones
3. **Resultado:** Productos completos con toda la información necesaria

## Notas Técnicas

- ✅ La operación es **idempotente** (puede ejecutarse múltiples veces sin problemas)
- ✅ Solo crea elementos si no existen (evita duplicados)
- ⚠️ Requiere que existan productos en la BD (ejecutar `/sync/platos` primero)
- ✅ Las reglas de asociación de alérgenos son inteligentes (busca palabras clave en nombres)

## Casos de Uso

**HU-C10:** Cliente con restricciones — Ver alérgenos del producto elegido  
**HU-C07:** Cliente que personaliza — Añadir extras disponibles a mi selección  
**HU-A04:** Admin — Gestionar alérgenos por producto
