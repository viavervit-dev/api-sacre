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
from src.modules.inventory.dto import PrivateReadCategoryDTO, PublicReadCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.product import ProductRepository
from src.modules.inventory.services.categories.get_category import GetCategoryService

router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserOptionalPermissionChecker(
    allowed_roles=[
        UserRoles.ADMINISTRATOR.value,
        UserRoles.CUSTOMER.value,
    ],
    permissions={
        UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.read.private",
        UserRoles.CUSTOMER.value: f"{Category.__tablename__}.read.public",
    },
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
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
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
    private = False
    status = True

    if user_account and user_account.role == UserRoles.ADMINISTRATOR.value:
        private = True
        status = None

    service = GetCategoryService(db=db, product_repo=ProductRepository)
    categories, total_items = await service.get_list_categories(
        private=private,
        status=status,
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
