# Especificación (breve) — GET Root

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path:** *(no aplica)*
- **Recurso (constante):** `/`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)
- **Notas:** ⚠️ **NO** usa el prefijo `/api/v1`

**URL patrón:** `{HOST}/`

## DESCRIPCIÓN

Endpoint raíz del API. Proporciona información básica sobre el servicio y enlaces a la documentación.

## ENTRADA

No requiere parámetros.

## SALIDA (200 OK)

```json
{
  "message": "Restaurant Backend API",
  "version": "1.0.0",
  "environment": "production",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Comment |
|-------|-----------|---------|
| `message` | string | Nombre del API. |
| `version` | string | Versión actual del servicio. |
| `environment` | string | Ambiente de ejecución ("production" o "development"). |
| `docs` | string | Ruta a Swagger UI. |
| `redoc` | string | Ruta a ReDoc UI. |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/" \
  -H "accept: application/json"
```

**Local:** `http://127.0.0.1:8000/`

## Notas Técnicas

- ✅ Endpoint **público** sin autenticación
- ✅ Útil para verificar que el servicio está activo
- ⚠️ **NO** incluye el prefijo `/api/v1`
