from typing import Annotated

from fastapi import Depends

from src.api.modules.countries.repositories import CountryRepository
from src.api.modules.countries.services import (
    RetrieveContriesService,
    RetrieveOrganizationCountryService,
)
from src.api.settings.database import DBSession


def country_repository(db: DBSession) -> CountryRepository:
    """Provee una instancia del repositorio de países."""

    return CountryRepository(db=db)


def get_organization_country_service(
    country_repo: Annotated[CountryRepository, Depends(country_repository)],
) -> RetrieveOrganizationCountryService:
    """Provee una instancia del servicio de consulta de organización territorial."""

    return RetrieveOrganizationCountryService(country_repo=country_repo)


def get_contries_service(
    country_repo: Annotated[CountryRepository, Depends(country_repository)],
) -> RetrieveContriesService:
    """Provee una instancia del servicio de consulta de países."""

    return RetrieveContriesService(country_repo=country_repo)
