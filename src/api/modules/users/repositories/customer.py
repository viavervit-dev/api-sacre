from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.users.models import Customer
from src.api.modules.users.repositories.interfaces import ICustomerRepository
from src.api.settings.database import DBSessionDep


class CustomerRepository(ICustomerRepository):
    """Repositorio SQLAlchemy para la gestión de perfiles de clientes en `users.customers`."""

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


def customer_repository(db: DBSessionDep) -> CustomerRepository:
    """
    Dependencia que provee el repositorio para gestionar la información de clientes en la
    base de datos.
    """

    return CustomerRepository(db=db)


CustomerRepositoryDep = Annotated[CustomerRepository, Depends(customer_repository)]
