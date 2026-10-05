from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.common.constants import PAGINATION_LIMIT_DESCRIPTION, PAGINATION_OFFSET_DESCRIPTION
from src.common.response import PaginatedData, PaginationMeta, Response
from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.config.parameters import settings
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.users.dependencies import get_retrieve_list_customer_wholesale_service
from src.modules.users.dto import ReadCustomerWholesaleDTO
from src.modules.users.models.customer_wholesale import CustomerWholesale
from src.modules.users.services.customers_wholesale.get_list_customer_wholesale import (
    RetrieveListCustomerWholesaleService,
)

get_list_customers_wholesale = APIRouter(prefix="/users", tags=["Usuarios"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{CustomerWholesale.__tablename__}.read"},
)


@get_list_customers_wholesale.get(
    path="/customer_wholesale/",
    response_description="**(OK)** Lista de clientes mayoristas obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de clientes mayoristas obtenida exitosamente.",
            "model": Response[PaginatedData[ReadCustomerWholesaleDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen clientes mayoristas",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de clientes mayoristas obtenida exitosamente.",
                                "data": {
                                    "items": [
                                        {
                                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                            "email": "user@email.com",
                                            "name_or_company_name": "Juan Pablo",
                                            "ruc": "1790011674001",
                                            "phone": "+593 123456789",
                                            "location": {
                                                "country": "Ecuador",
                                                "province": "Pichincha",
                                                "canton": "Quito",
                                                "city": "Zámbiza",
                                                "address": "Manuel Larrea y Av. 6 de Diciembre",
                                            },
                                            "extra_contacts": [
                                                {
                                                    "position": "Secretaria",
                                                    "name": "María Pérez",
                                                    "email": "user@email.com",
                                                    "phone": "+593 987654321",
                                                },
                                            ],
                                        },
                                    ],
                                    "meta": {
                                        "total": 1,
                                        "offset": 0,
                                        "limit": settings.pagination_limit,
                                    },
                                },
                            },
                        },
                        "response_2": {
                            "summary": "No existen clientes mayoristas",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de clientes mayoristas obtenida exitosamente.",
                                "data": {
                                    "items": [],
                                    "meta": {
                                        "total": 0,
                                        "offset": 0,
                                        "limit": settings.pagination_limit,
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
async def get_customers_wholesale(
    user: Annotated[User, Depends(require_admin)],
    service: Annotated[
        RetrieveListCustomerWholesaleService,
        Depends(get_retrieve_list_customer_wholesale_service),
    ],
    offset: int = Query(
        title="Registros a omitir",
        description=PAGINATION_OFFSET_DESCRIPTION,
        ge=0,
    ),
    limit: int = Query(
        le=settings.pagination_limit,
        title="Límite de registros",
        description=PAGINATION_LIMIT_DESCRIPTION,
        ge=1,
    ),
) -> Response[PaginatedData[ReadCustomerWholesaleDTO]]:
    """
    Permite consultar el listado de clientes mayoristas almacenados con soporte para
    paginación y ordenamiento cronológico descendente.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `customer_wholesale.read`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
         `customer_wholesale.read`.
    2. **Consulta en Base de Datos y Paginación:**
        - Realiza el conteo total de clientes mayoristas en `users.customer_wholesale`.
        - Si no existen registros registrados, retorna una lista vacía y total 0.
        - Si existen registros, consulta los clientes ordenados de forma descendente por fecha
         de registro, aplicando `offset` y `limit`.
    3. **Serialización:**
        - Mapea la lista de clientes mayoristas al DTO de lectura.
    """

    customers_wholesale, total_items = await service.get_customers_wholesale(
        offset=offset,
        limit=limit,
    )

    return Response(
        success=True,
        pagination=True,
        message="Lista de clientes mayoristas obtenida exitosamente.",
        data=PaginatedData(
            items=customers_wholesale,
            meta=PaginationMeta(total=total_items, offset=offset, limit=limit),
        ),
    )
