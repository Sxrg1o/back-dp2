"""
Excepciones personalizadas para el módulo de sesiones.

Define las excepciones específicas que pueden ocurrir durante las operaciones
relacionadas con sesiones.
"""


class SesionValidationError(Exception):
    """
    Excepción lanzada cuando falla la validación de datos de una sesión.

    Se utiliza cuando los datos proporcionados para crear o actualizar una sesión
    no cumplen con las reglas de validación del negocio.

    Examples
    --------
    >>> raise SesionValidationError("El id_domotica no puede estar vacío")
    """

    pass


class SesionNotFoundError(Exception):
    """
    Excepción lanzada cuando no se encuentra una sesión.

    Se utiliza cuando se intenta acceder, actualizar o eliminar una sesión
    que no existe en la base de datos.

    Examples
    --------
    >>> raise SesionNotFoundError("No se encontró la sesión con ID 123")
    """

    pass


class SesionConflictError(Exception):
    """
    Excepción lanzada cuando hay un conflicto al crear o actualizar una sesión.

    Se utiliza cuando se intenta crear una sesión que ya existe o cuando
    hay conflictos de integridad referencial.

    Examples
    --------
    >>> raise SesionConflictError("Ya existe una sesión activa para este local")
    """

    pass
