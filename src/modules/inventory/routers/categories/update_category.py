from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dependencies import get_category
from src.modules.inventory.dto import PrivateReadCategoryDTO, UpdateCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.product import ProductRepository
from src.modules.inventory.services.categories.update_category import UpdateCategoryService

router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.update"},
)


async def validations(
    data: UpdateCategoryDTO,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> UpdateCategoryDTO:
    """Ejecuta validaciones adicionales para la actualización de una categoria de producto."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [data.check_name]

    for check in checks:
        try:
            await check(db=db, product_repo=ProductRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(errors=all_errors)

    return data


@router.patch(
    path="/category/{category_id}/",
    response_description="**(OK)** Categoría de producto actualizada exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        400: response_scheme_400(dto_class=UpdateCategoryDTO),
        401: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
        ),
        403: response_scheme_403(),
        404: response_scheme_404(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def update_category(
    category_id: Annotated[
        UUID,
        Path(
            title="ID de la categoria del producto.",
            description="El identificador único en formato UUID v4.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
    ],
    user: Annotated[tuple[User, Admin], Depends(require_admin)],
    category: Annotated[Category, Depends(get_category)],
    data: Annotated[UpdateCategoryDTO, Depends(validations)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[PrivateReadCategoryDTO]:
    """
    Endpoint para la actualización de una categoria de producto, recibe una petición con los datos
    necesarios y ejecuta validaciones adicionales. Si todo es correcto, actualiza la categoria en
    la base de datos y devuelve su información.
    """

    service = UpdateCategoryService(db=db, product_repo=ProductRepository)
    updated_category = await service.update_category(instance=category, data=data)

    return Response(
        success=True,
        pagination=False,
        message="Categoria de producto actualizada exitosamente.",
        data=updated_category,
    )
