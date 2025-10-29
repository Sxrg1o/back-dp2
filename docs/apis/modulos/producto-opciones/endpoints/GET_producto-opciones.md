# Especificación (breve) — GET Producto Opciones

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/producto-opciones`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

## ENTRADA

### Query Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `skip` | integer | NO | Offset (default `0`). |
| `limit` | integer | NO | Tamaño de página (default `100`). |

## SALIDA (200 OK)

```json
{
  "items": [
    {
      "id": "01K7ZF34CDEF7O8PI17RLE5PQ8",
      "nombre": "Ají suave",
      "precio_adicional": "0.00",
      "disponible": true,
      "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6",
      "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
      "orden": 1,
      "created_at": "2024-10-23T05:16:30.123456Z",
      "updated_at": "2024-10-23T05:16:30.123456Z"
    }
  ],
  "skip": 0,
  "limit": 100,
  "total": 50
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/producto-opciones?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/producto-opciones?skip=0&limit=100" \
  -H "accept: application/json"
```
