# Guía de Documentación para el Proyecto

## Principios Generales

1. **Idioma**: Toda la documentación debe estar en español, manteniendo las palabras clave (keywords) en inglés.
2. **Consistencia**: Mantener un estilo uniforme en toda la documentación.
3. **Claridad**: Escribir de manera clara y concisa, evitando jerga técnica innecesaria.
4. **Exhaustividad**: Documentar todas las clases, métodos y atributos públicos.
5. **Actualización**: Mantener la documentación actualizada con el código.

## Formato de Docstrings (Estilo NumPy/SciPy)

### Para Módulos

```python
"""
[Nombre del módulo].

[Descripción breve del módulo].

[Descripción más detallada si es necesaria].

Examples
--------
[Ejemplos de uso si aplica]
"""
```

### Para Clases

```python
"""
[Nombre de la clase].

[Descripción breve de la clase].

[Descripción más detallada, incluyendo propósito y uso].

Attributes
----------
[atributo1] : [Tipo]
    [Descripción]
[atributo2] : [Tipo]
    [Descripción]
...

Notes
-----
[Notas adicionales si son necesarias]
"""
```

### Para Métodos y Funciones

```python
"""
[Verbo en tercera persona] [descripción de lo que hace].

[Descripción más detallada si es necesaria].

Parameters
----------
[argumento1] : [Tipo]
    [Descripción]
[argumento2] : [Tipo]
    [Descripción]
...

Returns
-------
[Tipo]
    [Descripción de lo que retorna]

Raises
------
[Excepción1]
    [Condición que causa la excepción]
[Excepción2]
    [Condición que causa la excepción]
...

Examples
--------
[Ejemplos de uso si aplica]
"""
```

## Buenas Prácticas

1. **Verbos**:
   - Comenzar las descripciones de métodos con verbos en tercera persona (ej: "Convierte", "Calcula", "Obtiene").
   - Usar presente simple para describir comportamientos.

2. **Tipos de Datos**:
   - Especificar siempre los tipos de los parámetros y valores de retorno.
   - Usar anotaciones de tipo de Python además de mencionarlos en la documentación.

3. **Ejemplos**:
   - Incluir ejemplos de uso cuando sea útil para clarificar.
   - Asegurarse de que los ejemplos funcionen correctamente.

4. **Estructuración**:
   - Mantener la misma estructura en todos los docstrings (orden de secciones).
   - Usar secciones como "Args", "Returns", "Raises", "Ejemplos", "Notas", etc. de manera consistente.

5. **Formato**:
   - Usar triple comillas dobles (`"""`) para todos los docstrings.
   - Mantener la primera línea como un resumen corto y conciso.
   - Dejar una línea en blanco después de la primera línea si hay más descripción.

6. **Herencia**:
   - Documentar comportamientos heredados solo si se modifican.
   - Hacer referencia a la documentación de la clase padre cuando sea apropiado.

## Referencias Externas

- [PEP 257 -- Convenciones de Docstrings](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)