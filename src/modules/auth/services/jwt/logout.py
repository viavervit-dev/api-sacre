from uuid import UUID

import jwt

from src.common.exceptions import InvalidJWT
from src.config.parameters import settings
from src.modules.auth.constants import ExceptionErrorMessages
from src.modules.auth.repositories.interfaces import IUserRepository


class LogoutService:
    """Servicio encargado de gestionar la invalidación de sesiones de usuario."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def logout(self, access_token: str, refresh_token: str) -> None:
        """
        Invalida la sesión activa de un usuario verificando sus tokens de acceso y actualización.

        Raises:
            InvalidJWT: Si alguno de los tokens es inválido o ha expirado. Si los identificadores
                de usuario en ambos tokens no coinciden.
        """

        # Validaciones del token de acceso
        try:
            access_token_payload = jwt.decode(
                jwt=access_token,
                key=settings.public_key,
                algorithms=[settings.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_EXPIRED.value)  # noqa
        except jwt.InvalidTokenError:
            raise InvalidJWT(message=ExceptionErrorMessages.ACCESS_JWT_INVALID.value)  # noqa

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

            raise InvalidJWT(message=ExceptionErrorMessages.SESSION_CORRUPTED.value)

        await self.__user_repo.increment_session_versions(
            user_ids=[UUID(access_token_payload["sub"])],
        )
