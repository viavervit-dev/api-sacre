from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from uuid import UUID, uuid4

import jwt

from src.api.common.exceptions import InvalidJWT
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.settings.parameters import api_parameters


def create_access_token(user_id: UUID, user_role: str, session_version: int) -> str:
    """
    Genera un token JWT de acceso con la información del usuario y su rol, utilizando una clave
    privada para su firma.
    """

    now = datetime.now(tz=UTC)
    payload = {
        "sub": str(user_id),
        "exp": now + timedelta(minutes=api_parameters.access_token_expire),
        "nbf": now,
        "jti": str(uuid4()),
        "user_role": user_role,
        "session_version": session_version,
        "token_type": "access",
    }
    encoded_jwt = jwt.encode(
        payload=payload,
        key=api_parameters.private_key,
        algorithm="EdDSA",
    )

    return encoded_jwt


def create_refresh_token(user_id: UUID, user_role: str, session_version: int) -> str:
    """
    Genera un token JWT de refresco con una vida útil más larga. Su único propósito es ser canjeado
    por un nuevo token de acceso cuando este expire.
    """

    now = datetime.now(tz=UTC)
    payload = {
        "sub": str(user_id),
        "exp": now + timedelta(minutes=api_parameters.refresh_token_expire),
        "nbf": now,
        "jti": str(uuid4()),
        "user_role": user_role,
        "session_version": session_version,
        "token_type": "refresh",
    }
    encoded_jwt = jwt.encode(
        payload=payload,
        key=api_parameters.private_key,
        algorithm="EdDSA",
    )

    return encoded_jwt


def decode_token(
    token: str,
    expected_type: Literal["access", "refresh"],
    verify_exp: bool = True,
) -> dict[str, Any]:
    """
    Decodifica y valida la firma, vigencia, claims requeridos y tipo de un token JWT.

    Raises:
        InvalidJWT: Si el token ha expirado, es inválido o no corresponde al tipo esperado.
    """

    expired_msg = (
        ExceptionErrorMessages.ACCESS_JWT_EXPIRED.value
        if expected_type == "access"
        else ExceptionErrorMessages.REFRESH_JWT_EXPIRED.value
    )
    invalid_msg = (
        ExceptionErrorMessages.ACCESS_JWT_INVALID.value
        if expected_type == "access"
        else ExceptionErrorMessages.REFRESH_JWT_INVALID.value
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            jwt=token,
            key=api_parameters.public_key,
            algorithms=["EdDSA"],
            options={
                "verify_exp": verify_exp,
                "require": [
                    "sub",
                    "exp",
                    "nbf",
                    "user_role",
                    "session_version",
                    "token_type",
                ],
            },
        )
    except jwt.ExpiredSignatureError as exc:
        raise InvalidJWT(message=expired_msg) from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidJWT(message=invalid_msg) from exc
    if payload["token_type"] != expected_type:
        raise InvalidJWT(message=invalid_msg)

    return payload
