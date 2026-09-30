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
from src.modules.inventory.dependencies import get_create_category_service
from src.modules.inventory.dto import CreateCategoryDTO, PrivateReadCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.services.categories.create_category import CreateCategoryService

create_category_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.create"},
)


@create_category_router.post(
    path="/category/",
    response_description="**(CREATED)** Categoría creada exitosamente.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=CreateCategoryDTO),
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
async def create_category(
    user: Annotated[User, Depends(require_admin)],
    data: CreateCategoryDTO,
    service: Annotated[CreateCategoryService, Depends(get_create_category_service)],
) -> Response[PrivateReadCategoryDTO]:
    """
    Crea una nueva categoría de productos e inicializa sus métricas.

    ### Descripción
    Registra una nueva categoría en el sistema a partir del nombre y la descripción provistos.
    Verifica la unicidad del nombre en el inventario e inicializa automáticamente los valores
    por defecto de la entidad (contador de productos en cero y estado inactivo).

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `categories.create`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Comprueba que el usuario tenga rol de administrador y el permiso `categories.create`.
    2. **Validación Sintáctica (DTO):**
        - Valida que el nombre y la descripción cumplan con los esquemas definidos.
    3. **Validación de Reglas de Negocio:**
        - **Unicidad de Nombre:** Consulta la base de datos para confirmar que no exista otra
         categoría con el mismo nombre.
    4. **Inicialización de Valores:**
        - Asigna `product_count = 0` (sin artículos asociados inicialmente).
        - Asigna `status = False` (inactiva por defecto hasta que disponga de productos).
    5. **Persistencia:**
        - Guarda el registro en la base de datos.
    """

    category = await service.create_category(data=data)

    return Response(
        success=True,
        pagination=False,
        message="Categoría creada exitosamente.",
        data=category,
    )
