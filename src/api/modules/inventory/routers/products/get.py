from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_409,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserOptionalPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dependencies import get_product_service
from src.api.modules.inventory.dto import ReadProductPrivateDTO, ReadProductPublicDTO
from src.api.modules.inventory.models.product import Product
from src.api.modules.inventory.services.products.get import GetProductService

get_product_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserOptionalPermissionChecker(
    allowed_roles=[
        UserRoles.ADMINISTRATOR.value,
        UserRoles.CUSTOMER.value,
    ],
    permissions={
        UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.read.private",
        UserRoles.CUSTOMER.value: f"{Product.__tablename__}.read.public",
    },
)


@get_product_router.get(
    path="/product/{product_id}/",
    response_description="**(OK)** Producto consultado exitosamente.",
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
        status.HTTP_409_CONFLICT: response_scheme_409(product_not_available=True),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def get_product(
    user: Annotated[User | None, Depends(require_admin)],
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único del producto en formato UUID v4.",
            examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        ),
    ],
    service: Annotated[GetProductService, Depends(get_product_service)],
) -> Response[ReadProductPrivateDTO | ReadProductPublicDTO]:
    """
    Permite consultar el detalle completo de un producto específico. La respuesta se adapta
    dinámicamente según el nivel de privilegios del usuario solicitante:
    - **Público / Clientes:** Expone información comercial pública. Si el producto es
        exclusivo y se encuentra inactivo, no estará disponible para consulta.
    - **Administradores:** Expone la vista administrativa completa, incluyendo márgenes de
        ganancia, costos netos, desglose de inventario y estado global.

    ### Requisitos de Acceso
    - **Acceso Anónimo:** Permitido sin autenticación (vista pública).
    - **Clientes (`customer`):** Requiere permiso `products.read.public`.
    - **Administradores (`admin`):** Requiere permiso `products.read.private`.
    - **Autenticación:** Opcional vía cookies `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación Opcional y Autorización:**
        - Si se proporcionan cookies JWT, valida el token, la vigencia de la sesión y la
            existencia del usuario.
        - Valida que el rol sea `admin` o `customer` y verifica sus permisos respectivos.
        - Si no se envían cookies, permite el acceso anónimo con nivel de visibilidad público.
    2. **Validación Sintáctica del Parámetro de Ruta:**
        - Valida que el identificador `product_id` cumpla con el formato estándar UUID v4.
    3. **Consulta en Base de Datos:**
        - Busca el producto en la base de datos a través de su identificador único.
        - Si el producto no existe, interrumpe el flujo levantando (404 Not Found).
    4. **Validación de Reglas de Dominio y Disponibilidad:**
        - Si el solicitante no es administrador, valida si el producto es exclusivo y se
            encuentra inactivo; de ser así, emite (409 Conflict - Producto no disponible).
    5. **Serialización y Retorno:**
        - Mapea el registro al DTO correspondiente (`ReadProductPrivateDTO` para administradores
          o `ReadProductPublicDTO` para clientes y público general).
    """

    product = await service.get(product_id=product_id, user=user)

    return Response(
        success=True,
        pagination=False,
        message="Producto consultado exitosamente.",
        data=product,
    )
