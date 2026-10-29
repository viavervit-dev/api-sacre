from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Path, status

from src.api.common.schema import (
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
from src.api.modules.payments.dependencies import create_payment_link_service
from src.api.modules.payments.models.payment import Payment
from src.api.modules.payments.services.links.create import CreatePaymentLinkService

create_payment_link_router = APIRouter(prefix="/payments", tags=["Pagos"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Payment.__tablename__}.create"},
)


@create_payment_link_router.post(
    path="/links/{shopping_order_id}/",
    response_description="**(NO_CONTENT)** Enlace de pago generado exitosamente.",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def create_payment_link(
    user: Annotated[User, Depends(require_admin)],
    shopping_order_id: Annotated[
        UUID,
        Path(
            title="ID de la orden de compra",
            description="El identificador único de la orden de compra en formato UUID v4.",
        ),
    ],
    background_tasks: BackgroundTasks,
    service: Annotated[CreatePaymentLinkService, Depends(create_payment_link_service)],
) -> None:
    """
    Genera un enlace de pago único y seguro a través del servicio de pagos para una transacción,
    registra la transacción y envía la notificación con el enlace al cliente por correo.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `payments.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario posea rol de administrador y el permiso `payments.create`.
    2. **Validación Sintáctica de Parámetros:**
        - Valida el identificador de la orden de compra como un UUID v4.
    3. **Búsqueda y Verificación de la Orden de Compra:**
        - Consulta la orden de compra en la base de datos mediante su identificador.
        - Si no existe, interrumpe el flujo emitiendo (404 Not Found).
    4. **Generación del Enlace en la Pasarela de Pagos:**
        - Convierte los importes financieros a centavos enteros exactos, garantizando que no
         existan más de dos decimales.
        - Realiza la solicitud HTTP al servicio de pago externo configurando el enlace de pago para
         un solo uso y monto no editable.
    5. **Persistencia de la Transacción:**
        - Almacena la transacción en la base de datos asociada a la orden y su estado actual.
    6. **Notificación al Cliente por Correo:**
        - Renderiza la plantilla HTML de confirmación de la orden con el botón de pago seguro.
        - Genera una versión en texto plano como respaldo para clientes sin soporte HTML y
         mitigación de filtros anti-spam.
        - Encola la tarea en segundo plano para despachar el correo electrónico al destinatario
         sin demorar la respuesta HTTP.
    """

    await service.execute(
        shopping_order_id=shopping_order_id,
        background_tasks=background_tasks,
    )
