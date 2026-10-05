from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db_session
from src.modules.auth.dependencies import get_user_repository
from src.modules.auth.repositories.user import UserRepository
from src.modules.users.repositories.customer import CustomerRepository
from src.modules.users.repositories.wholesale import CustomerWholesaleRepository
from src.modules.users.services.customers.create_customer import CreateCustomerService
from src.modules.users.services.customers_wholesale.create_wholesale import (
    CreateCustomerWholesaleService,
)
from src.modules.users.services.customers_wholesale.get_list_customer_wholesale import (
    RetrieveListCustomerWholesaleService,
)


def get_customer_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CustomerRepository:
    """Provee una instancia del repositorio de clientes."""

    return CustomerRepository(db=db)


def get_customer_wholesale_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CustomerWholesaleRepository:
    """Provee una instancia del repositorio de clientes mayoristas."""

    return CustomerWholesaleRepository(db=db)


def get_create_customer_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    customer_repo: Annotated[CustomerRepository, Depends(get_customer_repository)],
) -> CreateCustomerService:
    """Provee una instancia del servicio de creación de clientes."""

    return CreateCustomerService(user_repo=user_repo, customer_repo=customer_repo)


def get_create_customer_wholesale_service(
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(get_customer_wholesale_repository)
    ],
) -> CreateCustomerWholesaleService:
    """Provee una instancia del servicio de creación de clientes mayoristas."""

    return CreateCustomerWholesaleService(customer_wholesale_repo=customer_wholesale_repo)


def get_retrieve_list_customer_wholesale_service(
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(get_customer_wholesale_repository)
    ],
) -> RetrieveListCustomerWholesaleService:
    """Provee una instancia del servicio de obtención de lista de clientes mayoristas."""

    return RetrieveListCustomerWholesaleService(customer_wholesale_repo=customer_wholesale_repo)
