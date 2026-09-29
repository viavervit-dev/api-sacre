from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.modules.users.models.admin import Admin
from src.modules.users.models.customer import Customer
from src.modules.users.models.wholesale import Wholesale


class ICustomerRepository(ABC):
    """Contrato de persistencia para el perfil de clientes `users.customers`."""

    @abstractmethod
    async def create_customer(self, user_id: UUID, data: dict[str, Any]) -> Customer:
        """Crea y registra un nuevo perfil de cliente asociado a una cuenta de usuario."""

        pass

    @abstractmethod
    async def exists_customer(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe al menos un cliente que coincida con los filtros especificados."""

        pass


class IWholesaleRepository(ABC):
    """Contrato de persistencia para el perfil de mayorista `users.wholesale`."""

    @abstractmethod
    async def create_wholesale(self, data: dict[str, Any]) -> Wholesale:
        """Crea y registra un nuevo perfil de mayorista."""

        pass

    @abstractmethod
    async def exists_wholesale(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un mayorista que coincida con los filtros especificados."""

        pass


class IAdminRepository(ABC):
    """Contrato de persistencia para el perfil de administradores `users.admins`."""

    @abstractmethod
    async def create_admin(self, user_id: UUID, data: dict[str, Any]) -> Admin:
        """Crea y registra un nuevo perfil de administrador asociado a una cuenta de usuario."""

        pass

    @abstractmethod
    async def exists_admin(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un administrador que coincida con los filtros especificados."""

        pass
