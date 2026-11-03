from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.users.dependencies import get_wholesaler_service
from src.api.modules.users.dto import ReadWholesalerDTO
from src.api.modules.users.models.wholesaler import Wholesaler
from src.api.modules.users.services.wholesaler.get import GetWholesalerService

get_wholesaler_router = APIRouter(prefix="/users", tags=["Usuarios"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Wholesaler.__tablename__}.read"},
)


@get_wholesaler_router.get(
    path="/wholesaler/{wholesaler_id}/",
    response_description="**(OK)** Cliente mayorista consultado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
        ),
        status.HTTP_403_FORBIDDEN: response_scheme_403(),
        status.HTTP_404_NOT_FOUND: response_scheme_404(),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def get_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    wholesaler_id: Annotated[
        UUID,
        Path(
            title="ID del cliente mayorista",
            description="El identificador único del cliente mayorista en formato UUID v4.",
        ),
    ],
    service: Annotated[GetWholesalerService, Depends(get_wholesaler_service)],
) -> Response[ReadWholesalerDTO]:
    """
    Permite consultar la información detallada de un cliente mayorista por su identificador
    (`wholesaler_id`).

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `wholesaler.read`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
            `wholesaler.read`.
    2. **Validación Sintáctica del Parámetro de Ruta:**
        - Valida que el identificador `wholesaler_id` cumpla con el formato estándar UUID v4.
    3. **Consulta y Verificación en Base de Datos:**
        - Consulta al usuario en la base de datos filtrando por `id` y rol `wholesaler`.
        - Si el usuario no existe, interrumpe el flujo levantando (404 Not Found).
    4. **Construcción y Retorno de Respuesta:**
        - Consolida los atributos del usuario base con la información del perfil mayorista.
        - Mapea los datos al DTO detallado `ReadWholesalerDTO`.
    """

    wholesaler = await service.get(wholesaler_id=wholesaler_id)

    return Response(
        success=True,
        pagination=False,
        message="Cliente mayorista consultado exitosamente.",
        data=wholesaler,
    )
