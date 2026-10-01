from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.common.schema import (
    response_scheme_401,
    response_scheme_503,
)
from src.config.parameters import settings
from src.modules.auth.dependencies import get_jwt_refresh_token_service, get_raw_tokens
from src.modules.auth.services.jwt.refresh import RefreshTokenService

jwt_refresh_router = APIRouter(prefix="/authentication", tags=["Autenticación"])


@jwt_refresh_router.post(
    path="/jwt/refresh/",
    response_description="**(NO_CONTENT)** Se crea un nuevo token de acceso.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: response_scheme_401(
            access_jwt_missing=True,
            refresh_jwt_missing=True,
            access_jwt_invalid=True,
            refresh_jwt_invalid=True,
            access_jwt_not_expired=True,
            refresh_jwt_expired=True,
            auth_session_expired=True,
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: response_scheme_503(db_unavailable=True),
    },
)
async def refresh_token(
    tokens: Annotated[tuple[str, str], Depends(get_raw_tokens)],
    service: Annotated[RefreshTokenService, Depends(get_jwt_refresh_token_service)],
    response: Response,
) -> None:
    """
    Renueva el token de acceso expirado utilizando el token de actualización.

    ### Descripción
    Genera un nuevo token de acceso (`access_token`) a partir de un token de actualización
    (`refresh_token`) válido y vigente. Requiere que el token de acceso previo haya expirado
    para evitar renovaciones innecesarias, verifica la integridad entre ambos tokens y actualiza
    la cookie de sesión correspondiente con una respuesta sin contenido.

    ### Requisitos de Acceso
    - **Autenticación requerida:** Cookies obligatorias `access_token` y `refresh_token` (JWT).
    - **Condición de Renovación:** El `access_token` debe haber expirado y el `refresh_token`
      debe estar vigente.

    ### Flujo de Ejecución
    1. **Extracción y Validación de Cookies:**
        - Intercepta los tokens `access_token` y `refresh_token` presentes en las cookies HTTP.
        - Si falta alguno de los tokens, interrumpe el flujo con error 401 (MissingJWT).
    2. **Validación del Token de Acceso:**
        - Verifica la firma criptográfica del `access_token`.
        - Comprueba que el `access_token` efectivamente haya expirado. Si aún es vigente,
         deniega la renovación.
    3. **Validación del Token de Actualización:**
        - Verifica la firma y comprueba que el `refresh_token` se encuentre vigente (no expirado).
    4. **Comprobación de Integridad y Sesión:**
        - Comprueba que ambos tokens pertenezcan al mismo usuario (`sub`).
        - Verifica que el usuario exista en la base de datos y que la versión de sesión
         (`session_version`) coincida con la registrada en el token.
    5. **Emisión del Nuevo Token y Actualización de Cookie:**
        - Genera un nuevo `access_token` con una nueva fecha de expiración.
        - Configura la cookie `access_token` (`HttpOnly`, `SameSite=Lax`, `Secure`).
    """

    access_token, refresh_token = tokens
    new_access_token = await service.refresh_token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.access_token_expire * 60,
    )
