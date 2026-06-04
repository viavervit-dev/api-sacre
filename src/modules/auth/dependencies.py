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

    async def __call__(self, request: Request) -> tuple[str, str]:
        """Extrae los tokens de acceso y refresco de las cookies de la petición."""

        # Extraer tokens exclusivamente de las cookies
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token or not refresh_token:
            raise MissingJWT()

        return access_token, refresh_token


get_raw_tokens = JWTAuthentication()


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


class UserPermissionChecker:
    """Verifica si el usuario autenticado posee los permisos requeridos."""

    def __init__(self, allowed_role: str, permission: str) -> None:
        self.__allowed_role = allowed_role
        self.__permission = permission

    async def __call__(
        self, user: Annotated[tuple[User, Any], Depends(get_user)]
    ) -> tuple[User, Any]:
        """Extrae el usuario autenticado y verifica su rol."""

        user_account, user_profile = user

        # Verificamos si el rol del usuario es el permitido
        if user_account.role != self.__allowed_role:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        if not user_account.has_permission(permission_name=self.__permission):
            raise PermissionDenied()

        return user_account, user_profile
