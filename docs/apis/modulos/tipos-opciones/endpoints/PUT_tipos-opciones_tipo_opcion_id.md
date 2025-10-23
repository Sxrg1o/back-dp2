# Especificación (breve) — PUT Tipo de Opción por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/tipos-opciones/{tipo_opcion_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `tipo_opcion_id` | string | YES | ID del tipo de opción (ULID). |

### BODY

```json
{
  "obligatorio": false,
  "orden": 2
}
```

## SALIDA (200 OK)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Nivel de picante",
  "descripcion": "Selecciona el nivel de ají",
  "obligatorio": false,
  "multiple_seleccion": false,
  "orden": 2,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X PUT "https://back-dp2.onrender.com/api/v1/tipos-opciones/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "Content-Type: application/json" \
  -d '{"obligatorio": false}'
```
