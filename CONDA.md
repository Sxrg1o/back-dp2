# Guía de Conda para back-dp2

Este proyecto soporta **Conda** como gestor de entornos alternativo a `venv`.

## Instalación inicial

### 1. Instalar Miniconda/Anaconda

**Windows:**
```powershell
# Descargar e instalar desde:
# https://docs.conda.io/en/latest/miniconda.html
```

**Linux/Mac:**
```bash
# Descargar instalador
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# o para Mac: Miniconda3-latest-MacOSX-x86_64.sh

# Ejecutar instalador
bash Miniconda3-latest-Linux-x86_64.sh
```

### 2. Crear el entorno

#### Opción A: Script automático (recomendado)

**Windows:**
```powershell
.\setup-conda.ps1
```

**Linux/Mac:**
```bash
bash setup-conda.sh
```

#### Opción B: Comando manual

```bash
# Crear entorno desde environment.yml
conda env create -f environment.yml

# Activar entorno
conda activate back-dp2

# Verificar instalación
python --version
pip list
```

## Comandos útiles

### Gestión del entorno

```bash
# Activar entorno
conda activate back-dp2

# Desactivar entorno
conda deactivate

# Listar entornos
conda env list

# Eliminar entorno
conda env remove -n back-dp2

# Actualizar entorno desde environment.yml
conda env update -f environment.yml --prune
```

### Gestión de paquetes

```bash
# Instalar nuevo paquete
conda install -c conda-forge <paquete>
# o con pip dentro del entorno:
pip install <paquete>

# Listar paquetes instalados
conda list
pip list

# Exportar entorno actualizado
conda env export --from-history > environment.yml

# Exportar con versiones exactas (para reproducibilidad)
conda env export > environment-lock.yml
```

## Desarrollo

### Ejecutar la aplicación

```bash
# Activar entorno
conda activate back-dp2

# Modo desarrollo con hot-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Tests

```bash
# Activar entorno
conda activate back-dp2

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=term-missing

# Tests específicos
pytest tests/integration/api/
pytest tests/unit/
```

## CI/CD con Conda

### GitHub Actions

```yaml
name: tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: conda-incubator/setup-miniconda@v3
        with:
          environment-file: environment.yml
          activate-environment: back-dp2
          auto-activate-base: false
      
      - name: Run tests
        shell: bash -l {0}
        run: |
          conda activate back-dp2
          pytest --cov=src
```

### Docker con Conda

```dockerfile
FROM continuumio/miniconda3:latest

WORKDIR /app

# Copiar archivos de configuración
COPY environment.yml .

# Crear entorno
RUN conda env create -f environment.yml

# Activar entorno en el shell
SHELL ["conda", "run", "-n", "back-dp2", "/bin/bash", "-c"]

# Copiar código
COPY . .

# Comando de inicio
CMD ["conda", "run", "--no-capture-output", "-n", "back-dp2", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Ventajas de usar Conda

1. **Gestión de dependencias nativas**: Conda maneja librerías C/C++ automáticamente
2. **Reproducibilidad**: Entornos idénticos en Windows/Linux/Mac
3. **Velocidad**: Resolución de dependencias más rápida con mamba
4. **Compatibilidad**: Funciona con pip para paquetes no disponibles en conda-forge
5. **Aislamiento completo**: Python + todas las dependencias del sistema

## Migración desde venv

Si ya tienes un entorno `venv` activo:

```bash
# Desactivar venv
deactivate

# Crear entorno conda
conda env create -f environment.yml

# Activar conda
conda activate back-dp2

# Verificar que todo funcione
pytest
```

## Troubleshooting

### Error: "CondaHTTPError"
```bash
# Limpiar caché de conda
conda clean --all

# Reintentar
conda env create -f environment.yml
```

### Error: "PackagesNotFoundError"
```bash
# Actualizar conda
conda update conda

# Añadir canal conda-forge
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Entorno lento al activar
```bash
# Usar mamba (más rápido que conda)
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
```

## Recursos adicionales

- [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)
- [Conda vs pip vs virtualenv](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html)
- [Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
