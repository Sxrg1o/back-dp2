# Especificación (breve) — PUT Categoría por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/categorias/{categoria_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}{BASE_PATH}/categorias/{categoria_id}`

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `categoria_id` | string | YES | ULID | Identificador único de la categoría. |

### BODY

```json
{
  "nombre": "Entradas Gourmet",
  "descripcion": "Aperitivos especiales",
  "orden": 2,
  "activo": false
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `nombre` | string | NO | 3-100 caracteres | Nuevo nombre (debe ser único). |
| `descripcion` | string | NO | 0-500 caracteres | Nueva descripción. |
| `imagen_path` | string | NO | | Nueva ruta de imagen. |
| `orden` | integer | NO | >= 0 | Nuevo orden. |
| `activo` | boolean | NO | | Nuevo estado. |

## SALIDA (200 OK)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Entradas Gourmet",
  "descripcion": "Aperitivos especiales",
  "imagen_path": "/static/categorias/entradas.jpg",
  "orden": 2,
  "activo": false,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

## ERRORES

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Datos inválidos. |
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 409 | `CONFLICT` | Conflicto | Nombre duplicado. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X PUT "https://back-dp2.onrender.com/api/v1/categorias/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Entradas Gourmet", "orden": 2}'
```
