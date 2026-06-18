from typing import Annotated, Any
from uuid import UUID

import jwt
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import MissingJWT, PermissionDenied, UserNotFound
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.auth.models.user import User
from src.modules.auth.repositories.user import UserRepository


class JWTAuthentication:
    """
    Dependencia que extrae estrictamente el token de acceso y de refresco
    desde las cookies HTTPOnly.
    """

    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> tuple[str | None, str | None]:
        """Extrae los tokens de acceso y refresco de las cookies de la petición."""

        # Extraer tokens exclusivamente de las cookies
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token or not refresh_token:
            if self.auto_error:
                raise MissingJWT()

            return None, None

        return access_token, refresh_token


# Instancia opcional para flujos donde permitimos usuarios anónimos
get_optional_raw_tokens = JWTAuthentication(auto_error=False)

# Instancia estricta para flujos donde se requieren usuarios autenticados
get_raw_tokens = JWTAuthentication(auto_error=True)


async def get_user(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> tuple[User, Any]:
    """
    Decodifica el token de acceso de la cookie de la petición y retorna el usuario al que
    pertenece.
    """

    # Decodificar el token de acceso del usuario
    access_token, _ = tokens
    payload = jwt.decode(
        jwt=access_token,
        key=settings.public_key,
        algorithms=[settings.jwt_algorithm],
    )
    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    exists = await UserRepository.exists_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )

    if not exists:
        raise UserNotFound()

    return await UserRepository.get_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )


async def get_user_optional(
    tokens: Annotated[tuple[str | None, str | None], Depends(get_optional_raw_tokens)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> tuple[User | None, Any | None]:
    """
    Decodifica el token de acceso de la cookie de la petición y retorna el usuario al que
    pertenece.
    """

    # Decodificar el token de acceso del usuario
    access_token, _ = tokens

    if not access_token:
        return None, None

    payload = jwt.decode(
        jwt=access_token,
        key=settings.public_key,
        algorithms=[settings.jwt_algorithm],
    )
    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    exists = await UserRepository.exists_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )

    if not exists:
        raise UserNotFound()

    return await UserRepository.get_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )


class UserPermissionChecker:
    """Verifica si el usuario autenticado posee los permisos requeridos."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(
        self,
        user: Annotated[tuple[User, Any], Depends(get_user)],
    ) -> tuple[User, Any]:
        """Extrae el usuario autenticado y verifica su rol."""

        user_account, user_profile = user

        # Verificamos si el rol del usuario es el permitido
        if user_account.role not in self.__allowed_roles:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user_account.role == role and not user_account.has_permission(
                permission_name=permission
            ):
                raise PermissionDenied()

        return user_account, user_profile


class UserOptionalPermissionChecker:
    """Verifica si el usuario autenticado posee los permisos requeridos."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(
        self,
        user: Annotated[tuple[User | None, Any | None], Depends(get_user_optional)],
    ) -> tuple[User | None, Any | None]:
        """Extrae el usuario autenticado y verifica su rol."""

        user_account, user_profile = user

        if not user_account:
            return None, None

        # Verificamos si el rol del usuario es el permitido
        if user_account.role not in self.__allowed_roles:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user_account.role == role and not user_account.has_permission(
                permission_name=permission
            ):
                raise PermissionDenied()

        return user_account, user_profile
