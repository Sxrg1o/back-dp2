# 📋 Ejemplos de Uso de los Nuevos Endpoints

## 🍽️ Acompañamientos

### 1. Obtener acompañamientos de un item específico
```bash
GET /api/menu/items/1/acompanamientos
```

**Respuesta:**
```json
{
  "item_id": 1,
  "item_nombre": "Ceviche",
  "acompanamientos": [
    {
      "etiqueta": "Camote",
      "precio_adicional": 3.0,
      "es_default": false,
      "seleccionado": false
    },
    {
      "etiqueta": "Choclo",
      "precio_adicional": 2.5,
      "es_default": false,
      "seleccionado": false
    },
    {
      "etiqueta": "Papas fritas",
      "precio_adicional": 4.0,
      "es_default": false,
      "seleccionado": false
    },
    {
      "etiqueta": "Sin acompañamiento",
      "precio_adicional": 0.0,
      "es_default": true,
      "seleccionado": false
    }
  ],
  "max_selecciones": 2,
  "tipo_personalizacion": "acompanamiento"
}
```

### 2. Obtener todos los acompañamientos disponibles
```bash
GET /api/menu/acompanamientos
```

**Respuesta:**
```json
{
  "acompanamientos": [
    {
      "etiqueta": "Camote",
      "precio_adicional": 3.0,
      "es_default": false,
      "items_disponibles": [
        {
          "item_id": 1,
          "item_nombre": "Ceviche"
        }
      ]
    },
    {
      "etiqueta": "Choclo",
      "precio_adicional": 2.5,
      "es_default": false,
      "items_disponibles": [
        {
          "item_id": 1,
          "item_nombre": "Ceviche"
        }
      ]
    }
  ],
  "total_acompanamientos": 4
}
```

## ✅ Validación de Disponibilidad

### 1. Validar un item individual
```bash
GET /api/menu/validar-disponibilidad/1?cantidad=2
```

**Respuesta:**
```json
{
  "item_id": 1,
  "cantidad": 2,
  "disponible": true,
  "mensaje": "Disponible"
}
```

### 2. Validar múltiples items (carrito completo)
```bash
POST /api/menu/validar-disponibilidad-multiple
Content-Type: application/json

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

**Respuesta:**
```json
{
  "todos_disponibles": true,
  "resultados": [
    {
      "item_id": 1,
      "cantidad": 2,
      "disponible": true,
      "mensaje": "Disponible"
    },
    {
      "item_id": 2,
      "cantidad": 1,
      "disponible": true,
      "mensaje": "Disponible"
    },
    {
      "item_id": 6,
      "cantidad": 3,
      "disponible": true,
      "mensaje": "Disponible"
    }
  ],
  "total_items": 3
}
```

## 🚀 Casos de Uso en el Frontend

### 1. **Página de producto individual**
```javascript
// Obtener detalles del producto
const producto = await fetch('/api/menu/items/1').then(r => r.json());

// Obtener acompañamientos específicos
const acompanamientos = await fetch('/api/menu/items/1/acompanamientos').then(r => r.json());

// Mostrar opciones de acompañamiento
acompanamientos.acompanamientos.forEach(opcion => {
  console.log(`${opcion.etiqueta} - +$${opcion.precio_adicional}`);
});
```

### 2. **Página de personalización**
```javascript
// Obtener todos los acompañamientos disponibles
const todosAcompanamientos = await fetch('/api/menu/acompanamientos').then(r => r.json());

// Mostrar catálogo completo de acompañamientos
todosAcompanamientos.acompanamientos.forEach(acompanamiento => {
  console.log(`${acompanamiento.etiqueta} - +$${acompanamiento.precio_adicional}`);
  console.log(`Disponible en: ${acompanamiento.items_disponibles.map(i => i.item_nombre).join(', ')}`);
});
```

### 3. **Validación antes del checkout**
```javascript
// Validar carrito completo antes de proceder
const carrito = [
  { item_id: 1, cantidad: 2 },
  { item_id: 2, cantidad: 1 },
  { item_id: 6, cantidad: 3 }
];

const validacion = await fetch('/api/menu/validar-disponibilidad-multiple', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(carrito)
}).then(r => r.json());

if (validacion.todos_disponibles) {
  // Proceder al checkout
  console.log('Todos los items están disponibles');
} else {
  // Mostrar errores
  validacion.resultados.forEach(resultado => {
    if (!resultado.disponible) {
      console.error(`Item ${resultado.item_id}: ${resultado.mensaje}`);
    }
  });
}
```

## 📱 URLs de Prueba

Una vez que tengas el servidor ejecutándose:

- **Acompañamientos del Ceviche**: http://localhost:8000/api/menu/items/1/acompanamientos
- **Todos los acompañamientos**: http://localhost:8000/api/menu/acompanamientos
- **Validar Ceviche**: http://localhost:8000/api/menu/validar-disponibilidad/1?cantidad=2
- **Documentación completa**: http://localhost:8000/docs
