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
from src.modules.inventory.dependencies import get_retrieve_list_category_service
from src.modules.inventory.dto import PrivateReadCategoryDTO, PublicReadCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.services.categories.get_list_category import RetrieveListCategoryService

get_categories_router = APIRouter(prefix="/inventory", tags=["Inventario"])
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


@get_categories_router.get(
    path="/category/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "**(OK)** Lista de categorías de productos obtenida exitosamente.",
            "model": Response[PaginatedData[PrivateReadCategoryDTO | PublicReadCategoryDTO]],
            "content": {
                "application/json": {
                    "examples": {
                        "response_1": {
                            "summary": "Existen categorías - Datos privados",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de categorías de productos obtenida exitosamente.",  # noqa
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
                        "response_2": {
                            "summary": "Existen categorías - Datos públicos",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de categorías de productos obtenida exitosamente.",  # noqa
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
                        "response_3": {
                            "summary": "No existen categorías",
                            "value": {
                                "success": True,
                                "pagination": True,
                                "message": "Lista de categorías de productos obtenida exitosamente.",  # noqa
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
async def get_list_categories(
    user: Annotated[User | None, Depends(require_admin)],
    service: Annotated[RetrieveListCategoryService, Depends(get_retrieve_list_category_service)],
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
) -> Response[PaginatedData[PrivateReadCategoryDTO | PublicReadCategoryDTO]]:
    """
    Obtiene una lista paginada de categorías con visibilidad adaptativa según el usuario.

    ### Descripción
    Consulta y retorna las categorías de productos con soporte para paginación y ordenamiento
    cronológico descendente. La información y los filtros aplicados se adaptan dinámicamente
    según el nivel de privilegios del usuario solicitante:
    - **Público / Clientes:** Acceso libre o como cliente. Solo lista categorías
     activas (`status=True`) y expone datos comerciales públicos.
    - **Privado / Administradores:** Usuarios con rol de administrador. Acceden a todas las
     categorías (activas e inactivas) y visualizan de datos comerciales públicos y privados.

    ### Requisitos de Acceso
    - **Acceso Anónimo:** Permitido sin autenticación (vista pública).
    - **Clientes (`customer`):** Requiere permiso `categories.read.public`.
    - **Administradores (`admin`):** Requiere permiso `categories.read.private`.
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
        - Si existen registros, consulta las categorías ordenadas descendentemente por fecha de
         creación, aplicando `offset` y `limit`.
    4. **Serialización Dinámica:**
        - Mapea los resultados a visión administrativa completa o visión pública segura sin estado
         interno.
    """

    private = False
    status = True

    if user and user.role == UserRoles.ADMINISTRATOR.value:
        private = True
        status = None

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
