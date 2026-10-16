from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.api.common.exceptions import MissingJWT
from src.api.common.schema import response_scheme_401, response_scheme_503
from src.api.modules.auth.constants import ExceptionErrorMessages
from src.api.modules.auth.dependencies import jwt_refresh_token_service, optional_tokens
from src.api.modules.auth.services.jwt.refresh import RefreshTokenService
from src.api.settings.parameters import api_parameters

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
    tokens: Annotated[tuple[str | None, str | None], Depends(optional_tokens)],
    response: Response,
    service: Annotated[RefreshTokenService, Depends(jwt_refresh_token_service)],
) -> None:
    """
    Permite generar un nuevo token de acceso (`access_token`) a partir de un token de actualización
    (`refresh_token`) válido y vigente. Requiere que el token de acceso previo haya expirado
    para evitar renovaciones innecesarias, verifica la integridad entre ambos tokens y actualiza
    la cookie de sesión correspondiente con una respuesta sin contenido.

    ### Requisitos de Acceso
    - **Acceso Público:** Endpoint abierto para renovación de tokens de acceso.
    - **Condición de Renovación:** El `refresh_token` debe estar vigente y válido.

    ### Flujo de Ejecución
    1. **Extracción y Validación de Cookies:**
        - Intercepta el token `refresh_token` presentes en las cookies HTTP.
        - Si falta el token, interrumpe el flujo con error 401 (MissingJWT).
    2. **Validación del Token de Actualización:**
        - Verifica la firma y comprueba que el `refresh_token` se encuentre vigente (no expirado).
    3. **Comprobación de Integridad y Sesión:**
        - Comprueba que ambos tokens pertenezcan al mismo usuario (`sub`).
        - Verifica que el usuario exista en la base de datos y que la versión de sesión
         (`session_version`) coincida con la registrada en el token.
    4. **Emisión del Nuevo Token y Actualización de Cookie:**
        - Genera un nuevo `access_token` con una nueva fecha de expiración.
        - Configura la cookie `access_token` (`HttpOnly`, `SameSite=Lax`, `Secure`).
    """

    _, refresh_token = tokens

    if not refresh_token:
        raise MissingJWT(message=ExceptionErrorMessages.REFRESH_JWT_MISSING.value)

    new_access_token = await service.refresh_token(refresh_token=refresh_token)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=not api_parameters.debug,
        samesite="lax",
        max_age=api_parameters.access_token_expire * 60,
    )
