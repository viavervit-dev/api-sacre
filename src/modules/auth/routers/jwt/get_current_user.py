from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.dto import CurrentUserDTO
from src.modules.auth.models.user import User
from src.modules.auth.services.jwt.get_current_user import GetCurrentUserService
from src.modules.customers.models.customer import Customer

router = APIRouter(prefix="/authentication", tags=["Autenticación"])
require_user = UserPermissionChecker(
    allowed_roles=[
        UserRoles.ADMINISTRATOR.value,
        UserRoles.CUSTOMER.value,
    ],
    permissions={
        UserRoles.ADMINISTRATOR.value: f"{Admin.__tablename__}.read",
        UserRoles.CUSTOMER.value: f"{Customer.__tablename__}.read",
    },
)


@router.get(
    path="/jwt/me/",
    response_description="**(OK)** Se retorna la información del usuario de la sesión actual.",
    status_code=status.HTTP_200_OK,
    responses={
        401: response_scheme_401(
            access_jwt_missing=True,
            access_jwt_invalid=True,
            jwt_user_not_found=True,
        ),
        403: response_scheme_403(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def get_current_user(
    user: Annotated[tuple[User, Admin | Customer], Depends(require_user)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[CurrentUserDTO]:
    """
    Endpoint para obtener la información del usuario de la sesión actual, recibe una petición con
    los datos necesarios y ejecuta validaciones adicionales. Si todo es correcto, devuelve la
    información del usuario.
    """

    _, user_profile = user
    service = GetCurrentUserService
    user_data = await service.get_current_user(instance=user_profile)

    return Response(
        success=True,
        pagination=False,
        message="Se obtuvo la información del usuario de la sesión actual.",
        data=user_data,
    )
