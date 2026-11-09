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
from src.api.modules.orders.dependencies import get_purchase_order_service
from src.api.modules.orders.dto import ReadOrderDTO
from src.api.modules.orders.models import Order
from src.api.modules.orders.services.purchase import GetPurchaseOrderService

get_purchase_order_router = APIRouter(prefix="/orders", tags=["Órdenes/Transacciones"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Order.__tablename__}.read"},
)


@get_purchase_order_router.get(
    path="/purchase/{purchase_order_id}/",
    response_description="**(OK)** Orden de compra obtenida exitosamente.",
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
async def get_purchase_order(
    user: Annotated[User, Depends(require_admin)],
    purchase_order_id: Annotated[
        UUID,
        Path(
            title="ID de la orden de compra",
            description="El identificador único de la orden de compra en formato UUID v4.",
        ),
    ],
    service: Annotated[GetPurchaseOrderService, Depends(get_purchase_order_service)],
) -> Response[ReadOrderDTO]:
    """
    Permite consultar el detalle completo de una orden de compra específica a partir de su ID
    (`purchase_order_id`). Retorna el número de orden, el desglose de productos adquiridos
    con sus subtotales e impuestos, la instantánea con datos del cliente y la información
    de la pasarela o enlace de pago asociado.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `orders.read`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
            `orders.read`.
    2. **Validación Sintáctica del Parámetro de Ruta:**
        - Valida que el identificador `purchase_order_id` cumpla con el formato estándar UUID v4.
    3. **Consulta y Verificación en Base de Datos:**
        - Consulta la orden en la base de datos mediante su identificador único.
        - Si la orden no existe, interrumpe el flujo levantando (404 Not Found).
    4. **Serialización y Retorno:**
        - Extrae las estructuras anidadas (`customer_data`, `product_data` y `payment_data`).
        - Mapea los datos al DTO detallado `ReadOrderDTO`.
    """

    order = await service.get(purchase_order_id=purchase_order_id)

    return Response(
        success=True,
        pagination=False,
        message="Orden de compra obtenida exitosamente.",
        data=order,
    )
