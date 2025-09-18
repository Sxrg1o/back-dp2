FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copiar los requisitos de ambos microservicios
COPY users-ms/requirements.txt /app/users-ms-requirements.txt
COPY menu-ms/requirements.txt /app/menu-ms-requirements.txt

# Instalar todas las dependencias
RUN pip install --no-cache-dir -r /app/users-ms-requirements.txt
RUN pip install --no-cache-dir -r /app/menu-ms-requirements.txt

# Copiar configuración
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar código fuente de ambos microservicios
COPY users-ms/ /app/users-ms/
COPY menu-ms/ /app/menu-ms/

# Crear directorios para datos persistentes
RUN mkdir -p /app/menu-ms/data

# Crear directorios para logs
RUN mkdir -p /var/log

# Exponer puerto 80 para Nginx que funcionará como proxy reverso
EXPOSE 80

# Comando de inicio para supervisord con configuración explícita
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]