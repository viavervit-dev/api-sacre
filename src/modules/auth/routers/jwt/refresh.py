from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.auth.dependencies import get_raw_tokens
from src.modules.auth.repositories.user import UserRepository
from src.modules.auth.services.jwt.refresh import RefreshTokenService

router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@router.get(
    path="/jwt/refresh/",
    response_description="**(NO_CONTENT)** Se crea un nuevo token de acceso.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            refresh_jwt_invalid=True,
            access_jwt_not_expired=True,
            refresh_jwt_expired=True,
            auth_session_expired=True,
        ),
        403: response_scheme_403(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def refresh_token(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
    response: Response,
) -> None:
    """Endpoint para refrescar el token de acceso utilizando un token de actualización válido."""

    access_token, refresh_token = tokens
    service = RefreshTokenService(user_repo=UserRepository, db=db)
    new_access_token = await service.refresh_token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.access_token_expire * 60,
    )
