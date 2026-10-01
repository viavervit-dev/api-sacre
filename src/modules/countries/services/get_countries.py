from src.modules.countries.dto import ReadCountryDTO
from src.modules.countries.repositories.interfaces import ICountryRepository


class RetrieveContriesService:
    """Servicio encargado de la consulta y serialización del catálogo de países."""

    def __init__(self, country_repo: ICountryRepository) -> None:
        self.__country_repo = country_repo

    async def get_countries(self) -> list[ReadCountryDTO]:
        """Obtiene los países registrados y los transforma a DTOs de lectura."""

        countries = await self.__country_repo.get_countries()

        if not countries:
            return []

        result = []

        for country in countries:
            result.append(
                ReadCountryDTO.model_construct(
                    name=country.name,
                    code=country.code,
                )
            )

        return result
