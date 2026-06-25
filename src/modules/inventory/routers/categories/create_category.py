from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.config.database import get_db_session
from src.modules.admins.models.admin import Admin
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dto import CreateCategoryDTO, PrivateReadCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.repositories.product import ProductRepository
from src.modules.inventory.services.categories.create_category import CreateCategoryService

router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.create"},
)


async def validations(
    data: CreateCategoryDTO,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> CreateCategoryDTO:
    """Ejecuta validaciones adicionales para la creación de una categoría."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [data.check_name]

    for check in checks:
        try:
            await check(db=db, product_repo=ProductRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(all_errors)

    return data


@router.post(
    path="/category/",
    response_description="**(CREATED)** Categoría creada exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: response_scheme_400(dto_class=CreateCategoryDTO),
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
async def create_category(
    user: Annotated[tuple[User, Admin], Depends(require_admin)],
    data: Annotated[CreateCategoryDTO, Depends(validations)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[PrivateReadCategoryDTO]:
    """
    Endpoint para la creación de una categoría de productos, recibe una petición con los datos
    necesarios y ejecuta validaciones adicionales. Si todo es correcto, crea la categoría en la
    base de datos y devuelve su información.
    """

    service = CreateCategoryService(db=db, product_repo=ProductRepository)
    category = await service.create_category(data=data)

    return Response(
        success=True,
        pagination=False,
        message="Categoría creada exitosamente.",
        data=category,
    )
