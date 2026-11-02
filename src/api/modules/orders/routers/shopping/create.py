from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_500,
    response_scheme_502,
    response_scheme_503,
    response_scheme_504,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.orders.dependencies import create_order_customer_wholesale_service
from src.api.modules.orders.dto import CreateOrderDTO, ReadOrderDTO
from src.api.modules.orders.models.order import Order
from src.api.modules.orders.services.shopping.create import CreateOrderCustomerWholesaleService

create_order_customer_wholesale_router = APIRouter(
    prefix="/orders",
    tags=["Órdenes/Transacciones"],
)
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Order.__tablename__}.create"},
)


@create_order_customer_wholesale_router.post(
    path="/shopping/customer_wholesale/{customer_wholesale_id}/",
    response_description="**(CREATED)** Órden/transacción creada exitosamente.",
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: response_scheme_500(
            smtp_credentials_not_configured=True,
            smtp_authentication_error=True,
        ),
        status.HTTP_502_BAD_GATEWAY: response_scheme_502(
            payment_gateway_config_error=True,
            payment_gateway_unavailable=True,
            payment_gateway_rejected=True,
            payment_gateway_invalid_response=True,
            payment_email_delivery_error=True,
        ),
        status.HTTP_504_GATEWAY_TIMEOUT: response_scheme_504(
            payment_gateway_connection_error=True,
            payment_gateway_timeout=True,
        ),
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
    Permite crear una órden/transacción vinculada a un cliente mayorista a partir de los datos
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
        - Consulta al usuario mayorista en la base de datos.
        - Si no existe, interrumpe el flujo levantando  (404 Not Found).
    4. **Validaciones de Reglas de Negocio:**
        - **Unicidad:** Comprueba que la clave de idempotencia (`idempotency_key`) no esté
            registrado.
        - **Catálogo de Productos:** Comprueba la existencia en inventario de cada artículo.
        - **Cálculo de Impuestos por Ítem:** Audita el IVA y total individual de cada producto.
        - **Consistencia Financiera Global:** Verifica que los totales declarados en cabecera
            (`subtotal`, `tax_amount`, `total`, `units`) coincidan con la sumatoria de los ítems.
    5. **Instantáneas (Snapshots) y Estado Inicial:**
        - Genera una instantánea inmutable de los datos del cliente mayorista.
        - Enriquece los ítems con información descriptiva de cada producto.
        - Asigna el estado inicial de la orden como pendiente de pago.
    6. **Generación del Enlace en la Pasarela de Pagos:**
        - Convierte los importes financieros a centavos enteros exactos, garantizando que no
            existan más de dos decimales.
        - Realiza la solicitud HTTP al servicio de pago externo configurando el enlace de pago para
            un solo uso y monto no editable.
    7. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    order = await service.create(data=data, customer_wholesale_id=customer_wholesale_id)

    return Response(
        success=True,
        pagination=False,
        message="Órden/transacción creada exitosamente.",
        data=order,
    )
