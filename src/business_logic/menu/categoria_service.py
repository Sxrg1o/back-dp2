"""
Servicio para la gestión de categorías en el sistema.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repositories.menu.categoria_repository import CategoriaRepository
from src.models.menu.categoria_model import CategoriaModel
from src.api.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    CategoriaSummary,
    CategoriaList,
    ProductoCardMinimal,
    CategoriaConProductosCard,
    CategoriaConProductosCardList,
)
from src.business_logic.exceptions.categoria_exceptions import (
    CategoriaValidationError,
    CategoriaNotFoundError,
    CategoriaConflictError,
)


class CategoriaService:
    """Servicio para la gestión de categorías en el sistema.

    Esta clase implementa la lógica de negocio para operaciones relacionadas
    con categorías, incluyendo validaciones, transformaciones y manejo de excepciones.

    Attributes
    ----------
    repository : CategoriaRepository
        Repositorio para acceso a datos de categorías.
    """

    def __init__(self, session: AsyncSession):
        """
        Inicializa el servicio con una sesión de base de datos.

        Parameters
        ----------
        session : AsyncSession
            Sesión asíncrona de SQLAlchemy para realizar operaciones en la base de datos.
        """
        self.repository = CategoriaRepository(session)

    async def create_categoria(self, categoria_data: CategoriaCreate) -> CategoriaResponse:
        """
        Crea una nueva categoría en el sistema.
        
        Parameters
        ----------
        categoria_data : CategoriaCreate
            Datos para crear la nueva categoría.

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría creada.

        Raises
        ------
        CategoriaConflictError
            Si ya existe una categoría con el mismo nombre.
        """
        try:
            # Crear modelo de categoría desde los datos
            categoria = CategoriaModel(
                nombre=categoria_data.nombre,
                descripcion=categoria_data.descripcion,
                imagen_path=categoria_data.imagen_path
            )

            # Persistir en la base de datos
            created_categoria = await self.repository.create(categoria)

            # Convertir y retornar como esquema de respuesta
            return CategoriaResponse.model_validate(created_categoria)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            raise CategoriaConflictError(
                f"Ya existe una categoría con el nombre '{categoria_data.nombre}'"
            )

    async def get_categoria_by_id(self, categoria_id: str) -> CategoriaResponse:
        """
        Obtiene una categoría por su ID.

        Parameters
        ----------
        categoria_id : str
            Identificador único de la categoría a buscar (ULID).

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        """
        # Buscar la categoría por su ID
        categoria = await self.repository.get_by_id(categoria_id)

        # Verificar si existe
        if not categoria:
            raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

        # Convertir y retornar como esquema de respuesta
        return CategoriaResponse.model_validate(categoria)

    async def delete_categoria(self, categoria_id: str) -> bool:
        """
        Elimina una categoría por su ID.
        
        Parameters
        ----------
        categoria_id : str
            Identificador único de la categoría a eliminar (ULID).

        Returns
        -------
        bool
            True si la categoría fue eliminada correctamente.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        """
        # Verificar primero si la categoría existe
        categoria = await self.repository.get_by_id(categoria_id)
        if not categoria:
            raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

        # Eliminar la categoría
        result = await self.repository.delete(categoria_id)
        return result

    async def get_categorias(self, skip: int = 0, limit: int = 100) -> CategoriaList:
        """
        Obtiene una lista paginada de categorías.

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        CategoriaList
            Esquema con la lista de categorías y el total.
        """
        # Validar parámetros de entrada
        if skip < 0:
            raise CategoriaValidationError(
                "El parámetro 'skip' debe ser mayor o igual a cero"
            )
        if limit < 1:
            raise CategoriaValidationError("El parámetro 'limit' debe ser mayor a cero")

        # Obtener categorías desde el repositorio
        categorias, total = await self.repository.get_all(skip, limit)

        # Convertir modelos a esquemas de resumen
        categoria_summaries = [CategoriaSummary.model_validate(categoria) for categoria in categorias]

        # Retornar esquema de lista
        return CategoriaList(items=categoria_summaries, total=total)

    async def update_categoria(self, categoria_id: str, categoria_data: CategoriaUpdate) -> CategoriaResponse:
        """
        Actualiza una categoría existente.

        Parameters
        ----------
        categoria_id : str
            Identificador único de la categoría a actualizar (ULID).
        categoria_data : CategoriaUpdate
            Datos para actualizar la categoría.

        Returns
        -------
        CategoriaResponse
            Esquema de respuesta con los datos de la categoría actualizada.

        Raises
        ------
        CategoriaNotFoundError
            Si no se encuentra una categoría con el ID proporcionado.
        CategoriaConflictError
            Si ya existe otra categoría con el mismo nombre.
        """
        # Convertir el esquema de actualización a un diccionario,
        # excluyendo valores None (campos no proporcionados para actualizar)
        update_data = categoria_data.model_dump(exclude_none=True)

        if not update_data:
            # Si no hay datos para actualizar, simplemente retornar la categoría actual
            return await self.get_categoria_by_id(categoria_id)

        try:
            # Actualizar la categoría
            updated_categoria = await self.repository.update(categoria_id, **update_data)

            # Verificar si la categoría fue encontrada
            if not updated_categoria:
                raise CategoriaNotFoundError(f"No se encontró la categoría con ID {categoria_id}")

            # Convertir y retornar como esquema de respuesta
            return CategoriaResponse.model_validate(updated_categoria)
        except IntegrityError:
            # Capturar errores de integridad (nombre duplicado)
            if "nombre" in update_data:
                raise CategoriaConflictError(
                    f"Ya existe una categoría con el nombre '{update_data['nombre']}'"
                )
            # Si no es por nombre, reenviar la excepción original
            raise

    async def get_categorias_con_productos_cards(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> CategoriaConProductosCardList:
        """
        Obtiene una lista de categorías con sus productos en formato minimal (solo id, nombre, imagen).

        Parameters
        ----------
        skip : int, optional
            Número de registros a omitir (offset), por defecto 0.
        limit : int, optional
            Número máximo de registros a retornar, por defecto 100.

        Returns
        -------
        CategoriaConProductosCardList
            Lista de categorías con sus productos en formato minimal.
        """
        # Obtener categorías con productos eager-loaded
        categorias, total = await self.repository.get_all_with_productos(
            skip=skip,
            limit=limit,
            activo=True  # Solo categorías activas
        )

        # Construir la lista de categorías con productos
        items = []
        for categoria in categorias:
            # Construir lista de productos minimal
            productos_minimal = [
                ProductoCardMinimal(
                    id=producto.id,
                    nombre=producto.nombre,
                    imagen_path=producto.imagen_path
                )
                for producto in categoria.productos
            ]

            # Construir categoría con productos
            categoria_card = CategoriaConProductosCard(
                id=categoria.id,
                nombre=categoria.nombre,
                imagen_path=categoria.imagen_path,
                productos=productos_minimal
            )
            items.append(categoria_card)

        return CategoriaConProductosCardList(items=items, total=total)
