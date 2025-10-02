# Guía de Postman - API Gestión de Restaurante

## Descripción
Esta colección de Postman está diseñada para probar los casos de uso específicos de Charlie:
- **C4**: Crear una nueva orden con productos seleccionados, acompañamientos y comentarios especiales
- **C10**: Obtener todos los acompañamientos disponibles para mostrar en el proceso de personalización
- **C11**: Validar disponibilidad de productos antes de confirmar pedido

## Configuración Inicial

### 1. Importar la Colección
1. Abre Postman
2. Haz clic en "Import"
3. Selecciona el archivo `postman_collection.json`
4. La colección aparecerá en tu workspace

### 2. Configurar Variables de Entorno
La colección incluye las siguientes variables:
- `base_url`: `http://127.0.0.1:8000` (URL base de la API)
- `orden_id`: `1` (ID de orden para pruebas)

### 3. Iniciar el Servidor
Antes de ejecutar las pruebas, asegúrate de que el servidor esté ejecutándose:
```bash
cd E:\PROYECTOS\DP2\V3\back-dp2
python -m uvicorn app.main:app --reload
```

## Casos de Uso

### C4 - Crear Orden Completa
Este flujo simula el proceso completo de creación de una orden:

1. **Obtener Items Disponibles** - Ver qué productos están disponibles
2. **Obtener Acompañamientos de Item** - Ver opciones de personalización
3. **Validar Disponibilidad de Item** - Verificar stock antes de agregar
4. **Obtener Meseros Disponibles** - Ver meseros activos
5. **Crear Nueva Orden** - Crear la orden base
6. **Agregar Item Principal** - Agregar plato principal con comentarios
7. **Agregar Bebida** - Agregar bebidas a la orden
8. **Verificar Orden Completa** - Ver el resultado final

### C10 - Acompañamientos Disponibles
Endpoints para obtener información de acompañamientos:

1. **Obtener Todos los Acompañamientos** - Lista completa de opciones
2. **Acompañamientos de Ceviche** - Opciones específicas para ceviche
3. **Acompañamientos de Lomo Saltado** - Opciones para lomo saltado
4. **Acompañamientos de Arroz con Mariscos** - Opciones para arroz

### C11 - Validar Disponibilidad
Endpoints para validar stock antes de confirmar:

1. **Validar Item Individual** - Verificar un producto específico
2. **Validar Múltiples Items** - Verificar varios productos a la vez
3. **Validar Item con Cantidad Alta** - Probar límites de stock
4. **Validar Item No Disponible** - Manejo de errores
5. **Validar Disponibilidad de Orden Completa** - Verificar orden existente

## Ejemplos de Uso

### Crear una Orden Completa (Método Recomendado)
```json
POST /api/pedidos/ordenes/completa
{
  "comentarios_generales": "Orden completa para Cliente Charlie",
  "mesero_ids": [1],
  "items": [
    {
      "item_id": 1,
      "cantidad": 1,
      "comentarios": "Ceviche sin cebolla, bien picante",
      "acompanamientos_seleccionados": [1, 2],
      "opciones_adicionales_seleccionadas": [5]
    },
    {
      "item_id": 6,
      "cantidad": 2,
      "comentarios": "Cerveza bien fría",
      "acompanamientos_seleccionados": [],
      "opciones_adicionales_seleccionadas": []
    }
  ]
}
```

### Crear una Orden Simple (Método Alternativo)
```json
POST /api/pedidos/ordenes
{
  "comentarios": "Orden para Cliente Charlie",
  "mesero_ids": [1]
}
```

### Agregar Item con Comentarios Especiales
```json
POST /api/pedidos/ordenes/1/items
{
  "item_id": 1,
  "cantidad": 1,
  "comentarios": "Ceviche sin cebolla, bien picante"
}
```

