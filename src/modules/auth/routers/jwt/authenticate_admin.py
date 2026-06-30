from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.auth.dto import AdminCredentialsDTO
from src.modules.auth.repositories.user import UserRepository
from src.modules.auth.services.jwt.authenticate_admin import AuthAdminService

router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@router.post(
    path="/jwt/admin/",
    response_description="Administrador autenticado exitosamente.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: response_scheme_400(dto_class=AdminCredentialsDTO),
        401: response_scheme_401(credentials_invalid=True, access_jwt_invalid=True),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def authenticate_admin(
    credentials: AdminCredentialsDTO,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    response: Response,
) -> None:
    """
    Inicia sesión como administrador. Si las credenciales son correctas, se establecen las cookies
    con los tokens de acceso y refresco.
    """

    service = AuthAdminService(user_repo=UserRepository, db=db)
    access_token, refresh_token = await service.authenticate_admin(credentials=credentials)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.access_token_expire * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.refresh_token_expire * 60,
    )
