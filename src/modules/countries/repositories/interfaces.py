from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.modules.countries.models.country import Country


class ICountryRepository(ABC):
    """Contrato de persistencia para operaciones sobre países (`countries.country`)."""

    @abstractmethod
    async def get_countries(self) -> Sequence[Country]:
        """Obtiene la lista de países registrados en la base de datos."""

        pass

    @abstractmethod
    async def get_organization_country(self, country: str) -> Country | None:
        """Obtiene la información y estructura político-territorial de un país específico."""

        pass
