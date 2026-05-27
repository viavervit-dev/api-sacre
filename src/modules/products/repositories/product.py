from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.models.product import Product
from src.modules.products.repositories.category import CategoryRepository
from src.modules.products.repositories.interfaces import IProductRepository


class ProductRepository(IProductRepository, CategoryRepository):
    """
    Repositorio para productos. Esta clase proporciona métodos que realizan operaciones en la tabla
    `product.products` de la base de datos, resuelve dinámicamente las consultas y relaciones.
    """

    @classmethod
    async def create_product(cls, db: AsyncSession, data: dict[str, Any]) -> Product:

        instance = Product(**data)
        db.add(instance)
        await db.flush()

        return instance

    @classmethod
    async def exists_product(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:

        query = select(Product.id).filter_by(**filters)
        exists_query = select(query.exists())
        result = await db.execute(exists_query)

        return result.scalar_one()
