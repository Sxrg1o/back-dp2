# Especificación (breve) — POST Productos

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/productos`
- **HTTP Method:** `POST`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}/api/v1/productos`

## ENTRADA

### BODY

```json
{
  "nombre": "Ceviche Clásico",
  "descripcion": "Pescado fresco del día marinado en limón",
  "precio_base": "25.00",
  "imagen_path": "/static/productos/ceviche-clasico.jpg",
  "disponible": true,
  "id_categoria": "01K7ZCT9QRST3K9FC94OIB2NL5"
}
```

**DICTIONARY (BODY)**

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `nombre` | string | YES | 3-200 caracteres | Nombre del producto. Debe ser único. |
| `descripcion` | string | NO | 0-1000 caracteres | Descripción del producto. |
| `precio_base` | string | YES | decimal >= 0 | Precio base del producto. |
| `imagen_path` | string | NO | | Ruta de la imagen. |
| `disponible` | boolean | NO | | Si está disponible (default: true). |
| `id_categoria` | string | YES | ULID | ID de la categoría a la que pertenece. |

## SALIDA (201 Created)

```json
{
  "id": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "nombre": "Ceviche Clásico",
  "descripcion": "Pescado fresco del día marinado en limón",
  "precio_base": "25.00",
  "imagen_path": "/static/productos/ceviche-clasico.jpg",
  "disponible": true,
  "id_categoria": "01K7ZCT9QRST3K9FC94OIB2NL5",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## ERRORES

| HTTP | Code | Comment |
|------|------|---------|
| 400 | `VALIDATION_ERROR` | Datos inválidos. |
| 409 | `CONFLICT` | Producto con nombre duplicado. |
| 500 | `INTERNAL_ERROR` | Error interno. |

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/productos`

**cURL:**
```bash
curl -X POST "https://back-dp2.onrender.com/api/v1/productos" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Ceviche Clásico", "precio_base": "25.00", "id_categoria": "01K7ZCT9QRST3K9FC94OIB2NL5"}'
```
