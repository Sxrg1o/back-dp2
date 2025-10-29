# Especificación (breve) — <METHOD> <RECURSO>

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `<recurso>`
- **HTTP Method:** `<GET|POST|PUT|PATCH|DELETE>`
- **Autenticación:** (Ninguna | Bearer JWT)
- **Notas:** En **GET** no enviar body. Usar **path/query params**.

**URL patrón (componentes separadas):**

```
{HOST}{BASE_PATH}{RECURSO}[?query]
```

## ENTRADA

> **Body:** *(NO aplica en GET/DELETE)*

### Path Params (si aplica)

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `<id_name>` | string | YES | uuid | Identificador del recurso. |

### Query Params (si aplica)

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

### BODY (solo POST/PUT/PATCH)

```json
{
  "<field1>": "<string>",
  "<field2>": 0
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `field1` | string | YES/NO | | Significado y validaciones. |
| `field2` | number | YES/NO | | Rangos / valores por defecto. |

## SALIDA (200/201 OK — ejemplo)

```json
{
  "id": "uuid",
  "status": "ACTIVE"
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `id` | string | uuid | Identificador creado. |
| `status` | string | enum | Estado del recurso. |

## ERRORES (4xx/5xx)

**Problem+JSON**

```json
{
  "type": "https://back-dp2.onrender.com/errors/<code>",
  "title": "...",
  "status": 400,
  "detail": "...",
  "instance": "<path>"
}
```

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Formato/rango inválido. |
| 401 | `UNAUTHORIZED` | Token inválido/ausente | Si requiere auth. |
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente. |
| 409 | `CONFLICT` | Conflicto de negocio | Duplicado/estado. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs. |

## URLs completas (listas para usar)

### **Producción**

**URL completa:** `https://back-dp2.onrender.com/api/v1/<recurso>`

**cURL:**

```bash
curl -X <METHOD> \
  "https://back-dp2.onrender.com/api/v1/<recurso>" \
  -H "accept: application/json"
```

### **Local**

**URL completa:** `http://127.0.0.1:8000/api/v1/<recurso>`

**cURL:**

```bash
curl -X <METHOD> \
  "http://127.0.0.1:8000/api/v1/<recurso>" \
  -H "accept: application/json"
```

## Variables y constantes (resumen)

**Constantes:**
- `BASE_PATH = /api/v1`
- `RECURSO = <recurso>`

**Variables:**
- `HOST` = `https://back-dp2.onrender.com` (prod) | `http://127.0.0.1:8000` (local)
- Query/path params según el endpoint

> **Tip:** Define `HOST` por ambiente (env var) y construye la URL como: `"$HOST/api/v1/<recurso>"`.
