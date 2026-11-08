from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.api.common.response import Response
from src.api.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.api.modules.auth.constants import UserRoles
from src.api.modules.auth.dependencies import UserPermissionChecker
from src.api.modules.auth.models.user import User
from src.api.modules.inventory.dependencies import update_product_wholesaler_service
from src.api.modules.inventory.dto import ReadWholesalerProductDTO, UpdateWholesalerProductDTO
from src.api.modules.inventory.models import WholesalerProduct
from src.api.modules.inventory.services.products.wholesaler import UpdateProductWholesalerService

update_product_wholesaler_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{WholesalerProduct.__tablename__}.update"},
)


@update_product_wholesaler_router.patch(
    path="/product/wholesaler/{product_id}/",
    response_description="**(OK)** Producto actualizado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=UpdateWholesalerProductDTO),
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
async def update_product_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    data: UpdateWholesalerProductDTO,
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único del producto en formato UUID v4.",
        ),
    ],
    service: Annotated[UpdateProductWholesalerService, Depends(update_product_wholesaler_service)],
) -> Response[ReadWholesalerProductDTO]:
    """
    Permite modificar de forma parcial un producto para clientes mayoristas a partir de los datos
    proporcionados y su identificador (`product_id`). Aplica validaciones de reglas de negocio para
    garantizar unicidad en el nombre y existencia previa de las categorías asociadas. Este producto
    es exclusivo del canal mayorista y no forma parte del catálogo público general.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `wholesaler_products.update`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Comprueba que el usuario cuente con rol de administrador y el permiso específico
            `wholesaler_products.update`.
    2. **Validación Sintáctica:**
        - Valida el identificador `product_id` en la ruta como un UUID v4 válido.
        - Valida el esquema del cuerpo de la petición, tipos de datos y longitudes de campos
            de texto.
    3. **Búsqueda del Recurso:**
        - Consulta el producto en la base de datos a través de su identificador único.
        - Si no existe el producto, interrumpe el flujo levantando (404 Not Found).
    4. **Validaciones de Reglas de Negocio:**
        - **Unicidad de Nombre:** Si se modifica `name`, comprueba que no esté en uso por otro
          producto mayorista.
        - **Existencia de Categorías:** Si se modifican `categories`, verifica que cada una de
          las categorías exista previamente en la base de datos.
    5. **Persistencia y Retorno:**
        - Aplica las modificaciones en la base de datos omitiendo campos no provistos.
        - Mapea el registro actualizado al DTO de lectura.
    """

    updated_product = await service.update(product_id=product_id, data=data)

    return Response(
        success=True,
        pagination=False,
        message="Producto actualizado exitosamente.",
        data=updated_product,
    )
