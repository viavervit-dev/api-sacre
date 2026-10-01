from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models.wholesale import CustomerWholesale
from src.modules.users.repositories.interfaces import ICustomerWholesaleRepository


class CustomerWholesaleRepository(ICustomerWholesaleRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de clientes mayorista
    `users.customer_wholesale`.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_wholesale(self, id: UUID) -> CustomerWholesale | None:

        instance = await self.__db.get(CustomerWholesale, id)

        return instance

    async def create_wholesale(self, data: dict[str, Any]) -> CustomerWholesale:

        instance = CustomerWholesale(**data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_wholesale(self, filters: dict[str, Any]) -> bool:

        stmt = select(CustomerWholesale.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
