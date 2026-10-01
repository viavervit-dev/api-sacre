from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.common.response import Response
from src.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_409,
    response_scheme_503,
)
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dependencies import get_delete_product_service
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.delete_product import DeleteProductService

delete_product_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.delete"},
)


@delete_product_router.delete(
    path="/product/{product_id}/",
    response_description="**(OK)** Producto eliminado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
        ),
        status.HTTP_403_FORBIDDEN: response_scheme_403(),
        status.HTTP_404_NOT_FOUND: response_scheme_404(),
        status.HTTP_409_CONFLICT: response_scheme_409(product_has_reserved_stock=True),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def delete_product(
    user: Annotated[User, Depends(require_admin)],
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único en formato UUID v4.",
            examples=["123e4567-e89b-12d3-a456-426614174000"],
        ),
    ],
    service: Annotated[DeleteProductService, Depends(get_delete_product_service)],
) -> Response[dict[str, str]]:
    """
    Elimina un producto del catálogo tras verificar las reglas de inventario.

    ### Descripción
    Elimina de forma permanente un producto existente en la base de datos a partir de su
    identificador único (`product_id`). Antes de proceder con el borrado, comprueba la existencia
    del recurso y valida que no existan compromisos de stock activo que impidan su eliminación.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `products.delete`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario.
        - Comprueba que el usuario tenga rol de administrador y el permiso `products.delete`.
    2. **Búsqueda del Recurso:**
        - Consulta el producto en la base de datos por su `product_id`.
        - Si no se encuentra ningún registro, interrumpe el flujo con un error 404 (Not Found).
    3. **Validación de Reglas de Negocio:**
        - Comprueba que el producto no posea stock en reserva (`stock_hand == 0`).
        - Si existen unidades reservadas en carritos activos (`stock_hand > 0`), deniega la
         eliminación para preservar la integridad del proceso de compra.
    4. **Persistencia:**
        - Elimina el registro del producto de la base de datos.
    """

    await service.delete_product(product_id=product_id)

    return Response(
        success=True,
        pagination=False,
        message="Producto eliminado exitosamente.",
        data={},
    )
