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
from src.api.modules.orders.dependencies import create_order_customer_wholesale_service
from src.api.modules.orders.dto import CreateOrderDTO, ReadOrderDTO
from src.api.modules.orders.models.order import Order
from src.api.modules.orders.services.create import CreateOrderCustomerWholesaleService

create_order_customer_wholesale_router = APIRouter(prefix="/orders", tags=["Ordenes de Compra"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Order.__tablename__}.create"},
)


@create_order_customer_wholesale_router.post(
    path="/customer_wholesale/{customer_wholesale_id}/",
    response_description="**(CREATED)** Orden de compra creada exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=CreateOrderDTO),
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
async def create_order_customer_wholesale(
    user: Annotated[User, Depends(require_admin)],
    data: CreateOrderDTO,
    customer_wholesale_id: Annotated[
        UUID,
        Path(
            title="ID del cliente mayorista",
            description="El identificador único en formato UUID v4.",
            examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        ),
    ],
    service: Annotated[
        CreateOrderCustomerWholesaleService, Depends(create_order_customer_wholesale_service)
    ],
) -> Response[ReadOrderDTO]:
    """
    Permite crear una orden de compra vinculada a un cliente mayorista a partir de los datos
    proporcionados y su identificador. Ejecuta validaciones sintácticas y comprobaciones de
    unicidad en la base de datos para prevenir duplicados.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `orders.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario posea rol de administrador y el permiso `orders.create`.
    2. **Validación Sintáctica y Parámetros:**
        - Valida el identificador del mayorista (`customer_wholesale_id`) como un UUID en la ruta.
        - Valida tipos de datos, montos decimales y lista de artículos.
    3. **Verificación de Existencia del Mayorista:**
        - Consulta al usuario mayorista en la base de datos con rol `customer_wholesale`.
        - Si no existe, interrumpe el flujo levantando `ResourceNotFound` (404 Not Found).
    4. **Validaciones de Reglas de Negocio:**
        - **Unicidad:** Comprueba que el número de orden (`order_number`) no esté registrado.
        - **Catálogo de Productos:** Comprueba la existencia en inventario de cada artículo.
        - **Cálculo de Impuestos por Ítem:** Audita el IVA y total individual de cada producto.
        - **Consistencia Financiera Global:** Verifica que los totales declarados en cabecera
         (`subtotal`, `tax_amount`, `total`, `units`) coincidan con la sumatoria de los ítems.
    5. **Instantáneas (Snapshots) y Estado Inicial:**
        - Genera una instantánea inmutable de los datos del cliente mayorista (`customer_data`).
        - Enriquece los ítems con información descriptiva de cada producto (`product_data`).
        - Asigna el estado inicial de la orden como pendiente de pago (`pending_payment`).
    6. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    order = await service.create(data=data, customer_wholesale_id=customer_wholesale_id)

    return Response(
        success=True,
        pagination=False,
        message="Orden de compra creada exitosamente.",
        data=order,
    )
