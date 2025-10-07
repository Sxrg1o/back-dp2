# Guía de GitHub

Para mejorar la forma de trabajar, ser más organizados y asegurar la calidad del proyecto, vamos a adoptar un flujo de trabajo estandarizado en GitHub. 

## El Flujo de Trabajo Básico

Cada vez que vayas a trabajar en una tarea (una nueva funcionalidad o la corrección de un error), sigue estos pasos:

1.  **Asigna un Issue**: Encuentra el Issue que vas a resolver en la sección `Issues` de GitHub y asígnatelo. Si no existe, créalo.
2.  **Crea una Rama**: Crea una nueva rama **desde `dev`** usando nuestra convención de nombres.
3.  **Desarrolla y Haz Commits**: Escribe tu código y haz commits pequeños y descriptivos.
4.  **Sube tus Cambios (Push)**: Sube tu rama a GitHub.
5.  **Actualiza tu Rama**: Antes de abrir un PR trata de traer los cambios de la rama destino, (normalmente `dev`) hacia tu rama para resolver posibles conflictos de merge.
6.  **Abre un Pull Request (PR)**: Abre un PR para fusionar tu rama con `dev`.
7.  **Revisión de Código**: Tu PR será revisado por al menos un miembro del equipo. Atiende los comentarios que puedan surgir.
8.  **Fusión (Merge)**: Una vez aprobado y con los tests en verde, tu PR será fusionado a `dev`.

## 1\. Nomenclatura de Ramas

Un nombre de rama claro nos dice qué está pasando sin necesidad de ver el código. A partir de ahora, usaremos el siguiente formato:

**`tipo/numero-issue-descripcion-breve`**

  * **`tipo`**: ¿Qué clase de trabajo es?
      * `feat`: Para una nueva funcionalidad (feature).
      * `fix`: Para una corrección de un error (bug).
      * `docs`: Para cambios en la documentación.
      * `chore`: Para tareas de mantenimiento (actualizar librerías, etc.).
  * **`numero-issue`**: El número del issue que estás resolviendo.
  * **`descripcion-breve`**: Un resumen corto de la tarea, en minúsculas y separado por guiones.

#### Ejemplos:

| Tarea | Nombre de Rama Correcto |
| :--- | :--- |
| Issue \#15: Crear login con Google | `feat/15-login-con-google` |
| Issue \#21: El total del carrito no se calcula bien| `fix/21-corregir-total-carrito` |
| Issue \#23: Actualizar el README | `docs/23-actualizar-readme` |

## 2\. Mensajes de Commit: La Historia de Nuestro Código 💬

Los mensajes de commit son la historia de nuestro proyecto. Un historial limpio nos ayuda a entender por qué se hizo un cambio y a encontrar errores más rápido. Usaremos el estándar **Conventional Commits**.

**`tipo(ámbito): descripción del commit`**

  * **`tipo`**: Igual que en las ramas (`feat`, `fix`, `docs`, `chore`, `refactor`, `style`).
  * **`ámbito`** (opcional): La parte del proyecto que modificaste (ej: `api`, `auth`, `ui`).
  * **`descripción`**: Un mensaje claro, en presente y en minúsculas.

#### Ejemplos:

```bash
# Bueno: claro y descriptivo
git commit -m "feat(auth): implementar endpoint para registro de usuarios"

# Bueno: una corrección específica
git commit -m "fix(checkout): validar que el stock sea mayor a cero"

# Malo: no aporta información
git commit -m "arreglos"

# Malo: demasiado vago
git commit -m "avance"

# Terrible: cualquier cosa generada por AI

# TIP: mientras menos cambios por commit la ia generara menos trash
```

## 3\. Pull Requests (PRs)

El Pull Request es donde proponemos nuestros cambios y nos aseguramos de que todo funcione correctamente antes de integrarlo.

#### Al abrir un PR:

1.  **Destino `dev`**: Asegúrate de que tu PR apunte a la rama `dev`, no a `main`.
2.  **Rellena la Plantilla**: Se cargará una plantilla automáticamente. Tómate un minuto para rellenarla.
      * **Contexto**: Enlaza el Issue que resuelve (ej: `Closes #15`).
      * **Descripción**: Explica qué hiciste y por qué.
      * **Pruebas**: Describe cómo puede el revisor probar tus cambios.
3.  **Usa "Draft PR"**: Si tu trabajo no está listo para ser revisado, pero quieres que el equipo vea tu progreso, crea un "Draft Pull Request".
4.  **Revisa tus Propios Cambios**: Antes de pedir una revisión, mira la pestaña "Files changed" para detectar errores obvios.

#### Durante la revisión de código:

  * **Para el Autor**: Sé receptivo a los comentarios. La crítica es al código, no a la persona xd.
  * **Para el Revisor**: Sé constructivo y respetuoso. Haz preguntas en lugar de dar órdenes. El objetivo es mejorar el código juntos.

## 4\. Nuestro Entorno de Ramas

Para mantener el orden, estas son nuestras ramas principales y su propósito:

  * **`main`**: Es el reflejo de lo que está en **Producción**. Nadie debe trabajar directamente en esta rama.
  * **`dev`**: Es nuestra rama de **desarrollo**. Todas las nuevas ramas se crean desde `dev` y se fusionan de vuelta aquí. Es la fuente de verdad de lo que está por venir.
  * **`qa`** (si la usamos): Es una rama para el entorno de **Pruebas/QA**. Se actualiza desde `dev` cuando un grupo de funcionalidades está listo para ser validado.

-----
