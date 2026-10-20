from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class ProductRepository(IProductRepository):
    """Repositorio SQLAlchemy para la gestión de productos en `inventory.products`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_product_by_id(self, id: UUID) -> Product | None:

        instance = await self.__db.get(Product, id)

        return instance

    async def get_products_public_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id)).where(
            Product.exclusive == False,  # noqa: E712
            Product.status == True,  # noqa: E712
        )
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(Product)
            .where(
                Product.exclusive == False,  # noqa: E712
                Product.status == True,  # noqa: E712
            )
            .order_by(Product.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_products_private_catalog(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id)).where(Product.exclusive == False)  # noqa: E712
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(Product)
            .where(Product.exclusive == False)  # noqa: E712
            .order_by(Product.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_products_by_wholesaler(
        self,
        products_id: list[UUID],
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        if not products_id:
            return [], 0

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id)).where(Product.id.in_(products_id))
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Registros paginados
        stmt = (
            select(Product)
            .where(Product.id.in_(products_id))
            .order_by(Product.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def create_product(self, data: dict[str, Any]) -> Product:

        instance = Product(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_product(self, data: dict[str, Any], instance: Product) -> Product:

        for key, value in data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def delete_product(self, instance: Product) -> None:

        await self.__db.delete(instance)
        await self.__db.flush()

    async def exists_product(self, filters: dict[str, Any]) -> bool:

        stmt = select(Product.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
