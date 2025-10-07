-----

## 1\. Estructura de Carpetas de Pruebas

Estructura del directorio test

```plaintext
project/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   └── productos_controller.py
│   │   └── schemas/
│   │       └── producto_schema.py
│   ├── business_logic/
│   │   ├── menu/
│   │   │   └── producto_service.py
│   │   └── validators/
│   │       └── producto_validators.py
│   ├── models/
│   │   └── menu/
│   │       └── producto_model.py
│   └── repositories/
│       └── menu/
│           └── producto_repository.py
│
└── tests/
    ├── conftest.py          # Fixtures globales para las pruebas
    ├── __init__.py
    ├── e2e/
    ├── integration/
    └── unit/                # Aquí se centran las pruebas unitarias
        ├── __init__.py
        ├── api/
        │   └── controllers/
        │       └── test_productos_controller.py
        ├── business_logic/
        │   ├── menu/
        │   │   └── test_producto_service.py
        │   └── validators/
        │       └── test_producto_validators.py
        ├── models/
        │   └── menu/
        │       └── test_producto_model.py
        └── repositories/
            └── menu/
                └── test_producto_repository.py
```

-----

## 2\. El Flujo de Pruebas por Capas

El objetivo de las pruebas unitarias es **aislar** un componente (una función, una clase) y probar su lógica sin dependencias externas como bases de datos o APIs. Para lograr esto, usaremos intensivamente el concepto de **"Mocks"** (simulacros).


### Paso 1: Unit Testing de los `models`

  * **Objetivo**: Asegurar que los modelos de datos (ej. SQLAlchemy) se inicializan correctamente, tienen los valores por defecto esperados y cualquier método simple funciona como se espera.
  * **Aislamiento**: No se necesita ninguna dependencia externa. Son las pruebas más sencillas.
  * **Ejemplo (`tests/unit/models/menu/test_producto_model.py`):**
    ```python
    from src.models.menu.producto_model import Producto

    def test_producto_model_creation():
        """
        Verifica que un objeto Producto se crea con los atributos correctos.
        """
        producto = Producto(
            nombre="Pizza Margherita",
            descripcion="Clásica pizza con tomate y mozzarella",
            precio=12.50,
            disponible=True
        )

        assert producto.nombre == "Pizza Margherita"
        assert producto.precio == 12.50
        assert producto.disponible is True
    ```

### Paso 2: Unit Testing de los `repositories` (Adapters)

  * **Objetivo**: Probar la lógica de acceso a datos. Por ejemplo, que el método `get_by_id` ejecute una consulta específica o que `create` añada y confirme la sesión.
  * **Aislamiento**: Aquí es crucial **simular (mock) la sesión de la base de datos** (`db_session`). No queremos que la prueba se conecte a una base de datos real.
  * **Ejemplo (`tests/unit/repositories/menu/test_producto_repository.py`):**
    ```python
    from unittest.mock import MagicMock
    from src.repositories.menu.producto_repository import ProductoRepository
    from src.models.menu.producto_model import Producto

    def test_get_producto_by_id():
        """
        Verifica que el repositorio llama a los métodos correctos de la sesión de BD.
        """
        # 1. Creamos un mock para la sesión de la base de datos
        mock_db_session = MagicMock()
        
        # 2. Configuramos el mock para que devuelva un producto de prueba
        producto_esperado = Producto(id=1, nombre="Pizza Test")
        mock_db_session.query.return_value.filter.return_value.first.return_value = producto_esperado
        
        # 3. Instanciamos el repositorio con el mock
        repo = ProductoRepository(db_session=mock_db_session)
        
        # 4. Ejecutamos el método a probar
        resultado = repo.get_by_id(1)
        
        # 5. Verificamos que se llamó al método correcto y que el resultado es el esperado
        mock_db_session.query.assert_called_with(Producto)
        assert resultado.id == 1
        assert resultado.nombre == "Pizza Test"
    ```

### Paso 3: Unit Testing de la `business_logic` (Services)

  * **Objetivo**: Verificar la lógica de negocio. Por ejemplo, que no se pueda crear un producto con precio negativo, o que al actualizar un producto se llame al repositorio correspondiente.
  * **Aislamiento**: **Simulamos (mock) los repositorios** de los que depende el servicio. La prueba no debe saber cómo funciona el repositorio, solo qué se espera que devuelva.
  * **Ejemplo (`tests/unit/business_logic/menu/test_producto_service.py`):**
    ```python
    from unittest.mock import MagicMock
    import pytest
    from src.business_logic.menu.producto_service import ProductoService
    from src.business_logic.exceptions.menu_exceptions import ProductoInvalidoError

    def test_create_producto_precio_negativo():
        """
        Verifica que el servicio lanza una excepción si el precio es negativo.
        """
        # 1. Creamos un mock para el repositorio (no se usará, pero es una dependencia)
        mock_producto_repo = MagicMock()
        
        # 2. Instanciamos el servicio con el mock
        service = ProductoService(producto_repository=mock_producto_repo)
        
        # 3. Verificamos que se lanza la excepción correcta
        with pytest.raises(ProductoInvalidoError, match="El precio no puede ser negativo"):
            service.create_producto(
                nombre="Producto Malo", 
                precio=-10.0
            )

    def test_create_producto_llama_al_repositorio():
        """
        Verifica que el servicio llama al método 'create' del repositorio.
        """
        mock_producto_repo = MagicMock()
        service = ProductoService(producto_repository=mock_producto_repo)

        service.create_producto(nombre="Buen Producto", precio=20.0)

        # Verificamos que el método 'create' del repositorio fue llamado una vez
        mock_producto_repo.create.assert_called_once()
    ```

