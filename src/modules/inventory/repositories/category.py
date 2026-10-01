from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.interfaces import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    """Repositorio SQLAlchemy para la gestión de categorías en `inventory.categories`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_list_categories(
        self,
        offset: int,
        limit: int,
        status: bool | None = None,
    ) -> tuple[Sequence[Category], int]:

        count_stmt = select(func.count()).select_from(Category)

        if status is not None:
            count_stmt = count_stmt.where(Category.status == status)

        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        stmt = select(Category)

        if status is not None:
            stmt = stmt.where(Category.status == status)

        stmt = stmt.order_by(Category.date_joined.desc()).offset(offset).limit(limit)
        result = await self.__db.scalars(stmt)
        items = result.all()

        return items, total_items

    async def get_category(self, id: UUID) -> Category | None:

        return await self.__db.get(Category, id)

    async def create_category(self, data: dict[str, Any]) -> Category:

        instance = Category(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_category(self, update_data: dict[str, Any], instance: Category) -> Category:

        for key, value in update_data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def add_product_to_category(self, name: str) -> None:
        # fmt: off
        stmt = (
            update(Category).where(Category.name == name)
            .values({Category.product_count: Category.product_count + 1})
            .returning(Category)
        )
        # fmt: off

        await self.__db.execute(stmt)
        await self.__db.flush()

    async def delete_category(self, instance: Category) -> None:

        await self.__db.delete(instance)
        await self.__db.flush()

    async def exists_category(self, filters: dict[str, Any]) -> bool:

        stmt = select(Category.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
