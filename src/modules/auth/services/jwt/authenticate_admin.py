from src.common.exceptions import AuthenticationFailed
from src.modules.auth.constants import ExceptionErrorMessages, UserRoles
from src.modules.auth.dto import AdminCredentialsDTO
from src.modules.auth.jwt import create_access_token, create_refresh_token
from src.modules.auth.repositories.interfaces import IUserRepository


class AuthAdminService:
    """Servicio encargado de la autenticación y emisión de tokens JWT para administradores."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self.__user_repo = user_repo

    async def authenticate_admin(self, credentials: AdminCredentialsDTO) -> tuple[str, str]:
        """
        Autentica a un administrador y genera tokens de acceso y actualización.

        Raises:
            AuthenticationFailed: Si el usuario no existe, carece de permisos o la
                contraseña es inválida.
        """

        password = credentials.password
        email = credentials.email
        instance = await self.__user_repo.get_user(role=UserRoles.ADMINISTRATOR.value, email=email)

        if not instance:
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)
        if not instance.has_permission(permission_name="authentication.jwt"):
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)
        if not instance.verify_password(password=password):
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)

        access_token = create_access_token(
            session_version=instance.session_version,
            user_role=UserRoles.ADMINISTRATOR.value,
            user_id=instance.id,
        )
        refresh_token = create_refresh_token(
            session_version=instance.session_version,
            user_role=UserRoles.ADMINISTRATOR.value,
            user_id=instance.id,
        )

        return access_token, refresh_token
