from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.models.customer import Customer
from src.modules.users.repositories.interfaces import ICustomerRepository


class CustomerRepository(ICustomerRepository):
    """
    Repositorio SQLAlchemy para la gestión de perfiles de clientes en `customer.customers`.

    Implementa operaciones asíncronas para la creación y verificación de existencia
    de clientes vinculados a una cuenta de usuario.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def create_customer(self, user_id: UUID, data: dict[str, Any]) -> Customer:

        instance = Customer(user_id=user_id, **data)
        self.__db.add(instance)
        await self.__db.flush()

        return instance

    async def exists_customer(self, filters: dict[str, Any]) -> bool:

        stmt = select(Customer.id).filter_by(**filters)
        result = await self.__db.scalar(select(stmt.exists()))

        return bool(result)
