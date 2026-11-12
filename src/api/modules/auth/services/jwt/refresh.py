from uuid import UUID

from src.api.common.exceptions import (
    AuthenticationFailed,
    UserNotFound,
)
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.jwt import create_access_token, decode_token
from src.api.modules.auth.repositories.interfaces import IUserRepository


class RefreshTokenService:
    """Servicio encargado de la validación y renovación de tokens de acceso JWT."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def refresh(self, refresh_token: str) -> str:
        """
        Renueva un token de acceso expirado utilizando un token de actualización válido.

        Raises:
            UserNotFound: Si el usuario codificado en el token de actualización no existe.
            AuthenticationFailed: Si la versión de sesión del usuario ha caducado.
        """

        refresh_token_payload = decode_token(token=refresh_token, expected_type="refresh")
        instance = await self.__user_repo.get_user(
            filters={
                "id": UUID(refresh_token_payload["sub"]),
                "role": refresh_token_payload["user_role"],
            }
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
