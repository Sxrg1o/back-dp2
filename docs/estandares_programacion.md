# Estándares de Programación del Repositorio

Este documento define los estándares de programación y convenciones de código que **DEBEN** seguirse estrictamente en el repositorio.

---

## ⚠️ ESTÁNDARES CRÍTICOS - ORDEN OBLIGATORIO

### 📋 Resumen Rápido de Orden

#### **Modelos (Models)**
1. `__tablename__`
2. **Foreign Keys** (todas las claves foráneas)
3. **Columnas específicas** (atributos propios del modelo)
4. **Relaciones** (SQLAlchemy relationships)
5. `__table_args__` (índices, constraints)
6. **Métodos utilitarios**: `to_dict()`, `from_dict()`, `update_from_dict()`, `__repr__()`

#### **Repositorios (Repositories)**
1. `__init__(session: AsyncSession)`
2. `create(entity: EntityModel) -> EntityModel`
3. `get_by_id(entity_id: UUID) -> Optional[EntityModel]`
4. `delete(entity_id: UUID) -> bool`
5. `update(entity_id: UUID, **kwargs) -> Optional[EntityModel]`
6. `get_all(skip: int = 0, limit: int = 100) -> Tuple[List[EntityModel], int]`
7. **Métodos específicos del dominio** (ej: `get_by_codigo()`, `get_activos()`)

#### **Servicios (Services)**
1. `__init__(session: AsyncSession)`
2. `create_{entidad}(data: EntidadCreate) -> EntidadResponse`
3. `get_{entidad}_by_id(entidad_id: UUID) -> EntidadResponse`
4. `delete_{entidad}(entidad_id: UUID) -> bool`
5. `get_{entidades}(skip: int = 0, limit: int = 100) -> EntidadList`
6. `update_{entidad}(entidad_id: UUID, data: EntidadUpdate) -> EntidadResponse`

#### **Controladores (Controllers)**
1. `POST ""` → `create_{entidad}()`
2. `GET "/{id}"` → `get_{entidad}()`
3. `GET ""` → `list_{entidades}()`
4. `PUT "/{id}"` → `update_{entidad}()`
5. `DELETE "/{id}"` → `delete_{entidad}()`

#### **Schemas (Pydantic)**
1. `{Entidad}Base` (campos comunes)
2. `{Entidad}Create` (hereda de Base)
3. `{Entidad}Update` (todos opcionales)
4. `{Entidad}Response` (incluye id y auditoría)
5. `{Entidad}Summary` (resumen para listas)
6. `{Entidad}List` (lista paginada)

#### **Imports (en todos los archivos)**
1. **Biblioteca estándar** (`typing`, `uuid`, `datetime`)
2. **Terceros** (`sqlalchemy`, `fastapi`, `pydantic`)
3. **Locales** (`src.models`, `src.repositories`, etc.)

---

## 1. Modelos (Models)

### 1.1 Orden Estricto de Atributos

**OBLIGATORIO**: Los atributos deben seguir este orden exacto:

```python
class NombreModel(BaseModel, AuditMixin):
    """Docstring de la clase con formato NumPy."""
    
    # 1. Nombre de tabla
    __tablename__ = "nombre_tabla"
    
    # 2. Foreign Keys (TODAS primero)
    id_categoria: Mapped[UUID] = mapped_column(ForeignKey(...), ...)
    
    # 3. Columnas específicas del modelo
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio_base: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), ...)
    
    # 4. Relaciones (después de columnas)
    categoria: Mapped["CategoriaModel"] = relationship(...)
    
    # 5. Índices y constraints
    __table_args__ = (Index('idx_busqueda', 'nombre', 'descripcion'),)
    
    # 6. Métodos utilitarios (en este orden)
    def to_dict(self) -> Dict[str, Any]: ...
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T: ...
    
    def update_from_dict(self, data: Dict[str, Any]) -> None: ...
    
    def __repr__(self) -> str: ...
```

### 1.2 Reglas de Modelos

- ✅ **Herencia**: Todos heredan de `BaseModel`, los que requieren auditoría también de `AuditMixin`
- ✅ **Tipado**: Usar `Mapped[Tipo]` para todas las columnas
- ✅ **Opcionales**: Usar `Optional[Tipo]` para campos nullable
- ✅ **Relaciones circulares**: Usar `TYPE_CHECKING` para imports de tipos

---

## 2. Repositorios (Repositories)

### 2.1 Orden Estricto de Métodos

**OBLIGATORIO**: Los métodos deben seguir este orden exacto:

