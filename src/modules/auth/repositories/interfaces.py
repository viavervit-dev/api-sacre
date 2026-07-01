from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Literal, overload
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.admins.models.admin import Admin
from src.modules.auth.models.user import User
from src.modules.customers.models.customer import Customer


class IUserRepository(ABC):
    """
    Interfaz de `UserRepository`, define el contrato para un repositorio que administra la
    tabla `auth.users` en la base de datos.
    """

    @classmethod
    @overload
    async def get_user(
        cls,
        db: AsyncSession,
        filters: dict[str, Any],
        role: Literal["customer"],
    ) -> tuple[User, Customer]: ...

    @classmethod
    @overload
    async def get_user(
        cls,
        db: AsyncSession,
        filters: dict[str, Any],
        role: Literal["admin"],
    ) -> tuple[User, Admin]: ...

    @classmethod
    @abstractmethod
    async def get_user(
        cls,
        db: AsyncSession,
        filters: dict[str, Any],
        role: str,
    ) -> tuple[User, Any]:
        """Obtiene un usuario que coincida con los filtros proporcionados."""

        pass

    @classmethod
    @abstractmethod
    async def exists_user(cls, db: AsyncSession, filters: dict[str, Any], role: str) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass

    @classmethod
    @overload
    async def create_user(
        cls,
        db: AsyncSession,
        user_data: dict[str, Any],
        profile_data: dict[str, Any],
        role: Literal["customer"],
    ) -> tuple[User, Customer]: ...

    @classmethod
    @overload
    async def create_user(
        cls,
        db: AsyncSession,
        user_data: dict[str, Any],
        profile_data: dict[str, Any],
        role: Literal["admin"],
    ) -> tuple[User, Admin]: ...

    @classmethod
    @abstractmethod
    async def create_user(
        cls,
        db: AsyncSession,
        user_data: dict[str, Any],
        profile_data: dict[str, Any],
        role: str,
    ) -> tuple[User, Any]:
        """Crea un nuevo usuario y su perfil asociado en la base de datos."""

        pass

    @classmethod
    @abstractmethod
    async def increment_session_versions(cls, db: AsyncSession, user_ids: Sequence[UUID]) -> None:
        """Incrementa en 1 la versión de la sesión de múltiples usuarios en una sola consulta."""

        pass


class IJWTBlacklistRepository(ABC):
    """
    Interfaz de `JWTBlacklistRepository`, define el contrato para un repositorio que administra la
    tabla `auth.json_web_token_blacklist` en la base de datos.
    """

    @classmethod
    @abstractmethod
    async def exists_token(cls, db: AsyncSession, jti: str) -> bool:
        """Consulta si existe al menos un registro que coincida con los filtros proporcionados."""

        pass

    @classmethod
    @abstractmethod
    async def add_to_list(cls, db: AsyncSession, data: dict[str, Any]) -> None:
        """Agrega un token a la lista negra."""

        pass
