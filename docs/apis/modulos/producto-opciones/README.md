# Módulo: Producto Opciones

[⬅ Volver al Índice](../../README.md)

## Descripción

Gestión de opciones específicas de productos. Define las opciones concretas que se pueden aplicar a un producto dentro de un tipo de opción (ej: "Ají suave", "Ají picante" dentro del tipo "Nivel de picante").

## Recurso Base

```
/api/v1/producto-opciones
```

## Endpoints Disponibles

- **[POST /producto-opciones](endpoints/POST_producto-opciones.md)** — Crea una nueva opción de producto
- **[GET /producto-opciones](endpoints/GET_producto-opciones.md)** — Lista opciones de productos (paginado)
- **[GET /producto-opciones/{producto_opcion_id}](endpoints/GET_producto-opciones_producto_opcion_id.md)** — Obtiene una opción por ID
- **[PUT /producto-opciones/{producto_opcion_id}](endpoints/PUT_producto-opciones_producto_opcion_id.md)** — Actualiza una opción
- **[DELETE /producto-opciones/{producto_opcion_id}](endpoints/DELETE_producto-opciones_producto_opcion_id.md)** — Elimina una opción

## Schema Principal

```json
{
  "id": "01K7ZCT8PNJA2J8EB83NHA1MK4",
  "nombre": "Ají suave",
  "precio_adicional": "0.00",
  "disponible": true,
  "id_producto": "01K7ZD12XYZW4M5NG95PJC3NO6",
  "id_tipo_opcion": "01K7ZE23BCDE6N7OH06QKD4OP7",
  "orden": 1,
  "created_at": "2024-10-23T05:16:30.123456Z",
  "updated_at": "2024-10-23T05:16:30.123456Z"
}
```

## Reglas de Negocio

- ✅ Cada opción pertenece a **un producto** y **un tipo de opción**
- ✅ El `precio_adicional` puede ser 0 (sin cargo extra) o positivo
- ✅ El campo `disponible` permite deshabilitar opciones temporalmente
- ✅ El campo `orden` controla la secuencia de visualización dentro del tipo

## Caso de Uso

**HU-C07:** Cliente que personaliza — Añadir extras disponibles a mi selección

## Errores Comunes

| HTTP | Code | Descripción |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Datos de entrada inválidos |
| 404 | `NOT_FOUND` | Opción, producto o tipo no encontrados |
| 409 | `CONFLICT` | Opción duplicada para el producto/tipo |
| 500 | `INTERNAL_ERROR` | Error interno del servidor |
