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
from src.modules.inventory.dependencies import get_update_category_service
from src.modules.inventory.dto import PrivateReadCategoryDTO, UpdateCategoryDTO
from src.modules.inventory.models.category import Category
from src.modules.inventory.services.categories.update_category import UpdateCategoryService

update_category_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.update"},
)


@update_category_router.patch(
    path="/category/{category_id}/",
    response_description="**(OK)** Categoría de producto actualizada exitosamente.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: response_scheme_400(dto_class=UpdateCategoryDTO),
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
async def update_category(
    user: Annotated[User, Depends(require_admin)],
    data: UpdateCategoryDTO,
    category_id: Annotated[
        UUID,
        Path(
            title="ID de la categoria del producto.",
            description="El identificador único en formato UUID v4.",
        ),
    ],
    service: Annotated[UpdateCategoryService, Depends(get_update_category_service)],
) -> Response[PrivateReadCategoryDTO]:
    """
    Actualiza parcialmente una categoría existente en el catálogo.

    ### Descripción
    Actualiza los datos de una categoría en la base de datos mediante una modificación parcial
    (PATCH) a partir de su identificador único (`category_id`). Permite modificar su nombre
    y/o su descripción, verificando la unicidad del nuevo nombre en el inventario antes de
    aplicar los cambios.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `categories.update`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Comprueba que el usuario tenga rol de administrador y el permiso `categories.update`.
    2. **Búsqueda del Recurso:**
        - Consulta la categoría en la base de datos por su `category_id`.
        - Si no existe, interrumpe el flujo con un error 404 (Not Found).
    3. **Validación Sintáctica y de Reglas de Negocio:**
        - Valida el esquema y límites de los campos enviados.
        - **Unicidad de Nombre:** Si se modifica el nombre, comprueba que no se encuentre
         registrado previamente en otra categoría.
    4. **Persistencia:**
        - Aplica las modificaciones del registro en la base de datos.
    """

    updated_category = await service.update_category(category_id=category_id, data=data)

    return Response(
        success=True,
        pagination=False,
        message="Categoria de producto actualizada exitosamente.",
        data=updated_category,
    )
