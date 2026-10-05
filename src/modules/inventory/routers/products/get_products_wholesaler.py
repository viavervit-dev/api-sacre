from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

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
from src.modules.inventory.dependencies import get_products_by_wholesaler_service
from src.modules.inventory.dto import PrivateReadProductDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.get_products_wholesaler import (
    RetrieveProductsWholesalerService,
)

get_products_wholesaler_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.read.private"},
)


@get_products_wholesaler_router.get(
    path="/product/{wholesaler_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de productos obtenida exitosamente.",
            "model": Response[PaginatedData[PrivateReadProductDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen productos asignados",
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
                                            "description_long": "Este rosario está fabricado a "
                                            "mano utilizando madera de alta calidad, ideal para "
                                            "orar en el día a día. Cuenta con un diseño elegante "
                                            "y tradicional.",
                                            "images": [
                                                "https://example.com/image1.jpg",
                                                "https://example.com/image2.jpg",
                                                "https://example.com/image3.jpg",
                                            ],
                                            "price_neto": "10.50",
                                            "price_sale": "15.00",
                                            "profit_margin": "0.16",
                                            "iva": "0.16",
                                            "stock_total": 100,
                                            "stock_hand": 80,
                                            "stock_sale": 20,
                                            "status": True,
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
                            "summary": "No existen productos asignados",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de productos obtenida exitosamente.",
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
async def get_products_by_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    wholesaler_id: Annotated[
        UUID,
        Path(
            title="ID del cliente mayorista",
            description="El ID del cliente mayorista del cual se obtendrán los productos.",
        ),
    ],
    service: Annotated[
        RetrieveProductsWholesalerService, Depends(get_products_by_wholesaler_service)
    ],
    offset: int = Query(
        title="Registros a omitir",
        description=PAGINATION_OFFSET_DESCRIPTION,
        ge=0,
    ),
    limit: int = Query(
        title="Límite de registros",
        description=PAGINATION_LIMIT_DESCRIPTION,
        le=settings.pagination_limit,
        ge=1,
    ),
) -> Response[PaginatedData[PrivateReadProductDTO]]:
    """
    Permite consultar el listado de productos exclusivos asociados a un cliente mayorista
    específico con soporte para paginación y ordenamiento cronológico descendente.
    Estos productos no hacen parte del catálogo de productos que se ofrecen a los usuarios finales.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `products.read.private`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
         `products.read.private`.
    2. **Validación de Parámetros:**
        - Valida que `wholesaler_id` en la ruta corresponda a un UUID válido.
        - Valida los parámetros de paginación `offset` (>= 0) y `limit` (entre 1 y el valor
         máximo configurado).
    3. **Consulta en Base de Datos y Paginación:**
        - Realiza el conteo total de productos vinculados al mayorista (`wholesaler_id`).
        - Si no existen coincidencias, retorna una colección vacía y total 0.
        - Si existen productos, consulta los registros ordenados descendentemente por fecha
         de creación, aplicando `offset` y `limit`.
    4. **Serialización Dinámica:**
        - Mapea los resultados a visión administrativa completa sensibles de negocio al
         DTO de lectura.
    """

    products, total_items = await service.get_products_by_wholesaler(
        wholesaler_id=wholesaler_id,
        offset=offset,
        limit=limit,
    )

    return Response(
        success=True,
        pagination=True,
        message="Lista de productos obtenida exitosamente.",
        data=PaginatedData(
            items=products,
            meta=PaginationMeta(total=total_items, offset=offset, limit=limit),
        ),
    )
