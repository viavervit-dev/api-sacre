from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.inventory.models.category import Category
from src.api.modules.inventory.repositories.interfaces import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    """Repositorio SQLAlchemy para la gestión de categorías en `inventory.categories`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_list_categories(self, offset: int, limit: int) -> tuple[Sequence[Category], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Category.id))
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = select(Category).order_by(Category.date_joined.desc()).offset(offset).limit(limit)
        result = await self.__db.scalars(stmt)
        items = result.all()

        return items, total_items

    async def get_list_categories_activated(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Category], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(Category.id)).where(Category.status == True)  # noqa: E712
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(Category)
            .where(Category.status == True)  # noqa: E712
            .order_by(Category.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)
        items = result.all()

        return items, total_items

    async def get_category_by_id(self, id: UUID) -> Category | None:

        return await self.__db.get(Category, id)

    async def create_category(self, data: dict[str, Any]) -> Category:

        instance = Category(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_category(self, data: dict[str, Any], instance: Category) -> Category:

        for key, value in data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def delete_category(self, instance: Category) -> None:

        await self.__db.delete(instance)
        await self.__db.flush()

    async def exists_category(self, filters: dict[str, Any]) -> bool:

        stmt = select(Category.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
