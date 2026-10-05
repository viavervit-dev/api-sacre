from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.response import Response
from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_403,
    response_scheme_503,
)
from src.modules.auth.constants import UserRoles
from src.modules.auth.dependencies import UserPermissionChecker
from src.modules.auth.models.user import User
from src.modules.inventory.dependencies import get_create_product_service
from src.modules.inventory.dto import CreateProductDTO, PrivateReadProductDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.create_product import CreateProductService

create_product_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.create"},
)


@create_product_router.post(
    path="/product/",
    response_description="**(CREATED)** Producto creado exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=CreateProductDTO),
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
async def create_product(
    user: Annotated[User, Depends(require_admin)],
    data: CreateProductDTO,
    service: Annotated[CreateProductService, Depends(get_create_product_service)],
) -> Response[PrivateReadProductDTO]:
    """
    Permite crear un nuevo producto. Ejecuta validaciones sintácticas y comprobaciones de
    unicidad en la base de datos para prevenir duplicados. Este producto sí hará parte del
    catálogo de productos que se ofrecen a los usuarios finales.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `products.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario.
        - Comprueba que el usuario tenga rol de administrador y el permiso `products.create`.
    2. **Validación Sintáctica (DTO):**
        - Valida tipos de datos, longitudes y rangos numéricos mediante.
    3. **Validaciones de Reglas de Negocio:**
        - **Unicidad:** Verifica que el nombre del producto no esté previamente registrado.
        - **URLs de Imágenes:** Comprueba que cada URL de la lista sea válida.
        - **Categorías:** Comprueba que cada una de las categorías indicadas exista
         previamente en la base de datos.
    4. **Cálculos y Transformaciones:**
        - **Precio de Venta (`price_sale`):** Se calcula automáticamente mediante la fórmula:
         `price_sale = round_half_up(price_neto * (1 + profit_margin) * (1 + iva), 2)`.
        - **Estado inicial (`status`):** Se establece en `True` si `stock_total > 0`;
         en caso contrario, se define en `False`.
        - **Stocks auxiliares:** Inicializa `stock_hand` y `stock_sale` en `0`.
        - **Categorías:** Incrementa en `1` el contador de productos (`product_count`)
         de cada categoría asignada.
    5. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    product = await service.create_product(data=data)

    return Response(
        success=True,
        pagination=False,
        message="Producto creado exitosamente.",
        data=product,
    )
