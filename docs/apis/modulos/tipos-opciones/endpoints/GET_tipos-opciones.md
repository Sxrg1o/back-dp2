# Especificación (breve) — GET Tipos de Opciones

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/tipos-opciones`
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
      "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
      "nombre": "Nivel de picante",
      "descripcion": "Selecciona el nivel de ají",
      "obligatorio": true,
      "multiple_seleccion": false,
      "orden": 1,
      "created_at": "2024-10-23T05:16:30.123456Z",
      "updated_at": "2024-10-23T05:16:30.123456Z"
    }
  ],
  "skip": 0,
  "limit": 100,
  "total": 4
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/tipos-opciones?skip=0&limit=100`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/tipos-opciones?skip=0&limit=100" \
  -H "accept: application/json"
```
