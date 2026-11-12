from uuid import UUID

from src.api.common.exceptions import InvalidJWT
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.jwt import decode_token
from src.api.modules.auth.repositories.interfaces import IUserRepository


class LogoutService:
    """Servicio encargado de gestionar la invalidación de sesiones de usuario."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def logout(self, access_token: str, refresh_token: str) -> None:
        """
        Invalida la sesión activa de un usuario verificando sus tokens de acceso y actualización.

        Raises:
            InvalidJWT: Si los identificadores de usuario en ambos tokens no coinciden.
        """

        access_token_payload = decode_token(token=access_token, expected_type="access")
        refresh_token_payload = decode_token(token=refresh_token, expected_type="refresh")

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