### Paso 4: Unit Testing de los `controllers` (Endpoints)

  * **Objetivo**: Asegurar que el endpoint procesa correctamente las solicitudes HTTP, llama al servicio adecuado y devuelve el código de estado y la respuesta esperados.
  * **Aislamiento**: **Simulamos (mock) los servicios** de lógica de negocio. El controlador no debe ejecutar la lógica de negocio real, solo delegarla. Usaremos el `TestClient` de FastAPI.
  * **Ejemplo (`tests/unit/api/controllers/test_productos_controller.py`):**
    ```python
    from fastapi.testclient import TestClient
    from unittest.mock import MagicMock
    from src.main import app # Importas tu app de FastAPI

    # Creamos un cliente de prueba
    client = TestClient(app)

    def test_get_producto_success():
        """
        Verifica que el endpoint GET /productos/{id} funciona correctamente.
        """
        # 1. Creamos un mock del servicio de productos
        mock_producto_service = MagicMock()
        mock_producto_service.get_producto_by_id.return_value = {
            "id": 1, 
            "nombre": "Pizza desde el mock", 
            "precio": 15.0
        }
        
        # 2. Sobrescribimos la dependencia en la app de FastAPI para usar nuestro mock
        # Esto es clave para el aislamiento
        from src.core.dependencies import get_producto_service
        app.dependency_overrides[get_producto_service] = lambda: mock_producto_service
        
        # 3. Realizamos la llamada HTTP al endpoint
        response = client.get("/api/v1/productos/1")
        
        # 4. Verificamos la respuesta
        assert response.status_code == 200
        assert response.json() == {"id": 1, "nombre": "Pizza desde el mock", "precio": 15.0}
        
        # 5. Limpiamos la sobrescritura para no afectar otras pruebas
        app.dependency_overrides = {}
    ```

-----

## 3\. Herramientas y Configuración

1.  **Instalación**: Asegúrate de tener `pytest` y `pytest-mock` en tu `requirements.txt`.
    ```bash
    pip install pytest pytest-mock "fastapi[all]"
    ```
2.  **Configuración (`pytest.ini` o `pyproject.toml`)**: Es útil crear un archivo `pytest.ini` en la raíz del proyecto para que `pytest` sepa dónde encontrar tu código fuente.
    ```ini
    [pytest]
    pythonpath = . src
    testpaths = tests
    ```
3.  **Fixtures (`conftest.py`)**: Para evitar repetir código (como la creación de mocks), puedes usar fixtures de `pytest` en el archivo `tests/conftest.py`. Por ejemplo, puedes crear un fixture que provea un `TestClient` para todas las pruebas de controladores.

-----

## 4\. Ejecución y Automatización

  * **Ejecutar todas las pruebas**: Desde la raíz de tu proyecto, simplemente ejecuta:

    ```bash
    pytest
    ```

  * **Obtener cobertura de pruebas**: Para ver qué porcentaje de tu código está cubierto por las pruebas, usa `pytest-cov`.

    ```bash
    pytest --cov=src --cov-report=term-missing
    ```

  * **Integración Continua (CI)**: En tu archivo `.github/workflows/deploy_backend.yml`, añade un paso **antes** del despliegue para ejecutar las pruebas. Si las pruebas fallan, el flujo de trabajo se detendrá y no se desplegará código roto.

-----

## 5\. Estructura de Docstrings para Pruebas

Cada función de prueba (`test_*`) debe incluir un docstring estructurado con el siguiente formato para facilitar la comprensión y mantenimiento:

```python
def test_metodo_caso():
    """
    Descripción breve de lo que verifica la prueba.

    PRECONDICIONES:
        - Lista de requisitos previos o estado inicial necesario para la prueba.
        - Mocks, fixtures o datos requeridos antes de ejecutar la prueba.

    PROCESO:
        - Pasos detallados de lo que hace la prueba.
        - Configuración de mocks o simulaciones.
        - Llamadas a métodos o funciones que se están probando.
        - Verificaciones o aserciones que se realizan.

    POSTCONDICIONES:
        - Resultados esperados después de que la prueba se ejecute.
        - Estado del sistema después de la ejecución.
        - Efectos secundarios verificables.
    """
```

### Ejemplo de docstring en una prueba de repositorio:

```python
@pytest.mark.asyncio
async def test_get_rol_by_id():
    """
    Verifica que el método get_by_id recupera correctamente un rol por su ID.

    PRECONDICIONES:
        - Se debe tener una instancia mock de AsyncSession.
        - Se debe tener un UUID válido para buscar.

    PROCESO:
        - Configurar el mock para simular la respuesta de la base de datos.
        - Llamar al método get_by_id con un ID específico.
        - Verificar que se ejecute la consulta correcta y se retorne el resultado esperado.

    POSTCONDICIONES:
        - El método debe retornar un objeto RolModel cuando existe el rol.
        - El método debe retornar None cuando no existe el rol.
        - La consulta SQL debe formarse correctamente.
    """
    # Implementación de la prueba...
```

Este formato de documentación ayuda a:
1. **Clarificar el propósito** de cada prueba.
2. **Documentar las dependencias** necesarias para ejecutar la prueba.
3. **Explicar el proceso** que sigue la prueba, facilitando su comprensión.
4. **Definir las expectativas** sobre los resultados y efectos de la prueba.
5. **Facilitar el mantenimiento** y actualización de las pruebas a lo largo del tiempo.
