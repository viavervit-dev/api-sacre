import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config.serialization import JSONResponse

logger = logging.getLogger("uvicorn.error")


def format_error_response(code: int, detail: Any, extra_data: Any = None) -> dict[str, Any]:
    """Formatea la respuesta de error de manera consistente."""

    res = {"code": code, "detail": detail}

    if extra_data is not None:
        res["extra_data"] = extra_data

    return res


def register_exception_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores comunes y customizados de excepciones."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Manejador de errores de validación de entrada."""

        logger.warning(f"Validation error on {request.url}: {exc}")
        code = getattr(exc, "status_code", status.HTTP_422_UNPROCESSABLE_CONTENT)

        return JSONResponse(
            status_code=code,
            content=format_error_response(code, "Input validation error", exc.errors()),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        """Manejador de errores HTTP estándar."""

        logger.info(f"HTTP error {exc.status_code} on {request.url}: {exc.detail}")

        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(exc.status_code, exc.detail),
        )
