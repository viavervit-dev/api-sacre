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
from src.modules.inventory.dependencies import get_delete_category_service
from src.modules.inventory.models.category import Category
from src.modules.inventory.services.categories.delete_category import DeleteCategoryService

delete_category_router = APIRouter(prefix="/inventory", tags=["Inventario"])
require_admin = UserPermissionChecker(
    allowed_roles=[UserRoles.ADMINISTRATOR.value],
    permissions={UserRoles.ADMINISTRATOR.value: f"{Category.__tablename__}.delete"},
)


@delete_category_router.delete(
    path="/category/{category_id}/",
    response_description="**(OK)** Categoría de producto eliminada exitosamente.",
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
        status.HTTP_409_CONFLICT: response_scheme_409(category_has_dependencies=True),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def delete_category(
    user: Annotated[User, Depends(require_admin)],
    category_id: Annotated[
        UUID,
        Path(
            title="ID de la categoría del producto",
            description="El identificador único en formato UUID v4.",
            examples=["123e4567-e89b-12d3-a456-426614174000"],
        ),
    ],
    service: Annotated[DeleteCategoryService, Depends(get_delete_category_service)],
) -> Response[dict[str, str]]:
    """
    Elimina una categoría del catálogo tras verificar sus dependencias.

    ### Descripción
    Elimina de forma permanente una categoría existente en la base de datos a partir de su
    identificador único (`category_id`). Antes de proceder con el borrado, comprueba la existencia
    del recurso y valida que no cuente con productos asociados para preservar la integridad
    del inventario.

    ### Requisitos de Acceso
    - **Rol requerido:** Administrador (`admin`).
    - **Permiso requerido:** `categories.delete`.
    - **Autenticación:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Autenticación y Autorización:**
        - Extrae y valida los tokens JWT presentes en las cookies de la petición.
        - Verifica la vigencia de la sesión y la existencia del usuario en la base de datos.
        - Comprueba que el usuario tenga rol de administrador y el permiso `categories.delete`.
    2. **Búsqueda del Recurso:**
        - Consulta la categoría en la base de datos por su `category_id`.
        - Si no se encuentra ningún registro, interrumpe el flujo con un error 404 (Not Found).
    3. **Validación de Reglas de Negocio:**
        - Comprueba que la categoría no tenga productos vinculados (`product_count == 0`).
        - Si posee artículos asociados (`product_count > 0`), deniega la eliminación para evitar
         inconsistencias en el catálogo.
    4. **Persistencia:**
        - Elimina el registro de la categoría de la base de datos.
    """

    await service.delete_category(category_id=category_id)

    return Response(
        success=True,
        pagination=False,
        message="Categoría de producto eliminada exitosamente.",
        data={},
    )
