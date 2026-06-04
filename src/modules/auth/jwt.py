from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt

from src.config.parameters import settings


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



