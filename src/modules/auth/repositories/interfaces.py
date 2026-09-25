from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Literal, overload
from uuid import UUID

from src.modules.auth.models.user import User


class IUserRepository(ABC):
    """Contrato de persistencia para operaciones sobre usuarios (`auth.users`)."""

    @overload
    async def get_user(
        self,
        role: Literal["customer"],
        id: UUID | None = None,
        email: str | None = None,
        load_permissions: bool = True,
    ) -> User | None: ...

    @overload
    async def get_user(
        self,
        role: Literal["admin"],
        id: UUID | None = None,
        email: str | None = None,
        load_permissions: bool = True,
    ) -> User | None: ...

    @abstractmethod
    async def get_user(
        self,
        role: str,
        id: UUID | None = None,
        email: str | None = None,
        load_permissions: bool = True,
    ) -> User | None:
        """Obtiene un usuario por ID o email, cargando su perfil según el rol y sus permisos."""

        pass

    @abstractmethod
    async def create_user(
        self,
        email: str,
        password: str,
        role: str,
    ) -> User:
        """Crea y registra un nuevo usuario asignándole su rol y grupo de permisos inicial."""

        pass

    @abstractmethod
    async def exists_user(self, filters: dict[str, Any]) -> bool:
        """Verifica si existe al menos un usuario que coincida con los filtros especificados."""

        pass

    @abstractmethod
    async def increment_session_versions(self, user_ids: Sequence[UUID]) -> None:
        """Incrementa en uno la versión de sesión de múltiples usuarios para revocar tokens."""

        pass
