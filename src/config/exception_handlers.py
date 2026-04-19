from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError

from src.common.constants import ValidationErrorMessages
from src.common.response import Response
from src.config.serialization import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores comunes y customizados de excepciones."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Manejador de errores de validación de entrada."""

        translations = {
            # Campos requeridos
            "missing": ValidationErrorMessages.MISSING.value,
            "extra_forbidden": ValidationErrorMessages.EXTRA_FORBIDDEN.value,
            # Texto
            "string_type": ValidationErrorMessages.STRING_TYPE.value,
            "string_too_long": ValidationErrorMessages.STRING_TOO_LONG.value,
            "string_too_short": ValidationErrorMessages.STRING_TOO_SHORT.value,
            "string_pattern_mismatch": ValidationErrorMessages.STRING_PATTERN_MISMATCH.value,
            "string_unicode": ValidationErrorMessages.STRING_UNICODE.value,
            # Números enteros
            "int_type": ValidationErrorMessages.INT_TYPE.value,
            "int_parsing": ValidationErrorMessages.INT_PARSING.value,
            # Números decimales
            "float_type": ValidationErrorMessages.FLOAT_TYPE.value,
            "float_parsing": ValidationErrorMessages.FLOAT_PARSING.value,
            # Booleanos (bool)
            "bool_type": ValidationErrorMessages.BOOL_TYPE.value,
            "bool_parsing": ValidationErrorMessages.BOOL_PARSING.value,
            # Restricciones numéricas
            "greater_than": ValidationErrorMessages.GREATER_THAN.value,
            "greater_than_equal": ValidationErrorMessages.GREATER_THAN_EQUAL.value,
            "less_than": ValidationErrorMessages.LESS_THAN.value,
            "less_than_equal": ValidationErrorMessages.LESS_THAN_EQUAL.value,
            "multiple_of": ValidationErrorMessages.MULTIPLE_OF.value,
            "finite_number": ValidationErrorMessages.FINITE_NUMBER.value,
            # Enumeraciones
            "enum": ValidationErrorMessages.ENUM.value,
            "literal_error": ValidationErrorMessages.LITERAL_ERROR.value,
            # UUID
            "uuid_type": ValidationErrorMessages.UUID_TYPE.value,
            "uuid_parsing": ValidationErrorMessages.UUID_PARSING.value,
            "uuid_version": ValidationErrorMessages.UUID_VERSION.value,
            # JSON
            "json_invalid": ValidationErrorMessages.JSON_INVALID.value,
            "json_type": ValidationErrorMessages.JSON_TYPE.value,
            # Genérico (fallback)
            "value_error": ValidationErrorMessages.VALUE_ERROR.value,
        }

        errors_dict = {}

        for error in exc.errors():
            field = str(error["loc"][-1]) if error["loc"] else "unknown"

            if field not in errors_dict:
                error_type = error.get("type", "")
                error_msg = error.get("msg", "")

                if error_type == "domain_validation":
                    errors_dict[field] = error_msg or "Error de validación."
                elif error_type == "value_error" and "email" in error_msg:
                    errors_dict[field] = ValidationErrorMessages.VALUE_ERROR_EMAIL.value
                else:
                    errors_dict[field] = translations.get(
                        error_type, "El valor ingresado es incorrecto."
                    )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
            content=Response(
                success=False,
                message="Error de validación en los datos enviados.",
                data=errors_dict,
            ).model_dump(),
        )

    @app.exception_handler(OperationalError)
    async def db_unavailable_handler(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: OperationalError,
    ) -> JSONResponse:
        """Manejador de errores cuando la base de datos no está disponible."""

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=Response(
                success=False,
                message="El servicio de base de datos no está disponible.",
                data=None,
            ).model_dump(),
        )
