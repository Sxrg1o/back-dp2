# 🐳 Docker Compose - Microservicios Domótica

## Descripción

Este archivo `docker-compose.yml` permite ejecutar todos los microservicios de Domótica de manera coordinada usando Docker.

## 🚀 Servicios Incluidos

### 👤 Users MS (Microservicio de Usuarios)
- **Puerto**: 8001
- **Documentación**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **Descripción**: Gestión de usuarios del sistema

### 🍽️ Menu MS (Microservicio de Menú y Carta)
- **Puerto**: 8002
- **Documentación**: http://localhost:8002/docs
- **Health Check**: http://localhost:8002/health
- **Descripción**: Gestión de menú, platos, bebidas e ingredientes

## 🛠️ Comandos Principales

### Iniciar todos los servicios
```bash
# Opción 1: Script automático (Windows)
run_all_services.bat

# Opción 2: Comando directo
docker-compose up -d
```

### Detener todos los servicios
```bash
# Opción 1: Script automático (Windows)
stop_all_services.bat

# Opción 2: Comando directo
docker-compose down
```

### Ver logs en tiempo real
```bash
docker-compose logs -f
```

### Ver estado de los servicios
```bash
docker-compose ps
```

### Reiniciar un servicio específico
```bash
docker-compose restart users-ms
docker-compose restart menu-ms
```

### Reconstruir imágenes
```bash
docker-compose build --no-cache
```

## 📋 Requisitos Previos

### 1. Docker Desktop
- Descargar desde: https://docker.com
- Instalar y configurar Docker Desktop
- Verificar instalación: `docker --version`

### 2. Docker Compose
- Incluido con Docker Desktop
- Verificar instalación: `docker-compose --version`

## 🔧 Configuración

### Variables de Entorno
Los servicios se configuran automáticamente con las siguientes variables:

**Users MS:**
- `PORT=8000`
- `HOST=0.0.0.0`
- `RELOAD=true`

**Menu MS:**
- `PORT=8002`
- `HOST=0.0.0.0`
- `RELOAD=true`
- `DATABASE_URL=sqlite:///./menu.db`

### Volúmenes
- **Código fuente**: Montado para desarrollo en tiempo real
- **Base de datos**: Persistente para el microservicio de menú
- **Cache**: Excluido para evitar conflictos

### Redes
- **domotica-network**: Red interna para comunicación entre servicios

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd back-dp2
```

### 2. Ejecutar servicios
```bash
# Windows
run_all_services.bat

# Linux/Mac
docker-compose up -d
```

### 3. Verificar servicios
- Abrir http://localhost:8001/docs (Users MS)
- Abrir http://localhost:8002/docs (Menu MS)

## 🔍 Monitoreo y Debugging

### Ver logs de un servicio específico
```bash
docker-compose logs -f users-ms
docker-compose logs -f menu-ms
```

### Entrar a un contenedor
```bash
docker-compose exec users-ms bash
docker-compose exec menu-ms bash
```

### Ver uso de recursos
```bash
docker stats
```

### Verificar health checks
```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
```

## 🗄️ Base de Datos

### SQLite (Desarrollo)
- **Ubicación**: Volumen `menu-db-data`
- **Archivo**: `menu.db`
- **Persistencia**: Los datos se mantienen entre reinicios

### PostgreSQL (Producción)
Para usar PostgreSQL en producción, descomenta la sección correspondiente en `docker-compose.yml`:

```yaml
postgres:
  image: postgres:15-alpine
  container_name: domotica-postgres
  environment:
    POSTGRES_DB: domotica_db
    POSTGRES_USER: domotica_user
    POSTGRES_PASSWORD: domotica_password
  volumes:
    - postgres_data:/var/lib/postgresql/data
  ports:
    - "5432:5432"
  restart: unless-stopped
  networks:
    - domotica-network
```

## 🧹 Limpieza

### Detener y eliminar todo
```bash
docker-compose down -v
docker system prune -f
```

### Eliminar solo volúmenes
```bash
docker-compose down -v
```

### Eliminar imágenes
```bash
docker-compose down --rmi all
```

## 🔧 Desarrollo

### Modo desarrollo
Los servicios están configurados con `--reload` para desarrollo en tiempo real. Los cambios en el código se reflejan automáticamente.

### Estructura de archivos
```
back-dp2/
├── docker-compose.yml          # Configuración principal
├── run_all_services.bat        # Script de inicio (Windows)
├── stop_all_services.bat       # Script de parada (Windows)
├── users-ms/                   # Microservicio de usuarios
│   ├── Dockerfile
│   ├── main.py
│   └── ...
└── menu-ms/                    # Microservicio de menú
    ├── Dockerfile
    ├── main.py
    └── ...
```

## 🐛 Solución de Problemas

### Puerto ya en uso
```bash
# Ver qué proceso usa el puerto
netstat -ano | findstr :8001
netstat -ano | findstr :8002

# Detener proceso
taskkill /PID <PID> /F
```

### Error de permisos
```bash
# En Windows, ejecutar como administrador
# En Linux/Mac, agregar usuario al grupo docker
sudo usermod -aG docker $USER
```

### Limpiar Docker completamente
```bash
docker system prune -a --volumes
```

## 📚 Enlaces Útiles

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [SQLAlchemy with Docker](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)

---

**¡Disfruta desarrollando con Docker! 🐳✨**

