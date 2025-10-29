# Especificación (breve) — PUT Alérgeno por ID

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Recurso:** `/api/v1/alergenos/{alergeno_id}`
- **HTTP Method:** `PUT`
- **Autenticación:** (Ninguna)

## ENTRADA

### Path Params

| Field | Data Type | Required | Comment |
|-------|-----------|----------|---------|
| `alergeno_id` | string | YES | ID del alérgeno (ULID). |

### BODY

```json
{
  "nombre": "Crustáceos",
  "descripcion": "Langostinos, camarones, etc."
}
```

## SALIDA (200 OK)

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Crustáceos",
  "descripcion": "Langostinos, camarones, etc.",
  "icono_path": "/static/alergenos/mariscos.svg",
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T07:22:15.789012Z"
}
```

## URLs

**Prod:** `https://back-dp2.onrender.com/api/v1/alergenos/01K7ZCT8PNJA2J8EB83NHA1MK4`

**cURL:**
```bash
curl -X PUT "https://back-dp2.onrender.com/api/v1/alergenos/01K7ZCT8PNJA2J8EB83NHA1MK4" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Crustáceos"}'
```