```python
class NombreRepository:
    """Docstring de la clase."""
    
    # 1. Constructor
    def __init__(self, session: AsyncSession): ...
    
    # 2. Create
    async def create(self, entity: EntityModel) -> EntityModel: ...
    
    # 3. Get by ID
    async def get_by_id(self, entity_id: UUID) -> Optional[EntityModel]: ...
    
    # 4. Delete
    async def delete(self, entity_id: UUID) -> bool: ...
    
    # 5. Update
    async def update(self, entity_id: UUID, **kwargs) -> Optional[EntityModel]: ...
    
    # 6. Get All (paginado)
    async def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[EntityModel], int]: ...
    
    # 7. Métodos específicos del dominio (al final)
    async def get_by_codigo(self, codigo: str) -> Optional[EntityModel]: ...
```

### 2.2 Reglas de Repositorios

- ✅ **Manejo de errores**: `try/except` con `rollback()` en operaciones de escritura (create, update, delete)
- ✅ **Update**: Filtrar campos válidos, excluir `id`, usar `.returning()`
- ✅ **Lectura**: No hacer rollback en `get_by_id()` y `get_all()`

---

## 3. Servicios (Services)

### 3.1 Orden Estricto de Métodos

**OBLIGATORIO**: Los métodos deben seguir este orden exacto:

```python
class NombreService:
    """Docstring de la clase."""
    
    # 1. Constructor
    def __init__(self, session: AsyncSession): ...
    
    # 2. Create
    async def create_{entidad}(self, data: EntidadCreate) -> EntidadResponse: ...
    
    # 3. Get by ID
    async def get_{entidad}_by_id(self, entidad_id: UUID) -> EntidadResponse: ...
    
    # 4. Delete
    async def delete_{entidad}(self, entidad_id: UUID) -> bool: ...
    
    # 5. Get All (listado)
    async def get_{entidades}(self, skip: int = 0, limit: int = 100) -> EntidadList: ...
    
    # 6. Update
    async def update_{entidad}(self, entidad_id: UUID, data: EntidadUpdate) -> EntidadResponse: ...
```

### 3.2 Reglas de Servicios

- ✅ **Validación**: Validar parámetros de entrada antes de operaciones
- ✅ **Transformación**: Convertir entre modelos y schemas usando `model_validate()`
- ✅ **Excepciones**: Capturar `IntegrityError` y lanzar excepciones de negocio (`ConflictError`, `NotFoundError`, `ValidationError`)
- ✅ **Verificación**: Validar existencia antes de update/delete

---

## 4. Controladores (Controllers)

### 4.1 Orden Estricto de Endpoints

**OBLIGATORIO**: Los endpoints deben seguir este orden exacto:

```python
router = APIRouter(prefix="/entidades", tags=["Entidades"])

# 1. POST (Create)
@router.post("", response_model=EntidadResponse, status_code=status.HTTP_201_CREATED, ...)
async def create_{entidad}(...): ...

# 2. GET by ID
@router.get("/{entidad_id}", response_model=EntidadResponse, ...)
async def get_{entidad}(...): ...

# 3. GET List
@router.get("", response_model=EntidadList, ...)
async def list_{entidades}(...): ...

# 4. PUT (Update)
@router.put("/{entidad_id}", response_model=EntidadResponse, ...)
async def update_{entidad}(...): ...

# 5. DELETE
@router.delete("/{entidad_id}", status_code=status.HTTP_204_NO_CONTENT, ...)
async def delete_{entidad}(...): ...
```

### 4.2 Reglas de Controladores

- ✅ **Decoradores**: Incluir `response_model`, `status_code`, `summary`, `description`
- ✅ **Excepciones HTTP**: 
  - `404 NOT_FOUND` para `NotFoundError`
  - `409 CONFLICT` para `ConflictError`
  - `400 BAD_REQUEST` para `ValidationError`
  - `500 INTERNAL_SERVER_ERROR` para errores genéricos
- ✅ **Dependencias**: Usar `Depends(get_database_session)`, crear servicio dentro del endpoint

---

## 5. Schemas (Pydantic)

### 5.1 Orden Estricto de Schemas

**OBLIGATORIO**: Los schemas deben seguir este orden exacto:

