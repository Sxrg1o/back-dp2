# Especificación (breve) — POST Roles

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path (constante):** `/api/v1`
- **Recurso (constante):** `/roles`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)
- **Notas:** Crea un nuevo rol en el sistema.

**URL patrón (componentes separadas):**

```
{HOST}{BASE_PATH}{RECURSO}
```

## ENTRADA

### Headers

**DICTIONARY**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `accept` | string | YES | `application/json` | Tipo de respuesta. |
| `Content-Type` | string | YES | `application/json` | Tipo de contenido del body. |

### BODY

```json
{
  "nombre": "Administrador"
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `nombre` | string | YES | 3-50 caracteres | Nombre del rol. Debe ser único. |

## SALIDA (201 Created — ejemplo)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Administrador",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Format | Comment |
|-------|-----------|--------|---------|
| `id` | string | ULID | Identificador único del rol creado. |
| `nombre` | string | | Nombre del rol. |
| `created_at` | string | ISO 8601 | Fecha de creación. |
| `updated_at` | string | ISO 8601 | Fecha de última actualización. |

## ERRORES (4xx/5xx)

**Problem+JSON**

```json
{
  "type": "https://back-dp2.onrender.com/errors/CONFLICT",
  "title": "Conflicto de datos",
  "status": 409,
  "detail": "Ya existe un rol con el nombre 'Administrador'",
  "instance": "/api/v1/roles"
}
```

| HTTP | Code | Title / Message | Comment |
|------|------|-----------------|---------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | El nombre es demasiado corto o largo. |
| 409 | `CONFLICT` | Conflicto de negocio | Ya existe un rol con ese nombre. |
| 500 | `INTERNAL_ERROR` | Error interno | Revisar logs del servidor. |

## URLs completas (listas para usar)

### **Producción**

**URL completa:** `https://back-dp2.onrender.com/api/v1/roles`

**cURL:**

```bash
curl -X POST \
  "https://back-dp2.onrender.com/api/v1/roles" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Administrador"}'
```

### **Local**

**URL completa:** `http://127.0.0.1:8000/api/v1/roles`

**cURL:**

```bash
curl -X POST \
  "http://127.0.0.1:8000/api/v1/roles" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Administrador"}'
```

## Variables y constantes (resumen)

**Constantes:**
- `BASE_PATH = /api/v1`
- `RECURSO = /roles`

**Variables:**
- `HOST` = `https://back-dp2.onrender.com` (prod) | `http://127.0.0.1:8000` (local)
- `nombre` — Nombre del rol a crear
