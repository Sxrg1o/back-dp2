# Autenticación y Autorización

[⬅ Volver al Índice](../README.md)

## Estado Actual

**⚠️ IMPORTANTE:** La mayoría de los endpoints actuales **NO** requieren autenticación en esta versión.

```
Autenticación: (Ninguna)
```

## Endpoints Públicos

Los siguientes módulos son de acceso público sin autenticación:

- ✅ **Roles** — `/api/v1/roles`
- ✅ **Categorías** — `/api/v1/categorias`
- ✅ **Alérgenos** — `/api/v1/alergenos`
- ✅ **Productos** — `/api/v1/productos`
- ✅ **Tipos de Opciones** — `/api/v1/tipos-opciones`
- ✅ **Producto Opciones** — `/api/v1/producto-opciones`
- ✅ **Sincronización** — `/api/v1/sync` (endpoints internos)
- ✅ **Default** — `/` y `/health`

## Esquema Futuro (Bearer JWT)

En versiones futuras, algunos endpoints requerirán autenticación mediante **Bearer Token (JWT)**:

### Header de Autenticación

```http
Authorization: Bearer <jwt_token>
```

### Ejemplo de Request con Autenticación

```bash
curl -X GET "https://back-dp2.onrender.com/api/v1/protected-resource" \
  -H "accept: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Respuestas de Error

#### 401 Unauthorized
```json
{
  "type": "https://back-dp2.onrender.com/errors/UNAUTHORIZED",
  "title": "No autorizado",
  "status": 401,
  "detail": "Token de autenticación inválido o ausente",
  "instance": "/api/v1/protected-resource"
}
```

#### 403 Forbidden
```json
{
  "type": "https://back-dp2.onrender.com/errors/FORBIDDEN",
  "title": "Acceso denegado",
  "status": 403,
  "detail": "No tiene permisos para acceder a este recurso",
  "instance": "/api/v1/protected-resource"
}
```

## Roles y Permisos (Planificado)

| Rol | Descripción | Acceso |
|-----|-------------|--------|
| **Admin** | Administrador del sistema | Acceso completo a todos los recursos |
| **Mesero** | Personal de servicio | Lectura de menú, gestión de pedidos |
| **Cliente** | Usuario final | Lectura de menú, realizar pedidos |
| **Cocina** | Personal de cocina | Lectura de pedidos activos |

## Notas de Implementación

- Los tokens JWT contendrán: `user_id`, `rol`, `exp` (expiración)
- Los tokens tendrán una duración de **30 minutos** de inactividad
- Se implementará **refresh token** para renovación automática
- Las contraseñas se almacenarán con **bcrypt**
