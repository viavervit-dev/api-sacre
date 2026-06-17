from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.constants import PAGINATION_LIMIT_DESCRIPTION, PAGINATION_OFFSET_DESCRIPTION
from src.common.response import PaginatedData, PaginationMeta, Response
from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.config.parameters import settings
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserOptionalPermissionChecker
from src.modules.auth.models.user import User
from src.modules.products.dto import PrivateReadProductDTO, PublicReadProductDTO
from src.modules.products.models.product import Product
from src.modules.products.repositories.product import ProductRepository
from src.modules.products.services.get_product import GetProductService

router = APIRouter(prefix="/product", tags=["Productos"])
require_admin = UserOptionalPermissionChecker(
    allowed_role=UserRoles.ADMINISTRATOR.value,
    permission=f"{Product.__tablename__}.read",
)


@router.get(
    path="/",
    response_description="**(OK)** Lista de productos obtenida exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Estado de salud de los componentes de la API.",
            "model": Response[list[PrivateReadProductDTO | PublicReadProductDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "private_data": {
                            "summary": "Datos privados",
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
                        "public_data": {
                            "summary": "Datos públicos",
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
                        "there_not_products": {
                            "summary": "No hay productos",
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
        401: response_scheme_401(
            jwt_missing=True,
            jwt_invalid=True,
            jwt_expired=True,
            jwt_user_not_found=True,
        ),
        403: response_scheme_403(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def get_list_products(
    user: Annotated[tuple[User | None, Admin | None], Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = Query(
        default=0,
        ge=0,
        title="Registros a omitir",
        description=PAGINATION_OFFSET_DESCRIPTION,
    ),
    limit: int = Query(
        default=settings.pagination_limit,
        ge=1,
        le=settings.pagination_limit,
        title="Límite de registros",
        description=PAGINATION_LIMIT_DESCRIPTION,
    ),
) -> Response[PaginatedData[PrivateReadProductDTO | PublicReadProductDTO]]:
    """
    Endpoint para la creación de un producto, recibe una petición con los datos necesarios y
    ejecuta validaciones adicionales. Si todo es correcto, crea el producto en la base de datos
    y devuelve su información.
    """

    user_account, _ = user
    service = GetProductService(db=db, product_repo=ProductRepository)
    products, total_items = await service.get_list_products(
        private=bool(user_account),
        status=None if not bool(user_account) else True,
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
