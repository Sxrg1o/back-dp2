# Makefile para back-dp2
# Compatible con Conda y venv

.PHONY: help setup setup-conda setup-venv test test-cov test-unit test-integration run clean lint format

# Variables
PYTHON := python
PYTEST := pytest
UVICORN := uvicorn
APP_MODULE := src.main:app

help:
	@echo "Comandos disponibles:"
	@echo "  make setup         - Detecta y configura entorno (Conda o venv)"
	@echo "  make setup-conda   - Configura entorno Conda"
	@echo "  make setup-venv    - Configura entorno venv"
	@echo "  make test          - Ejecuta todos los tests"
	@echo "  make test-cov      - Ejecuta tests con cobertura"
	@echo "  make test-unit     - Ejecuta solo tests unitarios"
	@echo "  make test-integration - Ejecuta solo tests de integración"
	@echo "  make run           - Inicia servidor de desarrollo"
	@echo "  make run-prod      - Inicia servidor en modo producción"
	@echo "  make clean         - Limpia archivos temporales"
	@echo "  make lint          - Ejecuta linters (flake8, mypy)"
	@echo "  make format        - Formatea código (black, isort)"

setup:
	@echo "Detectando entorno disponible..."
	@if command -v conda > /dev/null 2>&1; then \
		echo "Conda detectado. Ejecuta: make setup-conda"; \
	else \
		echo "Conda no detectado. Ejecuta: make setup-venv"; \
	fi

setup-conda:
	@echo "Configurando entorno Conda..."
	conda env create -f environment.yml
	@echo "✓ Entorno creado. Activa con: conda activate back-dp2"

setup-venv:
	@echo "Configurando entorno venv..."
	$(PYTHON) -m venv venv
	@echo "Activando entorno e instalando dependencias..."
	@if [ -f "venv/bin/activate" ]; then \
		. venv/bin/activate && pip install -r requirements.txt; \
	else \
		venv\Scripts\activate && pip install -r requirements.txt; \
	fi
	@echo "✓ Entorno creado. Activa con: source venv/bin/activate (Linux/Mac) o venv\Scripts\activate (Windows)"

test:
	@echo "Ejecutando tests..."
	$(PYTEST) -v

test-cov:
	@echo "Ejecutando tests con cobertura..."
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html
	@echo "Reporte HTML generado en: htmlcov/index.html"

test-unit:
	@echo "Ejecutando tests unitarios..."
	$(PYTEST) tests/unit/ -v

test-integration:
	@echo "Ejecutando tests de integración..."
	$(PYTEST) tests/integration/ -v

run:
	@echo "Iniciando servidor de desarrollo..."
	$(UVICORN) $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

run-prod:
	@echo "Iniciando servidor en modo producción..."
	$(UVICORN) $(APP_MODULE) --host 0.0.0.0 --port 8000 --workers 4

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "✓ Limpieza completada"

lint:
	@echo "Ejecutando linters..."
	@$(PYTHON) -m flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics || echo "flake8 no instalado"
	@$(PYTHON) -m mypy src/ || echo "mypy no instalado"

format:
	@echo "Formateando código..."
	@$(PYTHON) -m black src/ tests/ || echo "black no instalado - pip install black"
	@$(PYTHON) -m isort src/ tests/ || echo "isort no instalado - pip install isort"
	@echo "✓ Código formateado"

# Para Windows PowerShell, crear versión .ps1
install-dev-tools:
	@echo "Instalando herramientas de desarrollo..."
	pip install black isort flake8 mypy
	@echo "✓ Herramientas instaladas"
