from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.modules.auth.dependencies import get_user_repository
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.customers.repositories.customer import CustomerRepository
from src.modules.customers.repositories.interfaces import ICustomerRepository
from src.modules.customers.services.create import CreateCustomerService


def get_customer_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> ICustomerRepository:
    """Provee una instancia del repositorio de clientes."""

    return CustomerRepository(db=db)


def get_create_customer_service(
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
    customer_repo: Annotated[ICustomerRepository, Depends(get_customer_repository)],
) -> CreateCustomerService:
    """Provee una instancia del servicio de creación de clientes."""

    return CreateCustomerService(user_repo=user_repo, customer_repo=customer_repo)
