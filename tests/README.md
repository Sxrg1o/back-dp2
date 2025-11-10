# Testing Documentation

## Estructura de Tests

Los tests están organizados siguiendo la arquitectura Clean Architecture del proyecto:

```
tests/
├── conftest.py              # Fixtures globales
├── unit/                    # Tests unitarios (NO requieren backend corriendo)
│   ├── models/             # Capa 1: Tests de modelos SQLAlchemy
│   │   ├── auth/
│   │   ├── menu/
│   │   ├── mesas/
│   │   ├── pedidos/
│   │   └── pagos/
│   ├── repositories/       # Capa 2: Tests de repositorios (mock db_session)
│   │   ├── auth/
│   │   ├── menu/
│   │   ├── mesas/
│   │   ├── pedidos/
│   │   └── pagos/
│   ├── business_logic/     # Capa 3: Tests de servicios (mock repositories)
│   │   ├── auth/
│   │   ├── menu/
│   │   ├── validators/
│   │   └── exceptions/
│   └── api/               # Capa 4: Tests de endpoints (mock services)
│       └── controllers/
├── qa/                    # Tests QA - ⚠️ REQUIEREN BACKEND CORRIENDO
│   ├── test_cu05_validaciones_errores.py  # Python (RECOMENDADO)
│   ├── test_cu05_validaciones_errores.bat # Windows BAT
│   └── test_cu05_validaciones_errores.sh  # Linux/Mac Bash
├── integration/           # Tests de integración (próximamente)
└── e2e/                  # Tests end-to-end (próximamente)
```

## Tests Implementados

### Capa 1: Models (4 archivos)
- `test_producto_model.py` - Tests de ProductoModel
- `test_categoria_model.py` - Tests de CategoriaModel
- `test_rol_model.py` - Tests de RolModel
- `test_mesa_model.py` - Tests de MesaModel

**Objetivo**: Verificar que los modelos se crean correctamente y tienen los valores por defecto esperados.

### Capa 2: Repositories (2 archivos)
- `test_producto_repository.py` - Tests de ProductoRepository
- `test_rol_mysql_repository.py` - Tests de RolMySQLRepository

**Objetivo**: Probar la lógica de acceso a datos con **mock de db_session**.

### Capa 3: Business Logic (2 archivos)
- `test_producto_service.py` - Tests de ProductoService
- `test_rol_service.py` - Tests de RolService

**Objetivo**: Verificar reglas de negocio con **mock de repositorios**.

### Capa 4: API Controllers (2 archivos)
- `test_productos_controller.py` - Tests de ProductosController
- `test_roles_controller.py` - Tests de RolesController

**Objetivo**: Probar endpoints HTTP con **mock de servicios** usando `TestClient`.

## Configuración

### pytest.ini
```ini
[pytest]
pythonpath = . src
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

### Fixtures Globales (conftest.py)
- `test_client` - FastAPI TestClient
- `mock_db_session` - Mock de sesión de BD (sync)
- `async_mock_db_session` - Mock de sesión de BD (async)
- `cleanup_app` - Limpia dependency_overrides

## Ejecutar Tests

### Tests Unitarios (sin backend)

Los tests unitarios **NO requieren** que el backend esté corriendo:

```bash
# Todos los tests unitarios
pytest tests/unit/
```

### Con cobertura
```bash
pytest tests/unit/ --cov=src --cov-report=term-missing
```

### Por capa específica
```bash
pytest tests/unit/models/
pytest tests/unit/repositories/
pytest tests/unit/business_logic/
pytest tests/unit/api/
```

---

### Tests QA (requieren backend corriendo) ⚠️

Los tests QA **SÍ requieren** que el backend esté corriendo en el puerto especificado.

#### Paso 1: Iniciar el Backend

**Terminal 1:**
```bash
cd back-dp2
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python -m uvicorn src.main:app --reload --port 8000
```

Verifica que el servidor esté corriendo en: http://localhost:8000/docs

#### Paso 2: Ejecutar Tests QA

**Terminal 2:**
```bash
cd back-dp2
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Opción A: Python (RECOMENDADO - multiplataforma)
python tests/qa/test_cu05_validaciones_errores.py

