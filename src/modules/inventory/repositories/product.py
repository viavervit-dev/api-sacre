from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.inventory.models.product import Product
from src.modules.inventory.repositories.interfaces import IProductRepository


class ProductRepository(IProductRepository):
    """Repositorio SQLAlchemy para la gestión de productos en `inventory.products`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_products(
        self,
        offset: int,
        limit: int,
        private: bool,
        status: bool | None = None,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id))

        if not private:
            count_stmt = count_stmt.where(Product.wholesaler_id.is_(None))

        if status is not None:
            count_stmt = count_stmt.where(Product.status == status)

        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Registros paginados
        stmt = select(Product)

        if not private:
            stmt = stmt.where(Product.wholesaler_id.is_(None))

        if status is not None:
            stmt = stmt.where(Product.status == status)

        stmt = stmt.order_by(Product.date_joined.desc()).offset(offset).limit(limit)
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_product(self, id: UUID) -> Product | None:

        instance = await self.__db.get(Product, id)

        return instance

    async def get_products_by_wholesaler(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Product], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Product.id)).where(Product.wholesaler_id == wholesaler_id)
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Registros paginados
        stmt = select(Product).where(Product.wholesaler_id == wholesaler_id)
        stmt = stmt.order_by(Product.date_joined.desc()).offset(offset).limit(limit)
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def create_product(self, data: dict[str, Any]) -> Product:

        instance = Product(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_product(self, update_data: dict[str, Any], instance: Product) -> Product:

        for key, value in update_data.items():
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
