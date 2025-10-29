# Especificación (breve) — GET Producto por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/productos/{producto_id}`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}/api/v1/productos/{producto_id}`

## ENTRADA

### Path Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `producto_id` | string | YES | ULID | ID del producto. |

## SALIDA (200 OK)

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
| 404 | `NOT_FOUND` | Producto no encontrado. |
| 500 | `INTERNAL_ERROR` | Error interno. |

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/productos/01K7ZD12XYZW4M5NG95PJC3NO6" \
  -H "accept: application/json"
```
