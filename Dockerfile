FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copiar los requisitos de ambos microservicios
COPY users-ms/requirements.txt /app/users-ms-requirements.txt
COPY menu-ms/requirements.txt /app/menu-ms-requirements.txt

# Instalar todas las dependencias
RUN pip install --no-cache-dir -r /app/users-ms-requirements.txt
RUN pip install --no-cache-dir -r /app/menu-ms-requirements.txt

# Copiar código fuente de ambos microservicios
COPY users-ms/ /app/users-ms/
COPY menu-ms/ /app/menu-ms/

# Crear directorios para datos persistentes
RUN mkdir -p /app/menu-ms/data

# Exponer puertos
EXPOSE 8001 8002

# Comando de inicio para supervisord
CMD ["/usr/bin/supervisord"]