from abc import ABC, abstractmethod
from typing import Any

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
    async def create_category(cls, db: AsyncSession, data: dict[str, Any]) -> Category:
        """Crea una nueva cateogria de prductos en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def add_product_to_category(cls, db: AsyncSession, name: str):
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
    async def create_product(cls, db: AsyncSession, data: dict[str, Any]) -> Product:
        """Crea un nuevo producto en la base de datos."""

        pass


    @classmethod
    @abstractmethod
    async def exists_product(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass
