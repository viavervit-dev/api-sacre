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
from src.modules.auth.models.user import User
from src.modules.auth.permissions import UserPermissionChecker
from src.modules.products.dto import ReadProductDTO, UpdateProductDTO
from src.modules.products.models.product import Product
from src.modules.products.repositories.product import ProductRepository
from src.modules.products.services.update_product import UpdateProductService

router = APIRouter(prefix="/product", tags=["Productos"])
require_admin = UserPermissionChecker(
    allowed_role=UserRoles.ADMINISTRATOR.value,
    permission=f"{Product.__tablename__}.update",
)


async def validations(
    data: UpdateProductDTO,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> UpdateProductDTO:
    """Ejecuta validaciones adicionales para la actualización de un producto."""

    all_errors: list[Any] = []

    # Lista de todas las validaciones que queremos correr
    checks = [data.check_name, data.check_images_urls, data.check_categories]

    for check in checks:
        try:
            await check(db=db, product_repo=ProductRepository)
        except RequestValidationError as e:
            all_errors.extend(e.errors())

    if all_errors:
        raise RequestValidationError(errors=all_errors)

    return data


@router.patch(
    path="/{product_id}/",
    response_description="Producto actualizado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        400: response_scheme_400(dto_class=UpdateProductDTO),
        401: response_scheme_401(
            jwt_missing=True,
            jwt_invalid=True,
            jwt_expired=True,
            jwt_user_not_found=True,
        ),
        403: response_scheme_403(),
        404: response_scheme_404(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def update_product(
    user: Annotated[tuple[User, Admin], Depends(require_admin)],
    data: Annotated[UpdateProductDTO, Depends(validations)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único del producto en formato UUID v4.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
    ],
) -> Response[ReadProductDTO]:
    """
    Endpoint para la actualización de un producto, recibe una petición con los datos necesarios y
    ejecuta validaciones adicionales. Si todo es correcto, actualiza el producto en la base de
    datos y devuelve su información.
    """

    service = UpdateProductService(db=db, product_repo=ProductRepository)
    product = await service.update_product(id=product_id, data=data)

    return Response(
        success=True,
        message="Producto actualizado exitosamente.",
        data=product,
    )
