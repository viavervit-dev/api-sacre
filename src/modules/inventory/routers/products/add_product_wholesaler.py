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
from src.modules.inventory.dependencies import get_add_product_wholesale_service
from src.modules.inventory.dto import CreateProductDTO, ReadProductWholesalerDTO
from src.modules.inventory.models.product import Product
from src.modules.inventory.services.products.add_product_wholesaler import (
    AddProductWholesaleService,
)

add_product_wholesaler_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Product.__tablename__}.create"},
)


@add_product_wholesaler_router.post(
    path="/product/{wholesaler_id}/",
    response_description="**(CREATED)** Producto agregado exitosamente.",
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
        status.HTTP_404_NOT_FOUND: response_scheme_404(),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def add_product_wholesaler(
    user: Annotated[User, Depends(require_admin)],
    data: CreateProductDTO,
    wholesaler_id: Annotated[
        UUID,
        Path(
            title="ID del cliente mayorista",
            description="El ID del cliente mayorista al que se le asignará el producto.",
        ),
    ],
    service: Annotated[AddProductWholesaleService, Depends(get_add_product_wholesale_service)],
) -> Response[ReadProductWholesalerDTO]:
    """
    Crea un nuevo producto en el inventario asignado exclusivamente a un cliente mayorista.

    ### Descripción
    Registra un producto exclusivo para un cliente mayorista a partir de los datos
    proporcionados y su identificador (`wholesaler_id`), ejecutando validaciones sintácticas
    y de negocio. Tras validar los datos y la existencia del mayorista, calcula el precio
    de venta final, determina el estado inicial, incrementa el contador de productos en las
    categorías asociadas y persiste la información vinculada al mayorista en la base de datos.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `products.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario.
        - Comprueba que el usuario tenga rol de administrador y el permiso `products.create`.
    2. **Validación Sintáctica y Parámetros:**
        - Valida el identificador del mayorista (`wholesaler_id`) como un UUID en la ruta.
        - Valida tipos de datos, longitudes y rangos numéricos.
    3. **Verificación de Existencia del Mayorista:**
        - Comprueba que el cliente mayorista exista en la base de datos. Si no existe, levanta
         (código HTTP 404 Not Found).
    4. **Validaciones de Reglas de Negocio:**
        - **Unicidad:** Verifica que el nombre del producto no esté previamente registrado.
        - **URLs de Imágenes:** Comprueba que cada URL de la lista sea válida.
        - **Categorías:** Comprueba que cada una de las categorías indicadas exista
         previamente en la base de datos.
    5. **Cálculos y Transformaciones:**
        - **Precio de Venta (`price_sale`):** Se calcula automáticamente mediante la fórmula:
         `price_sale = round_half_up(price_neto * (1 + profit_margin) * (1 + iva), 2)`.
        - **Estado inicial (`status`):** Se establece en `True` si `stock_total > 0`;
         en caso contrario, se define en `False`.
        - **Stocks auxiliares:** Inicializa `stock_hand` en `0` y `stock_sale` con `stock_total`.
        - **Categorías:** Incrementa en `1` el contador de productos (`product_count`)
         de cada categoría asignada.
        - **Asignación:** Vincula el producto al mayorista mediante `wholesaler_id`.
    6. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    product = await service.add_product(data=data, wholesaler_id=wholesaler_id)

    return Response(
        success=True,
        pagination=False,
        message="Producto agregado exitosamente.",
        data=product,
    )