```python
# 1. Base (campos comunes)
class EntidadBase(BaseModel):
    nombre: str = Field(...)
    descripcion: Optional[str] = Field(...)

# 2. Create (hereda de Base)
class EntidadCreate(EntidadBase):
    pass

# 3. Update (todos opcionales)
class EntidadUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, ...)
    descripcion: Optional[str] = Field(default=None, ...)

# 4. Response (incluye id y auditoría)
class EntidadResponse(EntidadBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(...)
    fecha_creacion: Optional[datetime] = Field(...)
    fecha_modificacion: Optional[datetime] = Field(...)

# 5. Summary (resumen para listas)
class EntidadSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(...)
    nombre: str = Field(...)

# 6. List (lista paginada)
class EntidadList(BaseModel):
    items: List[EntidadSummary] = Field(...)
    total: int = Field(...)
```

### 5.2 Orden de Campos en Schemas

1. **Campos de identificación**: `id` (solo en Response)
2. **Campos de negocio**: Campos específicos de la entidad
3. **Campos de auditoría**: `fecha_creacion`, `fecha_modificacion` (solo en Response)
4. **Campos de listado**: `items`, `total` (solo en List)

### 5.3 Reglas de Schemas

- ✅ **Field()**: Todos los campos deben usar `Field()` con `description`
- ✅ **Opcionales**: Campos opcionales con `default=None`
- ✅ **Validaciones**: Campos requeridos con validaciones (`min_length`, `max_length`, `gt`, etc.)
- ✅ **ConfigDict**: Usar `ConfigDict(from_attributes=True)` en Response y Summary

---

## 6. Imports

### 6.1 Orden Estricto de Imports

**OBLIGATORIO**: Los imports deben seguir este orden exacto:

```python
# 1. Biblioteca estándar
from typing import Optional, List, Dict, Any, Type, TypeVar, Tuple
from uuid import UUID
from datetime import datetime
from decimal import Decimal

# 2. Terceros
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field, ConfigDict

# 3. Locales (del proyecto)
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin
from src.repositories.menu.producto_repository import ProductoRepository
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import ProductoCreate, ProductoResponse
from src.business_logic.exceptions.producto_exceptions import ProductoNotFoundError
```

### 6.2 Reglas de Imports

- ✅ **Separación**: Cada grupo separado por línea en blanco
- ✅ **Orden alfabético**: Dentro de cada grupo, ordenar alfabéticamente
- ✅ **TYPE_CHECKING**: Usar para imports de tipos en relaciones circulares

---

## 7. Convenciones de Nombres

### 7.1 Archivos

- **Modelos**: `{entidad}_model.py` → `producto_model.py`
- **Repositorios**: `{entidad}_repository.py` → `producto_repository.py`
- **Servicios**: `{entidad}_service.py` → `producto_service.py`
- **Controladores**: `{entidad}_controller.py` → `producto_controller.py`
- **Schemas**: `{entidad}_schema.py` → `producto_schema.py`
- **Excepciones**: `{entidad}_exceptions.py` → `producto_exceptions.py`

### 7.2 Clases

- **Modelos**: `{Entidad}Model` → `ProductoModel`
- **Repositorios**: `{Entidad}Repository` → `ProductoRepository`
- **Servicios**: `{Entidad}Service` → `ProductoService`
- **Schemas**: `{Entidad}Base`, `{Entidad}Create`, `{Entidad}Update`, `{Entidad}Response`, `{Entidad}Summary`, `{Entidad}List`
- **Excepciones**: `{Entidad}Error`, `{Entidad}NotFoundError`, `{Entidad}ValidationError`, `{Entidad}ConflictError`

### 7.3 Métodos y Funciones

- **Servicios**: `create_{entidad}()`, `get_{entidad}_by_id()`, `update_{entidad}()`, `delete_{entidad}()`, `get_{entidades}()`
- **Repositorios**: `create()`, `get_by_id()`, `update()`, `delete()`, `get_all()`
- **Endpoints**: `create_{entidad}()`, `get_{entidad}()`, `list_{entidades}()`, `update_{entidad}()`, `delete_{entidad}()`

### 7.4 Variables

- **Snake_case** para variables y funciones
- **PascalCase** para clases
- **UPPER_CASE** para constantes
- Nombres descriptivos en español para variables de negocio

---

## 8. Docstrings

### 8.1 Formato

- ✅ **Formato NumPy/SciPy**: Ver `docs/docstring.md` para detalles
- ✅ **Idioma**: Documentación en español, keywords en inglés (`Parameters`, `Returns`, `Raises`)

### 8.2 Estructura

- **Módulos**: Descripción breve y detallada
- **Clases**: Descripción + sección `Attributes` con todos los atributos
- **Métodos/Funciones**: Descripción + `Parameters`, `Returns`, `Raises`, `Examples` (si aplica)

