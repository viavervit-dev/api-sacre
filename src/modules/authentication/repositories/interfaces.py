from abc import ABC, abstractmethod
from typing import Any, Literal, overload

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.admins.models.admin import Admin
from src.modules.authentication.models.user import User
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
        session: AsyncSession,
        filters: dict[str, Any],
        role: Literal["customer"],
    ) -> tuple[User | None, Customer]: ...

    @classmethod
    @overload
    async def get_user(
        cls,
        session: AsyncSession,
        filters: dict[str, Any],
        role: Literal["admin"],
    ) -> tuple[User | None, Admin]: ...

    @classmethod
    @abstractmethod
    async def get_user(
        cls,
        session: AsyncSession,
        filters: dict[str, Any],
        role: str,
    ) -> tuple[User | None, Any]:
        """Obtiene un usuario que coincida con los filtros proporcionados."""

        pass
