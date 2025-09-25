#!/bin/bash

# Script para iniciar la aplicación con Docker

echo "🐳 Iniciando Menu API con Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [opción]"
    echo ""
    echo "Opciones:"
    echo "  dev     Iniciar en modo desarrollo (con hot reload)"
    echo "  prod    Iniciar en modo producción"
    echo "  build   Construir la imagen Docker"
    echo "  stop    Detener los contenedores"
    echo "  logs    Mostrar logs de los contenedores"
    echo "  clean   Limpiar contenedores e imágenes"
    echo "  help    Mostrar esta ayuda"
}

# Función para limpiar
clean_docker() {
    echo "🧹 Limpiando contenedores e imágenes..."
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
    echo "✅ Limpieza completada"
}

# Procesar argumentos
case "${1:-dev}" in
    "dev")
        echo "🚀 Iniciando en modo desarrollo..."
        docker-compose up --build
        ;;
    "prod")
        echo "🚀 Iniciando en modo producción..."
        docker-compose -f docker-compose.prod.yml up --build -d
        echo "✅ Aplicación iniciada en http://localhost:8000"
        echo "📚 Documentación disponible en http://localhost:8000/docs"
        ;;
    "build")
        echo "🔨 Construyendo imagen Docker..."
        docker-compose build
        ;;
    "stop")
        echo "🛑 Deteniendo contenedores..."
        docker-compose down
        ;;
    "logs")
        echo "📋 Mostrando logs..."
        docker-compose logs -f
        ;;
    "clean")
        clean_docker
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Opción no válida: $1"
        show_help
        exit 1
        ;;
esac
