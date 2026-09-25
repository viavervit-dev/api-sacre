from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import (
    AuthenticationFailed,
    InvalidJWT,
    MissingJWT,
    PermissionDenied,
    UserNotFound,
)
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.auth.constants import ExceptionErrorMessages
from src.modules.auth.models.user import User
from src.modules.auth.repositories.interfaces import IUserRepository
from src.modules.auth.repositories.user import UserRepository
from src.modules.auth.services.jwt.authenticate_admin import AuthAdminService
from src.modules.auth.services.jwt.get_current_user import RetrieveCurrentUserService
from src.modules.auth.services.jwt.logout import LogoutService
from src.modules.auth.services.jwt.refresh import RefreshTokenService


class JWTAuthentication:
    """Dependencia para extraer tokens JWT de acceso y actualización desde cookies HTTP."""

    def __init__(self, auto_error: bool = True) -> None:
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> tuple[str | None, str | None]:
        """
        Extrae los tokens JWT de las cookies de la solicitud HTTP.

        Raises:
            MissingJWT: Si auto_error es True y falta alguno de los tokens requeridos.
        """

        # Extraer tokens exclusivamente de las cookies
        access_token = request.cookies.get("access_token", None)
        refresh_token = request.cookies.get("refresh_token", None)

        if not access_token and self.auto_error:
            raise MissingJWT(message=ExceptionErrorMessages.ACCESS_JWT_MISSING.value)
        if not refresh_token and self.auto_error:
            raise MissingJWT(message=ExceptionErrorMessages.REFRESH_JWT_MISSING.value)

        return access_token, refresh_token


# Instancia opcional para flujos donde permitimos usuarios anónimos
get_optional_raw_tokens = JWTAuthentication(auto_error=False)

# Instancia estricta para flujos donde se requieren usuarios autenticados
get_raw_tokens = JWTAuthentication(auto_error=True)


def get_user_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> IUserRepository:
    """Provee una instancia del repositorio de usuarios."""

    return UserRepository(db=db)


async def get_user(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
) -> User:
    """
    Obtiene y valida el usuario autenticado a partir del token de acceso obligatorio.

    Raises:
        InvalidJWT: Si el token de acceso es inválido o ha expirado.
        UserNotFound: Si el usuario codificado en el token no existe.
        AuthenticationFailed: Si la versión de sesión del usuario ha caducado.
    """

    access_token, _ = tokens

    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.public_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_EXPIRED.value)  # noqa
    except jwt.InvalidTokenError:
        raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_INVALID.value)  # noqa

    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    instance = await user_repo.get_user(role=payload["user_role"], id=user_id)

    if not instance:
        raise UserNotFound(message=ExceptionErrorMessages.JWT_USER_NOT_FOUND.value)

    if instance.session_version != payload["session_version"]:
        raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

    return instance


async def get_user_optional(
    tokens: Annotated[tuple[str | None, str | None], Depends(get_optional_raw_tokens)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
) -> User | None:
    """
    Obtiene y valida el usuario autenticado de forma opcional.

    Raises:
        InvalidJWT: Si el token proporcionado es inválido o ha expirado.
        UserNotFound: Si el usuario referenciado en el token no existe.
        AuthenticationFailed: Si la versión de sesión del usuario ha caducado.
    """

    access_token, _ = tokens

    if not access_token:
        return None

    try:
        payload = jwt.decode(
            jwt=access_token,
            key=settings.public_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_EXPIRED.value)  # noqa
    except jwt.InvalidTokenError:
        raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_INVALID.value)  # noqa

    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    instance = await user_repo.get_user(role=payload["user_role"], id=user_id)

    if not instance:
        raise UserNotFound(message=ExceptionErrorMessages.JWT_USER_NOT_FOUND.value)

    if instance.session_version != payload["session_version"]:
        raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

    return instance


class UserPermissionChecker:
    """Dependencia para validar roles y permisos específicos en usuarios autenticados."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(self, user: Annotated[User, Depends(get_user)]) -> User:
        """
        Verifica que el usuario cumpla con los roles y permisos configurados.

        Raises:
            PermissionDenied: Si el rol o los permisos requeridos no son satisfechos.
        """

        # Verificamos si el rol del usuario es el permitido
        if user.role not in self.__allowed_roles:
            raise PermissionDenied(message=ExceptionErrorMessages.PERMISSION_DENIED.value)

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user.role == role and not user.has_permission(permission_name=permission):
                raise PermissionDenied(message=ExceptionErrorMessages.PERMISSION_DENIED.value)

        return user


class UserOptionalPermissionChecker:
    """Dependencia para validar roles y permisos de forma opcional si existe usuario."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(
        self,
        user: Annotated[User | None, Depends(get_user_optional)],
    ) -> User | None:
        """
        Verifica roles y permisos si hay un usuario autenticado en la solicitud.

        Raises:
            PermissionDenied: Si habiendo usuario, no cumple con el rol o permiso requerido.
        """

        if not user:
            return None

        # Verificamos si el rol del usuario es el permitido
        if user.role not in self.__allowed_roles:
            raise PermissionDenied(message=ExceptionErrorMessages.PERMISSION_DENIED.value)

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user.role == role and not user.has_permission(permission_name=permission):
                raise PermissionDenied(message=ExceptionErrorMessages.PERMISSION_DENIED.value)

        return user


def get_retrieve_user_service() -> type[RetrieveCurrentUserService]:
    """Provee la clase del servicio de consulta de usuario actual."""

    return RetrieveCurrentUserService


def get_jwt_admin_service(
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
) -> AuthAdminService:
    """Provee una instancia del servicio de autenticación de administradores."""

    return AuthAdminService(user_repo=user_repo)


def get_jwt_logout_service(
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
) -> LogoutService:
    """Provee una instancia del servicio de cierre de sesión."""

    return LogoutService(user_repo=user_repo)


def get_jwt_refresh_token_service(
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
) -> RefreshTokenService:
    """Provee una instancia del servicio de renovación de tokens."""

    return RefreshTokenService(user_repo=user_repo)
