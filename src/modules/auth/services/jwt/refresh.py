from uuid import UUID

import jwt

from src.common.exceptions import (
    AuthenticationFailed,
    DomainRuleViolation,
    InvalidJWT,
    UserNotFound,
)
from src.config.parameters import settings
from src.modules.auth.constants import ExceptionErrorMessages
from src.modules.auth.jwt import create_access_token
from src.modules.auth.repositories.interfaces import IUserRepository


class RefreshTokenService:
    """Servicio encargado de la validación y renovación de tokens de acceso JWT."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def refresh_token(self, access_token: str, refresh_token: str) -> str:
        """
        Renueva un token de acceso expirado utilizando un token de actualización válido.

        Raises:
            InvalidJWT: Si alguno de los tokens posee una estructura o firma inválida, o si el
                token de actualización ha expirado.
            DomainRuleViolation: Si el token de acceso aún no ha expirado o si los identificadores
                de usuario en ambos tokens no coinciden.
            U
        """

        access_token_expired = False

        # Validaciones del token de acceso
        try:
            access_token_payload = jwt.decode(
                jwt=access_token,
                key=settings.public_key,
                algorithms=[settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            access_token_payload = jwt.decode(
                jwt=access_token,
                key=settings.public_key,
                algorithms=[settings.jwt_algorithm],
                options={"verify_exp": False},
            )
            access_token_expired = True
        except jwt.InvalidTokenError:
            raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_INVALID.value)  # noqa

        if not access_token_expired:
            raise DomainRuleViolation(message=ExceptionErrorMessages.ACCESS_JWT_NOT_EXPIRED.value)

        # Validaciones del token de actualización
        try:
            refresh_token_payload = jwt.decode(
                jwt=refresh_token,
                key=settings.public_key,
                algorithms=[settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise InvalidJWT(message=ExceptionErrorMessages.REFRESH_JWT_EXPIRED.value)  # noqa
        except jwt.InvalidTokenError:
            raise InvalidJWT(message=ExceptionErrorMessages.REFRESH_JWT_INVALID.value)  # noqa

        # Validación del usuario del token de acceso
        if access_token_payload["sub"] != refresh_token_payload["sub"]:
            await self.__user_repo.increment_session_versions(
                user_ids=[
                    UUID(access_token_payload["sub"]),
                    UUID(refresh_token_payload["sub"]),
                ],
            )

            raise DomainRuleViolation(message=ExceptionErrorMessages.SESSION_CORRUPTED.value)

        instance = await self.__user_repo.get_user(
            role=access_token_payload["user_role"],
            id=UUID(access_token_payload["sub"]),
        )

        if not instance:
            raise UserNotFound(message=ExceptionErrorMessages.JWT_USER_NOT_FOUND.value)

        if instance.session_version != refresh_token_payload["session_version"]:
            raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

        return create_access_token(
            user_id=UUID(access_token_payload["sub"]),
            session_version=instance.session_version,
            user_role=instance.role,
        )
