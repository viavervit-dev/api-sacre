from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.inventory.models import WholesalerProduct
from src.api.modules.inventory.repositories.interfaces import IWholesalerProductRepository


class WholesalerProductRepository(IWholesalerProductRepository):
    """
    Repositorio SQLAlchemy para la gestión de productos de clientes mayoristas en
    `inventory.wholesaler_products`.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_product_by_id(self, id: UUID) -> WholesalerProduct | None:

        instance = await self.__db.get(WholesalerProduct, id)

        return instance

    async def get_all_products(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[WholesalerProduct], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(WholesalerProduct.id))
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(WholesalerProduct)
            .order_by(WholesalerProduct.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_products_by_wholesaler(
        self,
        wholesaler_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[WholesalerProduct], int]:

        # Total para metadatos de paginación
        count_stmt = (
            select(func.count(WholesalerProduct.id))
            .where(WholesalerProduct.wholesaler_id == wholesaler_id)
            .where(WholesalerProduct.status == True)  # noqa: E712
        )
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Registros paginados
        stmt = (
            select(WholesalerProduct)
            .where(WholesalerProduct.wholesaler_id == wholesaler_id)
            .where(WholesalerProduct.status == True)  # noqa: E712
            .order_by(WholesalerProduct.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def create_product(self, data: dict[str, Any], wholesaler_id: UUID) -> WholesalerProduct:

        instance = WholesalerProduct(wholesaler_id=wholesaler_id, **data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_product(
        self,
        data: dict[str, Any],
        instance: WholesalerProduct,
    ) -> WholesalerProduct:

        for key, value in data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def delete_product(self, instance: WholesalerProduct) -> None:

        await self.__db.delete(instance)
        await self.__db.flush()

    async def exists_product(self, filters: dict[str, Any]) -> bool:

        stmt = select(WholesalerProduct.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
