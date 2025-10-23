# Configuración en Windows (Sin PATH)

Guía específica para configurar el entorno Conda en Windows **sin agregar Conda al PATH del sistema**.

## ✅ Por qué NO agregar Conda al PATH

- ✅ Evita conflictos con otras instalaciones de Python
- ✅ Mantiene el sistema limpio
- ✅ Es la configuración **recomendada oficialmente** por Anaconda
- ✅ Más seguro y predecible

## 🚀 Configuración rápida

### Opción 1: Anaconda Prompt (Recomendada)

**Paso 1: Abrir Anaconda Prompt**
1. Presiona `Windows + S`
2. Escribe: **"Anaconda Prompt"** o **"Anaconda Prompt (miniconda3)"**
3. Abre la aplicación

**Paso 2: Navegar al proyecto**
```bash
cd E:\PROYECTOS\DP2\V6\back-dp2
```

**Paso 3: Crear entorno**
```bash
.\setup-conda.ps1
```

O manualmente:
```bash
conda env create -f environment.yml
```

**Paso 4: Activar y usar**
```bash
conda activate back-dp2
python --version
pytest
uvicorn src.main:app --reload
```

### Opción 2: Script .bat automático

Simplemente ejecuta desde PowerShell o CMD normal:
```cmd
setup-conda.bat
```

Este script:
- ✅ Busca Conda automáticamente en ubicaciones estándar
- ✅ No requiere PATH configurado
- ✅ Crea el entorno automáticamente
- ✅ Muestra instrucciones de próximos pasos

## 📝 Flujo de trabajo diario

### Primera vez (setup)

```bash
# 1. Abrir Anaconda Prompt
# 2. Navegar
cd E:\PROYECTOS\DP2\V6\back-dp2

# 3. Crear entorno (solo primera vez)
conda env create -f environment.yml
```

### Desarrollo diario

```bash
# 1. Abrir Anaconda Prompt
# 2. Navegar
cd E:\PROYECTOS\DP2\V6\back-dp2

# 3. Activar entorno
conda activate back-dp2

# 4. Trabajar normalmente
pytest
uvicorn src.main:app --reload

# 5. Al terminar
conda deactivate
```

## 🔧 Comandos útiles

### Gestión de entornos

```bash
# Listar entornos
conda env list

# Ver paquetes instalados
conda list

# Actualizar entorno
conda env update -f environment.yml --prune

# Eliminar entorno
conda env remove -n back-dp2
```

### Ejecución

```bash
# Servidor desarrollo
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Tests
pytest
pytest --cov=src --cov-report=html
pytest tests/integration/

# Verificar instalación
python --version
pip list
```

## 💡 Tips y trucos

### 1. Crear acceso directo en el escritorio (Automático)

**Ejecuta esto una sola vez:**
```powershell
.\create-desktop-shortcut.ps1
```

Esto crea un acceso directo llamado **"Back-DP2 Conda"** en tu escritorio. Con doble clic se abre Anaconda Prompt ya en tu proyecto con el entorno activado.

**Alternativa manual:**

Clic derecho en el escritorio → Nuevo → Acceso directo

**Ubicación:**
```
%windir%\System32\cmd.exe /K "%USERPROFILE%\miniconda3\Scripts\activate.bat" "%USERPROFILE%\miniconda3" && cd /D E:\PROYECTOS\DP2\V6\back-dp2 && conda activate back-dp2
```

### 2. Alias para comandos frecuentes

Crea un archivo `aliases.bat` en el proyecto:

```batch
@echo off
doskey test=pytest $*
doskey testcov=pytest --cov=src --cov-report=html $*
doskey run=uvicorn src.main:app --reload $*
doskey activate=conda activate back-dp2
```

Ejecútalo al inicio: `aliases.bat`

### 3. VSCode integration

Si usas VSCode, el editor detectará automáticamente el entorno Conda:

1. `Ctrl+Shift+P` → **"Python: Select Interpreter"**
2. Selecciona: `Python 3.11.x ('back-dp2')`
3. Los tests y el debugging funcionarán automáticamente

### 4. Verificar ruta de Conda

Si no encuentras Anaconda Prompt, busca Conda manualmente:

```powershell
Get-ChildItem -Path $env:USERPROFILE -Filter conda.exe -Recurse -ErrorAction SilentlyContinue
```

O ubicaciones comunes:
- `%USERPROFILE%\miniconda3\Scripts\conda.exe`
- `%USERPROFILE%\anaconda3\Scripts\conda.exe`
- `C:\ProgramData\miniconda3\Scripts\conda.exe`

## ⚠️ Troubleshooting

### "conda: command not found" en PowerShell normal

**Solución**: Usa **Anaconda Prompt** en su lugar, o ejecuta `setup-conda.bat`

### El script .ps1 no se ejecuta (error de firma)

```powershell
# Permitir scripts locales (ejecutar como Admin)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El entorno tarda mucho en crearse

```bash
# Usar mamba (más rápido)
conda install mamba -n base -c conda-forge
mamba env create -f environment.yml
```

### Quiero usar PowerShell normal (no Anaconda Prompt)

Si realmente necesitas usar PowerShell normal:

1. Inicializa Conda una vez:
   ```powershell
   & "$env:USERPROFILE\miniconda3\Scripts\conda.exe" init powershell
   ```
2. Reinicia PowerShell
3. Ahora `conda` funcionará en PowerShell

**Nota**: Esto modifica tu perfil de PowerShell.

## 📚 Referencias

- Ver comandos completos: `conda-commands.bat`
- Guía completa: `CONDA.md`
- Inicio rápido: `QUICKSTART-CONDA.md`
- README principal: `README.md`

## 🎯 Resumen ejecutivo

| Situación | Comando/Acción |
|---|---|
| Primera instalación | Ejecutar `setup-conda.bat` |
| Desarrollo diario | Abrir "Anaconda Prompt" → `cd E:\...` → `conda activate back-dp2` |
| Ejecutar tests | `pytest` (en Anaconda Prompt) |
| Iniciar servidor | `uvicorn src.main:app --reload` (en Anaconda Prompt) |
| Actualizar entorno | `conda env update -f environment.yml` |

---

**¿Problemas?** Revisa la sección Troubleshooting o abre un issue en el repositorio.
