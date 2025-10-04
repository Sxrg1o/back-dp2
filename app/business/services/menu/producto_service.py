"""
Product service for business logic related to menu products.
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.menu.producto_repository import ProductoRepository
from app.data.repositories.menu.categoria_repository import CategoriaRepository
from app.data.models.menu.producto_model import ProductoModel
from app.business.exceptions.menu_exceptions import (
    ProductoNotFoundError,
    CategoriaNotFoundError,
    ProductoNotAvailableError
)
from app.business.validators.producto_validators import ProductoValidator
from app.shared.utils.pagination_utils import PaginationParams, PaginatedResponse


class ProductoService:
    """Product service for business operations."""

    def __init__(self):
        self.producto_repo = ProductoRepository()
        self.categoria_repo = CategoriaRepository()
        self.validator = ProductoValidator()

    async def create_product(
        self,
        db: AsyncSession,
        product_data: Dict[str, Any]
    ) -> ProductoModel:
        """
        Create a new product.

        Args:
            db: Database session
            product_data: Product creation data

        Returns:
            Created product

        Raises:
            CategoriaNotFoundError: If category doesn't exist
            ValueError: If validation fails
        """
        # Validate input data
        self.validator.validate_product_data(product_data)

        # Check if category exists
        category = await self.categoria_repo.get_by_id(db, product_data["id_categoria"])
        if not category:
            raise CategoriaNotFoundError(f"Category with ID {product_data['id_categoria']} not found")

        # Check if category is active
        if not category.activo:
            raise CategoriaNotFoundError("Cannot create product in inactive category")

        # Create product
        return await self.producto_repo.create(db, **product_data)

    async def get_product_by_id(
        self,
        db: AsyncSession,
        product_id: int,
        include_relations: bool = True
    ) -> ProductoModel:
        """
        Get product by ID.

        Args:
            db: Database session
            product_id: Product ID
            include_relations: Include related data

        Returns:
            Product instance

        Raises:
            ProductoNotFoundError: If product doesn't exist
        """
        if include_relations:
            product = await self.producto_repo.get_with_relations(
                db, product_id, ["categoria", "alergenos", "opciones"]
            )
        else:
            product = await self.producto_repo.get_by_id(db, product_id)

        if not product:
            raise ProductoNotFoundError(f"Product with ID {product_id} not found")

        return product

    async def get_products_by_category(
        self,
        db: AsyncSession,
        category_id: int,
        available_only: bool = True
    ) -> List[ProductoModel]:
        """
        Get products by category.

        Args:
            db: Database session
            category_id: Category ID
            available_only: Filter only available products

        Returns:
            List of products

        Raises:
            CategoriaNotFoundError: If category doesn't exist
        """
        # Check if category exists
        category = await self.categoria_repo.get_by_id(db, category_id)
        if not category:
            raise CategoriaNotFoundError(f"Category with ID {category_id} not found")

        return await self.producto_repo.get_by_category(
            db, category_id, available_only
        )

    async def search_products(
        self,
        db: AsyncSession,
        search_params: Dict[str, Any],
        pagination: PaginationParams
    ) -> PaginatedResponse[ProductoModel]:
        """
        Search products with filters and pagination.

        Args:
            db: Database session
            search_params: Search parameters
            pagination: Pagination parameters

        Returns:
            Paginated products
        """
        products = await self.producto_repo.search_products(
            db,
            search_term=search_params.get("search_term", ""),
            category_id=search_params.get("category_id"),
            min_price=search_params.get("min_price"),
            max_price=search_params.get("max_price"),
            available_only=search_params.get("available_only", True)
        )

        # Apply pagination (simplified - in production you'd do this at DB level)
        start_idx = (pagination.page - 1) * pagination.size
        end_idx = start_idx + pagination.size
        paginated_products = products[start_idx:end_idx]

        return PaginatedResponse(
            items=paginated_products,
            total=len(products),
            page=pagination.page,
            size=pagination.size,
            pages=(len(products) + pagination.size - 1) // pagination.size
        )

    async def update_product(
        self,
        db: AsyncSession,
        product_id: int,
        update_data: Dict[str, Any]
    ) -> ProductoModel:
        """
        Update product.

        Args:
            db: Database session
            product_id: Product ID
            update_data: Data to update

        Returns:
            Updated product

        Raises:
            ProductoNotFoundError: If product doesn't exist
        """
        # Check if product exists
        product = await self.get_product_by_id(db, product_id, include_relations=False)

        # Validate update data
        self.validator.validate_product_update(update_data)

        # If category is being updated, validate it exists
        if "id_categoria" in update_data:
            category = await self.categoria_repo.get_by_id(db, update_data["id_categoria"])
            if not category or not category.activo:
                raise CategoriaNotFoundError("Invalid or inactive category")

        # Update product
        updated_product = await self.producto_repo.update(db, product_id, **update_data)
        if not updated_product:
            raise ProductoNotFoundError(f"Product with ID {product_id} not found")

        return updated_product

    async def toggle_product_availability(
        self,
        db: AsyncSession,
        product_id: int
    ) -> ProductoModel:
        """
        Toggle product availability.

        Args:
            db: Database session
            product_id: Product ID

        Returns:
            Updated product
        """
        product = await self.get_product_by_id(db, product_id, include_relations=False)
        new_availability = not product.disponible

        return await self.producto_repo.update_availability(
            db, product_id, new_availability
        )

    async def get_featured_products(self, db: AsyncSession) -> List[ProductoModel]:
        """
        Get featured products.

        Args:
            db: Database session

        Returns:
            List of featured products
        """
        return await self.producto_repo.get_featured_products(db)

    async def calculate_product_final_price(
        self,
        db: AsyncSession,
        product_id: int,
        selected_options: List[int] = None
    ) -> Decimal:
        """
        Calculate final price including selected options.

        Args:
            db: Database session
            product_id: Product ID
            selected_options: List of selected option IDs

        Returns:
            Final calculated price

        Raises:
            ProductoNotFoundError: If product doesn't exist
            ProductoNotAvailableError: If product is not available
        """
        product = await self.get_product_by_id(db, product_id)

        if not product.disponible:
            raise ProductoNotAvailableError(f"Product {product.nombre} is not available")

        final_price = product.precio_base

        # Add option prices
        if selected_options:
            for option in product.opciones:
                if option.id in selected_options and option.activo:
                    final_price += option.precio_adicional

        return final_price

    async def delete_product(self, db: AsyncSession, product_id: int) -> bool:
        """
        Delete product.

        Args:
            db: Database session
            product_id: Product ID

        Returns:
            True if deleted successfully

        Raises:
            ProductoNotFoundError: If product doesn't exist
        """
        product = await self.get_product_by_id(db, product_id, include_relations=False)
        return await self.producto_repo.delete(db, product_id)