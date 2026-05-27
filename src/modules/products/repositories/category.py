from typing import Any

from sqlalchemy import select, update
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
    async def create_category(cls, db: AsyncSession, data: dict[str, Any]) -> Category:

        instance = Category(**data)
        db.add(instance)
        await db.flush()

        return instance

    @classmethod
    async def add_product_to_category(cls, db: AsyncSession, name: str):
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
    async def exists_category(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:

        query = select(Category.id).filter_by(**filters)
        exists_query = select(query.exists())
        result = await db.execute(exists_query)

        return result.scalar_one()
