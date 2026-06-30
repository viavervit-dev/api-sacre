from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.response import Response
from src.common.schema import (
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
from src.modules.inventory.dependencies import get_product
from src.modules.inventory.models.product import Product
from src.modules.inventory.repositories.product import ProductRepository
from src.modules.inventory.services.products.delete_product import DeleteProductService

router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.delete"},
)


@router.delete(
    path="/product/{product_id}/",
    response_description="**(OK)** Producto eliminado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        401: response_scheme_401(
            access_jwt_missing=True,
            access_jwt_invalid=True,
            jwt_user_not_found=True,
            product_has_reserved_stock=True,
        ),
        403: response_scheme_403(),
        404: response_scheme_404(),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def delete_product(
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único en formato UUID v4.",
            example="123e4567-e89b-12d3-a456-426614174000",
        ),
    ],
    user: Annotated[tuple[User, Admin], Depends(require_admin)],
    product: Annotated[Product, Depends(get_product)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Response[dict[str, str]]:
    """
    Endpoint para la eliminación de un producto, recibe una petición con los datos necesarios y
    ejecuta validaciones adicionales. Si todo es correcto, elimina el producto en la base de
    datos y devuelve su información.
    """

    service = DeleteProductService(db=db, product_repo=ProductRepository)
    await service.delete_product(instance=product)

    return Response(
        success=True,
        pagination=False,
        message="Producto eliminado exitosamente.",
        data={},
    )
