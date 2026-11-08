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
from src.api.modules.inventory.dependencies import get_list_products_wholesaler_service
from src.api.modules.inventory.dto import ReadWholesalerProductSummaryDTO
from src.api.modules.inventory.models import WholesalerProduct
from src.api.modules.inventory.services.products.wholesaler import GetListProductWholesalerService
from src.api.settings.parameters import api_parameters

get_list_products_wholesaler_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{WholesalerProduct.__tablename__}.read"},
)


@get_list_products_wholesaler_router.get(
    path="/product/wholesaler/",
    response_description="**(OK)** Lista de productos obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de productos obtenida exitosamente.",
            "model": Response[PaginatedData[ReadWholesalerProductSummaryDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen productos",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de productos obtenida exitosamente.",
                                "data": {
                                    "items": [
                                        {
                                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                            "name": "Rosario de madera",
                                            "categories": ["Rosarios", "Madera"],
                                            "description_short": "Rosario hecho a mano con cuentas"
                                            " de madera.",
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
                            "summary": "No existen productos",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de productos obtenida exitosamente.",
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
async def get_list_products_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    service: Annotated[
        GetListProductWholesalerService, Depends(get_list_products_wholesaler_service)
    ],
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
) -> Response[PaginatedData[ReadWholesalerProductSummaryDTO]]:
    """
    Permite consultar el listado de todos los productos para clientes mayoristas. Soporta
    paginación por desplazamiento (`offset`) y límite (`limit`), ordenando los resultados
    cronológicamente de forma descendente. Estos productos no forman parte del catálogo
    público general ofrecido a clientes finales.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `wholesaler_products.read`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
            `wholesaler_products.read`.
    2. **Validación de Parámetros de Consulta:**
        - Valida que `offset` sea un entero no negativo.
        - Valida que `limit` sea un entero positivo menor o igual al límite configurado.
    3. **Consulta en Base de Datos y Paginación:**
        - Realiza el conteo total de registros en la tabla `inventory.wholesaler_products`.
        - Si no existen productos registrados, retorna una colección vacía con total 0.
        - Si existen productos, consulta los registros ordenados descendentemente por fecha
          de creación.
    4. **Serialización y Retorno:**
        - Mapea la lista de productos al DTO de lectura resumida.
    """

    products, total_items = await service.get_list(offset=offset, limit=limit)

    return Response(
        success=True,
        pagination=True,
        message="Lista de productos obtenida exitosamente.",
        data=PaginatedData(
            items=products,
            meta=PaginationMeta(total=total_items, offset=offset, limit=limit),
        ),
    )
