from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.response import Response
from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.users.dependencies import get_create_customer_wholesale_service
from src.modules.users.dto import CreateCustomerWholesaleDTO, ReadCustomerWholesaleDTO
from src.modules.users.models.customer_wholesale import CustomerWholesale
from src.modules.users.services.customers_wholesale.create_customer_wholesale import (
    CreateCustomerWholesaleService,
)

create_wholesale_router = APIRouter(prefix="/users", tags=["Usuarios"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{CustomerWholesale.__tablename__}.create"},
)


@create_wholesale_router.post(
    path="/customer_wholesale/",
    response_description="**(CREATED)** Cliente mayorista creado exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=CreateCustomerWholesaleDTO),
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
        ),
        status.HTTP_403_FORBIDDEN: response_scheme_403(),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def create_customer_wholesale(
    user: Annotated[User, Depends(require_admin)],
    data: CreateCustomerWholesaleDTO,
    service: Annotated[
        CreateCustomerWholesaleService,
        Depends(get_create_customer_wholesale_service),
    ],
) -> Response[ReadCustomerWholesaleDTO]:
    """
    Registra un nuevo cliente mayorista en el sistema.

    ### Descripción
    Crea un perfil de cliente mayorista con sus datos comerciales, identificación
    tributaria (RUC), canales de contacto y dirección de entrega. Ejecuta validaciones
    sintácticas y comprobaciones de unicidad en la base de datos para prevenir duplicados.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `customer_wholesale.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario posea rol de administrador y el permiso
         `customer_wholesale.create`.
    2. **Validación Sintáctica (DTO):**
        - Valida el formato de correo electrónico, límites de caracteres en campos
         de texto y la estructura anidada de ubicación geográfica y contactos
         adicionales opcionales.
    3. **Validaciones de Reglas de Negocio:**
        - **Unicidad de Correo:** Verifica que el correo electrónico no esté registrado.
        - **Unicidad de Nombre / Razón Social:** Comprueba que la razón social no esté en uso.
        - **Unicidad de Teléfono:** Comprueba que el número de teléfono no esté asignado.
        - **Unicidad de RUC:** Si se envía RUC, verifica que no pertenezca a otro mayorista.
    4. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    customer_wholesale = await service.create_customer_wholesale(data=data)

    return Response(
        success=True,
        pagination=False,
        message="Cliente mayorista creado exitosamente.",
        data=customer_wholesale,
    )
