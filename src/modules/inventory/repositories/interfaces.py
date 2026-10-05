from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.modules.inventory.models.category import Category
from src.modules.inventory.models.product import Product


class ICategoryRepository(ABC):
    """Contrato de persistencia para operaciones sobre categorías (`inventory.categories`)."""

    @abstractmethod
    async def get_list_categories(
        self,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[Sequence[Category], int]:
        """Obtiene una lista paginada de categorías y el total de registros encontrados."""

        pass

    @abstractmethod
    async def get_category(self, id: UUID) -> Category | None:
        """Obtiene una categoría por su identificador único."""

        pass

    @abstractmethod
    async def create_category(self, data: dict[str, Any]) -> Category:
        """Crea una nueva categoría en la base de datos."""

        pass

    @abstractmethod
    async def update_category(self, update_data: dict[str, Any], instance: Category) -> Category:
        """Actualiza una categoría en la base de datos."""

        pass

    @abstractmethod
    async def add_product_to_category(self, name: str) -> None:
        """Incrementa en uno el contador de productos asociados a la categoría."""

        pass

    @abstractmethod
    async def delete_category(self, instance: Category) -> None:
        """Elimina una categoría de la base de datos."""

        pass

    @abstractmethod
    async def exists_category(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe una categoría que coincida con los filtros especificados."""

        pass


class IProductRepository(ABC):
    """Contrato de persistencia para operaciones sobre productos (`inventory.products`)."""

    @abstractmethod
    async def get_products(
        self,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[Sequence[Product], int]:
        """Obtiene una lista paginada de productos y el total de registros encontrados."""

        pass

    @abstractmethod
    async def get_product(self, id: UUID) -> Product | None:
        """Obtiene un producto por su identificador único."""

        pass

    @abstractmethod
    async def get_products_by_wholesaler(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:
        """
        Obtiene una lista paginada de productos asociados a un cliente mayorista y el total
        de registros encontrados.
        """

        pass

    @abstractmethod
    async def create_product(self, data: dict[str, Any]) -> Product:
        """Crea un nuevo producto en la base de datos."""

        pass

    @abstractmethod
    async def update_product(self, update_data: dict[str, Any], instance: Product) -> Product:
        """Actualiza un producto en la base de datos."""

        pass

    @abstractmethod
    async def delete_product(self, instance: Product) -> None:
        """Elimina un producto de la base de datos."""

        pass

    @abstractmethod
    async def exists_product(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un producto que coincida con los filtros especificados."""

        pass
