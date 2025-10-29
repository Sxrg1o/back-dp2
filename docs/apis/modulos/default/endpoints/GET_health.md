# Especificación (breve) — GET Health

[⬅ Volver al Módulo](../README.md) · [⬅ Índice](../../../README.md)

## META

- **Host (variable):**
  - **Prod:** `https://back-dp2.onrender.com`
  - **Local:** `http://127.0.0.1:8000`
- **Base Path:** *(no aplica)*
- **Recurso (constante):** `/health`
- **HTTP Method:** `GET`
- **Autenticación:** (Ninguna)
- **Notas:** ⚠️ **NO** usa el prefijo `/api/v1`

**URL patrón:** `{HOST}/health`

## DESCRIPCIÓN

Endpoint de verificación de salud del sistema. Permite monitorizar el estado de la API para herramientas de supervisión y balanceadores de carga.

## ENTRADA

No requiere parámetros.

## SALIDA (200 OK)

```json
{
  "status": "healthy",
  "service": "restaurant-backend",
  "version": "1.0.0",
  "environment": "production"
}
```

**DICTIONARY (OUTPUT)**

| Field | Data Type | Comment |
|-------|-----------|---------|
| `status` | string | Estado del servicio ("healthy"). |
| `service` | string | Nombre del servicio. |
| `version` | string | Versión actual del servicio. |
| `environment` | string | Ambiente de ejecución ("production" o "development"). |

## URLs completas

**Producción:** `https://back-dp2.onrender.com/health`

**cURL:**
```bash
curl -X GET "https://back-dp2.onrender.com/health" \
  -H "accept: application/json"
```

**Local:** `http://127.0.0.1:8000/health`

## Notas Técnicas

- ✅ Endpoint **público** sin autenticación
- ✅ Siempre retorna **200 OK** si el servicio está activo
- ✅ Útil para **monitoreo** y **health checks** de infraestructura
- ⚠️ **NO** incluye el prefijo `/api/v1`
- ✅ Compatible con sistemas de orquestación (Kubernetes, Docker Swarm, etc.)