---

## 9. Type Hints

### 9.1 Uso Obligatorio

- ✅ Todos los parámetros de funciones/métodos deben tener type hints
- ✅ Todos los valores de retorno deben tener type hints
- ✅ Variables complejas deben tener type hints cuando no son obvias

### 9.2 Tipos Comunes

- `UUID` para identificadores
- `Optional[T]` para valores que pueden ser `None`
- `List[T]` para listas
- `Dict[str, Any]` para diccionarios genéricos
- `Tuple[List[T], int]` para tuplas (listas paginadas con total)

---

## 10. Ejemplos Completos

### 10.1 Modelo Completo

```python
"""
Modelo de productos para la gestión del menú del restaurante.
"""

from typing import Any, Dict, Optional, Type, TypeVar, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, DECIMAL, ForeignKey, Index
from uuid import UUID
from src.models.base_model import BaseModel
from src.models.mixins.audit_mixin import AuditMixin

if TYPE_CHECKING:
    from src.models.menu.categoria_model import CategoriaModel

T = TypeVar("T", bound="ProductoModel")


class ProductoModel(BaseModel, AuditMixin):
    """Modelo para representar productos del menú."""
    
    __tablename__ = "producto"
    
    # Foreign Keys
    id_categoria: Mapped[UUID] = mapped_column(
        ForeignKey("categoria.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Columnas específicas
    nombre: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio_base: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, index=True)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relaciones
    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel",
        back_populates="productos",
        lazy="selectin"
    )
    
    # Índices
    __table_args__ = (
        Index('idx_busqueda', 'nombre', 'descripcion', mysql_prefix='FULLTEXT'),
    )
    
    # Métodos
    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        valid_columns = [c.name for c in cls.__table__.columns]
        filtered_data = {k: v for k, v in data.items() if k in valid_columns}
        return cls(**filtered_data)
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"<ProductoModel(id={self.id}, nombre='{self.nombre}')>"
```

### 10.2 Repositorio Completo

```python
"""
Repositorio para la gestión de productos en el sistema.
"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, func
from src.models.menu.producto_model import ProductoModel


class ProductoRepository:
    """Repositorio para gestionar operaciones CRUD del modelo de productos."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, producto: ProductoModel) -> ProductoModel:
        try:
            self.session.add(producto)
            await self.session.flush()
            await self.session.commit()
            await self.session.refresh(producto)
            return producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise
    
    async def get_by_id(self, producto_id: UUID) -> Optional[ProductoModel]:
        query = select(ProductoModel).where(ProductoModel.id == producto_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def delete(self, producto_id: UUID) -> bool:
        try:
            stmt = delete(ProductoModel).where(ProductoModel.id == producto_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.session.rollback()
            raise
    
    async def update(self, producto_id: UUID, **kwargs) -> Optional[ProductoModel]:
        try:
            valid_fields = {
                k: v for k, v in kwargs.items() 
                if hasattr(ProductoModel, k) and k != "id"
            }
            if not valid_fields:
                return await self.get_by_id(producto_id)
            stmt = (
                update(ProductoModel)
                .where(ProductoModel.id == producto_id)
                .values(**valid_fields)
                .returning(ProductoModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            updated_producto = result.scalars().first()
            if not updated_producto:
                return None
            await self.session.refresh(updated_producto)
            return updated_producto
        except SQLAlchemyError:
            await self.session.rollback()
            raise
    
    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ProductoModel], int]:
        query = select(ProductoModel).offset(skip).limit(limit)
        count_query = select(func.count(ProductoModel.id))
        result = await self.session.execute(query)
        count_result = await self.session.execute(count_query)
        productos = result.scalars().all()
        total = count_result.scalar() or 0
        return list(productos), total
```

### 10.3 Servicio Completo

