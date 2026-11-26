from typing import Annotated

from fastapi import Depends

from src.api.modules.auth.dependencies import UserRepositoryDep
from src.api.modules.users.repositories import WholesalerRepository
from src.api.modules.users.services.wholesaler import (
    CreateService,
    GetListWholesalerService,
    GetWholesalerService,
    UpdateService,
)
from src.api.settings.database import DBSessionDep


def wholesaler_repository(db: DBSessionDep) -> WholesalerRepository:
    """
    Dependencia que provee el repositorio para gestionar la información de clientes mayoristas
    en las base de datos.
    """

    return WholesalerRepository(db=db)


WholesalerRepositoryDep = Annotated[WholesalerRepository, Depends(wholesaler_repository)]


def get_wholesaler_service(user_repo: UserRepositoryDep) -> GetWholesalerService:
    """
    Dependencia que provee el servicio encargado de consultar el detalle de un cliente mayorista.
    """

    return GetWholesalerService(user_repo=user_repo)


GetWholesalerServiceDep = Annotated[GetWholesalerService, Depends(get_wholesaler_service)]


def get_list_service(user_repo: UserRepositoryDep) -> GetListWholesalerService:
    """Dependencia que provee el servicio encargado de listar clientes mayoristas."""

    return GetListWholesalerService(user_repo=user_repo)


GetListWholesalerServiceDep = Annotated[GetListWholesalerService, Depends(get_list_service)]


def create_service(
    user_repo: UserRepositoryDep,
    wholesaler_repo: WholesalerRepositoryDep,
) -> CreateService:
    """Dependencia que provee el servicio encargado de registrar nuevos clientes mayoristas."""

    return CreateService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


CreateServiceDep = Annotated[CreateService, Depends(create_service)]


def update_service(
    user_repo: UserRepositoryDep,
    wholesaler_repo: WholesalerRepositoryDep,
) -> UpdateService:
    """Dependencia que provee el servicio encargado de actualizar datos de clientes mayoristas."""

    return UpdateService(wholesaler_repo=wholesaler_repo, user_repo=user_repo)


UpdateServiceDep = Annotated[UpdateService, Depends(update_service)]
