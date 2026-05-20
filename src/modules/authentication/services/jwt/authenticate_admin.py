from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import AuthenticationError
from src.modules.authentication.constants import UserRoles
from src.modules.authentication.dto import AdminCredentialsDTO
from src.modules.authentication.jwt import create_access_token, create_refresh_token
from src.modules.authentication.repositories.interfaces import IUserRepository


class AuthAdminService:
    """Servicio para la autenticación de administradores."""

    def __init__(self, user_repo: type[IUserRepository], session: AsyncSession) -> None:
        self.user_repo = user_repo
        self.session = session

    async def authenticate_admin(self, credentials: AdminCredentialsDTO) -> tuple[str, str]:
        """
        Autentica un administrador en la base de datos. Si las credenciales son válidas,
        devuelve un par de tokens de acceso y actualización.
        """

        password = credentials.password
        email = credentials.email
        user_account, _ = await self.user_repo.get_user(
            session=self.session,
            filters={"email": email},
            role=UserRoles.ADMINISTRATOR.value,
        )

        if not user_account:
            raise AuthenticationError()
        if not user_account.has_permission(permission_name="authentication.jwt"):
            raise AuthenticationError()
        if not user_account.verify_password(password=password):
            raise AuthenticationError()

        access_token = create_access_token(
            user_id=user_account.id,
            user_role=user_account.role,
        )
        refresh_token = create_refresh_token(user_id=user_account.id)

        return access_token, refresh_token
