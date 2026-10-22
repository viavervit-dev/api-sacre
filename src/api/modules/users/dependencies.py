from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.users.repositories.customer import CustomerRepository
from src.api.modules.users.repositories.customer_wholesale import CustomerWholesaleRepository
from src.api.modules.users.services.customers.create import CreateCustomerService
from src.api.modules.users.services.customers_wholesale.create import (
    CreateCustomerWholesaleService,
)
from src.api.modules.users.services.customers_wholesale.get_list import (
    GetListCustomerWholesaleService,
)
from src.api.modules.users.services.customers_wholesale.update import (
    UpdateCustomerWholesaleService,
)
from src.api.settings.database import db_session


def customer_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> CustomerRepository:
    """Provee una instancia del repositorio de clientes."""

    return CustomerRepository(db=db)


def customer_wholesale_repository(
    db: Annotated[AsyncSession, Depends(db_session)],
) -> CustomerWholesaleRepository:
    """Provee una instancia del repositorio de clientes mayoristas."""

    return CustomerWholesaleRepository(db=db)


def create_customer_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    customer_repo: Annotated[CustomerRepository, Depends(customer_repository)],
) -> CreateCustomerService:
    """Provee una instancia del servicio de creación de clientes."""

    return CreateCustomerService(user_repo=user_repo, customer_repo=customer_repo)


def create_customer_wholesale_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(customer_wholesale_repository)
    ],
) -> CreateCustomerWholesaleService:
    """Provee una instancia del servicio de creación de clientes mayoristas."""

    return CreateCustomerWholesaleService(
        customer_wholesale_repo=customer_wholesale_repo,
        user_repo=user_repo,
    )


def update_customer_wholesale_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    customer_wholesale_repo: Annotated[
        CustomerWholesaleRepository, Depends(customer_wholesale_repository)
    ],
) -> UpdateCustomerWholesaleService:
    """Provee una instancia del servicio de actualización de clientes mayoristas."""

    return UpdateCustomerWholesaleService(
        customer_wholesale_repo=customer_wholesale_repo,
        user_repo=user_repo,
    )


def get_list_customer_wholesale_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
) -> GetListCustomerWholesaleService:
    """Provee una instancia del servicio de obtención de lista de clientes mayoristas."""

    return GetListCustomerWholesaleService(user_repo=user_repo)
