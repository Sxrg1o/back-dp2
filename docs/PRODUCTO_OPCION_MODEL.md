# ProductoOpcionModel - Modelo de Opciones de Productos

## 📋 Descripción

Tabla intermedia entre `producto` y `tipo_opcion` que define las opciones específicas disponibles para cada producto en el menú del restaurante.

## 🗄️ Esquema SQL Original

```sql
create table producto_opcion
(
    id_producto_opcion int unsigned auto_increment primary key,
    id_producto        int unsigned                             not null,
    id_tipo_opcion     int unsigned                             not null,
    nombre             varchar(100)                             not null comment 'Sin ají, Ají suave, Con choclo, Helada',
    precio_adicional   decimal(10, 2) default 0.00              null,
    activo             tinyint(1)     default 1                 null,
    orden              int unsigned   default '0'               null,
    fecha_creacion     timestamp      default CURRENT_TIMESTAMP null,
    fecha_modificacion timestamp      default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    
    constraint producto_opcion_ibfk_1
        foreign key (id_producto) references producto (id_producto) on delete cascade,
    constraint producto_opcion_ibfk_2
        foreign key (id_tipo_opcion) references tipo_opcion (id_tipo_opcion)
);

create index id_tipo_opcion on producto_opcion (id_tipo_opcion);
create index idx_producto_tipo on producto_opcion (id_producto, id_tipo_opcion);
```

## 🏗️ Modelo SQLAlchemy

### Archivo: `src/models/pedidos/producto_opcion_model.py`

**Características:**
- ✅ Heredaedad de `BaseModel` (UUID como PK)
- ✅ Heredaedad de `AuditMixin` (timestamps automáticos)
- ✅ Foreign Keys con `CASCADE DELETE`
- ✅ Relaciones bidireccionales con `ProductoModel` y `TipoOpcionModel`
- ✅ Índice compuesto `idx_producto_tipo`
- ✅ Precio adicional con precisión `DECIMAL(10, 2)`
- ✅ Métodos utilitarios: `to_dict()`, `from_dict()`, `update_from_dict()`, `__repr__()`

### Atributos

| Atributo | Tipo | Descripción | Nullable | Default |
|----------|------|-------------|----------|---------|
| `id` | UUID | Identificador único (PK) | No | `uuid4()` |
| `id_producto` | UUID | FK a `producto.id` | No | - |
| `id_tipo_opcion` | UUID | FK a `tipo_opcion.id` | No | - |
| `nombre` | str(100) | Nombre de la opción | No | - |
| `precio_adicional` | Decimal(10,2) | Costo adicional | No | `0.00` |
| `activo` | bool | Estado de la opción | No | `True` |
| `orden` | int | Orden de visualización | Sí | `0` |
| `fecha_creacion` | datetime | Timestamp de creación | No | `CURRENT_TIMESTAMP` |
| `fecha_modificacion` | datetime | Timestamp de modificación | No | `CURRENT_TIMESTAMP` |
| `creado_por` | str | Usuario creador | Sí | - |
| `modificado_por` | str | Usuario modificador | Sí | - |

### Relaciones

```python
# Relación con ProductoModel
producto: Mapped["ProductoModel"] = relationship(
    "ProductoModel",
    back_populates="opciones",
    lazy="selectin"
)

# Relación con TipoOpcionModel
tipo_opcion: Mapped["TipoOpcionModel"] = relationship(
    "TipoOpcionModel",
    back_populates="producto_opciones",
    lazy="selectin"
)
```

## 📝 Ejemplos de Uso

### Crear una opción de producto

```python
from src.models.pedidos.producto_opcion_model import ProductoOpcionModel
from decimal import Decimal
from uuid import uuid4

# Crear opción "Ají suave" para un ceviche
opcion = ProductoOpcionModel(
    id_producto=producto_id,  # UUID del ceviche
    id_tipo_opcion=tipo_opcion_id,  # UUID del tipo "Nivel de Ají"
    nombre="Ají suave",
    precio_adicional=Decimal("0.00"),  # Sin costo adicional
    activo=True,
    orden=2
)
```

### Ejemplos de opciones

**Para un Ceviche (id_tipo_opcion = "Nivel de Ají"):**
```python
opciones = [
    {"nombre": "Sin ají", "precio_adicional": Decimal("0.00"), "orden": 1},
    {"nombre": "Ají suave", "precio_adicional": Decimal("0.00"), "orden": 2},
    {"nombre": "Ají picante", "precio_adicional": Decimal("1.50"), "orden": 3},
]
```

**Para una Bebida (id_tipo_opcion = "Temperatura"):**
```python
opciones = [
    {"nombre": "Natural", "precio_adicional": Decimal("0.00"), "orden": 1},
    {"nombre": "Helada", "precio_adicional": Decimal("1.00"), "orden": 2},
]
```

