from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from src.api.modules.auth.models.user import User


class IUserRepository(ABC):
    """Contrato de persistencia para operaciones sobre usuarios (`auth.users`)."""

    @abstractmethod
    async def get_user(
        self,
        filters: dict[str, Any],
        load_permissions: bool = True,
    ) -> User | None:
        """Obtiene un usuario aplicando filtros dinámicos y cargando su perfil y permisos."""

        pass

    @abstractmethod
    async def get_list_users(
        self,
        offset: int,
        limit: int,
        filters: dict[str, Any],
        load_permissions: bool = True,
    ) -> tuple[Sequence[User], int]:
        """Obtiene una lista paginada y ordenada de usuarios junto con el total de registros."""

        pass

    @abstractmethod
    async def create_user(
        self,
        email: str,
        password: str,
        role: str,
    ) -> User:
        """Crea un nuevo usuario asignándole su rol y grupo de permisos inicial."""

        pass

    @abstractmethod
    async def exists_user(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe un usuario que coincida con los filtros especificados."""

        pass

    @abstractmethod
    async def increment_session_versions(self, user_ids: Sequence[UUID]) -> None:
        """Incrementa en uno la versión de sesión de múltiples usuarios para revocar tokens."""

        pass
