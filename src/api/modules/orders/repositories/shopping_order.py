from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.orders.models.shopping_order import ShoppingOrder, shopping_order_number_seq
from src.api.modules.orders.repositories.interfaces import IShoppingOrderRepository


class ShoppingOrderRepository(IShoppingOrderRepository):
    """Repositorio SQLAlchemy para la gestión de órdenes de compra en `orders.orders`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_order_by_id(self, id: UUID) -> ShoppingOrder | None:

        instance = await self.__db.get(ShoppingOrder, id)

        return instance

    async def create_order(self, data: dict[str, Any]) -> ShoppingOrder:

        instance = ShoppingOrder(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_order(self, filters: dict[str, Any]) -> bool:

        stmt = select(ShoppingOrder.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)

    async def get_next_order_number(self) -> str:

        seq_num = await self.__db.scalar(shopping_order_number_seq.next_value())
        year = datetime.now(tz=UTC).year

        # Formato de 15 caracteres exactos: 3 + 1 + 4 + 1 + 6 = 15
        return f"ORD-{year}-{seq_num:06d}"
