from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
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
    async def get_list_products(
        cls,
        offset: int,
        limit: int,
        db: AsyncSession,
        status: bool | None = None,
    ) -> tuple[Sequence[Product], int]:

        # Contamos el total de registros que coinciden con los filtros
        count_stmt = select(func.count()).select_from(Product)

        if status is not None:
            count_stmt = count_stmt.where(Product.status == status)

        total_result = await db.execute(count_stmt)
        total_items = total_result.scalar_one()

        # Luego obtenemos la página de productos solicitada con los mismos filtros
        stmt = select(Product)

        if status is not None:
            stmt = stmt.where(Product.status == status)

        stmt = stmt.order_by(Product.date_joined.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items, total_items

    @classmethod
    async def get_product_by_id(cls, db: AsyncSession, id: UUID) -> Product:

        return await db.get_one(Product, id)

    @classmethod
    async def create_product(cls, db: AsyncSession, data: dict[str, Any]) -> Product:

        instance = Product(**data)
        db.add(instance)
        await db.flush()

        return instance

    @classmethod
    async def update_product(
        cls,
        db: AsyncSession,
        update_data: dict[str, Any],
        instance: Product,
    ) -> Product:

        for key, value in update_data.items():
            setattr(instance, key, value)

        await db.commit()

        return instance

    @classmethod
    async def exists_product(cls, db: AsyncSession, filters: dict[str, Any]) -> bool:

        query = select(Product.id).filter_by(**filters)
        exists_query = select(query.exists())
        result = await db.execute(exists_query)

        return result.scalar_one()
