from typing import Annotated

from fastapi import Depends

from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.users.repositories import CustomerRepository
from src.api.modules.users.services.customers import CreateService
from src.api.settings.database import DBSessionDep


def customer_repository(db: DBSessionDep) -> CustomerRepository:
    """
    Dependencia que provee el repositorio para gestionar la información de clientes en la
    base de datos.
    """

    return CustomerRepository(db=db)


CustomerRepositoryDep = Annotated[CustomerRepository, Depends(customer_repository)]


def create_service(
    user_repo: UserRepositoryDep,
    customer_repo: CustomerRepositoryDep,
) -> CreateService:
    """Dependencia que provee el servicio encargado de registrar nuevos clientes."""

    return CreateService(user_repo=user_repo, customer_repo=customer_repo)


CreateServiceDep = Annotated[CreateService, Depends(create_service)]
