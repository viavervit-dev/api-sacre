from contextlib import suppress
from uuid import UUID

from src.api.common.exceptions import AuthenticationFailed, InvalidJWT
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.jwt import decode_token
from src.api.modules.auth.repositories.interfaces import IUserRepository


class LogoutService:
    """Servicio encargado de gestionar la invalidación de sesiones de usuario."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def logout(self, access_token: str | None, refresh_token: str) -> None:
        """
        Invalida la sesión activa de un usuario verificando la vigencia y `session_version`
        del token de actualización y comprobando coherencia si existe un token de acceso.

        Raises:
            AuthenticationFailed: Si el token de actualización ya fue revocado o la sesión expiró.
            InvalidJWT: Si los identificadores de usuario en ambos tokens no coinciden.
        """

        refresh_token_payload = decode_token(token=refresh_token, expected_type="refresh")
        refresh_user_id = UUID(refresh_token_payload["sub"])
        refresh_session_version = int(refresh_token_payload["session_version"])
        updated_ids = await self.__user_repo.increment_session_versions(
            sessions=[(refresh_user_id, refresh_session_version)],
        )

        if not updated_ids:
            raise AuthenticationFailed(message=ExceptionErrorMessages.AUTH_SESSION_EXPIRED.value)

        if access_token:
            with suppress(InvalidJWT, ValueError):
                access_token_payload = decode_token(
                    token=access_token,
                    expected_type="access",
                    verify_exp=False,
                )
                access_user_id = UUID(access_token_payload["sub"])

                if access_user_id != refresh_user_id:
                    access_session_version = int(access_token_payload["session_version"])
                    await self.__user_repo.increment_session_versions(
                        sessions=[(access_user_id, access_session_version)],
                    )

                    raise InvalidJWT(message=ExceptionErrorMessages.SESSION_CORRUPTED.value)
