from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.users.models.customer_wholesale import CustomerWholesale
from src.api.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class CustomerWholesaleRepository(ICustomerWholesaleRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de clientes mayorista
    `users.customer_wholesale`.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_customer_wholesale(
        self,
        user_id: UUID,
        data: dict[str, Any],
    ) -> CustomerWholesale:

        instance = CustomerWholesale(user_id=user_id, **data)
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
