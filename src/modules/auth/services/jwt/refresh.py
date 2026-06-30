from uuid import UUID

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import DomainRuleViolation, InvalidJWT
from src.config.parameters import settings
from src.modules.auth.constants import ExceptionErrorMessages
from src.modules.auth.jwt import create_access_token
from src.modules.auth.repositories.interfaces import IUserRepository


class RefreshTokenService:
    """Servicio encargado de gestionar la renovación de tokens de acceso (JWT)."""

    def __init__(self, user_repo: type[IUserRepository], db: AsyncSession) -> None:
        self.__user_repo = user_repo
        self.__db = db

    async def refresh_token(self, access_token: str, refresh_token: str) -> str:
        """Genera un nuevo token de acceso a partir de un token de refresco válido."""

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
                db=self.__db,
                user_ids=[
                    UUID(access_token_payload["sub"]),
                    UUID(refresh_token_payload["sub"]),
                ],
            )

            raise DomainRuleViolation(message=ExceptionErrorMessages.SESSION_CORRUPTED.value)

        user_account, _ = await self.__user_repo.get_user(
            filters={"id": UUID(access_token_payload["sub"])},
            role=access_token_payload["user_role"],
            db=self.__db,
        )

        return create_access_token(
            user_id=UUID(access_token_payload["sub"]),
            session_version=user_account.session_version,
            user_role=user_account.role,
        )
