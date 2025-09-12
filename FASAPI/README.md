# Restaurant Platform API - Backend Archetype

Este es un arquetipo de backend basado en **Python 3.11 + FastAPI** para la plataforma de atención de restaurantes. Proporciona una base reutilizable y consistente para el desarrollo de servicios REST con separación de capas, observabilidad, seguridad y capacidades de integración externa.

## 🚀 Características

- **Arquitectura en capas**: Routers, Services, Repositories, Models, Schemas y Mappers
- **Seguridad integrada**: JWT, control de acceso basado en roles
- **Observabilidad**: Logs estructurados, trazabilidad, métricas
- **Integraciones externas**: Web scraping (BeautifulSoup) y RPA (Playwright/Selenium)
- **Calidad de código**: pytest, black, ruff, mypy, pre-commit
- **Containerización**: Docker ready
- **Migraciones**: Alembic para base de datos
- **Cache**: Redis integrado
- **Jobs**: APScheduler para tareas programadas

## 📁 Estructura del Proyecto

```
FASAPI/
├── .gitignore
├── .env.example
├── Dockerfile
├── pyproject.toml
├── README.md
├── logs/
├── alembic/
├── app/
│   ├── main.py
│   ├── core/
│   ├── routers/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   ├── mappers/
│   ├── jobs/
│   ├── scheduler/
│   ├── oai/
│   ├── util/
│   ├── middlewares/
│   └── resources/
├── tests/
└── target/
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- Poetry
- PostgreSQL
- Redis

### Instalación

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd FASAPI
```

2. **Instalar dependencias**

```bash
poetry install
```

3. **Configurar variables de entorno**

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Ejecutar migraciones**

```bash
poetry run alembic upgrade head
```

5. **Inicializar base de datos con datos de prueba**

```bash
make init-db
```

6. **Ejecutar la aplicación**

```bash
make dev
```

## 🐳 Docker

```bash
# Construir imagen
docker build -t restaurant-api .

# Ejecutar contenedor
docker run -p 8000:8000 restaurant-api
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
poetry run pytest

# Con cobertura
poetry run pytest --cov=app

# Solo pruebas unitarias
poetry run pytest -m unit

# Solo pruebas de integración
poetry run pytest -m integration
```

## 🔧 Comandos Disponibles

```bash
make help          # Mostrar todos los comandos disponibles
make install       # Instalar dependencias
make dev           # Ejecutar servidor de desarrollo
make init-db       # Inicializar base de datos con datos de prueba
make test          # Ejecutar pruebas
make test-cov      # Ejecutar pruebas con cobertura
make lint          # Ejecutar linting
make format        # Formatear código
make docker-up     # Iniciar servicios con Docker
make docker-down   # Detener servicios Docker
make migrate       # Ejecutar migraciones de base de datos
```

## 🔧 Herramientas de Desarrollo

```bash
# Formatear código
poetry run black .

# Linting
poetry run ruff check .

# Type checking
poetry run mypy .

# Pre-commit hooks
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## � PProbando la API

### Opción 1: Usando Swagger UI (Recomendado)

1. Inicializar la base de datos: `make init-db`
2. Iniciar el servidor: `make dev`
3. Abrir el navegador en: `http://localhost:8000/docs`
4. Probar los endpoints disponibles:

#### Endpoints de Menú:

- **GET** `/api/v1/menu/` - Obtener menú completo
- **GET** `/api/v1/menu/categories` - Obtener menú por categorías
- **GET** `/api/v1/menu/search?query=tomate` - Buscar elementos del menú
- **GET** `/api/v1/menu/statistics` - Obtener estadísticas del menú
- **GET** `/api/v1/menu/nutrition` - Obtener resumen nutricional

### Opción 2: Usando curl

```bash
# Obtener menú completo
curl http://localhost:8000/api/v1/menu/

# Buscar elementos
curl "http://localhost:8000/api/v1/menu/search?query=tomate"

# Obtener estadísticas del menú
curl http://localhost:8000/api/v1/menu/statistics

# Health check
curl http://localhost:8000/health
```

### Datos de Prueba

La base de datos de desarrollo incluye datos de ejemplo:

- **Items**: Tomate, Pollo
- **Ingredientes**: Cebolla
- **Platos**: Ensalada César
- **Bebidas**: Agua Mineral

Puedes usar estos datos para probar los endpoints de la API.

## 📚 API Documentation

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🏗️ Arquitectura

### Principios

- **Separación de responsabilidades (SoC)**
- **Inversión de dependencias**
- **Domain Driven Design (DDD) ligero**
- **Clean/Hexagonal Architecture pragmático**

### Capas

1. **Routers**: Endpoints HTTP, validación de entrada
2. **Services**: Lógica de negocio y casos de uso
3. **Repositories**: Acceso a datos y persistencia
4. **Models**: Entidades de dominio (SQLAlchemy)
5. **Schemas**: DTOs de entrada/salida (Pydantic)
6. **Mappers**: Conversión entre models y schemas

## 🔌 Integraciones Externas

### Web Scraping

Para sitios con contenido estático:

```python
from app.oai.sources.scraper import WebScraper

scraper = WebScraper()
data = await scraper.scrape_menu("https://restaurant.com/menu")
```

### RPA (Robotic Process Automation)

Para sitios con contenido dinámico o que requieren interacción:

```python
from app.oai.sources.rpa import RPABot

bot = RPABot()
data = await bot.login_and_scrape("https://restaurant.com/admin")
```

## 📊 Monitoreo y Logs

Los logs se generan en formato estructurado y se almacenan en:

- Desarrollo: `logs/application.log`
- Producción: stdout (para agregación por contenedor)

## 🔐 Seguridad

- **JWT Tokens** para autenticación
- **Control de acceso basado en roles**
- **Validación de entrada** con Pydantic
- **Rate limiting** configurable
- **CORS** configurado

## 📈 Performance

- **Cache Redis** para datos frecuentemente accedidos
- **Connection pooling** para base de datos
- **Async/await** para operaciones I/O
- **Paginación** automática en listados

## 🚀 Despliegue

### Variables de Entorno de Producción

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-production-secret
DEBUG=False
LOG_LEVEL=INFO
```

### Health Checks

- **Endpoint**: `GET /health`
- **Database**: Verificación de conectividad
- **Redis**: Verificación de cache
- **External APIs**: Estado de integraciones

## 🤝 Contribución

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte y preguntas:

- Email: dev@restaurant-platform.com
- Issues: [GitHub Issues](https://github.com/your-org/restaurant-api/issues)
