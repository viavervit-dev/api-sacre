from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.response import Response
from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker, get_retrieve_user_service
from src.modules.auth.dto import ReadUserDTO
from src.modules.auth.models.user import User
from src.modules.auth.services.jwt.get_current_user import RetrieveCurrentUserService
from src.modules.users.models.admin import Admin
from src.modules.users.models.customer import Customer

jwt_me_router = APIRouter(prefix="/authentication", tags=["Autenticación"])
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


@jwt_me_router.get(
    path="/jwt/me/",
    response_description="**(OK)** Se retorna la información del usuario de la sesión actual.",
    status_code=status.HTTP_200_OK,
    responses={
        401: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
        ),
        403: response_scheme_403(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def get_current_user(
    user: Annotated[User, Depends(require_user)],
    service: Annotated[type[RetrieveCurrentUserService], Depends(get_retrieve_user_service)],
) -> Response[ReadUserDTO]:
    """
    Obtiene la información del perfil del usuario autenticado en la sesión actual.

    ### Descripción
    Recupera los datos personales y de cuenta del usuario que inició la sesión activa
    a partir del token JWT almacenado en las cookies. Soporta perfiles de administradores
    y de clientes, resolviendo dinámicamente sus atributos de perfil según su rol.

    ### Requisitos de Acceso
    - **Roles permitidos:** Administrador (`admin`) o Cliente (`customer`).
    - **Permisos requeridos:**
      - Administradores: `admins.read`.
      - Clientes: `customers.read`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Validación de Sesión:**
       - Extrae los tokens JWT presentes en las cookies de la petición HTTP.
       - Valida la firma criptográfica y vigencia del `access_token`.
       - Comprueba la versión de sesión del usuario en la base de datos contra el token.
    2. **Control de Acceso y Permisos:**
       - Verifica que el usuario cuente con un rol válido (`admin` o `customer`).
       - Comprueba que el usuario posea el permiso de lectura asociado a su rol.
    3. **Resolución de Perfil:**
       - Carga la entidad de perfil vinculada (`Admin` o `Customer`) según el rol del usuario.
       - Extrae los nombres, apellidos, correo y rol asignado.
    4. **Construcción de Respuesta:**
       - Mapea la información consolidada al esquema `ReadUserDTO`.
       - Retorna la estructura estandarizada `Response` con código 200 OK.
    """

    user_data = await service.get_current_user(instance=user)

    return Response(
        success=True,
        pagination=False,
        message="Se obtuvo la información del usuario de la sesión actual.",
        data=user_data,
    )
