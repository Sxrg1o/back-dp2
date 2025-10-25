# Especificación (breve) — GET Productos

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/productos`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

**URL patrón:** `{HOST}/api/v1/productos?skip={skip}&limit={limit}&id_categoria={id_categoria}`

## ENTRADA

### Query Params

| Field | Data Type | Required | Format | Comment |
|-------|-----------|----------|--------|---------|
| `skip` | integer | NO | >=0 | Offset (default `0`). |
| `limit` | integer | NO | 1..500 | Tamaño de página (default `100`). |
| `id_categoria` | string | NO | ULID | Filtrar por categoría (opcional). |

## SALIDA (200 OK)

```json
{
  "items": [
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
  ],
  "skip": 0,
  "limit": 100,
  "total": 274
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/productos?skip=0&limit=100`  
**Local:** `http://127.0.0.1:8000/api/v1/productos?skip=0&limit=100`

**Con filtro por categoría:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/productos?id_categoria=01K7ZCT9QRST3K9FC94OIB2NL5" \
  -H "accept: application/json"
```
