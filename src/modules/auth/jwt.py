from datetime import UTC, datetime, timedelta
from typing import Annotated, Any
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import MissingJWT, UserNotFound
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.auth.models.user import User
from src.modules.auth.repositories.user import UserRepository


class JWTAuthentication:
    """
    Dependencia que extrae estrictamente el token de acceso y de refresco
    desde las cookies HTTPOnly.
    """

    async def __call__(self, request: Request) -> tuple[str, str]:
        """Extrae los tokens de acceso y refresco de las cookies de la petición."""

        # Extraer tokens exclusivamente de las cookies
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token or not refresh_token:
            raise MissingJWT()

        return access_token, refresh_token


get_raw_tokens = JWTAuthentication()


def create_access_token(user_id: UUID, user_role: str) -> str:
    """
    Genera un token JWT de acceso con la información del usuario y su rol, utilizando una clave
    privada para su firma.
    """

    now = datetime.now(tz=UTC)
    payload = {
        "sub": str(user_id),
        "user_role": user_role,
        "exp": now + timedelta(minutes=settings.access_token_expire),
        "nbf": now,
        "jti": str(uuid4()),
        "token_type": "access",
    }
    encoded_jwt = jwt.encode(
        payload=payload,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def create_refresh_token(user_id: UUID) -> str:
    """
    Genera un token JWT de refresco con una vida útil más larga. Su único propósito es ser canjeado
    por un nuevo token de acceso cuando este expire.
    """

    now = datetime.now(tz=UTC)
    payload = {
        "sub": str(user_id),
        "exp": now + timedelta(minutes=settings.refresh_token_expire),
        "nbf": now,
        "jti": str(uuid4()),
        "token_type": "refresh",
    }
    encoded_jwt = jwt.encode(
        payload=payload,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


async def get_user(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> tuple[User, Any]:
    """
    Decodifica el token de acceso de la cookie de la petición y retorna el usuario al que
    pertenece.
    """

    # Decodificar el token de acceso del usuario
    access_token, _ = tokens
    payload = jwt.decode(
        jwt=access_token,
        key=settings.public_key,
        algorithms=[settings.jwt_algorithm],
    )
    user_id = UUID(payload["sub"])

    # Buscamos el usuario
    exists = await UserRepository.exists_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )

    if not exists:
        raise UserNotFound()

    return await UserRepository.get_user(
        role=payload["user_role"],
        filters={"id": user_id},
        db=db,
    )
