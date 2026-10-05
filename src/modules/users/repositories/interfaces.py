from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.modules.users.models.admin import Admin
from src.modules.users.models.customer import Customer
from src.modules.users.models.customer_wholesale import CustomerWholesale


class ICustomerRepository(ABC):
    """Contrato de persistencia para el perfil de clientes `users.customers`."""

    @abstractmethod
    async def create_customer(self, user_id: UUID, data: dict[str, Any]) -> Customer:
        """Crea un cliente asociado a una cuenta de usuario en la base de datos."""

        pass

    @abstractmethod
    async def exists_customer(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un cliente que coincida con los filtros especificados."""

        pass


class ICustomerWholesaleRepository(ABC):
    """Contrato de persistencia para el perfil de cliente mayorista `users.customer_wholesale`."""

    @abstractmethod
    async def get_customers_wholesale(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[CustomerWholesale], int]:
        """
        Obtiene una lista paginada de clientes mayoristas y el total de registros encontrados.
        """

        pass

    @abstractmethod
    async def get_customer_wholesale(self, id: UUID) -> CustomerWholesale | None:
        """Obtiene un cliente mayorista por su identificador único."""

        pass

    @abstractmethod
    async def create_customer_wholesale(self, data: dict[str, Any]) -> CustomerWholesale:
        """Crea un nuevo cliente mayorista en la base de datos."""

        pass

    @abstractmethod
    async def update_customer_wholesale(
        self,
        instance: CustomerWholesale,
        data: dict[str, Any],
    ) -> CustomerWholesale:
        """Actualiza un cliente mayorista en la base de datos."""

        pass

    @abstractmethod
    async def exists_customer_wholesale(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un cliente mayorista que coincida con los filtros especificados."""

        pass


class IAdminRepository(ABC):
    """Contrato de persistencia para el perfil de administradores `users.admins`."""

    @abstractmethod
    async def create_admin(self, user_id: UUID, data: dict[str, Any]) -> Admin:
        """Crea un nuevo administrador asociado a una cuenta de usuario en la base de datos."""

        pass

    @abstractmethod
    async def exists_admin(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un administrador que coincida con los filtros especificados."""

        pass
