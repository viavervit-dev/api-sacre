from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.orders.models.order import Order
from src.api.modules.orders.repositories.interfaces import IOrderRepository


class OrderRepository(IOrderRepository):
    """Repositorio SQLAlchemy para la gestión de órdenes en `orders.orders`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_order(self, data: dict[str, Any]) -> Order:

        instance = Order(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_order(self, filters: dict[str, Any]) -> bool:

        stmt = select(Order.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
