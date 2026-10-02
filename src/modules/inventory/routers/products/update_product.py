from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.common.response import Response
from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_404,
    response_scheme_503,
)
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dependencies import get_update_product_service
from src.modules.inventory.dto import PrivateReadProductDTO, UpdateProductDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.update_product import UpdateProductService

update_product_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.update"},
)


@update_product_router.patch(
    path="/product/{product_id}/",
    response_description="**(OK)** Producto actualizado exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=UpdateProductDTO),
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
async def update_product(
    user: Annotated[User, Depends(require_admin)],
    data: UpdateProductDTO,
    product_id: Annotated[
        UUID,
        Path(
            title="ID del producto",
            description="El identificador único en formato UUID v4.",
        ),
    ],
    service: Annotated[UpdateProductService, Depends(get_update_product_service)],
) -> Response[PrivateReadProductDTO]:
    """
    Actualiza parcialmente un producto existente y recalcula sus precios de venta.

    ### Descripción
    Actualiza los datos de un producto en el catálogo mediante una modificación parcial (PATCH).
    Permite modificar atributos informativos, listas de categorías, URLs de imágenes, costos,
    márgenes y existencias. Si se alteran valores financieros (`price_neto`, `profit_margin` o
    `iva`), recalcula automáticamente el precio de venta final (`price_sale`).

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `products.update`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario.
        - Comprueba que el usuario tenga rol de administrador y el permiso `products.update`.
    2. **Búsqueda del Recurso:**
        - Consulta el producto en la base de datos por su `product_id`.
        - Si no existe, interrumpe el flujo con un error 404 (Not Found).
    3. **Validación Sintáctica y de Reglas de Negocio:**
        - Valida el esquema y formatos de los campos enviados.
        - **Consistencia de Stock:** Si se envía `stock_total`, comprueba que no sea menor a las
         unidades en reserva activa (`stock_hand`).
        - **Unicidad:** Si se modifica el nombre, verifica que no esté registrado previamente.
        - **URLs de Imágenes:** Si se envían imágenes, valida que cada URL sea válida.
        - **Categorías:** Si se envían categorías, comprueba que todas existan en la base de datos.
    4. **Cálculos y Transformaciones:**
        - **Estado (`status`):** Si `stock_total == 0` y no hay reservas (`stock_hand == 0`), se
         establece `status = False` automáticamente.
        - **Recálculo de Precio (`price_sale`):** Calcula el precio de venta final combinando los
         nuevos valores provistos con los existentes en la base de datos:
         `price_sale = round_half_up(price_neto * (1 + profit_margin) * (1 + iva), 2)`.
    5. **Persistencia:**
        - Aplica las modificaciones del registro en la base de datos.
    """

    updated_product = await service.update_product(product_id=product_id, data=data)

    return Response(
        success=True,
        pagination=False,
        message="Producto actualizado exitosamente.",
        data=updated_product,
    )
