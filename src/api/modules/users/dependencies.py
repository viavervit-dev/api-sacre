from typing import Annotated

from fastapi import Depends

from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.users.repositories import CustomerRepository, WholesalerRepository
from src.api.modules.users.services.customers import CreateCustomerService
from src.api.modules.users.services.wholesaler import (
    CreateWholesalerService,
    GetListWholesalerService,
    GetWholesalerService,
    UpdateWholesalerService,
)
from src.api.settings.database import DBSessionDep


def customer_repository(db: DBSessionDep) -> CustomerRepository:
    """Provee una instancia del repositorio de clientes."""

    return CustomerRepository(db=db)


CustomerRepositoryDep = Annotated[CustomerRepository, Depends(customer_repository)]


def wholesaler_repository(db: DBSessionDep) -> WholesalerRepository:
    """Provee una instancia del repositorio de clientes mayoristas."""

    return WholesalerRepository(db=db)


WholesalerRepositoryDep = Annotated[WholesalerRepository, Depends(wholesaler_repository)]


def create_customer_service(
    user_repo: UserRepositoryDep,
    customer_repo: CustomerRepositoryDep,
) -> CreateCustomerService:
    """Provee una instancia del servicio de creación de clientes."""

    return CreateCustomerService(user_repo=user_repo, customer_repo=customer_repo)


CreateCustomerServiceDep = Annotated[CreateCustomerService, Depends(create_customer_service)]


def create_wholesaler_service(
    user_repo: UserRepositoryDep,
    wholesaler_repo: WholesalerRepositoryDep,
) -> CreateWholesalerService:
    """Provee una instancia del servicio de creación de clientes mayoristas."""

    return CreateWholesalerService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


CreateWholesalerServiceDep = Annotated[CreateWholesalerService, Depends(create_wholesaler_service)]


def update_wholesaler_service(
    user_repo: UserRepositoryDep,
    wholesaler_repo: WholesalerRepositoryDep,
) -> UpdateWholesalerService:
    """Provee una instancia del servicio de actualización de clientes mayoristas."""

    return UpdateWholesalerService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


UpdateWholesalerServiceDep = Annotated[UpdateWholesalerService, Depends(update_wholesaler_service)]


def get_list_wholesaler_service(user_repo: UserRepositoryDep) -> GetListWholesalerService:
    """Provee una instancia del servicio de obtención de lista de clientes mayoristas."""

    return GetListWholesalerService(user_repo=user_repo)


GetListWholesalerServiceDep = Annotated[
    GetListWholesalerService, Depends(get_list_wholesaler_service)
]


def get_wholesaler_service(user_repo: UserRepositoryDep) -> GetWholesalerService:
    """Provee una instancia del servicio de obtención de un cliente mayorista."""

    return GetWholesalerService(user_repo=user_repo)


GetWholesalerServiceDep = Annotated[GetWholesalerService, Depends(get_wholesaler_service)]
