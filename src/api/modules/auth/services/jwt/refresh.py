from uuid import UUID

import jwt

from src.api.common.exceptions import (
    AuthenticationFailed,
    InvalidJWT,
    UserNotFound,
)
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.jwt import create_access_token
from src.api.modules.auth.repositories.interfaces import IUserRepository
from src.api.settings.parameters import api_parameters


class RefreshTokenService:
    """Servicio encargado de la validación y renovación de tokens de acceso JWT."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def refresh_token(self, refresh_token: str) -> str:
        """
        Renueva un token de acceso expirado utilizando un token de actualización válido.

        Raises:
            InvalidJWT: Si alguno de los tokens posee una estructura o firma inválida, o si el
                token de actualización ha expirado.
            DomainRuleViolation: Si el token de acceso aún no ha expirado o si los identificadores
                de usuario en ambos tokens no coinciden.
            UserNotFound: Si el usuario codificado en el token de actualización no existe.
            AuthenticationFailed: Si la versión de sesión del usuario ha caducado.
        """

        # Validaciones del token de actualización
        try:
            refresh_token_payload = jwt.decode(
                jwt=refresh_token,
                key=api_parameters.public_key,
                algorithms=[api_parameters.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise InvalidJWT(message=ExceptionErrorMessages.REFRESH_JWT_EXPIRED.value)  # noqa
        except jwt.InvalidTokenError:
            raise InvalidJWT(message=ExceptionErrorMessages.REFRESH_JWT_INVALID.value)  # noqa

        instance = await self.__user_repo.get_user(
            role=refresh_token_payload["user_role"],
            id=UUID(refresh_token_payload["sub"]),
        )

        if not instance:
            raise UserNotFound(message=ExceptionErrorMessages.JWT_USER_NOT_FOUND.value)

        if instance.session_version != refresh_token_payload["session_version"]:
            raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

        return create_access_token(
            user_id=UUID(refresh_token_payload["sub"]),
            session_version=instance.session_version,
            user_role=instance.role,
        )
