from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.modules.countries.repositories.country import CountryRepository
from src.api.modules.countries.services.get_countries import RetrieveContriesService
from src.api.modules.countries.services.get_organization_country import (
    RetrieveOrganizationCountryService,
)
from src.api.settings.database import get_db_session


def get_country_repository(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CountryRepository:
    """Provee una instancia del repositorio de países."""

    return CountryRepository(db=db)


def get_retrieve_organization_country_service(
    country_repo: Annotated[CountryRepository, Depends(get_country_repository)],
) -> RetrieveOrganizationCountryService:
    """Provee una instancia del servicio de consulta de organización territorial."""

    return RetrieveOrganizationCountryService(country_repo=country_repo)


def get_retrieve_contries_service(
    country_repo: Annotated[CountryRepository, Depends(get_country_repository)],
) -> RetrieveContriesService:
    """Provee una instancia del servicio de consulta de países."""

    return RetrieveContriesService(country_repo=country_repo)
