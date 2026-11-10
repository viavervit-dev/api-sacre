from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models import User
from src.api.modules.inventory.dependencies import delete_product_wholesaler_service
from src.api.modules.inventory.models import WholesalerProduct
from src.api.modules.inventory.services.products.wholesaler import DeleteProductWholesalerService

delete_product_wholesaler_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{WholesalerProduct.__tablename__}.delete"},
)


@delete_product_wholesaler_router.delete(
    path="/product/wholesaler/{product_id}/",
    response_description="**(OK)** Producto eliminado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            access_jwt_expired=True,
            jwt_user_not_found=True,
            auth_session_expired=True,
        ),
        status.HTTP_403_FORBIDDEN: response_scheme_403(),
        status.HTTP_404_NOT_FOUND: response_scheme_404(),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def delete_product_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único del producto en formato UUID v4.",
            examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        ),
    ],
    service: Annotated[DeleteProductWholesalerService, Depends(delete_product_wholesaler_service)],
) -> Response[dict[str, str]]:
    """
    Permite eliminar de forma permanente un producto para cliente mayorista a partir de su
    identificador único (`product_id`). Antes de proceder con la eliminación física en la base
    de datos, verifica que el producto exista en el inventario. Este producto es exclusivo
    del canal mayorista y no forma parte del catálogo público general.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `wholesaler_products.delete`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Comprueba la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Verifica que el usuario cuente con rol de administrador y el permiso específico
          `wholesaler_products.delete`.
    2. **Validación Sintáctica del Parámetro de Ruta:**
        - Valida que el identificador `product_id` cumpla con el formato estándar UUID v4.
    3. **Búsqueda del Recurso:**
        - Invoca el método `delete` de `DeleteProductWholesalerService`.
        - Consulta el producto en la base de datos a través de su identificador único.
        - Si no existe el producto, interrumpe el flujo levantando `ResourceNotFound`
          (404 Not Found).
    4. **Persistencia y Retorno:**
        - Elimina de forma definitiva el registro del producto en la base de datos.
        - Retorna la respuesta unificada `Response` con código HTTP 200 (OK), confirmando
          la eliminación con un diccionario vacío en `data`.
    """

    await service.delete(product_id=product_id)

    return Response(
        success=True,
        pagination=False,
        message="Producto eliminado exitosamente.",
        data={},
    )
