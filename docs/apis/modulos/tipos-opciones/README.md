# Módulo: Tipos de Opciones

[⬅ Volver al Índice](../../README.md)

## Descripción

Gestión de tipos de opciones para productos. Define los grupos de opciones que pueden aplicarse a los productos (ej: "Nivel de picante", "Acompañamientos", "Bebidas").

## Recurso Base

```
/api/v1/tipos-opciones
```

## Endpoints Disponibles

- **[POST /tipos-opciones](endpoints/POST_tipos-opciones.md)** — Crea un nuevo tipo de opción
- **[GET /tipos-opciones](endpoints/GET_tipos-opciones.md)** — Lista tipos de opciones (paginado)
- **[GET /tipos-opciones/{tipo_opcion_id}](endpoints/GET_tipos-opciones_tipo_opcion_id.md)** — Obtiene un tipo de opción por ID
- **[PUT /tipos-opciones/{tipo_opcion_id}](endpoints/PUT_tipos-opciones_tipo_opcion_id.md)** — Actualiza un tipo de opción
- **[DELETE /tipos-opciones/{tipo_opcion_id}](endpoints/DELETE_tipos-opciones_tipo_opcion_id.md)** — Elimina un tipo de opción

## Schema Principal

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

## Reglas de Negocio

- ✅ El **nombre** del tipo de opción es **único** en el sistema
- ✅ El campo `obligatorio` indica si el cliente debe seleccionar al menos una opción
- ✅ El campo `multiple_seleccion` permite seleccionar múltiples opciones del mismo tipo
- ✅ El campo `orden` controla la secuencia de visualización

## Caso de Uso

**HU-C07:** Cliente que personaliza — Añadir extras disponibles a mi selección

## Errores Comunes

| HTTP | Code | Descripción |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Datos de entrada inválidos |
| 404 | `NOT_FOUND` | Tipo de opción no encontrado |
| 409 | `CONFLICT` | Tipo de opción con nombre duplicado |
| 500 | `INTERNAL_ERROR` | Error interno del servidor |
