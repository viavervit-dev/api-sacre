from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.modules.countries.models.country import Country
from src.modules.countries.repositories.interfaces import ICountryRepository


class CountryRepository(ICountryRepository):
    """
    Repositorio SQLAlchemy para la gestión de países en `countries.country`.

    Implementa operaciones asíncronas para la consulta y obtención de información geográfica
    y estructuras político-administrativas.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.__db = db

    async def get_countries(self) -> Sequence[Country]:

        stmt = (
            select(Country)
            .options(load_only(Country.name, Country.code))
            .order_by(Country.name.asc())
        )
        result = await self.__db.scalars(stmt)

        return result.all()

    async def get_organization_country(self, country: str) -> Country | None:

        stmt = (
            select(Country)
            .options(load_only(Country.administrative_structure))
            .where(Country.name == country)
        )
        result = await self.__db.scalar(stmt)

        return result
