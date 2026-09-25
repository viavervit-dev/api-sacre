from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.modules.admins.models.admin import Admin


class IAdminRepository(ABC):
    """Contrato de persistencia para el perfil de administradores (`admin.admins`)."""

    @abstractmethod
    async def create_admin(self, user_id: UUID, data: dict[str, Any]) -> Admin:
        """Crea y registra un nuevo perfil de administrador asociado a una cuenta de usuario."""

        pass

    @abstractmethod
    async def exists_admin(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un administrador que coincida con los filtros especificados."""

        pass
