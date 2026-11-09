from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.api.modules.users.models import Admin, Customer, Wholesaler


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


class IWholesalerRepository(ABC):
    """Contrato de persistencia para el perfil de cliente mayorista `users.customer_wholesale`."""

    @abstractmethod
    async def create_wholesaler(self, user_id: UUID, data: dict[str, Any]) -> Wholesaler:
        """Crea un nuevo cliente mayorista en la base de datos."""

        pass

    @abstractmethod
    async def update_wholesaler(self, instance: Wholesaler, data: dict[str, Any]) -> Wholesaler:
        """Actualiza un cliente mayorista en la base de datos."""

        pass

    @abstractmethod
    async def exists_wholesaler(self, filters: dict[str, Any]) -> bool:
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
