from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models.customer_wholesale import CustomerWholesale
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class CustomerWholesaleRepository(ICustomerWholesaleRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de clientes mayorista
    `users.customer_wholesale`.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_customers_wholesale(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[CustomerWholesale], int]:

        # Total para metadatos de paginación
        count_stmt = select(func.count(CustomerWholesale.id))
        total_items = await self.__db.scalar(count_stmt) or 0

        if total_items == 0:
            return [], 0

        # Registros paginados
        stmt = select(CustomerWholesale)
        stmt = stmt.order_by(CustomerWholesale.date_joined.desc()).offset(offset).limit(limit)
        result = await self.__db.scalars(stmt)

        return result.all(), total_items

    async def get_customer_wholesale(self, id: UUID) -> CustomerWholesale | None:

        instance = await self.__db.get(CustomerWholesale, id)

        return instance

    async def create_customer_wholesale(self, data: dict[str, Any]) -> CustomerWholesale:

        instance = CustomerWholesale(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def update_customer_wholesale(
        self,
        instance: CustomerWholesale,
        data: dict[str, Any],
    ) -> CustomerWholesale:

        for key, value in data.items():
            setattr(instance, key, value)

        await self.__db.flush()

        return instance

    async def exists_customer_wholesale(self, filters: dict[str, Any]) -> bool:

        stmt = select(CustomerWholesale.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
