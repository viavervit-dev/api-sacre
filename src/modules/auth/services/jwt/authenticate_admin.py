from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import AuthenticationFailed
from src.modules.auth.constants import ExceptionErrorMessages, UserRoles
from src.modules.auth.dto import AdminCredentialsDTO
from src.modules.auth.jwt import create_access_token, create_refresh_token
from src.modules.auth.repositories.interfaces import IUserRepository


class AuthAdminService:
    """Servicio para la autenticación de administradores."""

    def __init__(self, user_repo: type[IUserRepository], db: AsyncSession) -> None:
        self.__user_repo = user_repo
        self.__db = db

    async def authenticate_admin(self, credentials: AdminCredentialsDTO) -> tuple[str, str]:
        """
        Autentica un administrador en la base de datos. Si las credenciales son válidas,
        devuelve un par de tokens de acceso y actualización.
        """

        password = credentials.password
        email = credentials.email
        user_account, _ = await self.__user_repo.get_user(
            db=self.__db,
            filters={"email": email},
            role=UserRoles.ADMINISTRATOR.value,
        )

        if not user_account:
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)
        if not user_account.has_permission(permission_name="authentication.jwt"):
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)
        if not user_account.verify_password(password=password):
            raise AuthenticationFailed(message=ExceptionErrorMessages.CREDENTIALS_INVALID.value)

        access_token = create_access_token(
            session_version=user_account.session_version,
            user_id=user_account.id,
        )
        refresh_token = create_refresh_token(
            session_version=user_account.session_version,
            user_id=user_account.id,
        )

        return access_token, refresh_token