### Validar Disponibilidad Múltiple
```json
POST /api/menu/validar-disponibilidad-multiple
[
  {
    "item_id": 1,
    "cantidad": 2
  },
  {
    "item_id": 2,
    "cantidad": 1
  },
  {
    "item_id": 6,
    "cantidad": 3
  }
]
```

## Respuestas Esperadas

### Orden Completa Creada Exitosamente
```json
{
  "orden": {
    "id": 1,
    "numero_orden": 1001,
    "linea_pedidos": [
      {
        "id": 1,
        "item_id": 1,
        "item_nombre": "Ceviche",
        "item_precio": 28.0,
        "cant_pedida": 1,
        "subtotal": 28.0,
        "comentarios": "Ceviche sin cebolla, bien picante"
      }
    ],
    "num_items": 1,
    "monto_total": 28.0,
    "estado": "EN_COLA",
    "comentarios": "Orden completa para Cliente Charlie",
    "activo": true,
    "hora_registro": "2024-01-15T10:30:00",
    "meseros": []
  },
  "resultados_items": [
    {
      "item_id": 1,
      "item_nombre": "Ceviche",
      "cantidad": 1,
      "exitoso": true,
      "mensaje": "Item agregado exitosamente",
      "acompanamientos": [1, 2],
      "opciones_adicionales": [5]
    }
  ],
  "items_exitosos": 1,
  "items_fallidos": 0,
  "mensaje_general": "Orden creada exitosamente con 1 items"
}
```

### Orden Simple Creada Exitosamente
```json
{
  "id": 1,
  "numero_orden": 1001,
  "linea_pedidos": [],
  "num_items": 0,
  "monto_total": 0.0,
  "estado": "EN_COLA",
  "comentarios": "Orden para Cliente Charlie",
  "activo": true,
  "hora_registro": "2024-01-15T10:30:00",
  "meseros": []
}
```

### Item Agregado Exitosamente
```json
{
  "mensaje": "Item agregado a la orden exitosamente"
}
```

### Validación de Disponibilidad
```json
{
  "item_id": 1,
  "disponible": true,
  "stock_actual": 10,
  "cantidad_solicitada": 2,
  "mensaje": "Item disponible en la cantidad solicitada"
}
```

## Flujo de Pruebas Recomendado

### Método Recomendado: Orden Completa (Una sola llamada)
1. **Ejecutar Health Check** para verificar que la API esté funcionando
2. **Obtener Items Disponibles** para ver el catálogo
3. **Obtener Acompañamientos** para ver opciones de personalización
4. **Validar Disponibilidad** de los items que quieres agregar
5. **Crear Orden Completa** con todos los items, acompañamientos y comentarios
6. **Verificar Orden Completa** para confirmar el resultado

### Método Alternativo: Orden Simple (Múltiples llamadas)
1. **Ejecutar Health Check** para verificar que la API esté funcionando
2. **Obtener Items Disponibles** para ver el catálogo
3. **Obtener Acompañamientos** para ver opciones de personalización
4. **Validar Disponibilidad** de los items que quieres agregar
5. **Crear Nueva Orden** con mesero
6. **Agregar Items** uno por uno con comentarios especiales
7. **Verificar Orden Completa** para confirmar el resultado

## Notas Importantes

- Los IDs de items y meseros pueden variar según los datos de prueba
- Ajusta la variable `orden_id` después de crear una nueva orden
- Los comentarios especiales se pueden personalizar según las necesidades del cliente
- La validación de disponibilidad es crucial antes de confirmar pedidos grandes

## Troubleshooting

### Error 404 - Item No Encontrado
- Verifica que el item_id existe usando `GET /api/menu/items`
- Asegúrate de que el item esté disponible

### Error 400 - Stock Insuficiente
- Usa `GET /api/menu/validar-disponibilidad/{id}?cantidad={cantidad}` para verificar stock
- Reduce la cantidad solicitada

### Error 500 - Error del Servidor
- Verifica que el servidor esté ejecutándose
- Revisa los logs del servidor para más detalles

## Endpoints de Referencia

- **Documentación API**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`
