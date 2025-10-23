# Especificación (breve) — GET Roles

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/roles`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)
- **Notas:** En **GET** no enviar body. Usar **path/query params**.

**URL patrón (componentes separadas):**

```
{HOST}{BASE_PATH}{RECURSO}?skip={skip}&limit={limit}
```

## ENTRADA

> **Body:** *(no aplica en GET).*

### Query Params

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `skip` | integer | NO | >=0 | Offset (default `0`). |
| `limit` | integer | NO | 1..500 | Tamaño de página (default `100`). |

### Headers

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `accept` | string | YES | `application/json` | Tipo de respuesta. |

## SALIDA (200 OK — ejemplo)

```json
{
  "items": [
    {
      "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
      "nombre": "Administrador",
      "created_at": "2024-10-23T05:16:30.123456Z",
      "updated_at": "2024-10-23T05:16:30.123456Z"
    },
    {
      "id": "01K7ZCT9QRST3K9FC94OIB2NL5",
      "nombre": "Mesero",
      "created_at": "2024-10-23T05:17:45.654321Z",
      "updated_at": "2024-10-23T05:17:45.654321Z"
    }
  ],
  "skip": 0,
  "limit": 100,
  "total": 5
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `items` | array | | Lista de roles. |
| `items[].id` | string | ULID | ID del rol. |
| `items[].nombre` | string | | Nombre del rol. |
| `items[].created_at` | string | ISO 8601 | Fecha de creación. |
| `items[].updated_at` | string | ISO 8601 | Fecha de última actualización. |
| `skip` | integer | | Offset aplicado. |
| `limit` | integer | | Tamaño de página. |
| `total` | integer | | Total de registros disponibles. |

## ERRORES (4xx/5xx)

**Problem+JSON**

```json
{
  "type": "https://back-dp2.onrender.com/errors/VALIDATION_ERROR",
  "title": "Parámetros inválidos",
  "status": 400,
  "detail": "El parámetro 'limit' debe estar entre 1 y 500",
  "instance": "/api/v1/roles"
}
```

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | `skip`/`limit` fuera de rango. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas (listas para usar)

### **Producción**

**URL completa:** `https://back-dp2.onrender.com/api/v1/roles?skip=0&limit=100`

**cURL:**

```bash
curl -X GET \
  "https://back-dp2.onrender.com/api/v1/roles?skip=0&limit=100" \
  -H "accept: application/json"
```

### **Local**

**URL completa:** `http://127.0.0.1:8000/api/v1/roles?skip=0&limit=100`

**cURL:**

```bash
curl -X GET \
  "http://127.0.0.1:8000/api/v1/roles?skip=0&limit=100" \
  -H "accept: application/json"
```

## Variables y constantes (resumen)

**Constantes:**
- `BASE_PATH = /api/v1`
- `RECURSO = /roles`

**Variables:**
- `HOST` = `https://back-dp2.onrender.com` (prod) | `http://127.0.0.1:8000` (local)
- `skip`, `limit` — Parámetros de paginación

> **Tip:** Usa `API_HOST` como env var y construye: `"$API_HOST/api/v1/roles?skip=$SKIP&limit=$LIMIT"`.
