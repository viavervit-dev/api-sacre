from src.common.exceptions import ResourceNotFound
from src.modules.countries.dto import ReadAdministrativeStructureDTO
from src.modules.countries.repositories.interfaces import ICountryRepository


class RetrieveOrganizationCountryService:
    """Servicio encargado de consultar la estructura territorial de un país."""

    def __init__(self, country_repo: ICountryRepository) -> None:
        self.__country_repo = country_repo

    async def get_organization_country(self, country: str) -> ReadAdministrativeStructureDTO:
        """
        Obtiene la organización territorial de un país específico.

        Raises:
            ResourceNotFound: Si el país solicitado no se encuentra registrado.
        """

        organization_country = await self.__country_repo.get_organization_country(country=country)

        if not organization_country:
            raise ResourceNotFound()

        return ReadAdministrativeStructureDTO.model_construct(
            administrative_structure=organization_country.administrative_structure,
        )
