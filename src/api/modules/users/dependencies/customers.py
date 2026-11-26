from typing import Annotated

from fastapi import Depends

from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.users.repositories import CustomerRepositoryDep
from src.api.modules.users.services.customers import CreateService


def create_service(
    user_repo: UserRepositoryDep,
    customer_repo: CustomerRepositoryDep,
) -> CreateService:
    """Dependencia que provee el servicio encargado de registrar nuevos clientes."""

    return CreateService(user_repo=user_repo, customer_repo=customer_repo)


CreateServiceDep = Annotated[CreateService, Depends(create_service)]
