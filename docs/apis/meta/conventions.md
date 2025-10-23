# Convenciones de API

[⬅ Volver al Índice](../README.md)

## Formato de Fechas y Timestamps

### ISO 8601 con Timezone UTC

Todas las fechas y timestamps se retornan en formato **ISO 8601** con timezone UTC:

```json
{
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

**Formato:** `YYYY-MM-DDTHH:MM:SS.ffffffZ`

## Paginación

### Query Parameters

Los endpoints que retornan listas soportan paginación mediante:

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `skip` | integer | `0` | `>= 0` | Número de registros a omitir (offset) |
| `limit` | integer | `100` | `1..500` | Número máximo de registros a retornar |

### Ejemplo de Request

```bash
GET /api/v1/productos?skip=0&limit=20
```

### Formato de Respuesta Paginada

```json
{
  "items": [
    { "id": "01K7...", "nombre": "Producto 1" },
    { "id": "01K8...", "nombre": "Producto 2" }
  ],
  "skip": 0,
  "limit": 20,
  "total": 157
}
```

| Field | Type | Description |
|-------|------|-------------|
| `items` | array | Lista de elementos en la página actual |
| `skip` | integer | Offset aplicado |
| `limit` | integer | Límite aplicado |
| `total` | integer | Total de registros disponibles |

## Manejo de Errores

### Formato Problem+JSON (RFC 7807)

Todos los errores siguen el estándar **Problem+JSON**:

```json
{
  "type": "https://back-dp2.onrender.com/errors/<ERROR_CODE>",
  "title": "Título legible del error",
  "status": 400,
  "detail": "Descripción detallada del problema",
  "instance": "/api/v1/productos/01K7..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string (URI) | URI que identifica el tipo de error |
| `title` | string | Resumen corto del problema |
| `status` | integer | Código de estado HTTP |
| `detail` | string | Explicación detallada |
| `instance` | string | URI del recurso que causó el error |

### Códigos de Error Comunes

| HTTP | Code | Title | Descripción |
|------|------|-------|-------------|
| 400 | `VALIDATION_ERROR` | Parámetros inválidos | Datos de entrada no válidos |
| 401 | `UNAUTHORIZED` | No autorizado | Token ausente/inválido |
| 403 | `FORBIDDEN` | Acceso denegado | Sin permisos suficientes |
| 404 | `NOT_FOUND` | Recurso no encontrado | ID inexistente |
| 409 | `CONFLICT` | Conflicto | Duplicado o estado inconsistente |
| 422 | `UNPROCESSABLE_ENTITY` | Entidad no procesable | Error de validación de negocio |
| 500 | `INTERNAL_ERROR` | Error interno | Error inesperado del servidor |

### Ejemplos de Errores

#### 400 Bad Request
```json
{
  "type": "https://back-dp2.onrender.com/errors/VALIDATION_ERROR",
  "title": "Parámetros inválidos",
  "status": 400,
  "detail": "El parámetro 'limit' debe estar entre 1 y 500",
  "instance": "/api/v1/productos"
}
```

#### 404 Not Found
```json
{
  "type": "https://back-dp2.onrender.com/errors/NOT_FOUND",
  "title": "Recurso no encontrado",
  "status": 404,
  "detail": "No se encontró el producto con ID '01K7ZCT8PNJA2J8EB83NHA1MK4'",
  "instance": "/api/v1/productos/01K7ZCT8PNJA2J8EB83NHA1MK4"
}
```

#### 409 Conflict
```json
{
  "type": "https://back-dp2.onrender.com/errors/CONFLICT",
  "title": "Conflicto de datos",
  "status": 409,
  "detail": "Ya existe una categoría con el nombre 'Entradas'",
  "instance": "/api/v1/categorias"
}
```

## Identificadores

### Formato ULID

Los IDs de recursos usan el formato **ULID** (Universally Unique Lexicographically Sortable Identifier):

```
01K7ZCT8PNJA2J8EB83NHA1MK4
```

**Características:**
- ✅ 26 caracteres alfanuméricos
- ✅ Ordenables lexicográficamente
- ✅ Compatible con UUID
- ✅ Incluye timestamp

## Content-Type

### Request Headers
```http
Content-Type: application/json
Accept: application/json
```

### Response Headers
```http
Content-Type: application/json; charset=utf-8
```

## Métodos HTTP

| Método | Uso | Idempotente | Body |
|--------|-----|-------------|------|
| `GET` | Obtener recursos | ✅ Sí | ❌ No |
| `POST` | Crear recursos | ❌ No | ✅ Sí |
| `PUT` | Actualizar completo | ✅ Sí | ✅ Sí |
| `PATCH` | Actualizar parcial | ❌ No | ✅ Sí |
| `DELETE` | Eliminar recursos | ✅ Sí | ❌ No |

## Status Codes

| Code | Significado | Uso |
|------|-------------|-----|
| `200` | OK | Operación exitosa (GET, PUT) |
| `201` | Created | Recurso creado exitosamente (POST) |
| `204` | No Content | Operación exitosa sin contenido (DELETE) |
| `400` | Bad Request | Solicitud malformada |
| `401` | Unauthorized | Autenticación requerida |
| `403` | Forbidden | Sin permisos |
| `404` | Not Found | Recurso no encontrado |
| `409` | Conflict | Conflicto de datos |
| `422` | Unprocessable Entity | Error de validación |
| `500` | Internal Server Error | Error del servidor |