**Para un Arroz (id_tipo_opcion = "Acompañamiento"):**
```python
opciones = [
    {"nombre": "Sin acompañamiento", "precio_adicional": Decimal("0.00"), "orden": 1},
    {"nombre": "Con choclo", "precio_adicional": Decimal("2.50"), "orden": 2},
    {"nombre": "Con yuca", "precio_adicional": Decimal("2.50"), "orden": 3},
]
```

## 🧪 Tests

### Tests del Modelo: `tests/unit/models/pedidos/test_producto_opcion_model.py`

**5 tests unitarios:**
1. ✅ `test_producto_opcion_creation` - Creación con todos los atributos
2. ✅ `test_producto_opcion_to_dict` - Conversión a diccionario
3. ✅ `test_producto_opcion_defaults` - Valores predeterminados
4. ✅ `test_producto_opcion_precio_decimal` - Precisión de precios
5. ✅ `test_producto_opcion_repr` - Representación en string

**Resultado:** ✅ **5/5 tests pasando**

### Tests de Schemas: `tests/unit/api/schemas/test_producto_opcion_schema.py`

**10 tests unitarios:**
1. ✅ `test_producto_opcion_create_schema` - Schema de creación
2. ✅ `test_producto_opcion_create_with_defaults` - Valores por defecto
3. ✅ `test_producto_opcion_create_validation_error` - Validación de campos requeridos
4. ✅ `test_producto_opcion_create_negative_price` - Validación de precios >= 0
5. ✅ `test_producto_opcion_update_schema` - Schema de actualización
6. ✅ `test_producto_opcion_update_empty` - Actualización sin campos
7. ✅ `test_producto_opcion_response_schema` - Schema de respuesta
8. ✅ `test_producto_opcion_summary_schema` - Schema de resumen
9. ✅ `test_producto_opcion_list_schema` - Schema de lista paginada
10. ✅ `test_producto_opcion_decimal_precision` - Precisión decimal

**Resultado:** ✅ **10/10 tests pasando**

**Total de tests:** ✅ **15/15 tests pasando**

## 🔗 Modelos Relacionados Actualizados

### `ProductoModel` (src/models/menu/producto_model.py)

```python
# Nueva relación agregada
opciones: Mapped[List["ProductoOpcionModel"]] = relationship(
    "ProductoOpcionModel",
    back_populates="producto",
    lazy="selectin",
    cascade="all, delete-orphan"
)
```

### `TipoOpcionModel` (src/models/pedidos/tipo_opciones_model.py)

```python
# Nueva relación agregada
producto_opciones: Mapped[List["ProductoOpcionModel"]] = relationship(
    "ProductoOpcionModel",
    back_populates="tipo_opcion",
    lazy="selectin",
    cascade="all, delete-orphan"
)
```

## 📊 Diagrama de Relaciones

```
┌─────────────────┐         ┌──────────────────────┐         ┌────────────────┐
│  ProductoModel  │         │ ProductoOpcionModel  │         │ TipoOpcionModel│
├─────────────────┤         ├──────────────────────┤         ├────────────────┤
│ id (UUID)       │◄────────│ id_producto (UUID)   │         │ id (UUID)      │
│ nombre          │         │ id_tipo_opcion (UUID)│────────►│ codigo         │
│ precio_base     │         │ nombre               │         │ nombre         │
│ ...             │         │ precio_adicional     │         │ descripcion    │
└─────────────────┘         │ activo               │         └────────────────┘
                            │ orden                │
                            └──────────────────────┘
```

## ✅ Checklist de Implementación

- [x] Modelo creado siguiendo patrón de `RolModel`
- [x] Heredado de `BaseModel` y `AuditMixin`
- [x] Foreign Keys configuradas con `CASCADE DELETE`
- [x] Relaciones bidireccionales establecidas
- [x] Índice compuesto `idx_producto_tipo` creado
- [x] Métodos utilitarios implementados
- [x] Tests unitarios (5/5 pasando)
- [x] Modelos relacionados actualizados
- [x] Exportado en `__init__.py`
- [x] Documentación completa

## 🚀 Próximos Pasos Sugeridos

1. **Controller**: Crear `producto_opcion_controller.py` con endpoints CRUD
2. **Service**: Crear `producto_opcion_service.py` con lógica de negocio
3. **Repository**: Crear `producto_opcion_repository.py` con queries
4. **Schemas**: Crear `producto_opcion_schema.py` para validación Pydantic
5. **Tests Integración**: Tests de integración para el flujo completo
6. **Seed Data**: Agregar opciones de ejemplo en `seed_cevicheria_data.py`

## 📌 Notas Importantes

- El modelo usa **UUID** como PK (a diferencia del SQL original que usa `int`)
- El `CASCADE DELETE` está habilitado: eliminar un producto borra sus opciones
- El campo `precio_adicional` usa `Decimal` para evitar problemas de redondeo
- Las relaciones usan `lazy="selectin"` para optimizar queries N+1
- El modelo sigue el patrón establecido en `RolModel` y `ProductoModel`

---

**Total de tests en el proyecto: 238 ✅**
