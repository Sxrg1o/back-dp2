# Endpoints de Seed de Base de Datos

Este documento describe los endpoints disponibles para gestionar el seed de la base de datos.

## Endpoints Disponibles

### 1. Ejecutar Seed Manualmente

**POST** `/api/v1/seed/execute`

Ejecuta el script de seed para poblar la base de datos con datos iniciales de la cevichería.

#### Parámetros de Query

- `force` (boolean, opcional): Si es `true`, ejecuta el seed aunque ya existan datos. Por defecto es `false`.

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "result": {
    "success": true,
    "message": "Seed ejecutado exitosamente",
    "data_created": {
      "roles": 5,
      "categorias": 7,
      "alergenos": 8,
      "productos": 25,
      "tipos_opciones": 4,
      "productos_opciones": 45
    },
    "execution_time": 2.34
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

#### Respuesta de Error (409)

```json
{
  "detail": "Ya existen 7 categorías en la base de datos. Use force=true para sobrescribir."
}
```

#### Ejemplos de Uso

```bash
# Ejecutar seed solo si la BD está vacía
curl -X POST "http://localhost:8000/api/v1/seed/execute"

# Forzar ejecución del seed (sobrescribe datos existentes)
curl -X POST "http://localhost:8000/api/v1/seed/execute?force=true"
```

### 2. Verificar Estado del Seed

**GET** `/api/v1/seed/status`

Verifica si la base de datos ya contiene datos de seed.

#### Respuesta (200)

```json
{
  "is_populated": true,
  "total_records": 94,
  "counts": {
    "roles": 5,
    "categorias": 7,
    "alergenos": 8,
    "productos": 25,
    "tipos_opciones": 4,
    "productos_opciones": 45
  },
  "message": "Base de datos poblada"
}
```

#### Ejemplo de Uso

```bash
curl -X GET "http://localhost:8000/api/v1/seed/status"
```

## Comportamiento Automático

### Auto-Seed al Iniciar la Aplicación

La aplicación ejecuta automáticamente el seed cuando:

1. Se inicia la aplicación
2. La base de datos está vacía (no hay categorías)
3. Se ejecuta en un contenedor Docker

### Logs de Auto-Seed

Puedes ver los logs del auto-seed en la consola:

```
🔍 Verificando estado de la base de datos...
📊 Categorías encontradas: 0
🌱 Base de datos vacía detectada. Ejecutando seed automático...
🌊 Iniciando seed de datos para Cevichería...
👥 Creando roles...
📂 Creando categorías...
⚠️  Creando alérgenos...
🍽️  Creando productos...
🔗 Creando relaciones producto-alérgeno...
⚙️  Creando tipos de opciones...
🎛️  Creando opciones de productos...
✅ ¡Seed completado exitosamente!
```

## Datos Incluidos en el Seed

El seed incluye los siguientes datos:

### Roles (5)
- Administrador
- Mesero
- Cocinero
- Cajero
- Cliente

### Categorías (7)
- Ceviches
- Tiraditos
- Chicharrones
- Arroces
- Causas
- Bebidas
- Postres

### Alérgenos (8)
- Mariscos
- Pescado
- Moluscos
- Gluten
- Lácteos
- Ají
- Soja
- Frutos Secos

### Productos (25)
- 4 Ceviches
- 3 Tiraditos
- 3 Chicharrones
- 3 Arroces
- 3 Causas
- 6 Bebidas
- 4 Postres

### Tipos de Opciones (4)
- Nivel de Ají
- Acompañamiento
- Temperatura
- Tamaño

### Opciones de Productos (45+)
- Opciones de nivel de ají para platos picantes
- Opciones de acompañamiento para ceviches y chicharrones
- Opciones de temperatura para bebidas
- Opciones de tamaño para platos principales

## Solución de Problemas

### Base de Datos Vacía en Docker

Si la base de datos se queda vacía en Docker:

1. **Verificar volúmenes**: Asegúrate de que el directorio `./instance` esté montado correctamente
2. **Verificar logs**: Revisa los logs del contenedor para ver si el auto-seed se ejecutó
3. **Ejecutar manualmente**: Usa el endpoint `/api/v1/seed/execute` para poblar la BD

### Error de Permisos

Si hay errores de permisos:

1. Verifica que el usuario `app` tenga permisos de escritura en `/app/instance`
2. Asegúrate de que el directorio `instance` exista y tenga los permisos correctos

### Base de Datos Corrupta

Si la base de datos está corrupta:

1. Detén el contenedor
2. Elimina el archivo de base de datos: `rm -rf ./instance/`
3. Reinicia el contenedor
4. El auto-seed se ejecutará automáticamente

