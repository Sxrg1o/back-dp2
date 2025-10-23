# Especificación (breve) — GET Tipo de Opción por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/tipos-opciones/{tipo_opcion_id}`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `tipo_opcion_id` | string | YES | ID del tipo de opción (ULID). |

## SALIDA (200 OK)

```json
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
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "accept: application/json"
```
