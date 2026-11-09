from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.users.dependencies import update_wholesaler_service
from src.api.modules.users.dto import ReadWholesalerDTO, UpdateWholesalerDTO
from src.api.modules.users.models import Wholesaler
from src.api.modules.users.services.wholesaler import UpdateWholesalerService

update_wholesaler_router = APIRouter(prefix="/users", tags=["Usuarios"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Wholesaler.__tablename__}.update"},
)


@update_wholesaler_router.patch(
    path="/wholesaler/{wholesaler_id}/",
    response_description="**(OK)** Cliente mayorista actualizado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=UpdateWholesalerDTO),
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
async def update_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    data: UpdateWholesalerDTO,
    wholesaler_id: Annotated[
        UUID,
        Path(
            title="ID del cliente mayorista",
            description="El identificador único del cliente mayorista en formato UUID v4.",
        ),
    ],
    service: Annotated[UpdateWholesalerService, Depends(update_wholesaler_service)],
) -> Response[ReadWholesalerDTO]:
    """
    Permite modificar de forma parcial los datos de un cliente mayorista. Ejecuta validaciones
    sintácticas y comprobaciones de unicidad en la base de datos para prevenir duplicados.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `wholesaler.update`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
            `customer_wholesale.update`.
    2. **Búsqueda del Recurso:**
        - Consulta el cliente mayorista en la base de datos por su `wholesaler_id`.
        - Si no existe, interrumpe el flujo levantando (404 Not Found).
    3. **Validación Sintáctica y de Reglas de Negocio:**
        - Valida el esquema y formatos de los campos enviados.
        - **Unicidad de Correo:** Si se modifica `email`, verifica que no esté registrado.
        - **Unicidad de Razón Social:** Si se modifica `name_or_company_name`, comprueba su
            disponibilidad.
        - **Unicidad de Teléfono:** Si se modifica `phone`, verifica que no esté asignado.
        - **Unicidad de RUC:** Si se envía `ruc`, comprueba que no pertenezca a otra entidad.
    4. **Persistencia:**
        - Aplica las modificaciones del registro en la base de datos.
    """

    wholesaler = await service.update(wholesaler_id=wholesaler_id, data=data)

    return Response(
        success=True,
        pagination=False,
        message="Cliente mayorista actualizado exitosamente.",
        data=wholesaler,
    )
