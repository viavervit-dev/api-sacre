from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.common.schema import (
    response_scheme_400,
    response_scheme_401,
    response_scheme_503,
)
from src.config.parameters import settings
from src.modules.auth.dependencies import get_jwt_admin_service
from src.modules.auth.dto import AdminCredentialsDTO
from src.modules.auth.services.jwt.authenticate_admin import AuthAdminService

jwt_admin_router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@jwt_admin_router.post(
    path="/jwt/admin/",
    response_description="**(NO_CONTENT)** Administrador autenticado exitosamente.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: response_scheme_400(dto_class=AdminCredentialsDTO),
        401: response_scheme_401(credentials_invalid=True, access_jwt_invalid=True),
        503: response_scheme_503(db_unavailable=True),
    },
)
async def authenticate_admin(
    service: Annotated[AuthAdminService, Depends(get_jwt_admin_service)],
    credentials: AdminCredentialsDTO,
    response: Response,
) -> None:
    """
    Autentica a un administrador y establece las cookies de sesión con tokens JWT.

    ### Descripción
    Valida las credenciales de un administrador (correo y contraseña), comprueba que la cuenta
    posea los privilegios necesarios para autenticarse (`authentication.jwt`) y genera un par de
    tokens criptográficos (acceso y actualización). Los tokens se configuran directamente en
    cookies seguras (`HttpOnly`), devolviendo una respuesta sin contenido.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto para inicio de sesión de administradores.
    - **Condiciones de Cuenta:** Requiere rol `ADMINISTRATOR` y permiso `authentication.jwt`.

    ### Flujo de Ejecución
    1. **Validación Sintáctica (DTO):**
       - Valida el formato del correo electrónico (`EmailStr`) y la presencia de la contraseña.
    2. **Autenticación y Control de Permisos:**
       - Consulta al usuario en la base de datos verificando que posea rol de administrador.
       - Valida que el administrador cuente con el permiso específico `authentication.jwt`.
       - Compara la contraseña provista contra el hash almacenado (bcrypt).
       - Si cualquiera de estas comprobaciones falla, deniega el acceso con error 401.
    3. **Emisión de Tokens JWT:**
       - Genera un `access_token` firmado criptográficamente con la clave privada, conteniendo
         el identificador del usuario, rol, versión de sesión y tiempo de expiración.
       - Genera un `refresh_token` de mayor duración para renovación de sesiones.
    4. **Inyección de Cookies HTTP:**
       - Configura `access_token` y `refresh_token` como cookies `HttpOnly`, `SameSite=Lax` y
         con flag `Secure` habilitado en entornos no-debug.
    """

    access_token, refresh_token = await service.authenticate_admin(credentials=credentials)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.access_token_expire * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.refresh_token_expire * 60,
    )
