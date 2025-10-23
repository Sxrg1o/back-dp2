# Quick Start - Compilación con Conda

Guía rápida para compilar y ejecutar el proyecto usando **Conda** en lugar de `venv`.

## 🚀 Inicio rápido (3 pasos)

### 1. Instalar Miniconda

**Windows:**
```powershell
# Descargar desde: https://docs.conda.io/en/latest/miniconda.html
# Ejecutar instalador y reiniciar terminal
```

**Linux/Mac:**
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Reiniciar terminal
```

### 2. Crear entorno

**Windows (SIN añadir Conda al PATH - Recomendado):**

1. Abre **Anaconda Prompt (miniconda3)** desde el menú de inicio
2. Navega al proyecto:
   ```bash
   cd E:\PROYECTOS\DP2\V6\back-dp2
   ```
3. Ejecuta el script:
   ```bash
   .\setup-conda.ps1
   ```

**Windows (alternativa con .bat - busca Conda automáticamente):**
```cmd
setup-conda.bat
```

**Linux/Mac:**
```bash
bash setup-conda.sh
```

### 3. Ejecutar

**Desde Anaconda Prompt:**
```bash
conda activate back-dp2
uvicorn src.main:app --reload
```

¡Listo! La API está corriendo en http://localhost:8000

> **Nota Windows**: Siempre usa **Anaconda Prompt** (no PowerShell normal) si no agregaste Conda al PATH.

---

## 📋 Comandos esenciales

**Todos estos comandos se ejecutan en Anaconda Prompt:**

```bash
# Navegar al proyecto
cd E:\PROYECTOS\DP2\V6\back-dp2

# Activar entorno
conda activate back-dp2

# Desactivar
conda deactivate

# Ver paquetes instalados
conda list

# Ejecutar tests
pytest

# Tests con cobertura
pytest --cov=src

# Actualizar entorno
conda env update -f environment.yml --prune
```

> 💡 **Tip**: Crea un acceso directo a Anaconda Prompt en tu escritorio para acceso rápido

---

## 🔧 Ventajas vs venv tradicional

| Característica | Conda | venv |
|---|---|---|
| Gestión de Python | ✅ Incluida | ❌ Sistema |
| Dependencias nativas (C/C++) | ✅ Automático | ❌ Manual |
| Reproducibilidad | ✅ Alta | ⚠️ Media |
| Velocidad instalación | ✅ Rápida (mamba) | ⚠️ Variable |
| Compatibilidad Windows | ✅ Excelente | ⚠️ Problemas |
| Espacio en disco | ⚠️ ~1GB | ✅ ~100MB |

---

## 🐛 Troubleshooting común

### "conda: command not found"
```bash
# Reinicia la terminal después de instalar Miniconda
# O ejecuta:
source ~/miniconda3/bin/activate  # Linux/Mac
```

### Entorno lento al crear
```bash
# Usa mamba (más rápido)
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
```

### Error al instalar paquetes
```bash
# Limpia caché
conda clean --all

# Recrea entorno
conda env remove -n back-dp2
conda env create -f environment.yml
```

---

## 📚 Más información

- **Guía completa**: Ver [CONDA.md](./CONDA.md)
- **README principal**: Ver [README.md](./README.md)
- **Tests**: `pytest --help`
- **FastAPI docs**: http://localhost:8000/docs

---

## ✅ Verificación

Después de configurar, verifica que todo funcione:

```bash
# 1. Activar entorno
conda activate back-dp2

# 2. Verificar Python
python --version
# Debe mostrar: Python 3.11.x

# 3. Verificar paquetes clave
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__}')"

# 4. Ejecutar tests
pytest tests/integration/api/test_alergeno_controller_integration.py -v

# 5. Iniciar servidor
uvicorn src.main:app --reload
# Abrir: http://localhost:8000/docs
```

Si todos los pasos funcionan correctamente, ¡estás listo para desarrollar! 🎉
