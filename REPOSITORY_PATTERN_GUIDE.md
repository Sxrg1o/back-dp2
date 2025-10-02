# 🏗️ Guía del Patrón Repository

## 📋 Descripción

Se ha implementado el patrón Repository para separar la lógica de acceso a datos de la lógica de negocio. Esto permite cambiar fácilmente entre diferentes fuentes de datos sin modificar el código de los servicios.

## 🏛️ Arquitectura

### Estructura de Archivos

```
app/
├── repositories/
│   ├── __init__.py
│   ├── interfaces.py                    # Importa todas las interfaces
│   ├── menu_repository_interface.py     # Interfaz para menú
│   ├── pedidos_repository_interface.py  # Interfaz para pedidos
│   ├── mock_menu_repository.py          # Implementación mock para menú
│   ├── mock_pedidos_repository.py       # Implementación mock para pedidos
│   └── repository_factory.py            # Factory para crear repositorios
├── services/
│   ├── menu_service.py                  # Refactorizado para usar repositorio
│   └── pedidos_service.py               # Refactorizado para usar repositorio
├── config.py                            # Configuración de la aplicación
└── main.py                              # Actualizado para usar configuración
```

### Diagrama de Arquitectura

```
┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   FastAPI       │
│   Endpoints     │    │   Endpoints     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│  MenuService    │    │ PedidosService  │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│ IMenuRepository │    │IPedidosRepository│
│   (Interface)   │    │   (Interface)   │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│ MockMenuRepo    │    │MockPedidosRepo  │
│ DatabaseRepo    │    │DatabaseRepo     │
│ ApiMenuRepo     │    │ApiPedidosRepo   │
└─────────────────┘    └─────────────────┘
```

## 🔧 Uso

### 1. Configuración del Repositorio

El tipo de repositorio se configura en `app/config.py`:

```python
# Por defecto usa "mock"
REPOSITORY_TYPE = os.getenv("REPOSITORY_TYPE", "mock")
```

### 2. Cambiar Tipo de Repositorio

#### Opción 1: Variable de Entorno
```bash
export REPOSITORY_TYPE=database
python app/main.py
```

#### Opción 2: Modificar config.py
```python
REPOSITORY_TYPE = "database"  # o "api"
```

#### Opción 3: En el código
```python
from app.services.menu_service import MenuService

# Usar repositorio específico
menu_service = MenuService("database")
```

### 3. Tipos de Repositorio Disponibles

| Tipo | Estado | Descripción |
|------|--------|-------------|
| `mock` | ✅ Implementado | Datos en memoria para desarrollo y testing |
| `database` | 🚧 Pendiente | Base de datos SQL/NoSQL |
| `api` | 🚧 Pendiente | API externa |

### 4. Verificar Repositorio Actual

```bash
curl http://localhost:8000/
```

Respuesta:
```json
{
  "message": "API de Gestión de Menú y Carta",
  "version": "1.0.0",
  "repository_type": "mock",
  "available_repositories": {
    "mock": {
      "menu": true,
      "pedidos": true,
      "description": "Repositorio en memoria para desarrollo y testing"
    },
    "database": {
      "menu": false,
      "pedidos": false,
      "description": "Repositorio de base de datos (no implementado)"
    }
  }
}
```

## 🚀 Implementar Nuevo Repositorio

### 1. Crear Implementación

```python
# app/repositories/database_menu_repository.py
from app.repositories.menu_repository_interface import IMenuRepository

class DatabaseMenuRepository(IMenuRepository):
    def __init__(self, database_url: str):
        self.db = connect_to_database(database_url)
    
    def obtener_todos_los_items(self) -> Dict[int, Item]:
        # Implementar consulta a base de datos
        pass
    
    # ... implementar todos los métodos de la interfaz
```

### 2. Actualizar Factory

```python
# app/repositories/repository_factory.py
from .database_menu_repository import DatabaseMenuRepository

@staticmethod
def create_menu_repository(repository_type: str = "mock") -> IMenuRepository:
    if repository_type == "database":
        return DatabaseMenuRepository(Config.DATABASE_URL)
    # ... resto del código
```

### 3. Actualizar Configuración

```python
# app/config.py
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/menu_db")
```

## 🧪 Testing

### Tests con Repositorio Mock

```python
def test_menu_service():
    # Usar repositorio mock por defecto
    service = MenuService("mock")
    items = service.obtener_todos_los_items()
    assert len(items) > 0
```

### Tests con Repositorio Específico

```python
def test_menu_service_database():
    # Usar repositorio de base de datos
    service = MenuService("database")
    items = service.obtener_todos_los_items()
    assert len(items) > 0
```

## 📊 Beneficios

### 1. **Separación de Responsabilidades**
- Servicios se enfocan en lógica de negocio
- Repositorios manejan acceso a datos
- Fácil testing y mantenimiento

### 2. **Flexibilidad**
- Cambiar fuente de datos sin modificar servicios
- Múltiples implementaciones simultáneas
- Configuración por entorno

### 3. **Testabilidad**
- Mock repositories para tests unitarios
- Tests de integración con repositorios reales
- Aislamiento de dependencias

### 4. **Escalabilidad**
- Fácil agregar nuevas fuentes de datos
- Implementaciones específicas por dominio
- Patrón consistente en toda la aplicación

## 🔄 Migración

### Antes (Sin Repository)
```python
class MenuService:
    def obtener_todos_los_items(self):
        return obtener_todos_los_items()  # Llamada directa a datos
```

### Después (Con Repository)
```python
class MenuService:
    def __init__(self, repository_type: str = "mock"):
        self.repository = RepositoryFactory.create_menu_repository(repository_type)
    
    def obtener_todos_los_items(self):
        return self.repository.obtener_todos_los_items()  # A través del repositorio
```

## 🎯 Próximos Pasos

1. **Implementar DatabaseRepository**
   - SQLAlchemy + PostgreSQL
   - Migraciones con Alembic
   - Modelos de base de datos

2. **Implementar ApiRepository**
   - Cliente HTTP para APIs externas
   - Manejo de autenticación
   - Cache y rate limiting

3. **Agregar Cache Layer**
   - Redis para cache distribuido
   - Invalidación inteligente
   - Configuración por repositorio

4. **Monitoreo y Logging**
   - Métricas de rendimiento
   - Logs de acceso a datos
   - Alertas de fallos

## 📚 Referencias

- [Repository Pattern - Martin Fowler](https://martinfowler.com/eaaCatalog/repository.html)
- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)

---

**¡La arquitectura está lista para escalar!** 🚀