```python
"""
Servicio para la gestión de productos en el sistema.
"""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.repositories.menu.producto_repository import ProductoRepository
from src.models.menu.producto_model import ProductoModel
from src.api.schemas.producto_schema import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoSummary,
    ProductoList,
)
from src.business_logic.exceptions.producto_exceptions import (
    ProductoValidationError,
    ProductoNotFoundError,
    ProductoConflictError,
)


class ProductoService:
    """Servicio para la gestión de productos en el sistema."""
    
    def __init__(self, session: AsyncSession):
        self.repository = ProductoRepository(session)
    
    async def create_producto(self, producto_data: ProductoCreate) -> ProductoResponse:
        try:
            producto = ProductoModel(
                id_categoria=producto_data.id_categoria,
                nombre=producto_data.nombre,
                descripcion=producto_data.descripcion,
                precio_base=producto_data.precio_base,
            )
            created_producto = await self.repository.create(producto)
            return ProductoResponse.model_validate(created_producto)
        except IntegrityError:
            raise ProductoConflictError(
                f"Ya existe un producto con el nombre '{producto_data.nombre}'"
            )
    
    async def get_producto_by_id(self, producto_id: UUID) -> ProductoResponse:
        producto = await self.repository.get_by_id(producto_id)
        if not producto:
            raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")
        return ProductoResponse.model_validate(producto)
    
    async def delete_producto(self, producto_id: UUID) -> bool:
        producto = await self.repository.get_by_id(producto_id)
        if not producto:
            raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")
        return await self.repository.delete(producto_id)
    
    async def get_productos(self, skip: int = 0, limit: int = 100) -> ProductoList:
        if skip < 0:
            raise ProductoValidationError("El parámetro 'skip' debe ser mayor o igual a cero")
        if limit < 1:
            raise ProductoValidationError("El parámetro 'limit' debe ser mayor a cero")
        productos, total = await self.repository.get_all(skip, limit)
        producto_summaries = [ProductoSummary.model_validate(p) for p in productos]
        return ProductoList(items=producto_summaries, total=total)
    
    async def update_producto(
        self, producto_id: UUID, producto_data: ProductoUpdate
    ) -> ProductoResponse:
        update_data = producto_data.model_dump(exclude_none=True)
        if not update_data:
            return await self.get_producto_by_id(producto_id)
        try:
            updated_producto = await self.repository.update(producto_id, **update_data)
            if not updated_producto:
                raise ProductoNotFoundError(f"No se encontró el producto con ID {producto_id}")
            return ProductoResponse.model_validate(updated_producto)
        except IntegrityError:
            if "nombre" in update_data:
                raise ProductoConflictError(
                    f"Ya existe un producto con el nombre '{update_data['nombre']}'"
                )
            raise
```

### 10.4 Controlador Completo

```python
"""
Endpoints para gestión de productos.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_database_session
from src.business_logic.menu.producto_service import ProductoService
from src.api.schemas.producto_schema import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
    ProductoList,
)
from src.business_logic.exceptions.producto_exceptions import (
    ProductoValidationError,
    ProductoNotFoundError,
    ProductoConflictError,
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post(
    "",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto en el sistema con los datos proporcionados.",
)
async def create_producto(
    producto_data: ProductoCreate,
    session: AsyncSession = Depends(get_database_session)
) -> ProductoResponse:
    try:
        producto_service = ProductoService(session)
        return await producto_service.create_producto(producto_data)
    except ProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un producto por ID",
    description="Obtiene los detalles de un producto específico por su ID.",
)
async def get_producto(
    producto_id: UUID,
    session: AsyncSession = Depends(get_database_session)
) -> ProductoResponse:
    try:
        producto_service = ProductoService(session)
        return await producto_service.get_producto_by_id(producto_id)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.get(
    "",
    response_model=ProductoList,
    status_code=status.HTTP_200_OK,
    summary="Listar productos",
    description="Obtiene una lista paginada de productos.",
)
async def list_productos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, gt=0, le=500, description="Número máximo de registros"),
    session: AsyncSession = Depends(get_database_session),
) -> ProductoList:
    try:
        producto_service = ProductoService(session)
        return await producto_service.get_productos(skip, limit)
    except ProductoValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.put(
    "/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un producto",
    description="Actualiza los datos de un producto existente.",
)
async def update_producto(
    producto_id: UUID,
    producto_data: ProductoUpdate,
    session: AsyncSession = Depends(get_database_session),
) -> ProductoResponse:
    try:
        producto_service = ProductoService(session)
        return await producto_service.update_producto(producto_id, producto_data)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductoConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un producto",
    description="Elimina un producto existente del sistema.",
)
async def delete_producto(
    producto_id: UUID,
    session: AsyncSession = Depends(get_database_session)
) -> None:
    try:
        producto_service = ProductoService(session)
        await producto_service.delete_producto(producto_id)
    except ProductoNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}",
        )
```

---

## 📌 Recordatorio Final

**TODOS los archivos del repositorio DEBEN seguir estos estándares estrictamente. El orden de atributos, métodos y endpoints es OBLIGATORIO y no negociable.**
