from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.api.modules.inventory.models import Category, Product, WholesalerProduct


class ICategoryRepository(ABC):
    """Contrato de persistencia para operaciones sobre categorías (`inventory.categories`)."""

    @abstractmethod
    async def get_all_categories(self, offset: int, limit: int) -> tuple[Sequence[Category], int]:
        """
        Obtiene una lista paginada de todas las categorías y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_active_categories(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Category], int]:
        """
        Obtiene una lista paginada de categorías activadas y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_category_by_id(self, id: UUID) -> Category | None:
        """Obtiene una categoría por su identificador único."""

        pass

    @abstractmethod
    async def create_category(self, data: dict[str, Any]) -> Category:
        """Crea una nueva categoría en la base de datos."""

        pass

    @abstractmethod
    async def update_category(self, data: dict[str, Any], instance: Category) -> Category:
        """Actualiza una categoría en la base de datos."""

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
    async def get_product_by_id(self, id: UUID) -> Product | None:
        """Obtiene un producto por su identificador único."""

        pass

    @abstractmethod
    async def get_active_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:
        """
        Obtiene una lista paginada de productos activos y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_all_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:
        """
        Obtiene una lista paginada de todos los productos y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def create_product(self, data: dict[str, Any]) -> Product:
        """Crea un nuevo producto en la base de datos."""

        pass

    @abstractmethod
    async def update_product(self, data: dict[str, Any], instance: Product) -> Product:
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


class IWholesalerProductRepository(ABC):
    """
    Contrato de persistencia para operaciones sobre productos de clientes mayoristas
    (`inventory.wholesaler_products`).
    """

    @abstractmethod
    async def get_product_by_id(self, id: UUID) -> WholesalerProduct | None:
        """Obtiene un producto por su identificador único."""

        pass

    @abstractmethod
    async def get_active_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[WholesalerProduct], int]:
        """
        Obtiene una lista paginada de productos activos y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_all_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[WholesalerProduct], int]:
        """
        Obtiene una lista paginada de todos los productos y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_products_by_wholesaler(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[WholesalerProduct], int]:
        """
        Obtiene una lista paginada de productos asociados a un cliente mayorista y el total
        de registros encontrados.
        """

        pass

    @abstractmethod
    async def create_product(self, data: dict[str, Any], wholesaler_id: UUID) -> WholesalerProduct:
        """Crea un nuevo producto en la base de datos asociado a un cliente mayorista."""

        pass

    @abstractmethod
    async def update_product(
        self,
        data: dict[str, Any],
        instance: WholesalerProduct,
    ) -> WholesalerProduct:
        """Actualiza un producto en la base de datos."""

        pass

    @abstractmethod
    async def delete_product(self, instance: WholesalerProduct) -> None:
        """Elimina un producto de la base de datos."""

        pass

    @abstractmethod
    async def exists_product(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un producto que coincida con los filtros especificados."""

        pass
