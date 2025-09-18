# 🍽️ Microservicio de Menú y Carta - Domótica

## Descripción

El microservicio de **Menú y Carta** es parte del sistema de gestión del restaurante Domótica. Gestiona todos los elementos relacionados con los productos alimenticios, incluyendo platos, bebidas, ingredientes y sus características nutricionales.

## 🏗️ Arquitectura

Este microservicio sigue los principios de **Arquitectura Hexagonal (Clean Architecture)**:

```
menu-ms/
├── domain/                 # Capa de Dominio
│   ├── entities/          # Entidades de negocio
│   ├── repositories/      # Interfaces de repositorios
│   └── use_cases/         # Casos de uso
├── application/           # Capa de Aplicación
│   └── services/          # Servicios de aplicación
├── infrastructure/        # Capa de Infraestructura
│   ├── models/           # Modelos de base de datos
│   ├── repositories/     # Implementaciones de repositorios
│   ├── handlers/         # Endpoints REST
│   └── db.py            # Configuración de base de datos
├── tests/                # Tests unitarios e integración
└── main.py              # Punto de entrada de la aplicación
```

## 🚀 Características Principales

### ✅ Gestión Completa de Menú
- **Platos**: Entradas, platos principales y postres
- **Bebidas**: Alcohólicas y no alcohólicas
- **Ingredientes**: Control de inventario detallado

### ✅ Información Nutricional
- Valores nutricionales completos (calorías, proteínas, azúcares)
- Sistema de etiquetas para restricciones dietéticas
- Clasificación por tipos y categorías

### ✅ Control de Stock
- Gestión de disponibilidad por ítem
- Control de inventario a nivel de ingrediente
- Alertas de stock bajo

### ✅ Búsqueda y Filtros
- Búsqueda por nombre o descripción
- Filtros por precio, tipo, etiquetas
- Clasificación por categorías

## 📋 Entidades del Dominio

### Item (Clase Base)
- `id`: Identificador único
- `descripcion`: Descripción del ítem
- `precio`: Precio en el menú
- `valor_nutricional`: Información nutricional
- `tiempo_preparacion`: Tiempo de preparación
- `disponible`: Estado de disponibilidad
- `unidades_disponibles`: Stock disponible
- `kcal`, `calorias`, `proteinas`, `azucares`: Valores nutricionales
- `etiquetas`: Lista de etiquetas especiales

### Plato (Hereda de Item)
- `peso`: Peso total en gramos
- `tipo`: Clasificación (ENTRADA, FONDO, POSTRE)

### Bebida (Hereda de Item)
- `litros`: Cantidad en litros
- `alcoholico`: Indica si contiene alcohol

### Ingrediente
- `nombre`: Nombre del ingrediente
- `stock`: Cantidad disponible
- `peso`: Peso por unidad
- `tipo`: Clasificación (VERDURA, CARNE, FRUTA)

## 🏷️ Sistema de Etiquetas

### EtiquetaItem
- `SIN_GLUTEN`, `CON_GLUTEN`
- `PICANTE`, `SALADO`
- `CALIENTE`, `FRIO`
- `ACIDO`, `AGRIO`
- `VEGANO`

### EtiquetaPlato
- `ENTRADA`: Platos de aperitivo
- `FONDO`: Platos principales
- `POSTRE`: Platos dulces

### EtiquetaIngrediente
- `VERDURA`: Ingredientes vegetales
- `CARNE`: Productos cárnicos
- `FRUTA`: Ingredientes frutales

## 🛠️ Instalación y Configuración

### Requisitos
- Python 3.8+
- SQLite (desarrollo) / PostgreSQL (producción)

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd menu-ms

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración
```bash
# Variables de entorno (opcional)
export DATABASE_URL="sqlite:///./menu.db"
export PORT=8002
export HOST="0.0.0.0"
export RELOAD="true"
```

### Ejecución
```bash
# Desarrollo
python main.py

# O con uvicorn directamente
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

## 📚 API Documentation

Una vez ejecutado el servidor, la documentación interactiva estará disponible en:

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

## 🔗 Endpoints Principales

### Ítems del Menú
- `GET /items/` - Obtener todos los ítems
- `POST /items/platos` - Crear plato
- `POST /items/bebidas` - Crear bebida
- `GET /items/{id}` - Obtener ítem específico
- `PUT /items/platos/{id}` - Actualizar plato
- `PUT /items/bebidas/{id}` - Actualizar bebida
- `DELETE /items/{id}` - Eliminar ítem

### Búsqueda y Filtros
- `GET /items/search?q={term}` - Buscar ítems
- `GET /items/filter/price?min={min}&max={max}` - Filtrar por precio
- `GET /items/filter/etiqueta/{etiqueta}` - Filtrar por etiqueta

### Platos Específicos
- `GET /items/platos/entradas` - Obtener entradas
- `GET /items/platos/principales` - Obtener platos principales
- `GET /items/platos/postres` - Obtener postres

### Bebidas Específicas
- `GET /items/bebidas/alcoholicas` - Obtener bebidas alcohólicas
- `GET /items/bebidas/no-alcoholicas` - Obtener bebidas no alcohólicas
- `GET /items/bebidas/filter/volume?min={min}&max={max}` - Filtrar por volumen

### Ingredientes
- `GET /ingredientes/` - Obtener todos los ingredientes
- `POST /ingredientes/` - Crear ingrediente
- `GET /ingredientes/{id}` - Obtener ingrediente específico
- `PUT /ingredientes/{id}` - Actualizar ingrediente
- `DELETE /ingredientes/{id}` - Eliminar ingrediente

### Gestión de Stock
- `PATCH /items/{id}/stock` - Actualizar stock de ítem
- `PATCH /ingredientes/{id}/stock` - Actualizar stock de ingrediente
- `PATCH /ingredientes/{id}/reduce-stock` - Reducir stock de ingrediente
- `GET /ingredientes/low-stock` - Obtener ingredientes con stock bajo

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_entities.py
pytest tests/test_use_cases.py
pytest tests/test_integration.py

# Con cobertura
pytest --cov=domain --cov=application --cov=infrastructure
```

### Tipos de Tests
- **Tests Unitarios**: Entidades y casos de uso
- **Tests de Integración**: Servicios y repositorios
- **Tests de API**: Endpoints REST (próximamente)

## 🐳 Docker

### Dockerfile incluido
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8002
CMD ["python", "main.py"]
```

### Construir imagen
```bash
docker build -t menu-ms .
docker run -p 8002:8002 menu-ms
```

## 🔧 Desarrollo

### Estructura de Commits
```
feat: nueva funcionalidad
fix: corrección de bug
docs: documentación
test: tests
refactor: refactorización
```

### Linting y Formateo
```bash
# Formatear código
black .

# Ordenar imports
isort .

# Linting
flake8 .
```

## 📊 Monitoreo

### Health Check
```bash
curl http://localhost:8002/health
```

### Información del Servicio
```bash
curl http://localhost:8002/info
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Equipo

- **Desarrollo**: Equipo de Desarrollo Domótica
- **Email**: dev@domotica.com

## 🔗 Enlaces Útiles

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Arquitectura Hexagonal](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**¡Disfruta desarrollando con el microservicio de Menú y Carta! 🍽️✨**
