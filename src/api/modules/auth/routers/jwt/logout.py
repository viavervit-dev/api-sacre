from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.api.common.exceptions import AuthenticationFailed, InvalidJWT, MissingJWT
from src.api.common.response import Response as APIResponse
from src.api.common.schema import (
    response_scheme_401,
    response_scheme_503,
)
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.dependencies import jwt_logout_service, optional_tokens
from src.api.modules.auth.services.jwt import LogoutService
from src.api.settings.parameters import api_parameters
from src.api.settings.serialization import JSONResponse

jwt_logout_router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@jwt_logout_router.post(
    path="/jwt/logout/",
    response_description="**(NO_CONTENT)** Se cierra la sesión del usuario.",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            refresh_jwt_missing=True,
            refresh_jwt_invalid=True,
            refresh_jwt_expired=True,
            auth_session_expired=True,
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def logout(
    tokens: Annotated[tuple[str | None, str | None], Depends(optional_tokens)],
    response: Response,
    service: Annotated[LogoutService, Depends(jwt_logout_service)],
) -> Response | None:
    """
    Permite revocar la sesión activa del usuario autenticado invalidando su sesión a partir del
    `refresh_token` provisto en las cookies de la petición, sin impedir el cierre de sesión cuando
    el `access_token` esté vencido o ausente. Incrementa la versión de sesión (`session_version`)
    del usuario en la base de datos, lo que inhabilita de forma inmediata todos los tokens
    previamente emitidos, e incluye detección de integridad contra tokens cruzados.

    ### Requisitos de Acceso
    - **Autenticación requerida:** Cookie obligatoria `refresh_token` (JWT vigente). Cookie
        `access_token` opcional.

    ### Flujo de Ejecución
    1. **Extracción y Validación de Cookies:**
        - Intercepta las cookies HTTP `access_token` (opcional) y `refresh_token` (obligatoria).
        - Si falta `refresh_token`, elimina las cookies de autenticación y devuelve 401.
    2. **Validación Criptográfica de Tokens:**
        - Valida la firma, el tipo (`refresh`) y la vigencia del `refresh_token`.
        - Si está presente `access_token`, valida su firma y tipo (`access`) ignorando su
            expiración para comprobar coherencia de sesión (si es inválido, se descarta sin
            bloquear el cierre de sesión).
        - Verifica que `session_version` del token de actualización siga activa
            (401 si ya fue revocada).
    3. **Verificación de Coherencia de Sesión:**
        - Si `access_token` es criptográficamente válido pero su `sub` difiere del de
            `refresh_token` (sesión corrupta o mezcla de tokens), incrementa las versiones de
            sesión de ambos usuarios, elimina las cookies y deniega la operación con 401.
    4. **Invalidación de Sesión en Base de Datos:**
        - Incrementa en `1` la columna `session_version` del usuario en el esquema `auth.users`.
        - Al alterarse la versión, cualquier token emitido previamente queda revocado para
            todas las peticiones subsiguientes.
    5. **Eliminación de Cookies en el Navegador:**
        - Configura la respuesta HTTP para eliminar siempre las cookies `access_token` y
            `refresh_token` del navegador.
    """

    access_token, refresh_token = tokens

    try:
        if not refresh_token:
            raise MissingJWT(message=ExceptionErrorMessages.REFRESH_JWT_MISSING.value)

        await service.logout(access_token=access_token, refresh_token=refresh_token)
    except (MissingJWT, InvalidJWT, AuthenticationFailed) as exc:
        error_response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=APIResponse(
                success=False,
                pagination=False,
                message=exc.message,
                data=exc.data,
            ).model_dump(),
        )
        error_response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=not api_parameters.debug,
            samesite="lax",
        )
        error_response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=not api_parameters.debug,
            samesite="lax",
        )

        return error_response

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=not api_parameters.debug,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=not api_parameters.debug,
        samesite="lax",
    )

    return None
