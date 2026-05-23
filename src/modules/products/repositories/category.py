from typing import Any

from sqlalchemy import select
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
    async def create_category(
        cls,
        session: AsyncSession,
        data: dict[str, Any],
    ) -> Category:

        instance = Category(**data)
        session.add(instance)
        await session.flush()

        return instance

    @classmethod
    async def exists_category(cls, session: AsyncSession, filters: dict[str, Any]) -> bool:

        query = select(Category.id).filter_by(**filters)
        exists_query = select(query.exists())
        result = await session.execute(exists_query)

        return result.scalar_one()
