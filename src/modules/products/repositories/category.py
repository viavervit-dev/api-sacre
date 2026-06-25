from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.models.category import Category
from src.modules.products.repositories.interfaces import ICategoryRepository


class CategoryRepository(ICategoryRepository):
    """
    Repositorio para categorías de productos. Esta clase proporciona métodos que realizan
    operaciones en la tabla `product.categories` de la base de datos, resuelve dinámicamente las
    consultas y relaciones.
    """

    @classmethod
    async def get_list_categories(
        cls,
        offset: int,
        limit: int,
        db: AsyncSession,
        status: bool | None = None,
    ) -> tuple[Sequence[Category], int]:

        # Contamos el total de registros que coinciden con los filtros
        count_stmt = select(func.count()).select_from(Category)

        if status is not None:
            count_stmt = count_stmt.where(Category.status == status)

        total_result = await db.execute(count_stmt)
        total_items = total_result.scalar_one()

        # Luego obtenemos la página de categorias solicitada con los mismos filtros
        stmt = select(Category)

        if status is not None:
            stmt = stmt.where(Category.status == status)

        stmt = stmt.order_by(Category.date_joined.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items, total_items

    @classmethod
    async def get_category(cls, db: AsyncSession, id: UUID) -> Category:

        return await db.get_one(Category, id)

    @classmethod
    async def create_category(cls, db: AsyncSession, data: dict[str, Any]) -> Category:

        instance = Category(**data)
        db.add(instance)
        await db.flush()

        return instance

    @classmethod
    async def update_category(
        cls,
        db: AsyncSession,
        update_data: dict[str, Any],
        instance: Category,
    ) -> Category:

        for key, value in update_data.items():
            setattr(instance, key, value)

        await db.commit()

        return instance

    @classmethod
    async def add_product_to_category(cls, db: AsyncSession, name: str) -> None:
        # fmt: off
        stmt = (
            update(Category).where(Category.name == name)
            .values({Category.product_count: Category.product_count + 1})
            .returning(Category)
        )
        # fmt: off

        await db.execute(stmt)
        await db.commit()

    @classmethod
    async def delete_category(cls, db: AsyncSession, instance: Category) -> None:

        await db.delete(instance)
        await db.commit()

    @classmethod
    async def exists_category(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:

        query = select(Category.id).filter_by(**filters)
        exists_query = select(query.exists())
        result = await db.execute(exists_query)

        return result.scalar_one()
