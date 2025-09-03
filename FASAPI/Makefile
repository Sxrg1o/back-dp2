# Makefile for Restaurant Platform API

.PHONY: help install dev test lint format clean docker-build docker-up docker-down migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-up   - Start services with Docker Compose"
	@echo "  docker-down - Stop Docker Compose services"
	@echo "  migrate     - Run database migrations"

# Install dependencies
install:
	poetry install

# Run development server
dev:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	poetry run pytest

# Run tests with coverage
test-cov:
	poetry run pytest --cov=app --cov-report=html --cov-report=term

# Run linting
lint:
	poetry run ruff check .
	poetry run mypy .

# Format code
format:
	poetry run black .
	poetry run ruff check . --fix

# Clean build artifacts
clean:
	rm -rf target/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Docker commands
docker-build:
	docker build -t restaurant-api .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Database migrations
migrate:
	poetry run alembic upgrade head

# Create new migration
migration:
	poetry run alembic revision --autogenerate -m "$(msg)"

# Install pre-commit hooks
pre-commit:
	poetry run pre-commit install

# Run pre-commit on all files
pre-commit-all:
	poetry run pre-commit run --all-files