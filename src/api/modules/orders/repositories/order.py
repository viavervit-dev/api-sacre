from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.orders.models import Order, order_number_seq
from src.api.modules.orders.repositories.interfaces import IOrderRepository


class OrderRepository(IOrderRepository):
    """Repositorio SQLAlchemy para la gestión de órdenes de compra en `orders.orders`."""

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_order_by_id(self, id: UUID, order_type: str) -> Order | None:

        stmt = select(Order).where(
            Order.id == id,
            Order.payment_data["description"].astext == order_type,
        )

        return await self.__db.scalar(stmt)

    async def get_list_orders(
        self,
        offset: int,
        limit: int,
        order_type: str,
    ) -> tuple[Sequence[Order], int]:

        # Condición de filtro por tipo de orden en el JSONB
        order_type_filter = Order.payment_data["description"].astext == order_type

        # Total para metadatos de paginación
        count_stmt = select(func.count(Order.id)).where(order_type_filter)
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Paginación y ordenamiento
        stmt = (
            select(Order)
            .where(order_type_filter)
            .order_by(Order.date_joined.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.__db.scalars(stmt)
        items = result.all()

        return items, total_items

    async def create_order(self, data: dict[str, Any]) -> Order:

        instance = Order(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_order(self, filters: dict[str, Any]) -> bool:

        stmt = select(Order.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)

    async def get_next_order_number(self) -> str:

        seq_num = await self.__db.scalar(order_number_seq.next_value())
        year = datetime.now(tz=UTC).year

        # Formato de 15 caracteres exactos: 3 + 1 + 4 + 1 + 6 = 15
        return f"ORD-{year}-{seq_num:06d}"
