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
from src.modules.auth.dependencies import UserOptionalPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dependencies import get_retrieve_list_products_service
from src.modules.inventory.dto import PrivateReadProductDTO, PublicReadProductDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.get_list_products import RetrieveListProductsService

get_list_products_router = APIRouter(prefix="/inventory", tags=["Inventario"])
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


@get_list_products_router.get(
    path="/product/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de productos obtenida exitosamente.",
            "model": Response[PaginatedData[PrivateReadProductDTO | PublicReadProductDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen productos asignados - Datos privados",
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
                                            "orar en el día a día. Cuenta con un diseño elegante y"
                                            "tradicional.",
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
                            "summary": "Existen productos asignados - Datos públicos",
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
                                            "orar en el día a día. Cuenta con un diseño elegante y"
                                            " tradicional.",
                                            "images": [
                                                "https://example.com/image1.jpg",
                                                "https://example.com/image2.jpg",
                                                "https://example.com/image3.jpg",
                                            ],
                                            "price_sale": "15.00",
                                            "stock_sale": 20,
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
                        "response_3": {
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
async def get_list_products(
    user: Annotated[User | None, Depends(require_admin)],
    service: Annotated[RetrieveListProductsService, Depends(get_retrieve_list_products_service)],
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
) -> Response[PaginatedData[PrivateReadProductDTO | PublicReadProductDTO]]:
    """
    Permite consultar el listado de productos almacenados con soporte para paginación y
    ordenamiento cronológico descendente. La información y los filtros aplicados se adaptan
    dinámicamente según el nivel de privilegios del usuario solicitante:
    - **Público / Clientes:** Acceso libre o como cliente. Solo lista productos
     activos (`status=True`) y expone datos comerciales públicos.
    - **privado / Administradores:** Usuarios con rol de administrador. Acceden a todos los
     productos (activos e inactivos) y visualizan de datos comerciales públicos y privados.

    Estos productos hacen parte del catálogo de productos que se ofrecen a los usuarios finales.

    ### Requisitos de Acceso
    - **Acceso Anónimo:** Permitido sin autenticación (vista pública).
    - **Clientes (`customer`):** Requiere permiso `products.read.public`.
    - **Administradores (`admin`):** Requiere permiso `products.read.private`.
    - **Autenticación:** Opcional vía cookies `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación Opcional y Autorización:**
        - Si se proporcionan cookies JWT, valida el token, la existencia del usuario y la sesión.
        - Valida que el rol sea `admin` o `customer` y verifique sus permisos respectivos.
        - Si no se envían tokens, permite el acceso con rol público / anónimo.
    2. **Determinación de Visibilidad y Filtros:**
        - Si el usuario es administrador (`admin`): `private=True` y `status=None`.
        - Si es anónimo o cliente (`customer`): `private=False` y `status=True`.
    3. **Consulta en Base de Datos y Paginación:**
        - Realiza el conteo total de registros coincidentes para los metadatos de paginación.
        - Si existen registros, consulta los productos ordenados descendentemente por fecha de
         creación, aplicando `offset` y `limit`.
    4. **Serialización Dinámica:**
        - Mapea los resultados a visión administrativa completa o visión pública segura sin datos
         sensibles de negocio al DTO de lectura.
    """

    private = False
    status = True

    if user and user.role == UserRoles.ADMINISTRATOR.value:
        private = True
        status = None

    products, total_items = await service.get_list_products(
        private=private,
        status=status,
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
