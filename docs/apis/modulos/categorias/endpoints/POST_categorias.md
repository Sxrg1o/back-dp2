# Especificación (breve) — POST Categorías

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}{RECURSO}`

## ENTRADA

### BODY

```json
{
  "nombre": "Entradas",
  "descripcion": "Aperitivos y platos de entrada",
  "imagen_path": "/static/categorias/entradas.jpg",
  "orden": 1,
  "activo": true
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `nombre` | string | YES | 3-100 caracteres | Nombre de la categoría. Debe ser único. |
| `descripcion` | string | NO | 0-500 caracteres | Descripción de la categoría. |
| `imagen_path` | string | NO | | Ruta de la imagen de la categoría. |
| `orden` | integer | NO | >= 0 | Orden de visualización (default: 0). |
| `activo` | boolean | NO | | Si está activa o no (default: true). |

## SALIDA (201 Created)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Entradas",
  "descripcion": "Aperitivos y platos de entrada",
  "imagen_path": "/static/categorias/entradas.jpg",
  "orden": 1,
  "activo": true,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## ERRORES (4xx/5xx)

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Nombre demasiado corto/largo. |
| 409 | `CONFLICT` | Conflicto de negocio | Ya existe una categoría con ese nombre. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/categorias" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Entradas", "descripcion": "Aperitivos y platos de entrada", "orden": 1}'
```
