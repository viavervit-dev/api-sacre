from typing import Annotated

from fastapi import Depends

from src.api.modules.countries.repositories import CountryRepository
from src.api.modules.countries.services import (
    RetrieveContriesService,
    RetrieveOrganizationCountryService,
)
from src.api.settings.database import DBSessionDep


def country_repository(db: DBSessionDep) -> CountryRepository:
    """Provee una instancia del repositorio de países."""

    return CountryRepository(db=db)


CountryRepositoryDep = Annotated[CountryRepository, Depends(country_repository)]


def get_organization_country_service(
    country_repo: CountryRepositoryDep,
) -> RetrieveOrganizationCountryService:
    """Provee una instancia del servicio de consulta de organización territorial."""

    return RetrieveOrganizationCountryService(country_repo=country_repo)


RetrieveOrganizationCountryServiceDep = Annotated[
    RetrieveOrganizationCountryService, Depends(get_organization_country_service)
]


def get_contries_service(country_repo: CountryRepositoryDep) -> RetrieveContriesService:
    """Provee una instancia del servicio de consulta de países."""

    return RetrieveContriesService(country_repo=country_repo)


RetrieveContriesServiceDep = Annotated[RetrieveContriesService, Depends(get_contries_service)]
