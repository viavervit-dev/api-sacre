from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.inventory.models import Product
from src.api.modules.inventory.repositories.interfaces import IProductRepository


class ProductRepository(IProductRepository):
    """Repositorio SQLAlchemy para la gestión de productos en `inventory.products`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_product_by_id(self, id: UUID) -> Product | None:

        instance = await self.__db.get(Product, id)

        return instance

    async def get_products_by_ids(self, ids: Sequence[UUID]) -> Sequence[Product]:

        if not ids:
            return []

        stmt = select(Product).where(Product.id.in_(ids))
        result = await self.__db.scalars(stmt)

        return result.all()

    async def get_active_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id)).where(Product.status == True)  # noqa: E712
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(Product)
            .where(Product.status == True)  # noqa: E712
            .order_by(Product.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_all_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id))
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = select(Product).order_by(Product.date_joined.desc()).offset(offset).limit(limit)
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
