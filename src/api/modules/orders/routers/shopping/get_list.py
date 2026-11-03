from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.api.common.constants import PAGINATION_LIMIT_DESCRIPTION, PAGINATION_OFFSET_DESCRIPTION
from src.api.common.response import PaginatedData, PaginationMeta, Response
from src.api.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.orders.dependencies import get_list_purchase_order_service
from src.api.modules.orders.dto import ReadOrderSummaryDTO
from src.api.modules.orders.models.order import Order
from src.api.modules.orders.services.shopping.get_list import GetListPurchaseOrderService
from src.api.settings.parameters import api_parameters

get_list_purchase_orders_router = APIRouter(prefix="/orders", tags=["Órdenes/Transacciones"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Order.__tablename__}.read"},
)


@get_list_purchase_orders_router.get(
    path="/purchase/",
    response_description="**(OK)** Lista de órdenes de compra obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de órdenes de compra obtenida exitosamente.",
            "model": Response[PaginatedData[ReadOrderSummaryDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen órdenes de compra",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de órdenes de compra obtenida exitosamente.",
                                "data": {
                                    "items": [
                                        {
                                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                            "order_number": "ORD-2026-000001",
                                            "customer_data": {
                                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                                "name_or_company_name": "Parroquia San José",
                                                "ruc": "1790011674001",
                                            },
                                            "payment_data": {
                                                "description": "Orden de compra",
                                                "link": "https://ppls.me/rvzpDIGpvT2Fb1y4dx9aYQ",
                                            },
                                            "units": 100,
                                            "total": 230.50,
                                            "status": "Pendiente de pago",
                                            "date_joined": "2026-10-24T17:25:41.776689+00:00",
                                        },
                                    ],
                                    "meta": {
                                        "total": 1,
                                        "offset": 0,
                                        "limit": api_parameters.pagination_limit,
                                    },
                                },
                            },
                        },
                        "response_2": {
                            "summary": "No existen órdenes de compra",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de órdenes de compra obtenida exitosamente.",
                                "data": {
                                    "items": [],
                                    "meta": {
                                        "total": 0,
                                        "offset": 0,
                                        "limit": api_parameters.pagination_limit,
                                    },
                                },
                            },
                        },
                    },
                }
            },
        },
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
async def get_list_purchase_orders(
    user: Annotated[User, Depends(require_admin)],
    service: Annotated[GetListPurchaseOrderService, Depends(get_list_purchase_order_service)],
    offset: int = Query(
        title="Registros a omitir",
        description=PAGINATION_OFFSET_DESCRIPTION,
        ge=0,
    ),
    limit: int = Query(
        title="Límite de registros",
        description=PAGINATION_LIMIT_DESCRIPTION,
        le=api_parameters.pagination_limit,
        ge=1,
    ),
) -> Response[PaginatedData[ReadOrderSummaryDTO]]:
    """
    Permite consultar el listado de órdenes de compra almacenadas con soporte para
    paginación y ordenamiento cronológico descendente.

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
    2. **Consulta en Base de Datos y Paginación:**
        - Consulta el conteo total de registros coincidentes con tipo orden de compra.
        - Si existen registros, consulta las órdenes ordenadas de forma descendente por fecha
            de creación, aplicando `offset` y `limit`.
    3. **Serialización y Retorno:**
        - Mapea la lista de órdenes al DTO de lectura resumida.
    """

    orders, total_items = await service.get_list(offset=offset, limit=limit)

    return Response(
        success=True,
        pagination=True,
        message="Lista de órdenes de compra obtenida exitosamente.",
        data=PaginatedData(
            items=orders,
            meta=PaginationMeta(total=total_items, offset=offset, limit=limit),
        ),
    )
