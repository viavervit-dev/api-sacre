from typing import Any

import jwt
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError

from src.common.constants import DTOValidationErrorMessages, ExceptionErrorMessages
from src.common.exceptions import (
    AuthenticationFailed,
    DomainRuleViolation,
    MissingJWT,
    PermissionDenied,
    ResourceNotFound,
    UserNotFound,
)
from src.common.response import Response
from src.config.serialization import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores comunes y customizados de excepciones."""

    @app.exception_handler(RequestValidationError)
    async def validation_error(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Manejador de errores de validación de entrada."""

        translations = {
            # Campos requeridos
            "missing": DTOValidationErrorMessages.MISSING.value,
            "extra_forbidden": DTOValidationErrorMessages.EXTRA_FORBIDDEN.value,
            # Texto
            "string_type": DTOValidationErrorMessages.STRING_TYPE.value,
            "string_too_long": DTOValidationErrorMessages.STRING_TOO_LONG.value,
            "string_too_short": DTOValidationErrorMessages.STRING_TOO_SHORT.value,
            "string_pattern_mismatch": DTOValidationErrorMessages.STRING_PATTERN_MISMATCH.value,
            "string_unicode": DTOValidationErrorMessages.STRING_UNICODE.value,
            # Números enteros
            "int_type": DTOValidationErrorMessages.INT_TYPE.value,
            "int_parsing": DTOValidationErrorMessages.INT_PARSING.value,
            # Números decimales
            "float_type": DTOValidationErrorMessages.FLOAT_TYPE.value,
            "float_parsing": DTOValidationErrorMessages.FLOAT_PARSING.value,
            "decimal_max_places": DTOValidationErrorMessages.DECIMAL_MAX_PLACES.value,
            "decimal_max_digits": DTOValidationErrorMessages.DECIMAL_MAX_DIGITS.value,
            # Booleanos (bool)
            "bool_type": DTOValidationErrorMessages.BOOL_TYPE.value,
            "bool_parsing": DTOValidationErrorMessages.BOOL_PARSING.value,
            # Restricciones numéricas
            "greater_than": DTOValidationErrorMessages.GREATER_THAN.value,
            "greater_than_equal": DTOValidationErrorMessages.GREATER_THAN_EQUAL.value,
            "less_than": DTOValidationErrorMessages.LESS_THAN.value,
            "less_than_equal": DTOValidationErrorMessages.LESS_THAN_EQUAL.value,
            "multiple_of": DTOValidationErrorMessages.MULTIPLE_OF.value,
            "finite_number": DTOValidationErrorMessages.FINITE_NUMBER.value,
            # Enumeraciones
            "enum": DTOValidationErrorMessages.ENUM.value,
            "literal_error": DTOValidationErrorMessages.LITERAL_ERROR.value,
            # UUID
            "uuid_type": DTOValidationErrorMessages.UUID_TYPE.value,
            "uuid_parsing": DTOValidationErrorMessages.UUID_PARSING.value,
            "uuid_version": DTOValidationErrorMessages.UUID_VERSION.value,
            # JSON
            "json_invalid": DTOValidationErrorMessages.JSON_INVALID.value,
            "json_type": DTOValidationErrorMessages.JSON_TYPE.value,
            # Genérico (fallback)
            "value_error": DTOValidationErrorMessages.VALUE_ERROR.value,
        }

        errors_dict: dict[str, Any] = {}

        for error in exc.errors():
            loc = error.get("loc", ())

            # Ignoramos 'body', 'query', etc. si están en la raíz
            if len(loc) > 1 and loc[0] in ("body", "query", "path", "header", "cookie"):
                path = loc[1:]
            else:
                path = loc if loc else ("unknown",)

            error_type = error.get("type", "")
            error_msg = error.get("msg", "")

            if error_type == "domain_validation":
                msg = error_msg or "Error de validación."
            elif error_type == "value_error" and "email" in error_msg:
                msg = DTOValidationErrorMessages.VALUE_ERROR_EMAIL.value
            else:
                msg = translations.get(error_type, "El valor ingresado es incorrecto.")

            current_level = errors_dict

            for i, key in enumerate(path):
                key_str = str(key)

                if i == len(path) - 1:
                    # Nodo hoja
                    if key_str not in current_level:
                        current_level[key_str] = msg
                    elif isinstance(current_level[key_str], dict):
                        current_level[key_str]["__all__"] = msg
                else:
                    # Nodo intermedio
                    if key_str not in current_level:
                        current_level[key_str] = {}
                    elif not isinstance(current_level[key_str], dict):
                        current_level[key_str] = {"__all__": current_level[key_str]}
                    current_level = current_level[key_str]

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.REQUEST_DATA_INVALID.value,
                data=errors_dict,
            ).model_dump(),
        )

    @app.exception_handler(OperationalError)
    async def db_unavailable(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: OperationalError,
    ) -> JSONResponse:
        """Manejador de errores cuando la base de datos no está disponible."""

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.DB_UNAVAILABLE.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(jwt.ExpiredSignatureError)
    async def expired_token_jwt(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: jwt.ExpiredSignatureError,
    ) -> JSONResponse:
        """Manejador de error para tokens JWT expirados."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.JWT_EXPIRED.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(jwt.InvalidTokenError)
    async def invalid_token_jwt(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: jwt.InvalidTokenError,
    ) -> JSONResponse:
        """Manejador de error para tokens JWT inválidos o corruptos."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.JWT_INVALID.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(AuthenticationFailed)
    async def authentication_error(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: AuthenticationFailed,
    ) -> JSONResponse:
        """Manejador de error genérico para fallos en la autenticación."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.AUTHENTICATION_FAILED.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(MissingJWT)
    async def missing_jwt(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: MissingJWT,
    ) -> JSONResponse:
        """Manejador de error para tokens JWT faltantes."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.JWT_MISSING.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(ResourceNotFound)
    async def resource_not_found(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: ResourceNotFound,
    ) -> JSONResponse:
        """Manejador de error para recursos no encontrados."""

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.RESOURCE_NOT_FOUND.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: UserNotFound,
    ) -> JSONResponse:
        """Manejador de error para usuarios no encontrados."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.JWT_USER_NOT_FOUND.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(PermissionDenied)
    async def permission_denied(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: PermissionDenied,
    ) -> JSONResponse:
        """Manejador de error para permisos denegados."""

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.PERMISSION_DENIED.value,
                data=None,
            ).model_dump(),
        )

    @app.exception_handler(DomainRuleViolation)
    async def domain_rule_violation(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: DomainRuleViolation,
    ) -> JSONResponse:
        """Manejador de error para violaciones de reglas de dominio."""

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=Response(
                success=False,
                pagination=False,
                message=ExceptionErrorMessages.DOMAIN_RULE_VIOLATION.value,
                data=None,
            ).model_dump(),
        )
