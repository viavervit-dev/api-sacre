from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request

from src.api.common.exceptions import (
    AuthenticationFailed,
    MissingJWT,
    PermissionDenied,
    UserNotFound,
)
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.jwt import decode_token
from src.api.modules.auth.models import User
from src.api.modules.auth.repositories import UserRepository
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.modules.auth.services.jwt import (
    AuthenticateAdminService,
    GetAuthenticatedUserService,
    LogoutService,
    RefreshTokenService,
)
from src.api.settings.database import DBSessionDep


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
get_tokens_optional = JWTAuthentication(auto_error=False)
TokensOptionalDep = Annotated[tuple[str | None, str | None], Depends(get_tokens_optional)]

# Instancia estricta para flujos donde se requieren usuarios autenticados
get_tokens = JWTAuthentication(auto_error=True)
TokensDep = Annotated[tuple[str, str], Depends(get_tokens)]


def user_repository(db: DBSessionDep) -> IUserRepository:
    """Provee una instancia del repositorio de usuarios."""

    return UserRepository(db=db)


UserRepositoryDep = Annotated[UserRepository, Depends(user_repository)]


async def get_user(tokens: TokensDep, user_repo: UserRepositoryDep) -> User:
    """
    Obtiene y valida el usuario autenticado a partir del token de acceso obligatorio.

    Raises:
        InvalidJWT: Si el token de acceso es inválido o ha expirado.
        UserNotFound: Si el usuario codificado en el token no existe.
        AuthenticationFailed: Si la versión de sesión del usuario ha caducado.
    """

    access_token, _ = tokens
    payload = decode_token(token=access_token, expected_type="access")
    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    instance = await user_repo.get_user(filters={"id": user_id, "role": payload["user_role"]})

    if not instance:
        raise UserNotFound()

    if instance.session_version != payload["session_version"]:
        raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

    return instance


UserDep = Annotated[User, Depends(get_user)]


async def get_user_optional(
    tokens: TokensOptionalDep,
    user_repo: UserRepositoryDep,
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

    payload = decode_token(token=access_token, expected_type="access")
    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    instance = await user_repo.get_user(filters={"id": user_id, "role": payload["user_role"]})

    if not instance:
        raise UserNotFound()

    if instance.session_version != payload["session_version"]:
        raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

    return instance


UserOptionalDep = Annotated[User | None, Depends(get_user_optional)]


class UserPermissionChecker:
    """Dependencia para validar roles y permisos específicos en usuarios autenticados."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(self, user: UserDep) -> User:
        """
        Verifica que el usuario cumpla con los roles y permisos configurados.

        Raises:
            PermissionDenied: Si el rol o los permisos requeridos no son satisfechos.
        """

        # Verificamos si el rol del usuario es el permitido
        if user.role not in self.__allowed_roles:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user.role == role and not user.has_permission(permission_name=permission):
                raise PermissionDenied()

        return user


class UserOptionalPermissionChecker:
    """Dependencia para validar roles y permisos de forma opcional si existe usuario."""

    def __init__(self, allowed_roles: list[str], permissions: dict[str, str]) -> None:
        self.__allowed_roles = allowed_roles
        self.__permissions = permissions

    async def __call__(self, user: UserOptionalDep) -> User | None:
        """
        Verifica roles y permisos si hay un usuario autenticado en la solicitud.

        Raises:
            PermissionDenied: Si habiendo usuario, no cumple con el rol o permiso requerido.
        """

        if not user:
            return None

        # Verificamos si el rol del usuario es el permitido
        if user.role not in self.__allowed_roles:
            raise PermissionDenied()

        # Verificamos si el usuario tiene el permiso específico requerido
        for role, permission in self.__permissions.items():
            if user.role == role and not user.has_permission(permission_name=permission):
                raise PermissionDenied()

        return user


def retrieve_user_service() -> type[GetAuthenticatedUserService]:
    """Provee la clase del servicio que obtiene la instancia del usuario autenticado con JWT."""

    return GetAuthenticatedUserService


GetAuthenticatedUserServiceDep = Annotated[
    type[GetAuthenticatedUserService], Depends(retrieve_user_service)
]


def authenticate_admin_service(user_repo: UserRepositoryDep) -> AuthenticateAdminService:
    """Provee una instancia del servicio de autenticación de administradores."""

    return AuthenticateAdminService(user_repo=user_repo)


AuthenticateAdminServiceDep = Annotated[
    AuthenticateAdminService, Depends(authenticate_admin_service)
]


def logout_service(user_repo: UserRepositoryDep) -> LogoutService:
    """Provee una instancia del servicio de cierre de sesión."""

    return LogoutService(user_repo=user_repo)


LogoutServiceDep = Annotated[LogoutService, Depends(logout_service)]


def refresh_token_service(user_repo: UserRepositoryDep) -> RefreshTokenService:
    """Provee una instancia del servicio de renovación de tokens."""

    return RefreshTokenService(user_repo=user_repo)


RefreshTokenServiceDep = Annotated[RefreshTokenService, Depends(refresh_token_service)]
