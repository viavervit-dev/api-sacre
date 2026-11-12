from contextlib import suppress

from fastapi import status
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.api.common.response import Response
from src.api.settings.serialization import JSONResponse


class __BodyTooLargeError(Exception):
    """Excepción interna para abortar la lectura cuando un stream excede el límite."""


def __build_error_response(status_code: int, message: str) -> JSONResponse:
    """Construye una respuesta JSON estándar para errores de tamaño de petición."""

    return JSONResponse(
        status_code=status_code,
        content=Response(
            success=False,
            pagination=False,
            message=message,
            data=None,
        ).model_dump(),
    )


class MaxBodySizeMiddleware:
    """Limita el tamaño máximo permitido del cuerpo de peticiones HTTP."""

    def __init__(self, app: ASGIApp, max_body_size: int) -> None:
        self.max_body_size = max_body_size
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Intercepta peticiones HTTP para validar el tamaño del cuerpo mediante la cabecera
        `Content-Length` y el conteo progresivo de bytes del `stream` entrante.
        """

        if scope["type"] != "http":
            await self.app(scope, receive, send)

            return

        # Rechazo inmediato si Content-Length viene declarado y supera el límite
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() == b"content-length":
                try:
                    content_length = int(header_value.decode("ascii"))
                except UnicodeDecodeError, ValueError:
                    content_length = -1

                if content_length < 0:
                    resp = __build_error_response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        message="Cabecera Content-Length inválida.",
                    )
                    await resp(scope, receive, send)
                    return

                if content_length > self.max_body_size:
                    resp = __build_error_response(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        message="El cuerpo de la petición excede el tamaño máximo permitido.",
                    )
                    await resp(scope, receive, send)
                    return
                break

        # Conteo real por chunks
        received_bytes = 0
        response_started = False
        exceeded = False

        async def limited_receive() -> Message:
            """
            Lee los mensajes del `stream` HTTP entrante acumulando los bytes recibidos y aborta
            la lectura si se supera el tamaño máximo permitido.
            """

            nonlocal received_bytes, exceeded
            message = await receive()

            if message["type"] == "http.request":
                received_bytes += len(message.get("body", b""))

                if received_bytes > self.max_body_size:
                    exceeded = True

                    raise __BodyTooLargeError()

            return message

        async def tracking_send(message: Message) -> None:
            """
            Rastrea si la respuesta HTTP ya inició para evitar enviar mensajes duplicados
            o corruptos tras exceder el límite de tamaño.
            """

            nonlocal response_started

            if exceeded and not response_started:
                return
            if message["type"] == "http.response.start":
                response_started = True

            await send(message)

        with suppress(__BodyTooLargeError):
            await self.app(scope, limited_receive, tracking_send)

        if exceeded and not response_started:
            resp = __build_error_response(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                message="El cuerpo de la petición excede el tamaño máximo permitido.",
            )
            await resp(scope, receive, send)