# Opción B: BAT (solo Windows, requiere curl)
tests\qa\test_cu05_validaciones_errores.bat

# Opción C: Bash (Linux/Mac o Git Bash)
bash tests/qa/test_cu05_validaciones_errores.sh
```

#### Opciones Avanzadas para Tests QA

```bash
# Puerto personalizado
python tests/qa/test_cu05_validaciones_errores.py --port 8001

# URL completa
python tests/qa/test_cu05_validaciones_errores.py --url http://localhost:8001

# Modo verbose (muestra respuestas en fallos)
python tests/qa/test_cu05_validaciones_errores.py --verbose

# Ver todas las opciones
python tests/qa/test_cu05_validaciones_errores.py --help
```

**Nota:** Ver `tests/qa/GUIA_EJECUCION_TESTS_CU05.md` para más detalles.

---

### Un archivo específico
```bash
pytest tests/unit/models/menu/test_producto_model.py
```

### Con verbose
```bash
pytest -v
pytest -vv  # Más detalle
```

## Principios de Testing

### 1. Aislamiento con Mocks
Cada capa se prueba de forma aislada usando mocks de sus dependencias:
- **Models**: Sin mocks (son POJO)
- **Repositories**: Mock de `db_session`
- **Services**: Mock de `repositories`
- **Controllers**: Mock de `services` con `dependency_overrides`

### 2. Async/Await
Todos los tests async usan el decorator `@pytest.mark.asyncio`.

### 3. Fixtures
Reutilizar fixtures de `conftest.py` para evitar código duplicado.

### 4. Cleanup
Usar fixture `cleanup_app` para limpiar `dependency_overrides` después de cada test.

## Ejemplo de Test por Capa

### Capa 1 - Model (sin mocks)
```python
def test_producto_model_creation():
    producto = ProductoModel(
        id_producto=1,
        nombre="Pizza",
        precio_base=12.50
    )
    assert producto.nombre == "Pizza"
```

### Capa 2 - Repository (mock db_session)
```python
@pytest.mark.asyncio
async def test_get_by_id(mock_db_session):
    repo = ProductoRepository()
    resultado = await repo.get_by_id(mock_db_session, 1)
    mock_db_session.execute.assert_called_once()
```

### Capa 3 - Service (mock repository)
```python
@pytest.mark.asyncio
async def test_create_product():
    with patch.object(ProductoService, '__init__', lambda x: None):
        service = ProductoService()
        service.producto_repo = MagicMock()
        service.producto_repo.create = AsyncMock(...)

        resultado = await service.create_product(...)
        service.producto_repo.create.assert_called_once()
```

### Capa 4 - Controller (mock service)
```python
def test_create_product(cleanup_app):
    mock_service = AsyncMock()
    mock_service.create_product = AsyncMock(return_value={...})

    with patch('src.api.controllers.productos_controller.producto_service', mock_service):
        response = client.post("/api/v1/productos/", json={...})
        assert response.status_code == 201
```

## Cobertura Objetivo

- **Models**: 100% (son simples)
- **Repositories**: 80%+
- **Business Logic**: 90%+
- **Controllers**: 85%+

## Próximos Pasos

1. Agregar más tests unitarios para módulos pendientes:
   - Pedidos, Pagos, Mesas
   - Validators, Exceptions

2. Implementar tests de integración:
   - Pruebas con base de datos real (SQLite en memoria)
   - Flujos completos de negocio

3. Implementar tests E2E:
   - Escenarios completos de usuario
   - Tests con Docker

4. Integrar con CI/CD:
   - GitHub Actions para ejecutar tests en cada PR
   - Reportes de cobertura automáticos

## Dependencias de Testing

```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-mock==3.12.0
pytest-cov==4.1.0
```
