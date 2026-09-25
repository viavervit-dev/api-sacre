from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.modules.customers.models.customer import Customer


class ICustomerRepository(ABC):
    """Contrato de persistencia para el perfil de clientes (`customer.customers`)."""

    @abstractmethod
    async def create_customer(self, user_id: UUID, data: dict[str, Any]) -> Customer:
        """Crea y registra un nuevo perfil de cliente asociado a una cuenta de usuario."""

        pass

    @abstractmethod
    async def exists_customer(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe al menos un cliente que coincida con los filtros especificados."""

        pass
