from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.orders.models.order import ShoppingOrder
from src.api.modules.orders.repositories.interfaces import IShoppingOrderRepository


class ShoppingOrderRepository(IShoppingOrderRepository):
    """Repositorio SQLAlchemy para la gestión de órdenes de compra en `orders.orders`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_order(self, data: dict[str, Any]) -> ShoppingOrder:

        instance = ShoppingOrder(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_order(self, filters: dict[str, Any]) -> bool:

        stmt = select(ShoppingOrder.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
