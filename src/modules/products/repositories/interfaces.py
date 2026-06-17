from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.models.category import Category
from src.modules.products.models.product import Product


class ICategoryRepository(ABC):
    """
    Interfaz de `CategoryRepository`, define el contrato para un repositorio que administra la
    tabla `product.categories` en la base de datos.
    """

    @classmethod
    @abstractmethod
    async def get_list_categories(
        cls,
        offset: int,
        limit: int,
        db: AsyncSession,
        status: bool | None = None,
    ) -> tuple[Sequence[Category], int]:
        """Obtiene una secuencia paginada de categorias de productos filtradas por estado."""

        pass

    @classmethod
    @abstractmethod
    async def get_category_by_id(cls, db: AsyncSession, id: UUID) -> Category:
        """Obtiene una categoría de producto por su ID."""

        pass

    @classmethod
    @abstractmethod
    async def create_category(cls, db: AsyncSession, data: dict[str, Any]) -> Category:
        """Crea una nueva cateogria de prductos en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def update_category(
        cls,
        db: AsyncSession,
        update_data: dict[str, Any],
        id: UUID,
    ) -> Category:
        """Modifica los datos de una categoria de producto en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def add_product_to_category(cls, db: AsyncSession, name: str) -> None:
        """Incrementa el contador de productos asociados a una categoría en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def exists_category(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass


class IProductRepository(ICategoryRepository):
    """
    Interfaz de `ProductRepository`, define el contrato para un repositorio que administra la
    tabla `product.products` en la base de datos.
    """

    @classmethod
    @abstractmethod
    async def get_list_products(
        cls,
        offset: int,
        limit: int,
        db: AsyncSession,
        status: bool | None = None,
    ) -> tuple[Sequence[Product], int]:
        """Obtiene una secuencia paginada de productos filtrados por estado."""

        pass

    @classmethod
    @abstractmethod
    async def get_product_by_id(cls, db: AsyncSession, id: UUID) -> Product:
        """Obtiene un producto por su ID."""

        pass

    @classmethod
    @abstractmethod
    async def create_product(cls, db: AsyncSession, data: dict[str, Any]) -> Product:
        """Crea un nuevo producto en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def update_product(
        cls,
        db: AsyncSession,
        update_data: dict[str, Any],
        id: UUID,
    ) -> Product:
        """Modifica los datos de un producto en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def exists_product(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass
