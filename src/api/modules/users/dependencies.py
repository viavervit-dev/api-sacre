from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.auth.dependencies import UserRepository, user_repository
from src.api.modules.users.repositories.customer import CustomerRepository
from src.api.modules.users.repositories.wholesaler import WholesalerRepository
from src.api.modules.users.services.customers.create import CreateCustomerService
from src.api.modules.users.services.wholesaler.create import CreateWholesalerService
from src.api.modules.users.services.wholesaler.get_list import GetListWholesalerService
from src.api.modules.users.services.wholesaler.update import UpdateWholesalerService
from src.api.settings.database import db_session


def customer_repository(db: Annotated[AsyncSession, Depends(db_session)]) -> CustomerRepository:
    """Provee una instancia del repositorio de clientes."""

    return CustomerRepository(db=db)


def wholesaler_repository(
    db: Annotated[AsyncSession, Depends(db_session)],
) -> WholesalerRepository:
    """Provee una instancia del repositorio de clientes mayoristas."""

    return WholesalerRepository(db=db)


def create_customer_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    customer_repo: Annotated[CustomerRepository, Depends(customer_repository)],
) -> CreateCustomerService:
    """Provee una instancia del servicio de creación de clientes."""

    return CreateCustomerService(user_repo=user_repo, customer_repo=customer_repo)


def create_wholesaler_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    wholesaler_repo: Annotated[WholesalerRepository, Depends(wholesaler_repository)],
) -> CreateWholesalerService:
    """Provee una instancia del servicio de creación de clientes mayoristas."""

    return CreateWholesalerService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


def update_wholesaler_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
    wholesaler_repo: Annotated[WholesalerRepository, Depends(wholesaler_repository)],
) -> UpdateWholesalerService:
    """Provee una instancia del servicio de actualización de clientes mayoristas."""

    return UpdateWholesalerService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


def get_list_wholesaler_service(
    user_repo: Annotated[UserRepository, Depends(user_repository)],
) -> GetListWholesalerService:
    """Provee una instancia del servicio de obtención de lista de clientes mayoristas."""

    return GetListWholesalerService(user_repo=user_repo)
