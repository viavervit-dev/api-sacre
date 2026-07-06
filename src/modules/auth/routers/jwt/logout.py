from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.schema import (
    response_scheme_401,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.modules.auth.dependencies import get_raw_tokens
from src.modules.auth.repositories.user import UserRepository
from src.modules.auth.services.jwt.logout import LogoutService

router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@router.get(
    path="/jwt/logout/",
    response_description="**(NO_CONTENT)** Se cierra la sesión del usuario.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            refresh_jwt_invalid=True,
            access_jwt_expired=True,
            refresh_jwt_expired=True,
            auth_session_expired=True,
        ),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def logout(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> None:
    """Endpoint para cerrar la sesión del usuario."""

    access_token, refresh_token = tokens
    service = LogoutService(user_repo=UserRepository, db=db)
    await service.logout(access_token=access_token, refresh_token=refresh_token)
