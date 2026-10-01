from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.common.schema import (
    response_scheme_401,
    response_scheme_503,
)
from src.modules.auth.dependencies import get_jwt_logout_service, get_raw_tokens
from src.modules.auth.services.jwt.logout import LogoutService

jwt_logout_router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@jwt_logout_router.post(
    path="/jwt/logout/",
    response_description="**(NO_CONTENT)** Se cierra la sesión del usuario.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            refresh_jwt_invalid=True,
            access_jwt_expired=True,
            refresh_jwt_expired=True,
            auth_session_expired=True,
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def logout(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    service: Annotated[LogoutService, Depends(get_jwt_logout_service)],
) -> None:
    """
    Cierra la sesión activa del usuario e invalida sus tokens JWT.

    ### Descripción
    Revoca la sesión activa del usuario autenticado invalidando los tokens de acceso y
    actualización provistos en las cookies de la petición. Incrementa la versión de sesión
    (`session_version`) del usuario en la base de datos, lo que inhabilita de forma inmediata
    todos los tokens previamente emitidos. Incluye detección de integridad contra tokens cruzados
    o sesiones corruptas.

    ### Requisitos de Acceso
    - **Autenticación requerida:** Cookies obligatorias `access_token` y `refresh_token` (JWT).

    ### Flujo de Ejecución
    1. **Extracción y Validación de Cookies:**
        - Intercepta los tokens `access_token` y `refresh_token` presentes en las cookies HTTP.
        - Si falta alguno de los dos tokens, interrumpe el flujo con error 401 (MissingJWT).
    2. **Validación Criptográfica de Tokens:**
        - Valida la firma y expiración del `access_token`.
        - Valida la firma y expiración del `refresh_token`.
    3. **Verificación de Coherencia de Sesión:**
        - Comprueba que el identificador de usuario (`sub`) coincida en ambos tokens.
        - Si los identificadores difieren (sesión corrupta o mezcla de tokens), incrementa las
         versiones de sesión de ambos usuarios por seguridad y deniega la operación con 401.
    4. **Invalidación de Sesión en Base de Datos:**
        - Incrementa en `1` la columna `session_version` del usuario en el esquema `auth.users`.
        - Al alterarse la versión, cualquier token emitido previamente queda revocado para
         todas las peticiones subsiguientes.
    """

    access_token, refresh_token = tokens
    await service.logout(access_token=access_token, refresh_token=refresh_token)
