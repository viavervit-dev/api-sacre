from typing import Annotated

from fastapi import APIRouter, Depends, Query
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
from src.modules.products.dto import PrivateReadCategoryDTO, PublicReadCategoryDTO
from src.modules.products.models.category import Category
from src.modules.products.repositories.product import ProductRepository
from src.modules.products.services.get_category import GetCategoryService

router = APIRouter(prefix="/product", tags=["Productos"])
require_admin = UserOptionalPermissionChecker(
    allowed_role=UserRoles.ADMINISTRATOR.value,
    permission=f"{Category.__tablename__}.read",
)


schema_200_ok = {
    "description": "**(OK)** Lista de categorías de productos obtenida exitosamente.",
    "model": Response[list[PrivateReadCategoryDTO | PublicReadCategoryDTO]],
    "content": {
        "application/json": {
            "examples": {
                "private_data": {
                    "summary": "Datos privados",
                    "value": {
                        "success": True,
                        "pagination": True,
                        "message": "Lista de categorías de productos obtenida exitosamente.",
                        "data": {
                            "items": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "Rosarios",
                                    "description": "Categoría de rosarios de madera.",
                                    "product_count": 52,
                                    "status": True,
                                },
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "Joyas",
                                    "description": "Categoría de joyas de plata.",
                                    "product_count": 15,
                                    "status": False,
                                },
                            ],
                            "meta": {
                                "total": 2,
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
                        "message": "Lista de categorías de productos obtenida exitosamente.",
                        "data": {
                            "items": [
                                {
                                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "Rosarios",
                                    "description": "Categoría de rosarios de madera.",
                                    "product_count": 52,
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
                    "summary": "No hay categorías",
                    "value": {
                        "success": True,
                        "pagination": True,
                        "message": "Lista de categorías de productos obtenida exitosamente.",
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
}


@router.get(
    path="/category/",
    responses={
        200: schema_200_ok,
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
async def get_list_categories(
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
) -> Response[PaginatedData[PrivateReadCategoryDTO | PublicReadCategoryDTO]]:
    """
    Endpoint para la obtención de una lista de categorías, recibe una petición con los datos
    necesarios y ejecuta validaciones adicionales. Si todo es correcto, obtiene las categorías en
    la base de datos y devuelve su información.
    """

    user_account, _ = user
    service = GetCategoryService(db=db, product_repo=ProductRepository)
    categories, total_items = await service.get_list_categories(
        private=bool(user_account),
        status=None if not bool(user_account) else True,
        offset=offset,
        limit=limit,
    )

    return Response(
        success=True,
        pagination=True,
        message="Lista de categorías obtenida exitosamente.",
        data=PaginatedData(
            items=categories,
            meta=PaginationMeta(total=total_items, offset=offset, limit=limit),
        ),
    )
